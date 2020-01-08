TEE ?= 2>&1 | tee

default: 00 01 02 03 04 05


00: dst
	python run.py -h $(TEE) dst/$@help-message.output
01: dst
	python run.py $(TEE) dst/$@run.output
02: dst
	DEBUG=1 python run.py $(TEE) dst/$@run-with-debug.output
03: dst
	python -m handofcats def.py:run $(TEE) dst/$@run-from-handofcats.output
04: dst
	DEBUG=1 python -m handofcats def.py:run $(TEE) dst/$@run-from-handofcats-with-debug.output
05: FORMAT ?= {"level": "%(levelname)s", "funcname": "%(funcName)s", "message": "%(message)r"}
05: dst
	LOGGIG_FORMAT=stdout LOGGING_FORMAT='${FORMAT}' DEBUG=1 python -m handofcats def.py:run $(TEE) dst/$@run-from-handofcats-with-format.output

clean:
	rm -rf dst
.PHONY: clean

dst:
	mkdir -p dst
