# LUCID EMPIRE TITAN :: Hardware Masking Module Build System

# Kernel module object name
MODULE_NAME := titan_hw
obj-m += $(MODULE_NAME).o

# Kernel build directory
KERNEL_BUILD ?= /lib/modules/$(shell uname -r)/build

# Installation paths
INSTALL_MOD_DIR ?= /opt/lucid-empire/kernel-modules
MODULE_FILE := $(MODULE_NAME).ko

# Build targets
.PHONY: all clean install uninstall test

all:
@echo "Building TITAN hardware masking module..."
$(MAKE) -C $(KERNEL_BUILD) M=$(PWD) modules
@echo "Module built successfully: $(MODULE_FILE)"

clean:
@echo "Cleaning build artifacts..."
$(MAKE) -C $(KERNEL_BUILD) M=$(PWD) clean
rm -f *.o *.ko *.mod.c *.mod *.order *.symvers

install: all
@echo "Installing module to $(INSTALL_MOD_DIR)..."
install -d $(INSTALL_MOD_DIR)
install -m 644 $(MODULE_FILE) $(INSTALL_MOD_DIR)/
@echo "Module installed successfully"

uninstall:
@echo "Removing module from $(INSTALL_MOD_DIR)..."
rm -f $(INSTALL_MOD_DIR)/$(MODULE_FILE)

test:
@echo "Module testing requires kernel implementation"
@echo "Use /opt/lucid-empire/bin/validate-kernel-masking.py after loading"

help:
@echo "TITAN Hardware Masking Module - Build System"
@echo ""
@echo "Targets:"
@echo "  all       - Build the kernel module (default)"
@echo "  clean     - Remove build artifacts"
@echo "  install   - Install module to system directory"
@echo "  uninstall - Remove installed module"
@echo "  test      - Run validation tests"
@echo ""
@echo "Note: Requires kernel headers for $(shell uname -r)"
@echo "Install with: apt-get install linux-headers-$(shell uname -r)"
