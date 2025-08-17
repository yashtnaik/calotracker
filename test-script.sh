#!/bin/bash

cat Jenkinsfile
ls -lrth
sudo apt-get install cowsay -y
cowsay -f dragon "Hello, World!" > output.txt
cat output.txt