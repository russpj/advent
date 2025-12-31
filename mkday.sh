#!/bin/bash
# This script prints a greeting message
if [[ -n $1 ]] && [[ -n $2 ]] && [[ -n $3 ]]; then
    echo "copy ./$1/advent.py to $1/$2/$3"
    if ! [ -d "$1" ]; then
        mkdir $1
    fi
    if ! [ -d "$1/$2" ]; then
        mkdir $1/$2
    fi
    cp advent.py $1/$2/$3.py
    sed -i 's/{year}/2025/;s/{name}/network/;s/{day}/11/' $1/$2/$3.py
else
    echo "mkday.sh {year} {day} {name}"
fi