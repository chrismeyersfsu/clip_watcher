.PHONY: run

run:
	./src/clip_watcher/watch_clipboard.py

install:
	ansible-playbook install.yml -vv

build:
	rm -rf dist/*
	python3 -m pip install --upgrade build
	python3 -m build

publish:
	python3 -m pip install --upgrade twine
	python3 -m twine upload --repository testpypi dist/*

test-install:
	python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps clip_watcher
