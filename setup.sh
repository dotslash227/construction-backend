#!/bin/bash

VERSION=`lsb_release -a | grep "Distributor" | awk '{print $3}'`
PKG_INSTALLER="yum"
if [ "${VERSION}" == "Ubuntu" ]
then
 PKG_INSTALLER="apt-get"
 PKG_NAMES=" gcc libmysqlclient-dev python-devel libffi-devel openssl-devel "
else
 PKG_INSTALLER="yum"
 PKG_NAMES=" mysql-devel build-essential libssl-dev libffi-dev python-dev "
fi

sudo su - << COMMANDS
${PKG_INSTALLER} install ${PKG_NAMES} fabric python-devel -y
pip install virtualenv
COMMANDS

## Configure sudo less ssh localhost ##
ssh -o "StrictHostKeyChecking no" localhost "exit"
STATUS_CODE="$?"
if [ ${STATUS_CODE} != 0 ];then
  echo "Configuring ssh to localhost"
  ssh-keygen -b 2048 -t rsa -f ~/.ssh/id_rsa -q -N ""
  cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
  chmod og-wx ~/.ssh/authorized_keys
  ssh -o "StrictHostKeyChecking no" localhost "exit"
else
  echo "sudo less ssh already done"
fi

virtualenv venv
source venv/bin/activate
mkdir supervisor
python setup.py install
pip install -r requirements.txt
pip install supervisor
