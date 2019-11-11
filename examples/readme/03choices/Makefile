default:
	python -W ignore -m handofcats dump.py:run
	python -W ignore -m handofcats dump.py:run --format=csv
help:
	python -W ignore -m handofcats dump.py:run -h
expose:
	python -W ignore -m handofcats dump.py:run --expose | tee dump-exposed.py
.PHONY: help expose
