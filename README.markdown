## Readme

PopperCI is based on web2py, a free open source full-stack framework for rapid development of fast, scalable, secure and portable database-driven web-based applications. It is written and programmable in Python.

## Important reminder about this Git repo

An important part of web2py is the Database Abstraction Layer (DAL). In early 2015 this was decoupled into a separate code-base (PyDAL). In terms of git, it is a sub-module of the main repository.

The use of a sub-module requires a one-time use of the --recursive flag for git clone if you are cloning web2py from scratch.

    git clone --recursive https://github.com/systemslab/popperci.git

If you have an existing repository, the commands below need to be executed at least once:

    git submodule update --init --recursive

If you have a folder gluon/dal you must remove it:

    rm -r gluon/dal

PyDAL uses a separate stable release cycle to the rest of web2py. PyDAL releases will use a date-naming scheme similar to Ubuntu. Issues related to PyDAL should be reported to its separate repository.

## Installation Instructions

To start web2py there is NO NEED to install it. Just unzip and do:

    python web2py.py

That's it!

## web2py directory structure

    project/
        README
        LICENSE
        VERSION                    > this web2py version
        web2py.py                  > the startup script
        anyserver.py               > to run with third party servers
        ...                        > other handlers and example files
        gluon/                     > the core libraries
            packages/              > web2py submodules
              dal/
            contrib/               > third party libraries
            tests/                 > unittests
        applications/              > are the apps
            admin/                 > web based IDE
                ...
            popperci/              > the PopperCI webapp
                ABOUT
                LICENSE
                models/
                views/
                controllers/
                sessions/
                errors/
                cache/
                static/
                uploads/
                modules/
                cron/
                tests/
            ...                    > your own apps
        examples/                  > example config files, mv .. and customize
        extras/                    > other files which are required for building web2py
        scripts/                   > utility and installation scripts
        handlers/
            wsgihandler.py         > handler to connect to WSGI
            ...                    > handlers for Fast-CGI, SCGI, Gevent, etc
        site-packages/             > additional optional modules
        logs/                      > log files will go in there
        deposit/                   > a place where web2py stores apps temporarily

## Issues?

Report issues at https://github.com/systemslab/popperci/issues
