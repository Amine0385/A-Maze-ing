install:
	pip install 

build: install
	python3 -m build --no-isolation
	cp dist/mazegen-*.whl .
	cp dist/mazegen-*.tar.gz .
	@echo "Package created and moved to root."

clean:
	rm -rf build/ dist/ *.egg-info __pycache__ .mypy_cache
	rm -f *.whl *.tar.gz

lint:
	python3 -m flake8 .
	mypy --ignore-missing-imports .

.PHONY: install build clean lint