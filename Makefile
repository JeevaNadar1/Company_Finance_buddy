SKILL_DIR := company-finance-buddy
BUNDLE    := $(SKILL_DIR).skill
VERSION   := $(shell cat VERSION)

.PHONY: help validate build clean release-check install-hint

help:
	@echo "validate       structural checks on $(SKILL_DIR)/"
	@echo "build          validate, then package $(BUNDLE)"
	@echo "release-check  build and confirm the committed bundle is current"
	@echo "clean          remove build output"
	@echo "install-hint   how to load the bundle into Claude"

validate:
	@python3 scripts/validate.py $(SKILL_DIR)

build: validate
	@bash scripts/build.sh $(SKILL_DIR) $(BUNDLE)

release-check:
	@cp $(BUNDLE) /tmp/committed.skill 2>/dev/null || true
	@bash scripts/build.sh $(SKILL_DIR) /tmp/rebuilt.skill >/dev/null
	@cmp -s /tmp/committed.skill /tmp/rebuilt.skill \
		&& echo "OK  committed bundle matches source (v$(VERSION))" \
		|| (echo "STALE  $(BUNDLE) does not match $(SKILL_DIR)/ — run 'make build' and commit"; exit 1)

clean:
	@rm -f /tmp/rebuilt.skill /tmp/committed.skill
	@find . -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true
	@echo "cleaned"

install-hint:
	@echo "Claude → Settings → Capabilities → Skills → Upload → select $(BUNDLE)"
