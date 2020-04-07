#!/bin/bash

sudo apt-get update
sudo apt-get install -y python3 python3-pip git
git clone https://github.com/CU-NVM/redis-load-tester

cd redis-load-tester
cd Scripts
pip3 install -r requirments.txt


#locust -f redis_get_set.py --master
#
#locust -f redis_get_set.py --slave --master-host=35.193.187.125

