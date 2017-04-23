#!/usr/bin/env python

from subprocess import Popen, PIPE
from os import path
import argparse

stages = ['setup.sh', 'run.sh', 'teardown.sh', 'validate.sh']


def sh(cmd):
    process = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    out, err = process.communicate()
    ecode = process.returncode

    return ecode, out, err


def writefile(fname, content):
    with open(fname, 'w') as f:
        f.write(content)


def execute(stage):
    ecode, out, err = sh(stage)

    writefile('popper_logs/{}.{}'.format(stage, 'out'), out)
    writefile('popper_logs/{}.{}'.format(stage, 'err'), err)

    return ecode, out


def check_experiment():
    sh('rm -rf popper_logs/')
    sh('mkdir -p popper_logs/')

    STATUS = "SUCCESS"

    for stage in stages:

        if not path.isfile(stage):
            continue

        if stage in args.skip.split(','):
            continue

        print("Running stage: " + stage)

        ecode, out = execute('./' + stage)

        if ecode != 0:
            print("Stage {} failed. Check logs for details.".format(stage))
            STATUS = "FAIL"
            break

        if stage == 'validate.sh':
            for line in out.splitlines():
                if '[true]' not in line:
                    break
            STATUS = "GOLD"

    writefile('popper_status', STATUS + '\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--skip', default='',
                        help='Comma-separated list of stages to skip.')
    args = parser.parse_args()
    check_experiment()
