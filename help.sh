#!/bin/bash

for mod in requirements.txt
do 
    pip uninstall $mod 
done 