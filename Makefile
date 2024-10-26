init:
	pip install -r requirements.txt

run:
	python -m password-manager

dist:
	pyinstaller -F password-manager/__main__.py

run-exe: dist
	./dist/__main__

clean:
	rm -rf dist
	rm -rf build

.PHONY: init run run-exe clean
