default: 00 01 02 03 04 05 06

FLAKE8 := flake8 --ignore=E501,E302

# from handofcats import as_subcommand
00:
	python $(shell echo $@*/)cli.py --expose | tee $(shell echo $@*/)_expose.py
	$(FLAKE8) $(shell echo $@*)/_expose.py

# import handofcats
01:
	python $(shell echo $@*/)cli.py --expose | tee $(shell echo $@*/)_expose.py
	$(FLAKE8) $(shell echo $@*)/_expose.py

# from handofcats import as_subcommand as register
02:
	python $(shell echo $@*/)cli.py --expose | tee $(shell echo $@*/)_expose.py
	$(FLAKE8) $(shell echo $@*)/_expose.py

# import handfcats as h
03:
	python $(shell echo $@*/)cli.py --expose | tee $(shell echo $@*/)_expose.py
	$(FLAKE8) $(shell echo $@*)/_expose.py

# if name main
04:
	python $(shell echo $@*/)cli.py --expose | tee $(shell echo $@*/)_expose.py
	$(FLAKE8) $(shell echo $@*)/_expose.py

# from handfcats import (x, y, z)
05:
	python $(shell echo $@*/)cli.py --expose | tee $(shell echo $@*/)_expose.py
	$(FLAKE8) $(shell echo $@*)/_expose.py

# use as plain module
06:
	(cd $(shell echo $@*/) && python main.py) | tee $(shell echo $@*/)main.output
