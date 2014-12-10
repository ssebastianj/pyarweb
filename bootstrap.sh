#!/usr/bin/env bash

# Install dependencies
apt-get update
apt-get install -y git-core python3-dev python3-pip gettext libxml2-dev libxslt1-dev zlib1g-dev

# Install Redis
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make && make install

# Install project requirements
pip3 install -r /vagrant/requirements.txt
