# Install or update needed software
sudo apt-get update
sudo apt-get install -yq git supervisor python python-pip python3-distutils gunicorn
sudo pip install --upgrade pip virtualenv

# Fetch source code
mkdir -p $HOME/flask-app
cd $HOME/flask-app

git clone https://github.com/dr3jitsu/KafkaQuiz.git .

# Set ownership to newly created account
sudo chown -R $USER $HOME/flask-app

# Python environment setup
virtualenv -p python3 $HOME/flask-app/env
source $HOME/flask-app/env/bin/activate
$HOME/flask-app/env/bin/pip install -r $HOME/flask-app/requirements.txt


# Put supervisor configuration in proper place
#cp flask-ap/python-app.conf /etc/supervisor/conf.d/python-app.conf

# Start service via supervisorctl
supervisorctl reread
supervisorctl update
