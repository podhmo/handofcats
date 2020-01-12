default:
	$(MAKE) 00 2>&1 | tee 00.output
	$(MAKE) 01 2>&1 | tee 01.output
	$(MAKE) 02 2>&1 | tee 02.output
	$(MAKE) 03 2>&1 | tee 03.output
	$(MAKE) 04 2>&1 | sed 's@$(shell pwd)@CWD@g' | tee 04.output
	$(MAKE) 05 2>&1 | tee 05.output
	$(MAKE) 06 2>&1 | tee 06.output
	$(MAKE) show-help 2>&1 | tee show-help.output
	$(MAKE) run-debug 2>&1 | tee run-debug.output


# single command (without decorator)
00:
	python -m handofcats $(shell echo $@*.py):hello
	python -m handofcats $(shell echo $@*.py):hello -h
	python -m handofcats $(shell echo $@*.py):hello --expose

# single command with decorator
01:
	python -m handofcats $(shell echo $@*.py):hello
	python -m handofcats $(shell echo $@*.py):hello -h
	python -m handofcats $(shell echo $@*.py):hello --expose

# multi command (with out decorator)
02:
	python -m handofcats $(shell echo $@*.py) hello
	python -m handofcats $(shell echo $@*.py) byebye foo
	python -m handofcats $(shell echo $@*.py) -h
	python -m handofcats $(shell echo $@*.py) --expose

# multi command
03:
	python -m handofcats $(shell echo $@*.py) hello
	python -m handofcats $(shell echo $@*.py) byebye foo
	python -m handofcats $(shell echo $@*.py) -h
	python -m handofcats $(shell echo $@*.py) --expose


# file not found
04:
	python -m handofcats xxxx.py || exit 0

# attr is not found
05:
	python -m handofcats $(shell echo $@*.py):xxxx || exit 0
06:
# attr is not function
	python -m handofcats $(shell echo $@*.py):logger || exit 0

# help
show-help:
	python -m handofcats -h || exit 0
# logging
run-debug:
	python -m handofcats $(shell echo $@*.py):use_root_logger
	DEBUG=1 python -m handofcats $(shell echo $@*.py):use_root_logger

clean:
	rm -f *.output
