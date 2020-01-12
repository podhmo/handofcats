default: 00 01 02 03 04

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
	python $(shell echo $@*.py) --expose | tee $(patsubst %.py,%.output,$(shell echo $@*.py))
	flake8 --ignore=E501,E302,E303 $(patsubst %.py,%.output,$(shell echo $@*.py))

# eject with config, with multi-command
04:
	python $(shell echo $@*.py) --expose | tee $(patsubst %.py,%.output,$(shell echo $@*.py))
	flake8 --ignore=E501,E302,E303 $(patsubst %.py,%.output,$(shell echo $@*.py))

clean:
	rm -f *.output
