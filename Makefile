DIST = epel-7-x86_64
MOCK = mock --resultdir=RPMS
RPMBUILD = rpmbuild --define="_topdir $$PWD"

TELLCORE_SRC = SOURCES/tellcore-py-1.1.3.tar.gz
TELLCORE_SRPM = SRPMS/tellcore-py-1.1.3-1.el7.centos.src.rpm
TELLDUSCORE_SRC = SOURCES/telldus-core-2.1.2.tar.gz
TELLDUSCORE_SRPM = SRPMS/telldus-core-2.1.2-3.ts2.el7.centos.src.rpm
TELLIVE_SRC = SOURCES/tellive-py-0.5.2.tar.gz
TELLIVE_SRPM = SRPMS/tellive-py-0.5.2-3.el7.centos.src.rpm
TELLPROX_SRC = SOURCES/tellprox-f1461664020cd555567971068b577360a821b348.tar.gz
TELLPROX_SRPM = SRPMS/tellprox-0.28_20140710_f1461664-1.el7.centos.src.rpm

SOURCES = \
	${TELLCORE_SRC} \
	${TELLDUSCORE_SRC} \
	${TELLIVE_SRC} \
	${TELLPROX_SRC}

SRPMS = \
	${TELLCORE_SRPM} \
	${TELLDUSCORE_SRPM} \
	${TELLIVE_SRPM} \
	${TELLPROX_SRPM}

all: verified.stamp
	@echo "All sources are downloaded, you can now run make build or make mockbuild"

mockbuild: verified.stamp
	for srpm in ${SRPMS}; do \
		${MOCK} -r ${DIST} $$srpm; \
	done

build: srpms
	for srpm in ${SRPMS}; do \
		${RPMBUILD} --rebuild -ba $$srpm; \
	done

srpms: ${SRPMS}

${TELLCORE_SRPM}: verified.stamp
	${RPMBUILD} -bs SPECS/tellcore-py.spec

${TELLDUSCORE_SRPM}: verified.stamp
	${RPMBUILD} -bs SPECS/telldus-core.spec

${TELLIVE_SRPM}: verified.stamp
	${RPMBUILD} -bs SPECS/tellive-py.spec

${TELLPROX_SRPM}: verified.stamp
	${RPMBUILD} -bs SPECS/tellprox.spec

verified.stamp: ${SOURCES} sources.sha256
	sha256sum -c sources.sha256 && touch $@

download: ${SOURCES} sources.sha256
	sha256sum -c sources.sha256 && touch $@

SOURCES/tellcore-py-1.1.3.tar.gz:
	wget https://github.com/erijo/tellcore-py/archive/v1.1.3.tar.gz -O $@

SOURCES/telldus-core-2.1.2.tar.gz:
	wget http://download.telldus.se/TellStick/Software/telldus-core/telldus-core-2.1.2.tar.gz -O $@

SOURCES/tellive-py-0.5.2.tar.gz:
	wget https://github.com/erijo/tellive-py/archive/v0.5.2.tar.gz -O $@

SOURCES/tellprox-f1461664020cd555567971068b577360a821b348.tar.gz:
	wget https://github.com/p3tecracknell/tellprox/archive/f1461664020cd555567971068b577360a821b348.tar.gz -O $@

clean:
	rm -f verified.stamp ${SRPMS}
	rm -rf RPMS

distclean: clean
	rm -f ${SOURCES}
