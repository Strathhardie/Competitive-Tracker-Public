#!/bin/bash

mkdir -p ./excel_dump || { echo "error: excel_dump/ could not be created"; exit 1; }

if [ $1 == 'unzip' ]
then
	unzip -u Excel\ Scanner/competitive_scanner.xlsm -d ./excel_dump || { echo "error: can't unzip to excel_dump/"; exit 1; }

elif [ $1 == 'zip' ]
then
	cd ./excel_dump
	zip -r ../Excel\ Scanner/competitive_scanner2.xlsm $(ls) || { echo "error: excel dump is empty, please unzip file first"; exit 1; }
	cd ..

else
	echo "invalid argument"
	exit 1;
fi

exit 0;