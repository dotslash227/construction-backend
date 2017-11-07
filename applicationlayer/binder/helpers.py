import os
import importlib

class GetComponents:

    def init_components_directory(self):
      """Initializes components directory with init file
      """

      components_directory = 'applicationlayer/components'
      components_init = os.path.join(components_directory, '__init__.py')

      if not os.path.exists(components_directory):
        os.makedirs(components_directory)

      if not os.path.isfile(components_init):
        open(components_init, 'w+')

    def get_components(self):
      """Returns dictionary of all component python modules

      Returns:
        A dict mapping component names to their respective python modules
      """
      components = importlib.import_module('applicationlayer.components').__dict__
      return components
