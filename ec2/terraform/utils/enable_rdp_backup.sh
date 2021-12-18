sudo apt -y update
sudo apt -y upgrade
sed -i 's/^PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config
/etc/init.d/ssh restart
passwd ubuntu
#apt install xrdp xfce4 xfce4-goodies tightvncserver
apt install -y xrdp
apt install -y xfce4
apt install -y xfce4-goodies
apt install -y tightvncserver
xfce4-session > /home/ubuntu/.xsession
cp /home/ubuntu/.xsession /etc/skel
sed -i '0,/-1/s//ask-1/' /etc/xrdp/xrdp.ini
service xrdp restart
