#-------------------------------------------------
#
# Project created by QtCreator 2015-11-07T16:39:03
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = untitled
TEMPLATE = app


SOURCES += main.cpp\
        mainwindow.cpp \
    superslider.cpp

HEADERS  += mainwindow.h \
    superslider.h
#INCLUDEPATH += /usr/include/qxt/QxtCore
#INCLUDEPATH += /usr/include/qxt/QxtGui

FORMS    += mainwindow.ui

CONFIG += c++11

#CONFIG += gxt
#QXT += core gui


#LIBS += "/usr/local/lib/libopencv_core.so.3.0"
#LIBS += "/usr/local/lib/libopencv_imgproc.so.3.0"
#LIBS += "/usr/local/lib/libopencv_highgui.so.3.0"
LIBS += "/usr/local/lib/*.so*"
#LIBS += "/usr/lib/x86_64-linux-gnu/libQxtGui.so"
#LIBS += "/usr/lib/x86_64-linux-gnu/libQxtCore.so"
