docker-image:
	docker build -t cl-test .

docker-test:
	docker run -ti -v $(shell pwd):/build cl-test