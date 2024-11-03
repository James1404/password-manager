EXE_NAME = password-manager

SRC := $(shell find . -type f -iname "*.py" -not -path "*.direnv*")

init:
	pip install -r requirements.txt

run:
	python main.py

clean:
	@echo Cleaning up
	@rm -rf dist
	@rm -rf build

.PHONY: init run clean
