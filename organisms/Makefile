REPOS = $(wildcard *_ensembl *_ncbi *_flybase*) 

.PHONY: all

${REPOS}::
	cd $@; ${MAKE}

all: ${REPOS}

show:
	echo ${REPOS}
