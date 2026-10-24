##############################################################################
# biome (JS linting and formatting)
##############################################################################

.PHONY: biome-check
biome-check: $(NODEJS_TARGET)
	@echo "Run biome check"
	@biome check

.PHONY: biome-format
biome-format: $(NODEJS_TARGET)
	@echo "Run biome format"
	@biome check --write

CHECK_TARGETS+=biome-check
FORMAT_TARGETS+=biome-format
