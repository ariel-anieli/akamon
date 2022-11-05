BIN    := /usr/bin
PYTHON := $(BIN)/python3
SHELL  := $(BIN)/bash
SUDO   := $(BIN)/sudo
COOKIE := cookie
CONFIG := config.json
TEMP   := temp.json
LOG    := journal.json

CONTAINER	 := $(SUDO) $(BIN)/docker container
INIT_CONFIG	 := $(PYTHON) bin/init-config.py
CONFIG_CONTAINER := $(SHELL) bin/config-container.sh
INSTALL_CONFIG	 := $(PYTHON) bin/install-config.py
RANDOM_CONFIG	 := $(PYTHON) bin/random-config.py
CHECK_DEVICE	 := $(PYTHON) bin/check-device.py
TEST_DEVICE	 := $(PYTHON) bin/test-device.py
PRETTY_JSON	 := $(PYTHON) -mjson.tool --indent 2
JOURNAL_LOGGER	 := $(PYTHON) bin/logger.py

define silent-log
	$(JOURNAL_LOGGER) $1 $(CONFIG) >> $(LOG)
endef
define verbose-log
	$(JOURNAL_LOGGER) $1 $(CONFIG) | tee --append $(LOG)
endef

.SILENT: build
build: $(CONFIG)
	cp $< $(TEMP)
	$(CONFIG_CONTAINER) $(TEMP) > $<
	rm $(TEMP)
	$(call silent-log, $@)
	touch $@

.SILENT: install
install: $(CONFIG) build
	$(INSTALL_CONFIG) $< > $@ 
	$(call silent-log, $@)
	touch $@

.SILENT: test
test: $(CONFIG) install
	$(TEST_DEVICE) $(CONFIG)

.SILENT: check
check: $(CONFIG)
	$(CHECK_DEVICE) $(CONFIG) | $(PRETTY_JSON)

.SILENT: log
log:
	[ -f $(LOG) ] && tail -n5 $(LOG)

.SILENT: info
info:
	$(PRETTY_JSON) $(CONFIG)

.SILENT: config
config:
	$(RANDOM_CONFIG) $(if $(device), $(device), 1)

.SILENT: clean
clean: $(CONFIG) build
	$(CONTAINER) stop `jq -r '.container.id' $(CONFIG)` > /dev/null
	$(CONTAINER) rm `jq -r '.container.id' $(CONFIG)` > /dev/null
	jq 'del(.container)' $(CONFIG) > $(TEMP)
	cp $(TEMP) $(CONFIG)
	rm $(TEMP)
	[ -f build ] && rm build
	[ -f install ] && rm install
	$(call verbose-log, $@)

.SILENT: login
login: build $(CONFIG)
	sudo docker exec -it `jq -r '.container.id' $(CONFIG)` bash
