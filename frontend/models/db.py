# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.14.1":
    raise HTTP(500, "Requires web2py 2.13.3 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# app configuration made easy. Look inside private/appconfig.ini
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
myconf = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(myconf.get('db.uri'),
             pool_size=myconf.get('db.pool_size'),
             migrate_enabled=myconf.get('db.migrate'),
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = ['*'] if request.is_local else []
# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = myconf.get('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.get('forms.separator') or ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

from gluon.tools import Auth, Service, PluginManager
from gluon.contrib.login_methods.oauth10a_account import OAuthAccount
import requests

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=myconf.get('host.names'))
service = Service()
plugins = PluginManager()

# -------------------------------------------------------------------------
# create all tables needed by auth if not custom tables
# -------------------------------------------------------------------------

# define the auth_table before call to auth.define_tables()

auth_table = db.define_table(
   auth.settings.table_user_name,
   Field('first_name', length=128, default=""),
   Field('last_name', length=128, default=""),
   Field('username', length=128, default="", unique=True),
   Field('password', 'password', length=256, readable=False, label='Password'),
   Field('registration_key', length=128, default="", writable=False, readable=False))

auth_table.username.requires = IS_NOT_IN_DB(db, auth_table.username)
auth.define_tables()

CLIENT_ID = myconf.get('github.id')
CLIENT_SECRET = myconf.get('github.secret')
AUTH_URL = "http://github.com/login/oauth/authorize"
TOKEN_URL = "https://github.com/login/oauth/access_token"
ACCESS_TOKEN_URL = "https://github.com/login/oauth/access_token"


class GitHubOAuth(OAuthAccount):
    def get_user(self):
        if not self.accessToken():
            return None

        verify = requests.get(ACCESS_TOKEN_URL,
                              headers={"Authorization": "Bearer " + self.accessToken()}).json()

        # Test
        print verify

        # Populate nonsense for now
        return dict(id=verify['id'],
                    username=verify['id'],
                    first_name=verify['id'],
                    last_name=verify['id'])

auth.settings.login_form = GitHubOAuth(globals(),
                                       CLIENT_ID,
                                       CLIENT_SECRET,
                                       AUTH_URL,
                                       TOKEN_URL,
                                       ACCESS_TOKEN_URL)

auth.settings.actions_disabled = ['register', 'change_password', 'request_reset_password']

#auth.define_tables(username=True, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.get('smtp.server')
mail.settings.sender = myconf.get('smtp.sender')
mail.settings.login = myconf.get('smtp.login')
mail.settings.tls = myconf.get('smtp.tls') or False
mail.settings.ssl = myconf.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

from datetime import datetime

# Prevents crashes when logged out and auth.user is None
if auth.user is None:
    identifier = ''
    identifier_name = ''
else:
    identifier = auth.user.id
    identifier_name = auth.user.username

# Project status defined by most recent build
# Project status defined by most recent build
db.define_table('project',
                Field('project_name', 'string', required=True),
                Field('result_id', 'string', required=True),
                # Field('project_id', 'string', required=True), # Not used
                Field('time_stamp', 'datetime', default=datetime.utcnow(), required=True),
                Field('workspace', 'string', required=True)
                )

db.define_table('build',
                Field('user_id', 'integer', required=True),
                Field('project', 'string', required=True),     # to associate projects with builds
                Field('meta', 'string'),
                Field('status', 'string'),                    # NEW: Store running/done

                # Old/unused fields
                Field('build_name', 'string'),                 # if not needed, we can remove
                Field('build_id', 'string'),                   # to associate experiments with this build
                )

db.define_table('experiment',
                Field('experiment_name', 'string'),
                Field('build_id', 'integer'),                   # to associate each experiment with a build
                Field('status', 'string'),

                # Old/unused fields
                Field('experiment_id', 'string')             # to associate validations with an experiment
                )

db.define_table('validation',
                Field('validation_name', 'string'),
                Field('validation_id', 'string', required=True),
                Field('experiment_id', 'string', required=True),
                Field('validation', 'string', required=True),
                Field('status', 'string', required=True)
                )

db.define_table('credentials',
                Field('owner_id', 'string', readable=False, writable=False, required=True, default=identifier),
                Field('name', 'string', required=True),
                Field('is_attached', 'boolean', default=False, required=True),
                Field('cred_text', 'text'),
                Field('cred_file', 'upload')
                )

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)

