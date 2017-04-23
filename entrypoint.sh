#!/bin/bash

if [ ! -f /var/popperci/workspace ]; then
  echo "Expecting /var/popperci/workspace folder"
  exit 1
fi

if [ ! -f /var/popperci/credentials ]; then
  echo "Expecting /var/popperci/credentials folder"
  exit 1
fi

if [ ! -f /var/popperci/db ]; then
  echo "Expecting /var/popperci/db folder"
  exit 1
fi

if [ -z "$WEB2PY_ADMIN" ]; then
  WEB2PY_ADMIN=admin
fi

ln -s

cd /app
./executioner.py &
python webhooks.py &
/root/entrypoint.sh

