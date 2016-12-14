all: wdecrypt
	g++ -Wl,-O1 -o wdecrypt common.o crypto.o wdecrypt.o   -lcrypto -lpcap 

wdecrypt: common.o crypto.o wdecrypt.o
	g++ -Wl,-O1 -o wdecrypt common.o crypto.o wdecrypt.o   -lcrypto -lpcap 

common.o : common.c
	gcc -c -pipe -O2 -Wall -W -fPIC  -I. -Iinclude -o common.o common.c

crypto.o : crypto.c
	gcc -c -pipe -O2 -Wall -W -fPIC  -I. -Iinclude -o crypto.o crypto.c

wdecrypt.o : wdecrypt.cpp
	g++ -c -pipe -O2 -std=gnu++11 -Wall -W -fPIC  -I. -Iinclude -I/opt/Qt/5.7/gcc_64/mkspecs/linux-g++ -o wdecrypt.o wdecrypt.cpp

clean:
	rm -f wdecrypt
	rm -f *.o

