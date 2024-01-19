apt update -y # Need to update repositories so installs work
apt-get install python3-numpy libicu-dev -y
pip install -U pip
pip install -r requirements.txt
pip install jupyterlab