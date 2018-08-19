default: run
help:
	python greeting.py -h
.PHONY: help

expose:
	python greeting.py --expose | tee greeting-exposed.py
.PHONY: expose

run:
	python greeting.py --is-surprised hello
run-full:
	python greeting.py --is-surprised --name=foo hello
readme:
	rm -f output*
	@$(MAKE) help >> output.help  2>/dev/stdout
	@$(MAKE) default >> output.default  2>/dev/stdout

	echo help > readme.md
	echo '```console' >> readme.md
	cat output.help | grep -v '^make\[' >> readme.md
	echo '```' >> readme.md
	echo run >> readme.md
	echo '```console' >> readme.md
	cat output.default | grep -v '^make\[' >> readme.md
	echo '```' >> readme.md
	cat readme.md
.PHONY: help expose readme
