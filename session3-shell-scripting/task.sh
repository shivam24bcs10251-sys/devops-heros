#!/bin/bash

# print current date, hostname and username
date
hostname
whoami

# system info: disk usage and running processes
df -h
ps

# Uses variables to store and use data
name="Shivam"
roll_no="24bcs10251"
echo "My name is $name"
echo "My roll_no is $roll_no"

# Takes user input
read -p "Enter a comment : " comment
echo "My comment: $comment"

# create a directory and a file, then write process info into the file
mkdir -p task_files
touch process.log
ps > process.log
