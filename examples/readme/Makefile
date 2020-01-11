TARGET ?=

default: 00 01 02 03 04

00:
	$(MAKE) readme TARGET=$$(echo $@*)
01:
	$(MAKE) readme TARGET=$$(echo $@*)
02:
	$(MAKE) readme TARGET=$$(echo $@*)
03:
	$(MAKE) readme TARGET=$$(echo $@*)
04:
	$(MAKE) readme TARGET=$$(echo $@*)
05:
	$(MAKE) readme-multi TARGET=$$(echo $@*)

readme:
	@$(MAKE) -C ${TARGET} help 2>&1 | tee output.help
	@$(MAKE) -C ${TARGET} default 2>&1 | tee output.default
	@$(MAKE) -C ${TARGET} expose 2>&1 | tee output.expose

	echo help > ${TARGET}/readme.md
	echo '```console' >> ${TARGET}/readme.md
	printf '$$ ' >> ${TARGET}/readme.md
	cat output.help >> ${TARGET}/readme.md
	echo '```' >> ${TARGET}/readme.md

	echo run >> ${TARGET}/readme.md
	echo '```console' >> ${TARGET}/readme.md
	printf '$$ ' >> ${TARGET}/readme.md
	cat output.default >> ${TARGET}/readme.md
	echo '```' >> ${TARGET}/readme.md

	echo '`--expose`' >> ${TARGET}/readme.md
	echo '```console' >> ${TARGET}/readme.md
	printf '$$ ' >> ${TARGET}/readme.md
	cat output.expose >> ${TARGET}/readme.md
	echo '```' >> ${TARGET}/readme.md

readme-multi:
	@$(MAKE) -C ${TARGET} help 2>&1 | tee output.help
	@$(MAKE) -C ${TARGET} help-subcommand 2>&1 | tee output-subcomand.help
	@$(MAKE) -C ${TARGET} default 2>&1 | tee output.default
	# @$(MAKE) -C ${TARGET} expose 2>&1 | tee output.expose

	echo help > ${TARGET}/readme.md
	echo '```console' >> ${TARGET}/readme.md
	printf '$$ ' >> ${TARGET}/readme.md
	cat output.help >> ${TARGET}/readme.md
	echo '```' >> ${TARGET}/readme.md

	echo "help ( subcommand )" >> ${TARGET}/readme.md

	echo '```console' >> ${TARGET}/readme.md
	printf '$$ ' >> ${TARGET}/readme.md
	cat output-subcomand.help >> ${TARGET}/readme.md
	echo '```' >> ${TARGET}/readme.md

	echo run >> ${TARGET}/readme.md
	echo '```console' >> ${TARGET}/readme.md
	printf '$$ ' >> ${TARGET}/readme.md
	cat output.default >> ${TARGET}/readme.md
	echo '```' >> ${TARGET}/readme.md

	# echo '`--expose`' >> ${TARGET}/readme.md
	# echo '```console' >> ${TARGET}/readme.md
	# printf '$$ ' >> ${TARGET}/readme.md
	# cat output.expose >> ${TARGET}/readme.md
	# echo '```' >> ${TARGET}/readme.md
