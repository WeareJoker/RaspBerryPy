TEMPLATE = app
CONFIG += console c++11
CONFIG -= app_bundle
CONFIG -= qt

INCLUDEPATH *= include
LIBS *= -lcrypto -lpcap

SOURCES += \
    common.c \
    crypto.c \
    wdecrypt.cpp

HEADERS += \
    aircrack-ng.h \
    aircrack-ptw-lib.h \
    common.h \
    crctable.h \
    crypto.h \
    version.h \
    osdep/byteorder.h \
    include/eapol.h
