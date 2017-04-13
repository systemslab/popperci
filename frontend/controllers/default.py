# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# This is the page controller
# - index is the default action of PopperCI (the "dashboard")
# - user is required for authentication and authorization with Jenkins
# - download is for downloading files uploaded in the db (not currently used, from scaffold)
# -------------------------------------------------------------------------

key = 'sample_key'


@auth.requires_login()
def index():
    project_url = URL('default', 'load_projects', hmac_key=key)
    build_url = URL('default', 'load_builds', vars=dict(id=request.vars.id), hmac_key=key)
    experiment_url = URL('default', 'load_experiments', vars=dict(id=request.vars.id, build=request.vars.build), hmac_key=key)
    return dict(project_url=project_url, build_url=build_url, experiment_url=experiment_url)


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
    """
    Description: Shows a list of credentials associated with a user. If none, prompts them to add one
    Returns: A list of credentials. If none (or if the user wants to add), returns a form to add some
    """
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
    return dict(form=form, cred_list=cred_list, key=key)


# This function just deletes a credential from the credential page, there is no
# HTML associated with this function.
@auth.requires_login()
def delete_credentials():
    """
    Description: Deletes the credential specified in the URL parameters iff user requesting owns the credential
    Returns: Nothing, redirects only.
    Note: No HTML associated with page
    """

    if not URL.verify(request, hmac_key=key):
        raise HTTP(403)

    cred_id = request.args(0)
    # Check permissions before deleting
    if db(db.credentials.id == cred_id).select()[0].owner_id != str(auth.user.id):
        redirect(URL('default', 'index'))
    # Delete the credential and redirect to another page
    db(db.credentials.id == cred_id).delete()
    redirect(URL('default', 'credentials'))


def load_projects():
    """
    Description: Returns a list of projects to show on index.html. This is called from the JS.
    Returns: A JSON with a dictionary of all the builds and their database fields.
    Note: No HTML associated with page
    """

    if not URL.verify(request, hmac_key=key):
        raise HTTP(403)

    populate_tables()

    # Find list of project names that match the user ID
    q = db(db.build.user_id == auth.user.id).select()
    project_list = []

    for i in q:
        # Find the status of the most recent experiment in builds corresponding to the project
        # for the overall project status. If no experiments, return "N/A" as status.
        try:
            status = db(db.experiment.build_id == i.id).select(orderby=~db.experiment.id)[0].status
        except IndexError:
            status = "N/A"

        # Find the project row that corresponds to the project associated with the build
        project = db(db.project.project_name == i.project).select()[0]

        # Add the project to the JSON file if it doesn't exist there already
        if not any(info['name'] == project.project_name for info in project_list):
            print project_list
            project_list.append(dict(name=project.project_name,
                                     id=project.id,
                                     workspace=project.workspace,
                                     time=project.time_stamp,
                                     status=status))
    return response.json(dict(project_dict=project_list))


# Test/pre-populate the DB, remove when not needed
def populate_tables():
    """
    Description: Resets the project, build, and experiment databases and populates them with dummy fields for testing.
    Returns: Nothing
    Note: No HTML associated with page
    """
    from random import randint
    import uuid

    db.project.truncate()
    db.build.truncate()
    db.experiment.truncate()
    db.commit()

    some_count = randint(1, 10)
    for i in range(0, some_count):
        project_name = 'TestProject' + str(i)
        db.project.insert(project_name=project_name,
                          result_id=uuid.uuid4(),
                          workspace='~/Downloads/web2py')
        build_count = randint(1, 10)
        for idx, j in enumerate(range(0, build_count)):
            db.build.insert(user_id=auth.user.id,
                            project=project_name,
                            status='Running' if randint(0, 1) == 0 else 'Done'
                            )
            for k in range(1, randint(2, 10)):
                rand_status = randint(0, 2)
                if rand_status == 0:
                    status = 'GOLD'
                elif rand_status == 1:
                    status = 'PASS'
                else:
                    status = 'FAIL'
                db.experiment.insert(
                    experiment_name='Experiment ' + str(k+idx) + ' for build ' + str(j+1) + ' on ' + project_name,
                    build_id=idx,
                    status=status)

    pass


def load_builds():
    """
    Description: Returns a list of builds to show on index.html. This is called from the JS.
    Returns: A JSON with a dictionary of all the builds and their database fields.
    Note: No HTML associated with page
    """

    if not URL.verify(request, hmac_key=key):
        raise HTTP(403)

    val = request.vars.id
    project = db(db.build.project == val).select()
    builds = []

    for i in project:
        experiment_count = db(db.experiment.build_id == i.id).count()
        owner = db(db.auth_user.id == i.user_id).select()[0]
        build_name = "Build " + str(i.id) + " for " + owner.username
        builds.append(dict(project=i.project,
                           user=i.user_id,
                           id=i.id,
                           name=build_name,
                           count=experiment_count,
                           status=i.status))

    return response.json(dict(build_dict=builds))


def load_experiments():
    """
    Description: Returns a list of experiments to show on index.html. This is called from the JS.
    Returns: A JSON with a dictionary of all the builds and their database fields.
    Note: No HTML associated with page
    """

    if not URL.verify(request, hmac_key=key):
        raise HTTP(403)

    val = request.vars.build
    experiment = db((db.experiment.build_id == val)).select()
    experiment_list = []

    for i in experiment:
        experiment_list.append(dict(name=i.experiment_name,
                                    id=i.id,
                                    build_id=i.build_id,
                                    status=i.status))

    return response.json(dict(experiment_dict=experiment_list))


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
