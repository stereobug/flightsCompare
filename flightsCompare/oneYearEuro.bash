#! /bin/bash

for x in `cat eurocities.txt`
do
        python3.7 /code/seleniumHeadlessModThreadsSuperList.py -n 365 -u 70 -p 70 -c $x
done

