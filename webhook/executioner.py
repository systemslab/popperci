#!/usr/bin/env python

import logging
import json
import os
import os.path

from multiprocessing.connection import Listener
from sqlalchemy import *
from subprocess import Popen, PIPE

workspace_path = os.environ['WORKSPACE']
credentials_path = os.environ['CREDENTIALS']
sqlite_file = os.environ['SQLITEDB']

logger = logging.getLogger('webhook-handler')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
logger.addHandler(ch)


def sh(cmd):
    process = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    out, err = process.communicate()
    ecode = process.returncode

    return ecode, out, err


def shf(cmd):
    # run sh and fail if non-zero exit
    ecode, _, _ = sh(cmd)
    if ecode != 0:
        raise Exception("Non-zero exit ({}) for '{}'".format(ecode, cmd))


def popper_check_experiment(workspace, environment):
    cmd = (
        "docker run --rm "
        "  --volume `which docker`:/usr/bin/docker "
        "  --volume /var/run/docker.sock:/var/run/docker.sock "
        "  --volume {0}:{0} "
        "  --workdir {0} "
        "  {1} "
        "  ivotron/popperci"
    ).format(workspace, ' '.join(environment))

    logger.info("Executing: " + cmd)

    ecode, _, _ = sh(cmd)

    return ecode


def get_project_info(db, payload):
    project_name = payload['repository']['name']
    url = payload['repository']['url']
    uname = payload['repository']['owner']['name']

    users = Table('auth_user', MetaData(db), autoload=True)
    user = users.select(users.c.username == uname).execute().fetchone()

    if not user:
        raise Exception("User {} not registered.".format(uname))

    projects = Table('project', MetaData(db), autoload=True)
    project = users.select(projects.c.username == uname and
                           projects.c.name == projectname).execute().fetchone()

    if not project:
        projects.insert().execute(user_id=uid, name=project_name, url=url)

    return user.id, uname, project_name, url


def insert_execution(db, uid, project, payload):
    executions = Table('build', MetaData(db), autoload=True)
    res = executions.insert().execute(user_id=uid, project=project,
                                      meta=json.dumps(payload))
    return res.inserted_primary_key[0]


def get_credentials(db, uid):
    creds = Table('credentials', MetaData(db), autoload=True)
    return creds.select(creds.c.owner_id == uid).execute()


def insert_result(db, exec_id, ecode, experiment, workspace):
    if ecode != 0:
        experiment_status = 'FAIL'
    else:
        with open('{}/popper_status'.format(workspace), 'r') as f:
            experiment_status = f.read().strip()

    results = Table('experiment', MetaData(db), autoload=True)
    results.insert().execute(build_id=exec_id, experiment_name=experiment,
                             status=experiment_status)


def popper_check_project(payload):

    db = create_engine('sqlite:///{}'.format(sqlite_file))

    uid, uname, project, url = get_project_info(db, payload)

    exec_id = insert_execution(db, uid, project, payload)

    workspace = '{}/{}/{}/{}'.format(workspace_path, uname, project, exec_id)

    shf("mkdir -p " + workspace)
    shf("git clone --recursive {} {}".format(url, workspace))

    environment = []

    for c in get_credentials(db, uid):
        if c.cred_text:
            env_item = '-e {}={}'.format(c.name, c.cred_text)
        else:
            cred_path = credentials_path + '/' + c.cred_file
            env_item = '-v {}:{}'.format(cred_path, c.name)

        environment += [env_item]

    for experiment in os.listdir(workspace + '/experiments'):

        experiment_path = workspace + '/experiments/' + experiment
        ecode = popper_check_experiment(experiment_path, environment)

        insert_result(db, exec_id, ecode, experiment, experiment_path)

    db.dispose()


if __name__ == '__main__':

    if not os.path.isfile(sqlite_file):
        raise Exception("Can't find file {}".format(sqlite_file))
    if not os.path.isdir(credentials_path):
        raise Exception("Can't find folder {}".format(credentials_path))
    if not os.path.isdir(workspace_path):
        raise Exception("Can't find folder {}".format(workspace_path))

    address = ('localhost', 6000)
    listener = Listener(address)
    conn = listener.accept()

    while True:
        payload_fname = conn.recv()

        with open(payload_fname, 'r') as f:
            payload = json.load(f)

        popper_check_project(payload)
