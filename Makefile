# Define the virtual environment directory and the Python interpreter within it.
VENV_DIR := .venv
VENV_PYTHON := $(VENV_DIR)/bin/python

# Phony targets are rules that don't represent files.
.PHONY: install uninstall test

# This rule depends on the virtual environment's Python executable existing.
# If it doesn't, make will run the rule to create it first.
install: $(VENV_PYTHON)
	@$(VENV_PYTHON) -m pip install -e '.[test]'

# This rule runs pytest using the virtual environment's interpreter.
test: $(VENV_PYTHON)
	@$(VENV_PYTHON) -m pytest

# This rule removes the virtual environment and cached files.
uninstall:
	@rm -rf $(VENV_DIR)
	@find . -type d -name "__pycache__" -exec rm -r {} +
	@find . -type d -name ".pytest_cache" -exec rm -r {} +

# This is a helper rule that creates the virtual environment if it's missing.
# The 'install' and 'test' rules depend on its target file.
$(VENV_PYTHON):
	@python3 -m venv $(VENV_DIR)
