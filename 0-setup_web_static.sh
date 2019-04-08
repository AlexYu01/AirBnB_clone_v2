#!/usr/bin/env bash
# Install Nginx if not already installed. Create a webpage for Nginx to serve.
sudo apt-get update
sudo apt-get install -y nginx

mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/
echo "Hello world" > /data/web_static/releases/test/index.html
if [ -e "/data/web_static/current" ]
then
	rm /data/web_static/current
fi
ln -s /data/web_static/releases/test/ /data/web_static/current

chown -R ubuntu:ubuntu /data/

CONFIG="\tserver {\n\t\tlisten 80;\n\t\tlocation /hbnb_static {\n\t\t\talias /data/web_static/current/;\n\t\t}\n\t}"

sed -i "/^http {/ a\ $CONFIG" /etc/nginx/nginx.conf
sed -i "s/^\tinclude \/etc\/nginx\/sites-enabled\/\*;/\t#include \/etc\/nginx\/sites-enabled\/\*;/g" /etc/nginx/nginx.conf

sudo service nginx restart
