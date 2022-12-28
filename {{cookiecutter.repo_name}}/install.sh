#/usr/bin/sh

echo "create venv"
[ -d "venv" ] && echo "venv already exist" ||  { python -m venv venv; }

echo "install packages"
source venv/bin/activate
pip install --upgrade pip
pip install --requirement requirements/production.txt
pip install --requirement requirements/develop.txt

echo "download html-packages"

templateDir="src/{{cookiecutter.package_name}}/_templates"
staticDir="src/{{cookiecutter.package_name}}/_static"

cssDir="${staticDir}/css"
jsDir="${staticDir}/js"

mkdir -p "${templateDir}"

mkdir -p "${cssDir}"
mkdir -p "${jsDir}"


# Bootstrap
mkdir -p "${cssDir}/bootstrap"
mkdir -p "${jsDir}/bootstrap"

wget "https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" -O "${cssDir}/bootstrap/bootstrap.min.css"
wget "https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" -O "${jsDir}/bootstrap/bootstrap.bundle.min.js"
