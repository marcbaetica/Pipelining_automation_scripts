echo Updating apt packages:
sudo apt update && sudo apt update  # First does security and archive pulls, while second does AWS regional ones.
echo Installing XRDP:
sudo apt -qq install -y xrdp
echo Installing GNOME Desktop Environment:
sudo apt -qq install -y gnome-session gdm3
