default: 00 01 02 03

# ignore-logging=True -> logging options are disabled
00:
	python $(shell echo $@*.py) -h | tee $(patsubst %.py,%.output,$(shell echo $@*.py))
# ignore-expose=True -> expose options are disabled
01:
	python $(shell echo $@*.py) -h | tee $(patsubst %.py,%.output,$(shell echo $@*.py))
# ignore-expose=True, with multi-command
02:
	python $(shell echo $@*.py) -h | tee $(patsubst %.py,%.output,$(shell echo $@*.py))
# eject with config
03:
	python $(shell echo $@*.py) --expose | tee $(patsubst %.py,%-exposed.py,$(shell echo $@*.py))
	flake8 $(patsubst %.py,%-exposed.py,$(shell echo $@*.py))
