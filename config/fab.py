commands = {
  'clean': [
    'rm -rf applicationlayer/components/*',
    'rm -rf **/*.pyc',
    'rm -rf build ApplicationLayer.egg-info',
    'pip uninstall applicationlayer'
  ],
  'build': [
    'pip install -r requirements.txt',
    'python setup.py install >> /dev/null 2>&1'
  ],
  'virtualenv_activate': [
    'virtualenv venv',
    'source venv/bin/activate',
  ],
  'virtualenv_deactivate': [
    'deactivate',
  ],
  'setup': [
    'python setup.py install'
  ],
  'start_dev': [
    'python server.py'
  ],
  'remove_git_credentials': [
    'sed -i "/machine\ gitlab.com\ /d" ~/.netrc'
  ],
  'set_git_credentials': [
    'machine gitlab.com login {user_name} password {password} '
  ]
}
