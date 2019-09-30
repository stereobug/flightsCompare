#! /bin/bash

for x in GLA EDI PIK
do
        python3.7 /code/seleniumHeadlessModThreadsSuperList.py -n 365 -u 50 -p 16 -c $x
done

