#!/bin/bash

if [ $EUID -eq 0 ]
then
    wget https://www.python.org/ftp/python/2.6.8/Python-2.6.8.tgz
    tar xfz Python-2.6.8.tgz
    cd Python-2.6.8
    sed -i '463s/^# //' Modules/Setup     # uncomment line for zlib support
    sed -i '256,258s/^#//' Modules/Setup  # sha256 support
    ./configure 
    make
    make altinstall     # altinstall to prevent damage to existing py binaries
    rm Python-2.6.8.tgz
    rm -rf Python-2.6.8
else
    echo "Please run as root"
fi
