# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# This is the page controller
# - index is the default action of PopperCI (the "dashboard")
# - user is required for authentication and authorization with Jenkins
# - download is for downloading files uploaded in the db (not currently used, from scaffold)
# -------------------------------------------------------------------------


@auth.requires_login()
def index():
    return dict()


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


def credentials():
    # Make the form
    form = SQLFORM(db.credentials)
    db.credentials.owner_id.writable = False
    db.credentials.owner_id.readable = False
    db.credentials.is_attached.readable = False
    db.credentials.is_attached.writable = False
    # What to do if the form was filled out successfully
    if form.process().accepted:
        redirect(URL('default', 'index'))
    return dict(form=form)


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


