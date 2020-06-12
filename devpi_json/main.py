from devpi_web.views import get_user_info, get_files_info, get_docs_info 
from operator import attrgetter
from pyramid.response import Response
from pyramid.view import view_config
import json

def includeme(config):
    config.add_route(
        'projects_json',
        '/{user}/{index}/+json'
    )

    config.add_route(
        'indices_json',
        '/+json'
    )
    config.scan()

def devpiserver_pyramid_configure(config, pyramid_config):
    pyramid_config.include('devpi_json.main')

@view_config(route_name = 'projects_json', request_method = 'GET')
def json_view(context, request):
    projects = set()
    for stage, names in context.stage.op_sro('list_projects_perstage'):
        if stage.ixconfig['type'] == 'mirror':
            continue
        projects.update(names)

    data = {}
    for project in sorted(projects):
        data[project] = []
        for stage, versions in context.stage.op_sro_check_mirror_whitelist('key_projversions', project=project):
            if stage.ixconfig['type'] == 'mirror':
                continue

            for version in versions.get():
                linkstore = stage.get_linkstore_perstage(project, version)
                files = get_files_info(request, linkstore, False)
                docs = get_docs_info(request, stage, linkstore)

                data[project].append(dict(
                    version = version,
                    docs = docs,
                    files = files
                ))

    response = Response()
    response.json_body = data
    response.content_type = 'application/json'
    return response

@view_config(route_name = 'indices_json', request_method = 'GET')
def indices_json_view(context, request):

    indexes = []
    for user in [x.get() for x in context.model.get_userlist()]:
        for index in sorted(user.get('indexes', [])):
            stagename = '%s/%s' % (user['username'], index)
            stage = context.model.getstage(stagename)
            indexes.append(dict(
                stagename = stagename,
                title = stage.ixconfig.get('title', None),
                name = index,
                description = stage.ixconfig.get('description', None),
                url = request.stage_url(stagename)
            ))
    
    response = Response()
    response.json_body = indexes
    response.content_type = 'application/json'
    return response



