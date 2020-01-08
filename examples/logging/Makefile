TEE ?= 2>&1 | tee

default: 00 01 02 03 04


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

clean:
	rm -rf dst
.PHONY: clean

dst:
	mkdir -p dst
