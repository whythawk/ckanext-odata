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
}


t = p.toolkit
_base_url = None


def name_2_xml_tag(name):
    ''' Convert a name into a xml safe name. '''
    name = re.sub(' ', '_', name)
    name = re.sub('[^a-zA-Z0-9_\-]', '', name)
    return name


def get_qs_int(param, default):
    ''' Get a query sting param as an int '''
    value = t.request.GET.get(param, default)
    try:
        value = int(value)
    except ValueError:
        value = default
    return value


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

    limit = get_qs_int('$top', 500)
    offset = get_qs_int('$skip', 0)

    data_dict = {
        'resource_id': resource_id,
        'filters': filters,
        'limit': limit,
        'offset': offset,
    }

    output_json = t.request.GET.get('$format') == 'json'

    action = t.get_action('datastore_search')
    try:
        result = action({}, data_dict)
    except t.ObjectNotFound:
        t.abort(404, t._('DataStore resource not found'))
    except t.NotAuthorized:
        t.abort(401, t._('DataStore resource not authourized'))

    num_results = result['total']
    if num_results > offset + limit:
        next_query_string = '$skip=%s&$top=%s' % (offset + limit, limit)
    else:
        next_query_string = None


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
                # if we have no translation for a type use Edm.String
                'type': TYPE_TRANSLATIONS.get(field['type'], 'Edm.String'),
            }
        data = {
            'title': resource['name'],
            'updated': resource['last_modified'] or resource['created'],
            'base_url': base_url(),
            'convert': convert,
            'collection': uri,
            'entries': result['records'],
            'next_query_string': next_query_string,
        }
        t.response.headers['Content-Type'] = 'application/atom+xml;type=feed;charset=utf-8'
        return t.render('ckanext-odata/collection.xml', data)
