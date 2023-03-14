docker-image:
	docker build . -t integration -f docker/integration/

docker-test:
	docker run -ti -v $(shell pwd):/build integration 