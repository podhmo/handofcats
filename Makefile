test:
	python setup.py test
ci:
	$(MAKE) lint test examples
	git diff

examples:
	$(MAKE) -C examples/readme && \
 $(MAKE) -C examples/parse-args && \
 $(MAKE) -C examples/logging && \
 $(MAKE) -C examples/multi-command && \
 $(MAKE) -C examples/_misc \
 || ( GIT_PAGER=cat git diff 2>&1 && exit 1 )

.PHONY: examples

format:
#	pip install -e .[dev]
	black handofcats setup.py

lint:
#	pip install -e .[dev]
	flake8 handofcats --ignore W503,E203,E501

# typing:
# #	pip install -e .[dev]
# 	mypy --strict --strict-equality --ignore-missing-imports handofcats

build:
#	pip install wheel
	python setup.py bdist_wheel

upload:
#	pip install twine
	twine check dist/handofcats-$(shell cat VERSION)*
	twine upload dist/handofcats-$(shell cat VERSION)*

.PHONY: test format lint build upload examples typing
