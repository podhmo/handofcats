default:
	handofcats sum.py:psum 10 20
	handofcats sum.py:psum 10 20 --ys 1 --ys 2
help:
	handofcats sum.py:psum -h
expose:
	handofcats sum.py:psum --expose | tee sum-exposed.py
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
