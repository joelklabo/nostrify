docker-image:
	docker build -ti integration -f docker/integration/

docker-test:
	docker run -ti -v $(shell pwd):/build integration 