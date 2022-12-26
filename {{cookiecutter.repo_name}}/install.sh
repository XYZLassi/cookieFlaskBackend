#/usr/bin/sh

echo "create .venv"
python -m venv venv

echo "install packages"
source venv/bin/activate
pip install --upgrade pip
pip install --requirement requirements/production.txt
pip install --requirement requirements/develop.txt
