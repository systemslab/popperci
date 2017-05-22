# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# This is the page controller
# - index is the default action of PopperCI (the "dashboard")
# - credentials lets users add, upload, or delete credentials
# - delete_credentials handles the actual logic for deleting a credential and is called from the credentials view
# - load_projects generates a list of all projects with builds associated with the current user
# - populate_tables generates dummy data for projects, builds, and experiments when no real world data is available
# - load_builds, given a specific project, generates a list of builds associated with that project
# - load_experiments generates a list of experiments associated with a build, given that build ID
# - load _validations loads validations for a specific experiment
# - user handles user authentication, including username, email, and password management
# - download is for downloading files uploaded in the db (not currently used, from scaffold)
# -------------------------------------------------------------------------

from gluon.serializers import json
from gluon.tools import prettydate


@auth.requires_login()
def index():
    # Serves a badge SVG file if the badge argument is present
    if request.args(0) == 'badge':
        # Return to dashboard if project not found
        q = db(db.project.project_name == request.vars.id).select()[0]
        if request.args(0) is None or q is None:
            redirect('default', 'index')
            session.flash = T('Project not found')
        experiment = db(db.experiment.build_id == q.id).select(orderby=~db.experiment.id)[0]
        # Return to dashboard if not the owner of the project
        if db(db.build.id == experiment.build_id).select()[0].user_id != auth.user.id:
            redirect('default', 'index')
            session.flash = T('Permission denied')
        # Set the view to the SVG file
        response.view = 'default/badge.svg'
        return dict(status=experiment.status)
    # Fetch and return the project, build, and experiment lists in JSON format otherwise
    project_list = XML(json(load_projects()))
    build_list = XML(json(load_builds(request.vars.id)))
    experiment_list = XML(json(load_experiments(request.vars.id, request.vars.build)))
    validation_list = XML(json(load_validations(request.vars.id, request.vars.build, request.vars.experiment)))
    return dict(project_list=project_list,
                build_list=build_list,
                experiment_list=experiment_list,
                validation_list=validation_list)


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

    if (request.args(0) == 'edit') and (db(db.credentials.id == request.args(1)).select()):
        # Set the form fields we know the info about already
        cred_id = db(db.credentials.id == request.args(1)).select()[0].id
        # Hide the fields we don't want to show
        db.credentials.id.readable = False
        db.credentials.owner_id.writable = False
        db.credentials.owner_id.readable = False
        db.credentials.is_attached.writable = False
        db.credentials.is_attached.readable = False
        form = SQLFORM(db.credentials, record=int(cred_id))
        # Specify what fields are required and where to redirect next
        form.custom.widget.name['requires'] = IS_NOT_EMPTY()
        # What to do if the form was filled out successfully
        if form.process().accepted:
            session.flash = T('Credential edited')
            redirect(URL('default', 'credentials'))
        return dict(form=form)
    elif request.args(0) != 'add' and len(cred_list) == 0:
        redirect(URL('default', 'credentials', args=['add']))
    else:
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
@auth.requires_signature()
def delete_credentials():
    """
    Description: Deletes the credential specified in the URL parameters iff user requesting owns the credential
    Returns: Nothing, redirects only.
    Note: No HTML associated with page
    """
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

    # Find list of project names that match the user ID
    q = db(db.build.user_id == auth.user.id).select(orderby=~db.build.id)
    seen_projects = []
    project_list = []
    for i in q:
        if i.project not in seen_projects:
            seen_projects.append(i.project)
            # Find the status of the most recent experiment in builds corresponding to the project
            # for the overall project status. If no experiments, return "N/A" as status.
            try:
                row = db(db.experiment.build_id == i.id).select(orderby=~db.experiment.id)[0]
                status = row.status
            except IndexError:
                status = "N/A"

            # Find the project row that corresponds to the project associated with the build
            project = db(db.project.project_name == i.project).select()[0]

            # Add the project to the JSON file if it doesn't exist there already
            if not any(info['name'] == project.project_name for info in project_list):
                project_list.insert(0, dict(name=project.project_name,
                                         id=project.id,
                                         workspace=project.workspace,
                                         time=str(prettydate(project.time_stamp, T)),
                                         status=status))
    return project_list


def populate_demo():
    demo_tables()
    redirect(URL('default', 'index'))


@auth.requires_login()
def populate_tables():
    """
    Description: Resets the project, build, and experiment databases and populates them with dummy fields for testing.
    Returns: Nothing
    Note: No HTML associated with page
    """
    from random import randint
    import uuid

    # Remove existing data from the databases
    db.project.truncate()
    db.build.truncate()
    db.experiment.truncate()
    db.validation.truncate()
    db.commit()

    # Generate a random amount of projects, builds, and experiments, then insert them into the DB
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
                            meta=webhook,
                            status='Running' if randint(0, 1) == 0 else 'Done'
                            )
            for k in range(1, randint(4, 10)):
                rand_status = randint(0, 2)
                if rand_status == 0:
                    status = 'GOLD'
                elif rand_status == 1:
                    status = 'OK'
                else:
                    status = 'FAIL'
                db.experiment.insert(
                    experiment_name='Experiment ' + str(k) + ' for build ' + str(j) + ' on ' + project_name,
                    build_id=db(db.build.user_id == auth.user.id).select().last().id,
                    status=status)
                for l in range(1, randint(4, 10)):
                    randk_status = randint(0, 2)
                    if randk_status == 1:
                        valk_status = 'fail'
                    else:
                        valk_status = 'success'
                    db.validation.insert(
                        validation_name='Validation ' + str(l) + ' for experiment ' + str(j + 1) + ' on ' + project_name,
                        experiment_id=db(db.experiment).select().last().id,
                        validation_id=str(uuid.uuid4()),
                        validation="test validation field #" + str(l+k+j),
                        status=valk_status)
    redirect(URL('default', 'index'))
    pass


def load_builds(val):
    """
    Description: Returns a list of builds to show on index.html. This is called from the JS.
    Returns: A JSON with a dictionary of all the builds and their database fields.
    Note: No HTML associated with page
    """

    import json

    if val is None:
        return None

    project = db(db.build.project == val).select(orderby=~db.build.id)
    builds = []

    for i in project:
        experiment_count = db(db.experiment.build_id == i.id).count()
        owner = db(db.auth_user.id == i.user_id).select()[0]
        meta_info = json.loads(i.meta)
        build_name = "Build " + str(i.id) + " for " + owner.username
        builds.append(dict(project=i.project,
                           user=i.user_id,
                           build_id=i.id,
                           name=build_name,
                           count=experiment_count,
                           meta_author=meta_info['head_commit']['author']['name'],
                           meta_timestamp=meta_info['head_commit']['timestamp'],
                           meta_commit=meta_info['head_commit']['id'],
                           meta_message=meta_info['head_commit']['message'],
                           status=i.status))

    return builds


def load_experiments(project, val):
    """
    Description: Returns a list of experiments to show on index.html. This is called from the JS.
    Returns: A JSON with a dictionary of all the builds and their database fields.
    Note: No HTML associated with page
    """

    if project is None or val is None:
        return None
    experiment = db((db.experiment.build_id == (int(val)))).select(orderby=~db.experiment.id)
    experiment_list = []
    for i in experiment:
        experiment_list.append(dict(name=i.experiment_name,
                                    exp_id=i.id,
                                    build_id=i.build_id,
                                    status=i.status))
    return experiment_list


def load_validations(project, val, exp):
    if project is None or val is None or exp is None:
        return None
    validation = db((db.validation.experiment_id == int(exp))).select(orderby=~db.validation.id)
    validation_list = []
    for i in validation:
        validation_list.append(dict(name=i.validation_name,
                                    web2py_id=i.id,
                                    validation_id=i.validation_id,
                                    experiment_id=i.experiment_id,
                                    validation=i.validation,
                                    status=i.status.title()))
    return validation_list


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

