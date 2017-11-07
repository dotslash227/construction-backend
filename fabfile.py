import re
import os
import json
import getpass
from fabric.api import task, run, settings, hide, env
from config.fab import commands
from components_config.components import components

"""
Usage: fab -H host1,host2,... task1 task2 ...
"""

project_location = os.path.dirname(os.path.abspath(__file__))
components_location = os.path.join(project_location, 'applicationlayer/components')


@task
def start_dev():
  run_cmd(project_location, get_cmd('start_dev'))


@task
def clean():
  run_cmd(project_location, get_cmd('clean'))


@task
def build():
  run_cmd(project_location, get_cmd('build'))


@task
def clean_install():
  run_cmd(project_location, get_cmd(['clean', 'build']))


@task
def load_components():
  """Load all component modules into the app
  """
  # loading components from components config
  components = get_components_config()

  # loading components in App
  get_components(components)


@task
def load_component(*component_names):
  """Load given component modules into the app
  """
  # loading components from components config
  components = get_components_config()

  # matching given components from components in config
  matched_components = []
  for component in components:
      if component['name'] in component_names:
          matched_components.append(component)


  if len(matched_components) <= 0:
    # Raising exception if no component found
    raise Exception('Component not found')
  else:
    # loading components in App
    get_components(matched_components)

####################
# Helper Functions #
####################


def get_components(components):
  """Load component module into the app
  """
  build_cmd = get_cmd('virtualenv_activate')

  init_components_dir()
  set_git_credentials()

  for component in components:
    build_cmd += ' && ' + fetch_component(component)

  remove_git_credentials()

  build_cmd += ' && ' + get_cmd('build')
  run_cmd(project_location, build_cmd)


def get_components_config():
  components_file_path = env.get('DS_COMPONENTS_PATH')
  python_env = env.get('PYTHON_ENV', 'development')

  if python_env.lower()=='production' or not components_file_path:
    components_config = components
  else:
    with open(components_file_path) as components_file:
      components_config = json.loads(components_file.read()).get('components')

  return components_config


def fetch_component(component):
  # loads a single component
  # if component config changes, remove the component directory
  commands = []
  component_path = os.path.join(components_location, component.get('name'))
  if os.path.isdir(component_path):
    old_url = run_cmd(component_path, 'git remote -v', "((http://.*\.git)|(git@.*\.git))").strip()
    old_branch = run_cmd(component_path, 'git branch --no-color', "\* (.*)").strip()

    if old_url != component.get('gitUrl') or old_branch != component.get('branch'):
      run('rm -rf {dir}'.format(
        dir=component_path
      ))

  # git pull if component exists else clone
  if os.path.isdir(component_path):
    cmd = 'cd {dir} && git pull origin {branch} && cd ..'.format(
      dir=component.get('name'),
      branch=component.get('branch')
    )
  else:
    cmd = 'git clone -b {branch} {url} {dir}'.format(
      branch=component.get('branch'),
      url=component.get('gitUrl'),
      dir=component.get('name')
    )

  # import component in components init
  commands.append('echo "import {dir}" >> __init__.py'.format(
    dir=component.get('name')
  ))

  commands.append(cmd)

  run_cmd(components_location, ' && '.join(commands))

  # getting command to install requirements for component
  cmd = install_requirements(component_path)
  return cmd


def install_requirements(component_path):
    """Returns command to install dependencies from requirements.txt for given component
    """
    #Returns command to install component requirements (if exists)
    if os.path.isfile(os.path.join(component_path,'requirements.txt')):
        run_cmd = 'pip install -r '+component_path+'/requirements.txt'
    else:
        run_cmd = 'echo no Requirements file found ' + component_path

    return run_cmd


def init_components_dir():
  """Creates and initializes components directory with __init__
  """
  if not os.path.exists(components_location):
    os.makedirs(components_location)
  components_init = os.path.join(components_location, '__init__.py')
  open(components_init, 'w')


def run_cmd(path, command, output_regex=".*"):
  """Wrapper fabric run function
  """
  run_cmd = 'cd {path} && {cmd}'.format(
    path=path,
    cmd=command
  )
  # prevent aborting on non-zero exit codes
  with settings(warn_only=True):
    cli_out = run(run_cmd)
    res = re.search(output_regex, cli_out)
  matched_cli_out = None
  if res and len(res.groups()) > 0:
    matched_cli_out = res.groups()[0]
  return matched_cli_out


def get_cmd(cmd_types):
  cmds = []
  if isinstance(cmd_types, str):
    cmds = commands.get(cmd_types, [])
  else:
    for cmd_type in cmd_types:
      cmds.extend(commands.get(cmd_type, []))
  return ' && '.join(cmds)


def set_git_credentials():
  user_name = raw_input("Enter your git username: ")
  password = getpass.getpass("Enter your git password: ")
  cmd = commands.get('set_git_credentials')[0].format(
    user_name=user_name,
    password=password
  )
  cmd = 'echo ' + cmd + '>> ~/.netrc'
  with hide('running'):
    run(cmd)


def remove_git_credentials():
  cmd = commands.get('remove_git_credentials')[0]
  run(cmd)
