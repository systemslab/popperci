#!/bin/bash

if [ ! -d /var/popperci/workspace ]; then
  echo "Expecting /var/popperci/workspace folder"
  exit 1
fi

if [ ! -d /var/popperci/credentials ]; then
  echo "Expecting /var/popperci/credentials folder"
  exit 1
fi

if [ ! -d /var/popperci/db ]; then
  echo "Expecting /var/popperci/db folder"
  exit 1
fi

if [ -z "$WEB2PY_ADMIN" ]; then
  WEB2PY_ADMIN=admin
fi

ln -s /var/popperci/db /opt/web2py/applications/popperci/databases

touch /var/popperci/db/storage.sqlite

cd /app
./executioner.py &
python webhooks.py &
/sbin/my_init
