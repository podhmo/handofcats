default: run
help:
	python greeting.py -h
.PHONY: help

expose:
	python greeting.py --expose | tee greeting-exposed.py
.PHONY: expose

run:
	python greeting.py --is-surprised hello
run-full:
	python greeting.py --is-surprised --name=foo hello
.PHONY: run
