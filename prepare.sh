#!/bin/bash

# Dirty bash script to prepare the server for sheldonbot!

apt-get update
apt-get install git
apt-get install python-twisted
apt-get install python-setuptools
apt-get install python-pip
apt-get install python-bs4

pip install --upgrade requests


