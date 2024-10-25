init:
	pip install -r requirements.txt

run:
	python -m password-manager

dist:
	pyinstaller -F password-manager/__main__.py

run-exe: dist
	./dist/__main__

.PHONY: init run run-exe
