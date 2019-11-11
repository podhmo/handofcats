default: 00 01 02 03

# positional arguments
00:
	python $@*/main.py --expose | tee $$(echo $@*)/_exposed.py

# keyword arguments
01:
	python $@*/main.py --expose | tee $$(echo $@*)/_exposed.py

# use `__future__ import annotations`
02:
	python $@*/main.py --expose | tee $$(echo $@*)/_exposed.py

# with literal type
03:
	python $@*/main.py --expose | tee $$(echo $@*)/_exposed.py
