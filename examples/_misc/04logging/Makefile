TEE ?= 2>&1 | tee

default: 00 01 02 03 04 05


# help message
00: dst
	python run.py -h $(TEE) dst/$@help-message.output

# run output
01: dst
	python run.py $(TEE) dst/$@run.output

# run with debug option
02: dst
	DEBUG=1 python run.py $(TEE) dst/$@run-with-debug.output

# run via handofcats command
03: dst
	python -m handofcats def.py:run $(TEE) dst/$@run-from-handofcats.output

# run via handofcats command with debug option
04: dst
	DEBUG=1 python -m handofcats def.py:run $(TEE) dst/$@run-from-handofcats-with-debug.output

# customize logging via varenv
05: FORMAT ?= {"level": "%(levelname)s", "funcname": "%(funcName)s", "message": "%(message)r"}
05: dst
	LOGGIG_FORMAT=stdout LOGGING_FORMAT='${FORMAT}' DEBUG=1 python -m handofcats def.py:run $(TEE) dst/$@run-from-handofcats-with-format.output

# codegen
06:
	python run.py --expose | tee dst/$@run-exposed.py
	flake8 --ignore=E501,E302 dst/$@run-exposed.py
	python dst/$@run-exposed.py $(TEE) dst/$@run.output

clean:
	rm -rf dst
.PHONY: clean

dst:
	mkdir -p dst
