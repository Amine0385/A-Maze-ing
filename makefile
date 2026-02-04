all:run

build: clean
	python3 setup.py sdist
	cp dist/*.tar.gz .
	@echo "Package created in root directory."

debug:

install:
	pip install mazegen.tar.gz --target .

run:
	python3 a_maze_ing.py $(ARGS)

clean:
	rm -rf build/ dist/ *.egg-info __pycache__ .mypy_cache
	rm -f *.whl *.tar.gz

lint:
	python3 -m flake8 .
	python3 -m mypy . \
	--warn-return-any \
	--warn-unused-ignores \
	--ignore-missing-imports \
	--disallow-untyped-defs \
	--check-untyped-defs

.PHONY: build install run clean