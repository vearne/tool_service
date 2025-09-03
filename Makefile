VERSION := v0.0.1

COMMAND_NAME = tool-service

BUILD_COMMIT ?= $(shell git rev-parse --short=4 HEAD)
BUILD_TIME ?= $(shell date +%Y%m%d%H%M%S)

DOCKER_TAG := $(VERSION)-$(BUILD_TIME)-$(BUILD_COMMIT)
IMAGE_NAME = registry.cn-hangzhou.aliyuncs.com/vearne/$(COMMAND_NAME):$(DOCKER_TAG)

.PHONY: image
image:
	docker build --rm \
		-f ./build/Dockerfile  \
		-t $(IMAGE_NAME) .
	docker push $(IMAGE_NAME)