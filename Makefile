test:
	python setup.py test
ci:
	$(MAKE) lint test

format:
#	pip install -e .[dev]
	black handofcats setup.py

lint:
#	pip install -e .[dev]
	flake8 handofcats --ignore W503,E203,E501

# typing:
# #	pip install -e .[dev]
# 	mypy --strict --strict-equality --ignore-missing-imports handofcats

examples:
	$(MAKE) -C examples/openapi

build:
#	pip install wheel
	python setup.py bdist_wheel

upload:
#	pip install twine
	twine check dist/handofcats-$(shell cat VERSION)*
	twine upload dist/handofcats-$(shell cat VERSION)*

.PHONY: test format lint build upload examples typing
