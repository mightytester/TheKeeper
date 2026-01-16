PYTHON := python
PIP := pip

.PHONY: help install run clean

help:
	@echo "Available commands:"
	@echo "  make install  - Install dependencies using pyenv Python"
	@echo "  make run      - Run the image review app"
	@echo "  make clean    - Remove compiled files"

install:
	@$(PIP) install --upgrade pip
	@$(PIP) install -r requirements.txt

run:
	@echo "Using Python: $$(python --version)"
	@echo "Starting Image Review App..."
	@$(PYTHON) app.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
