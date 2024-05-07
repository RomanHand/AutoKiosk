#!/bin/bash

echo "Installing..."


mkdir /etc/webview-server/
mkdir /etc/webview-server/
mkdir /webview-server/
mkdir /webview-server/www/

cp ./config/config.yml /etc/webview-server/config.yml
cp ./web/* /webview-server/www/
cp ./main.py /usr/local/bin/wv-server
cp ./kiosk.py /usr/local/bin/kiosk

chmod +x /usr/local/bin/wv-server
chmod +x /usr/local/bin/kiosk

apt-get install $(grep -vE "^\s*#" ./reqs.txt  | tr "\n" " ")

cp ./system-files/xfwm-kiosk.desktop /usr/share/xsessions/xfwm-kiosk.desktop
cp ./system-files/lightdm.conf /etc/lightdm/lightdm.conf

chown -R kiosk:kiosk /webview-server/
chown -R kiosk:kiosk /etc/webview-server/
