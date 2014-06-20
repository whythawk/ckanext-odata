import re
import simplejson as json

import ckan.plugins as p


try:
    from collections import OrderedDict  # from python 2.7
except ImportError:
    from sqlalchemy.util import OrderedDict


TYPE_TRANSLATIONS = {
    'null': 'Edm.Null',
    'bool': 'Edm.Boolean',
    'float8': 'Edm.Double',
    'numeric': 'Edm.Double',
    'int4': 'Edm.Int32',
    'int8': 'Edm.Int64',
    'timestamp': 'Edm.DateTime',
    'text': 'Edm.String',
    'json': 'Edm.String',
}


t = p.toolkit
_base_url = None


def name_2_xml_tag(name):
    ''' Convert a name into a xml safe name. '''
    name = re.sub(' ', '_', name)
    name = re.sub('[^a-zA-Z0-9_\-]', '', name)
    return name


def base_url():
    ''' The base url of the OData service '''
    global _base_url
    if not _base_url:
        _base_url = t.url_for('/datastore/odata3.0/', qualified=True)
    return _base_url


def odata(context, data_dict):

    uri = data_dict.get('uri')

    match = re.search(r'^(.*)\((\d+)\)$', uri)
    if match:
        resource_id = match.group(1)
        row_id = int(match.group(2))
        filters = {'_id': row_id}
    else:
        row_id = None
        resource_id = uri
        filters = {}

    data_dict = {
        'resource_id': resource_id,
        'filters': filters,
        'limit': t.request.GET.get('$top', 500),
        'offset': t.request.GET.get('$skip', 0)
    }

    output_json = t.request.GET.get('$format') == 'json'

    action = t.get_action('datastore_search')
    try:
        result = action({}, data_dict)
    except t.ObjectNotFound:
        t.abort(404, t._('DataStore resource not found'))

    action = t.get_action('resource_show')
    resource = action({}, {'id': resource_id})

    if output_json:
        out = OrderedDict()
        out['odata.metadata'] = 'FIXME'
        out['value'] = result['records']

        response = json.dumps(out)
        return response
    else:
        convert = {}
        for field in result['fields']:
            convert[field['id']] = {
                'name': name_2_xml_tag(field['id']),
                'type': TYPE_TRANSLATIONS[field['type']],
            }
        data = {
            'title': resource['name'],
            'updated': resource['last_modified'] or resource['created'],
            'base_url': base_url(),
            'convert': convert,
            'collection': uri,
            'entries': result['records'],
        }
        t.response.headers['Content-Type'] = 'application/xml;charset=utf-8'
        return t.render('ckanext-odata/collection.xml', data)
