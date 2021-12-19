echo Updating apt packages:
sudo apt-get update
sudo apt-get update  # TODO: See why running only once does not find the rdp package in subsequent steps.
echo Installing XRDP:
sudo apt install -y xrdp
echo Installing GNOME Desktop Environment:
sudo apt install -y gnome-session gdm3

# sudo passwd ubuntu
