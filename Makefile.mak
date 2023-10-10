# CFLAGS = -g -Wall
# LDFLAGS= -pthread  -lpthread
# DEPS= linked_list.h
# OBJ= linked_list.o

# %.o: %.c $(DEPS)
#         $(CC) -c -o $@ $< $(CFLAGS)

# linked_list: $(OBJ)
#     $(CC) -o $@ $^ $(CFLAGS) $(LDFLAGS)

# linked_list.o: linked_list.c linked_list.h
# 	$(CC) -c linked_list.c $(CFLAGS) -I.

# linked_list: linked_list.c
# 	gcc -o linked_list linked_list.c -pthread
#gcc -pthread -o linked_list linked_list.cz


# The name of the source files
SOURCES = linked_list.c

# The name of the executable
EXE = linked_list

# Flags for compilation (adding warnings are always good)
CFLAGS = -Wall

# Flags for linking (none for the moment)
LDFLAGS = -lm -lrt -lpthread

# Libraries to link with (none for the moment)
LIBS =

# Use the GCC frontend program when linking
LD = gcc

# This creates a list of object files from the source files
OBJECTS = $(SOURCES:%.c=%.o)

# The first target, this will be the default target if none is specified
# This target tells "make" to make the "all" target
default: all

# Having an "all" target is customary, so one could write "make all"
# It depends on the executable program
all: $(EXE)

# This will link the executable from the object files
$(EXE): $(OBJECTS)
    $(LD) $(LDFLAGS) $(OBJECTS) -o  $(EXE) $(LIBS)

# This is a target that will compiler all needed source files into object files
# We don't need to specify a command or any rules, "make" will handle it automatically
%.o: %.c

# Target to clean up after us
clean:
    -rm -f $(EXE)      # Remove the executable file
    -rm -f $(OBJECTS)  # Remove the object files

# Finally we need to tell "make" what source and header file each object file depends on
linked_list.o: linked_list.c linked_list.h