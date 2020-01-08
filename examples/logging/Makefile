TEE ?= 2>&1 | tee

default: 00 01 02


00: dst
	python run.py -h $(TEE) dst/$@help-message.output
01: dst
	python run.py $(TEE) dst/$@run.output
02: dst
	DEBUG=1 python run.py $(TEE) dst/$@run-with-debug.output

dst:
	mkdir -p dst
