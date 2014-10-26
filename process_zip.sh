#!/bin/bash

mkdir -p tmp/$1
unzip $1 -d tmp/$1
cd tmp/$1
XYZ="$(cat *o | grep 'POSITION XYZ' | awk '{print $1,$2,$3}' | sed -e 's/ /, /g')"
RinDump *o ELE S1C --timefmt "%02d-%02m-%04Y %02H:%02M:%02S" --ref "\"${XYZ}"\" --eph *.sp3 > ../../$1.rindump
cd ../..
python detect_jam.py $1.rindump
rm -rf tmp/*
rm *.zip
echo "$1 processed"
