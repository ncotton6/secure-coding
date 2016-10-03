#/bin/bash
mkdir -p /rootkit
cp rootkit.py /rootkit/rootkit.py

cat > /etc/init.d/csci642.sh << EOF
#!/bin/bash
echo hello | tee text.txt
EOF
	
chown root /etc/init.d/csci642.sh
chmod 700 /etc/init.d/csci642.sh
ln -s /etc/init.d/csci642.sh /etc/rc.d/
