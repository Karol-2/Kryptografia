#!/bin/bash

if [ ! -e hash.txt ];then
    touch hash.txt
else
    rm hash.txt
    touch hash.txt
fi

cat personal.txt | md5sum >> hash.txt
cat personal.txt | sha1sum >> hash.txt
cat personal.txt | sha224sum >> hash.txt
cat personal.txt | sha256sum >> hash.txt
cat personal.txt | sha384sum >> hash.txt
cat personal.txt | sha512sum >> hash.txt
cat personal.txt | b2sum >> hash.txt
echo "Done"