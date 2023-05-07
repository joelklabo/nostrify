FROM ubuntu:latest as builder
MAINTAINER Christian Decker <decker@blockstream.com>

ARG LIGHTNINGD_VERSION=master
ENV DEBIAN_FRONTEND=noninteractiv

RUN apt-get update -qq \
	&& apt-get install -y --no-install-recommends \
	git build-essential autoconf automake build-essential git libtool libgmp-dev \
	libsqlite3-dev python3 python3-mako net-tools zlib1g-dev libsodium-dev \
	gettext apt-transport-https ca-certificates python3-pip wget 

RUN git clone --recursive https://github.com/ElementsProject/lightning.git /tmp/lightning
WORKDIR /tmp/lightning
RUN git checkout $LIGHTNINGD_VERSION
RUN ./configure --prefix=/tmp/lightning_install --enable-developer --disable-valgrind --enable-experimental-features
RUN make -j $(nproc) install

FROM ubuntu:latest as python-builder

COPY --from=builder /tmp/lightning/ /usr/local/src/lightning/

RUN apt-get update -qq \
	&& apt-get install -y --no-install-recommends \
	build-essential \
	pkg-config \
	python3 \
	python3-dev \
	python3-pip \
	python3-venv \
	git \
	tree \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /opt
COPY ./*.py /opt/
COPY ./nostr /opt/nostr
COPY ./tests /opt/tests

# RUN git submodule update --init --recursive
ADD ci-requirements.txt /tmp/

RUN python3 -m venv .venv
ENV PATH="/opt/.venv/bin:$PATH"
RUN pip3 install wheel
RUN pip3 install /usr/local/src/lightning/contrib/pyln-client
RUN pip3 install /usr/local/src/lightning/contrib/pyln-testing
RUN pip3 install -r /tmp/ci-requirements.txt

RUN pip3 install git+https://github.com/joelklabo/python-nostr.git

FROM ubuntu:latest as final

RUN apt-get update -qq \
	&& apt-get install -y --no-install-recommends \
	libsqlite3-dev \
	zlib1g-dev \
	libsodium-dev \
	libgmp-dev \
	python3 \
	python3-venv \
	wget \
	tree \
	&& rm -rf /var/lib/apt/lists/*

ARG BITCOIN_VERSION=24.0.1
ENV BITCOIN_TARBALL bitcoin-${BITCOIN_VERSION}-x86_64-linux-gnu.tar.gz
ENV BITCOIN_URL https://bitcoincore.org/bin/bitcoin-core-$BITCOIN_VERSION/$BITCOIN_TARBALL

RUN cd /tmp \
	&& wget -qO $BITCOIN_TARBALL "$BITCOIN_URL" \
	&& BD=bitcoin-$BITCOIN_VERSION/bin \
	&& tar -xzvf $BITCOIN_TARBALL $BD/bitcoin-cli $BD/bitcoind --strip-components=1 \
	&& cp bin/bitcoind bin/bitcoin-cli /usr/bin/ \
	&& rm -rf $BITCOIN_TARBALL bin

# Make the debug logs available during testing
ENV TEST_DEBUG 1

# Speed up testing by shortening all timeouts
ENV DEVELOPER 1

COPY --from=builder /tmp/lightning_install/ /usr/local/
COPY --from=python-builder /opt/.venv /opt/.venv
COPY --from=python-builder /opt/tests /opt/tests
# COPY --from=python-builder /opt/nostr /opt/nostr
COPY --from=python-builder /opt/*.py /opt/

ENV VIRTUAL_ENV=/opt/.venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

CMD ["pytest", "-vvv", "-n=auto", "-k", "tests"]
