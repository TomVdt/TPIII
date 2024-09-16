
MAKEDIR = $(realpath $(dir $(abspath $(lastword $(MAKEFILE_LIST)))))

.PHONY: install plots clean folders

install:
	test -d $(MAKEDIR)/.venv || (\
		python -m venv $(MAKEDIR)/../.venv && \
		. $(MAKEDIR)/../.venv/bin/activate && (\
			python -m pip install -r $(MAKEDIR)/../requirements.txt \
		)
	)

folders:
	mkdir -p $(MAKEDIR)/data $(MAKEDIR)/figures

plots: folders
	. $(MAKEDIR)/../.venv/bin/activate && (\
		python -m jupyter execute $(MAKEDIR)/analyse/*.ipynb \
	)

clean:
	@rm -f $(MAKEDIR)/figures/*.pdf
	@rm -f $(MAKEDIR)/rapport.aux \
		$(MAKEDIR)/rapport.bcf \
		$(MAKEDIR)/rapport.fdb_latexmk \
		$(MAKEDIR)/rapport.log \
		$(MAKEDIR)/rapport.run.xml \
		$(MAKEDIR)/rapport.bbl \
		$(MAKEDIR)/rapport.blg \
		$(MAKEDIR)/rapport.fls \
		$(MAKEDIR)/rapport.pdf \
		$(MAKEDIR)/rapport.synctex.gz

