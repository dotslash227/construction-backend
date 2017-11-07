import os
import types
import importlib
from termcolor import colored
from components_config.components import components as datashop_components
from helpers import GetComponents

class Router:
  """Handles route based manipulations

  Functions:
  - Loading routes mentioned in component route class
  - Internal routes (TODO)
  - Disabling routes via config (TODO)
  - Pre/Post route loading hooks (TODO)
  """

  def __init__(self):
    self.required_route_fields = [
      'name', 'pattern'
    ]

    self.optional_route_fields = [
      'permission', 'factory', 'for_', 'header', 'xhr', 'accept', 'path_info',
      'request_method', 'request_param', 'traverse', 'custom_predicates',
      'use_global_views', 'path', 'pregenerator', 'static',
    ]

  def register_routes(self, configurator):
    """Adds routes to configurator

    Args:
      configurator: pyramid configurator
    """

    print 'Registering components...'
    all_routes = self.get_all_routes()
    component_names = [component['name'] for component in datashop_components]
    for component in component_names:
      routes = all_routes.get(component)
      if not routes:
        continue
      sanitized_routes = self.sanitize_component_routes(routes)
      map(lambda route: configurator.add_route(**route), sanitized_routes)
      print '{check} {component_name} ({routes_count} routes)'.format(
        check=colored(u'\u2713'.encode('utf8'), 'green'),
        component_name=colored(component, attrs=['bold']),
        routes_count=len(routes)
      )

  def get_all_routes(self):
    """Loads component routes

    Returns:
      Dict of all component routes where key is component name and value is a
      list of component route dicts
    """

    component = GetComponents()
    component.init_components_directory()
    components = component.get_components()

    component_routes = {}

    for (component_name, component) in components.iteritems():
      if isinstance(component, types.ModuleType):
        not_found = {
          'router': False,
          'get_routes': False
        }
        if 'Router' not in dir(component):
          not_found['router'] = True
        else:
          component_router = component.Router()
          if 'get_routes' not in dir(component_router):
            not_found['get_routes'] = True
          else:
            component_routes[component_name] = component_router.get_routes()

        if not_found['router']:
          print 'No router found for component: {component}'.format(
            component=component_name
          )
        elif not_found['get_routes']:
          print 'No get_routes function defined in router of component: {component}'.format(
            component=component_name
          )

    return component_routes

  def sanitize_component_routes(self, routes):
    """Checks and cleans component routes

    Args:
    routes: List of component route dicts

    Returns:
    list of sanitized component route dicts
    """

    if not isinstance(routes, list):
      msg = 'get_routes method to return a list of route objects. Expected: List, Found: {routes_type}'.format(
        routes_type=type(routes)
      )
      raise Exception(msg)

    allowed_route_keys = self.required_route_fields + self.optional_route_fields

    sanitized_routes = []
    for route in routes[:]:
      # remove invalid keys from route object
      invalid_route_keys = set(route.keys()) - set(allowed_route_keys)
      if len(invalid_route_keys) > 0:
        for key in invalid_route_keys:
          del route[key]

      missing_route_fields = list(set(self.required_route_fields) - set(route.keys()))
      if len(missing_route_fields) > 0:
        msg = 'Missing required route fields ({fields}) for the route: {route_name} ({route})'.format(
          fields=missing_route_fields,
          route_name=route.get('name'),
          route=route.get('pattern')
        )
        raise Exception(msg)

      sanitized_routes.append(route)

    return sanitized_routes
