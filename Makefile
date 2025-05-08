# Makefile - Add your content here

.PHONY: help setup test lint format coverage clean install package

help:
	@echo "Available commands:"
	@echo "  setup      - Install development dependencies"
	@echo "  test       - Run tests"
	@echo "  lint       - Run linting"
	@echo "  format     - Format code with black"
	@echo "  coverage   - Run tests with coverage"
	@echo "  clean      - Clean up build artifacts"
	@echo "  install    - Install the package in development mode"
	@echo "  package    - Build package for distribution"

install:
	uv pip install -r requirements.txt

test:
	pytest tests/

lint:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

format:
	black .
	isort .

coverage:
	pytest --cov=. tests/
	pytest --cov=. --cov-report=html tests/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

setup:
	pip install -e .

package:
	python setup.py sdist bdist_wheel
