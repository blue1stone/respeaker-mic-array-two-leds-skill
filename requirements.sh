# Copy the rule file which allows non-root read/write access to the mic array
sudo cp ./99-respeaker-mycroft.rules /etc/udev/rules.d/
# Restart udev
sudo udevadm trigger