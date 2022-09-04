#!/usr/bin/bash

# This script is used to setup the environment for the project
# It is assumed that the user has already installed the required packages
# and has a working version of 

# Insall the required packages
pip install -r requirements.txt

# Download the required data and unzip it
echo "This script will download the required data for the project from kaggle"
echo "Please make sure you have a kaggle account and have installed the kaggle cli"
echo "wish to continue? (y/n)"
read ans

if [ $ans == "y" ]
then
    kaggle competitions download -c zillow-prize-1
    echo "Download complete"
    unzip zillow-prize-1.zip &
    pid=$!

    spin[0]="-"
    spin[1]="\\"
    spin[2]="|"
    spin[3]="/"

    echo -n "[unzipping the data] ${spin[0]}"
    while [ kill -0 $pid ]
    do
        for i in "${spin[@]}"
        do
            echo -ne "\b$i"
            sleep 0.1
        done
    done

    mv zillow-prize-1/* ./Zillow/dataset/
    rm jigsaw-toxic-comment-classification-challenge.zip
    rm -r zillow-prize-1
    
else
    echo "Download aborted"
    exit 1
fi