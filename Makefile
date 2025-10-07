CONTAINER_IDS := $(shell docker container ls -q)

.PHONY: test
test:
	python -m pytest tests/.

.PHONY: build-all
build-all:
	docker compose up -d

.PHONY: build-timescale
build-timescale:
	docker compose up timescaledb -d

.PHONY: build-api
build-api:
	docker compose up api -d

.PHONY: run-local
run-local:
	$(MAKE) build-timescale && python -m src.api.main