all: clean bcast_skeleton

CC = smpicc
OPTC = -O4

bcast: bcast_skeleton.o
	$(CC) $(OPTC) -o bcast_skeleton bcast_skeleton.o -lm


.c.o:
	$(CC) $(OPTC) -c $*.c

clean:
	rm -f bcast_skeleton *.o
