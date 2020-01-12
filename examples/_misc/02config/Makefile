default: 00 01

# ignore-logging=True -> logging options are disabled
00:
	python $(shell echo $@*.py) -h | tee $(patsubst %.py,%.output,$(shell echo $@*.py))
# ignore-expose=True -> expose options are disabled
01:
	python $(shell echo $@*.py) -h | tee $(patsubst %.py,%.output,$(shell echo $@*.py))
