init:
	pip install -r requirements.txt

tui:
	python -m password-manager tui


gui:
	python -m password-manager gui

dist:
	pyinstaller -F password-manager/__main__.py

run-exe: dist
	./dist/__main__

clean:
	rm -rf dist
	rm -rf build

.PHONY: init tui gui run-exe clean
