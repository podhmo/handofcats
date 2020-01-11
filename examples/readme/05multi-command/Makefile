default: run
help:
	python cli.py -h
.PHONY: help

help-subcommand:
	python cli.py hello -h
.PHONY: help-subcommand

expose:
	python cli.py --expose | tee cli-exposed.py
.PHONY: expose

run:
	python cli.py hello --name world
.PHONY: help expose
