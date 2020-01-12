default: 00 01

# mypy check, single command
00:
	python -m handofcats cli.py:hello --expose | tee $@exposed.py
	flake8 --ignore=E501,E303 $@exposed.py
	mypy --strict $@exposed.py

# mypy check, multicommand command
01:
	python -m handofcats cli.py --expose | tee $@exposed.py
	flake8 --ignore=E501,E303 $@exposed.py
	mypy --strict $@exposed.py
