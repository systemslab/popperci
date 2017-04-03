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


# Shows a list of credentials or prompts the user to create one if they haven't already
@auth.requires_login()
def credentials():
    # Pull up list of credentials for user
    cred_list = db(db.credentials.owner_id == auth.user.id).select(orderby=~db.credentials.id)
    # Redirect to add page if no credentials added yet
    if request.args(0) != 'add' and len(cred_list) == 0:
        redirect(URL('default', 'credentials', args=['add']))
    # Hide the fields we don't want to show and generate the form
    db.credentials.owner_id.writable = False
    db.credentials.owner_id.readable = False
    db.credentials.is_attached.writable = False
    db.credentials.is_attached.readable = False
    form = SQLFORM(db.credentials)
    if form.process().accepted:
        # If a file was uploaded, set is_attached to True
        if form.vars.cred_file is not None:
            db(db.credentials.id == form.vars.id).update(is_attached=True)
        redirect(URL('default', 'credentials'))
    return dict(form=form, cred_list=cred_list)


# This function just deletes a credential from the credential page, there is no
# HTML associated with this function.
@auth.requires_login()
def delete_credentials():
    cred_id = request.args(0)
    # Check permissions before deleting
    if db(db.credentials.id == cred_id).select()[0].owner_id != str(auth.user.id):
        redirect(URL('default', 'index'))
    # Delete the credential and redirect to another page
    db(db.credentials.id == cred_id).delete()
    redirect(URL('default', 'credentials'))


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


