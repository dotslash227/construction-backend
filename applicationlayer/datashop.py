from pyramid.config import Configurator
from .binder import Router

def main(global_config, **settings):
  """ Returns Pyramid WSGI app
  """
  config = Configurator(settings=settings)
  config.add_tween('.boot.tweens.headers_tween_factory')
  config.add_renderer('csv', '.utils.export_writers.CSVRenderer')
  router = Router()
  router.register_routes(config)

  # TODO: Don't uncomment this. This should be activated in later release
  # loader = LoadPermissions()
  # loader.load_permissions()

  # component_access = ComponentAccess()
  # component_access.permissions_handler()

  config.scan()

  return config.make_wsgi_app()
