
#******************************************************************************
# Makefile - Rules for building the project.
#
# Copyright (c) 2023
# All rights reserved.
#******************************************************************************
TARGET := firmware
BUILD := build

SHELL:=/bin/bash
#### Setup ####

TOOLCHAIN ?= arm-none-eabi

# Set Target family and name
FAMILY= STM32L5xx
BOARD= NUCLEO_L552ZE_Q

CPU = cortex-m33
FPU = fpv5-sp-d16
#FABI = softfp
FABI = hard

LINKER_FILE := ./STM32L552ZETXQ_FLASH.ld
STARTUP_FILE := startup_stm32l552zetxq.s

#### Required Executables ####
CC = $(TOOLCHAIN)-gcc
GCC = $(TOOLCHAIN)-gcc
CPP = $(TOOLCHAIN)-cpp
LD = $(TOOLCHAIN)-ld
CP = $(TOOLCHAIN)-objcopy
OD = $(TOOLCHAIN)-objdump
RD = $(TOOLCHAIN)-readelf
AR = $(TOOLCHAIN)-ar
SIZE = $(TOOLCHAIN)-size
RM = $(shell which rm 2>/dev/null)

EXECUTABLES = CC LD CP OD AR RD SIZE GCC
K := $(foreach exec,$(EXECUTABLES),\
		$(if $(shell which $($(exec)) 2>/dev/null),,\
		$(info $(exec) not found on PATH ($($(exec))).)$(exec)))
$(if $(strip $(value K)),$(info Required Program(s) $(strip $(value K)) not found))

ifneq ($(strip $(value K)),)
all clean:
	$(RM) -rf bin
else

DEFINES+= -DDEBUG

# Project includes
INCLUDES+=

# Project Path
VPATH = ./src
VPATH += ./asm

# Add ST Resources here...
SRC = $(STARTUP_FILE)

# Project
SRC += main.c
SRC += syscalls.c

# target
CSRC = $(filter %.c,$(SRC))
ASRC = $(filter %.s,$(SRC))

OBJS = $(CSRC:%.c=$(BUILD)/%.o)
OBJS+= $(ASRC:%.s=$(BUILD)/%.o)

DEPS = $(CSRC:%.c=$(BUILD)/%.d)
DEPS+= $(ASRC:%.s=$(BUILD)/%.d)

LIBS =

CFLAGS = -mthumb -mcpu=$(CPU) -mfpu=$(FPU) -mfloat-abi=$(FABI)
CFLAGS+= -ffunction-sections -fdata-sections -fmessage-length=0 -fstack-usage --specs=nano.specs
CFLAGS+= -std=gnu11 -Wall -g3 -c
CFLAGS+= -Os
CFLAGS+= $(DEFINES)
CFLAGS+= $(INCLUDES)
CFLAGS+= 

# 
LFLAGS = -mthumb -mcpu=$(CPU) -mfpu=$(FPU) -mfloat-abi=$(FABI)
LFLAGS+= --specs=nosys.specs -Wl,-Map="$(BUILD)/$(TARGET).map" -Wl,--gc-sections -static --specs=nano.specs
LFLAGS+= -Wl,--start-group -lc -lm -Wl,--end-group
LFLAGS+=

# Additional user specified CFLAGS
CFLAGS+=$(EXTRA_CFLAGS)
CPFLAGS = -Obinary
ODFLAGS = -S

#### Rules ####
all: directories $(BUILD)/$(TARGET).hex

directories: $(BUILD)

$(BUILD):
	@mkdir -p $@

$(BUILD)/%.o: %.c $(BUILD)/%.d
	@echo " Compiling $(COMPILERNAME) $<" ;\
	$(CC) -c $(CFLAGS) $< -o $@

$(BUILD)/%.o: %.s $(BUILD)/%.d
	@echo " Assembling $(COMPILERNAME) $<" ;\
	$(CC) -c $(CFLAGS) $< -o $@

$(BUILD)/$(TARGET).axf: $(OBJS)
	@echo " Linking $(COMPILERNAME) $@" ;\
	$(CC) -Wl,-T,$(LINKER_FILE) -o $@ $(OBJS) $(LFLAGS)

$(BUILD)/$(TARGET).bin: $(BUILD)/$(TARGET).axf
	@echo " Copying $(COMPILERNAME) $@..." ;\
	$(CP) $(CPFLAGS) $< $@ ;\
	$(OD) $(ODFLAGS) $< > $(BUILD)/$(TARGET).lst

$(BUILD)/$(TARGET).hex: $(BUILD)/$(TARGET).axf
	@echo " Copying $(COMPILERNAME) $@..." ;\
	$(CP) -O ihex $< $@ ;\

clean:
	@echo "Cleaning..." ;\
	$(RM) -f $(OBJS) $(DEPS) \
		$(BUILD)/$(TARGET).bin $(BUILD)/$(TARGET).axf \
		$(BUILD)/$(TARGET).lst $(BUILD)/$(TARGET).map \
		$(BUILD)/$(TARGET).hex

$(BUILD)/%.d: ;


# Automatically include any generated dependencies
-include $(DEPS)
endif
.PHONY: all clean directories
