docker-image:
	docker build . -t integration -f docker/integration/Dockerfile

docker-test:
	docker run -ti -v $(shell pwd):/build integration 