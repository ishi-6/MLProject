# Makefile for performance_module

CC = gcc
CFLAGS = -Wall -O2 -fPIC
TARGET = performance_module.so

all: $(TARGET)

$(TARGET): performance_module.c
	$(CC) $(CFLAGS) -shared -o $(TARGET) performance_module.c

clean:
	rm -f $(TARGET)
