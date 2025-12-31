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
    cp $1/advent.py $1/$2/$3
else
    echo "mkday.sh {year} {day} {name}"
fi