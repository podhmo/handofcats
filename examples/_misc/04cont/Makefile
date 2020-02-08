default: 00 01 02 03 04 05

# default cont (single command)
00:
	python $(shell echo $@*.py) | tee $(patsubst %.py,%.output,$(shell echo $@*.py))
# default cont (sub commands)
01:
	python $(shell echo $@*.py) hello | tee $(patsubst %.py,%.output,$(shell echo $@*.py))

# default cont with handofcats command
02:
	python -m handofcats $(shell echo $@*.py):hello | tee $(patsubst %.py,%.output,$(shell echo $@*.py))

# custom cont (single command)
03:
	python $(shell echo $@*.py) | tee $(patsubst %.py,%.output,$(shell echo $@*.py))

# custom cont (sub commands)
04:
	python $(shell echo $@*.py) hello | tee $(patsubst %.py,%.output,$(shell echo $@*.py))

# custom cont with handofcats command
05:
	python -m handofcats --cont=dump.py:dump $(shell echo $@*.py):hello | tee $(patsubst %.py,%.output,$(shell echo $@*.py))

clean:
	rm -f *.output
