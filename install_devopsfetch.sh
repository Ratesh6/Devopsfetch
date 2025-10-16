#!/usr/bin/env bash
set -euo pipefail

echo "Installing devopsfetch..."

apt-get update -y
apt-get install -y python3 python3-pip python3-venv nginx docker.io logrotate

mkdir -p /opt/devopsfetch /var/log/devopsfetch
cp devopsfetch.py /opt/devopsfetch/
chmod +x /opt/devopsfetch/devopsfetch.py

python3 -m venv /opt/devopsfetch/venv
source /opt/devopsfetch/venv/bin/activate
pip install tabulate python-dateutil

# Create wrapper
cat << 'EOF' > /usr/local/bin/devopsfetch
#!/usr/bin/env bash
source /opt/devopsfetch/venv/bin/activate
python /opt/devopsfetch/devopsfetch.py "$@"
EOF
chmod +x /usr/local/bin/devopsfetch

# Copy systemd files
cp devopsfetch.service /etc/systemd/system/
cp devopsfetch.timer /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now devopsfetch.timer

# Logrotate setup
cp devopsfetch.logrotate /etc/logrotate.d/devopsfetch

echo "Installation complete! Run 'devopsfetch -h'"
