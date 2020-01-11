default: 00 01 02 03 04 05

# positional arguments
00:
	python $@*/main.py --expose | tee $$(echo $@*)/_exposed.py
	flake8 --ignore=E302,E303,E305,E501 $$(echo $@*)/_exposed.py

# keyword arguments
01:
	python $@*/main.py --expose | tee $$(echo $@*)/_exposed.py
	flake8 --ignore=E302,E303,E305,E501 $$(echo $@*)/_exposed.py

# use `__future__ import annotations`
02:
	python $@*/main.py --expose | tee $$(echo $@*)/_exposed.py
	flake8 --ignore=E302,E303,E305,E501 $$(echo $@*)/_exposed.py

# with literal type
03:
	python $@*/main.py --expose | tee $$(echo $@*)/_exposed.py
	flake8 --ignore=E302,E303,E305,E501 $$(echo $@*)/_exposed.py

# use main()
04:
	python $@*/main.py --expose | tee $$(echo $@*)/_exposed.py
	flake8 --ignore=E302,E303,E305,E501 $$(echo $@*)/_exposed.py

# --typed
05:
	python $@*/main.py --typed --expose | tee $$(echo $@*)/_exposed.py
	flake8 --ignore=E302,E303,E305,E501 $$(echo $@*)/_exposed.py
