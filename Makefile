NAME = hom.py
PKGNAME = python-hom

.PHONY: git-archive VERSION-set TARGET-set

git-archive: VERSION-set
	git archive --prefix $(NAME)-$(VERSION)/ -o $(NAME)-$(VERSION).tar.gz v$(VERSION)

mock-buildsrpm: git-archive
	mock --buildsrpm --spec ${PKGNAME}.spec --sources . --resultdir ./srpm/
	cp ./srpm/${PKGNAME}*src.rpm .
	rm -Rf ./srpm/

mock-rebuild: mock-buildsrpm TARGET-set
	mock -r $(TARGET) --rebuild $(PKGNAME)*src.rpm --resultdir=./rpms/"%(dist)s"/"%(target_arch)s"/
	find rpms -name '*.log' | xargs rm

VERSION-set:
ifndef VERSION
	$(error VERSION undefined)
endif

TARGET-set:
ifndef TARGET
	$(error TARGET undefined)
endif
