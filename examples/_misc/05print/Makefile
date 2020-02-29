default: 00

00:
	python $(shell echo $@*.py) 2>&1 | tee $(patsubst %.py,%.output,$(shell echo $@*.py))
	DEBUG=1 python $(shell echo $@*.py) 2>&1 | tee $(patsubst %.py,%.debug.output,$(shell echo $@*.py))
	python $(shell echo $@*.py) --simple --expose | tee $(patsubst %.py,%.gen,$(shell echo $@*.py))
