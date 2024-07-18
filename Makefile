CONTAINER_IDS := $(shell docker container ls -q)

.PHONY: build-all
build-all:
	docker compose up -d

.PHONY: build-timescale
build-timescale:
	docker compose up timescaledb -d

.PHONY: build-api
build-api:
	docker compose up api -d

.PHONY: remove-containers
remove-containers:
	docker stop $(CONTAINER_IDS) && docker rm $(CONTAINER_IDS)

.PHONY: run-local
run-local:
	docker compose up timescaledb -d && python src/api/main.py