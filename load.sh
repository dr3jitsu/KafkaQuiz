#!/bin/bash
export CONFLUENT_HOME=/Users/ahartono/Downloads/workingspace/confluent-7.2.1
export PATH=$PATH:$CONFLUENT_HOME/bin
export PATH=/Users/ahartono/Downloads/workingspace/kafka-docker-playground/scripts/cli:$PATH
virtualenv env
source env/bin/activate
echo "Run :     source env/bin/activate"
echo "Run :     python app.py"
