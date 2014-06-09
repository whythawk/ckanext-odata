import ckan.plugins as p

import ckanext.odata.actions as action


def link(resource_id):
    return '%s%s' % (action.base_url(), resource_id)


class ODataPlugin(p.SingletonPlugin):

    p.implements(p.IConfigurer)
    p.implements(p.IRoutes, inherit=True)
    p.implements(p.IActions)
    p.implements(p.ITemplateHelpers, inherit=True)

    def update_config(self, config):
        p.toolkit.add_template_directory(config, 'templates')
        p.toolkit.add_resource('resources', 'odata')
        p.toolkit.add_public_directory(config, 'public')


    def before_map(self, m):
        m.connect('/datastore/odata3.0/{uri:.*?}',
                  controller='ckanext.odata.controller:ODataController',
                  action='odata')
        return m


    def get_actions(self):
        actions = {
            'ckanext-odata_odata': action.odata,
        }
        return actions

    def get_helpers(self):
        return {
            'ckanext_odata_link': link,
        }
