CC = gcc
CCOPTS = -c -g -Wall
LINKOPTS = -g

EXEC = gp_lib.o
TEST = test
OBJECTS = GlamourPrint.o LL.o

all: $(EXEC)

$(EXEC):
	$(CC) $(LINKOPTS) GlamourPrint.c -g -c -o $@

$.o:%.c
	$(CC) $(CCOPTS) -o $@ $^

$(TEST): testrunner.c $(OBJECTS)
	$(CC) $(LINKOPTS) -o $@ $^

clean:
	- $(RM) $(EXEC)
	- $(RM) $(OBJECTS)
	- $(RM) $(TEST)
	rm -r *.dSYM
