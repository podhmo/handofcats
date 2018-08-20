TARGET ?=

default:
	$(MAKE) readme TARGET=00greeting
	$(MAKE) readme TARGET=01sum
	$(MAKE) readme TARGET=02list

readme:
	@$(MAKE) -C ${TARGET} help >> output.help  2>/dev/stdout
	@$(MAKE) -C ${TARGET}  default >> output.default  2>/dev/stdout
	@$(MAKE) -C ${TARGET}  expose >> output.expose  2>/dev/stdout

	echo help > ${TARGET}/readme.md
	echo '```console' >> ${TARGET}/readme.md
	cat output.help | grep -v '^make\[' >> ${TARGET}/readme.md
	echo '```' >> ${TARGET}/readme.md
	echo run >> ${TARGET}/readme.md
	echo '```console' >> ${TARGET}/readme.md
	cat output.default | grep -v '^make\[' >> ${TARGET}/readme.md
	echo '```' >> ${TARGET}/readme.md
	echo --expose >> ${TARGET}/readme.md
	echo '```console' >> ${TARGET}/readme.md
	cat output.expose | grep -v '^make\[' >> ${TARGET}/readme.md
	echo '```' >> ${TARGET}/readme.md
	cat ${TARGET}/readme.md
