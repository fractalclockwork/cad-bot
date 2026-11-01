PART ?= kp08
NAME ?=

.PHONY: build pipeline pipeline-auto gallery new-part

build:
	docker compose build

pipeline:
	PART=$(PART) ./scripts/run_pipeline.sh

pipeline-auto:
	PART=$(PART) ./scripts/run_pipeline.sh --skip-human

gallery:
	PART=$(PART) ./scripts/open_gallery.sh

new-part:
	@test -n "$(NAME)" || (echo "Usage: make new-part NAME=my_part" >&2; exit 1)
	./scripts/new_part.sh $(NAME)
