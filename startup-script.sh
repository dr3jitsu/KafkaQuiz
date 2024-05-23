# Install or update needed software
apt-get update
apt-get install -yq git supervisor python python-pip python3-distutils
pip install --upgrade pip virtualenv

# Fetch source code
export HOME=/home/ahartono
mkdir -p $HOME/flask-app
cd $HOME/flask-app

git clone https://github.com/dr3jitsu/KafkaQuiz.git .

# Install Cloud Ops Agent
#sudo bash $HOME/flask-app/add-google-cloud-ops-agent-repo.sh --also-install

# Account to own server process
useradd -m -d $HOME/flask-ap flask-ap

# Python environment setup
virtualenv -p python3 $HOME/flask-app/env
/bin/bash -c "source $HOME/flask-app/env/bin/activate"
$HOME/flask-app/env/bin/pip install -r $HOME/flask-app/requirements.txt

# Set ownership to newly created account
chown -R flask-ap:flask-ap $HOME/flask-app

# Put supervisor configuration in proper place
#cp flask-ap/python-app.conf /etc/supervisor/conf.d/python-app.conf

# Start service via supervisorctl
supervisorctl reread
supervisorctl update
