#!/usr/bin/env python3

import ansible_runner
import getpass
import os
import json
import tempfile
import shutil

secret = getpass.getpass('Enter SSH password: ')
sshpass: dict = { r'SSH [pP]assword:\s*$': secret }
hosts: dict = {
    "local": {
        "hosts": {
            #"dummyhost.some.domain": {},
            "localhost": {
                'ansible_connection': 'local'
			},
        },
        'vars': {
	        'ansible_ssh_common_args': '-o StrictHostKeyChecking=no',
	        'ansible_user': 'root',
	        'ansible_timeout': 10,
            'gather_facts': False,
        }
    }
}

path = '/some/obscure/dir:'
path += os.environ.get('PATH', '')
envvars: dict = {
	'PATH': path,
    'PYTHONPATH': '/opt/homebrew/bin/python3:',
    'ANSIBLE_ROLES_PATH': 'etc/ansible/roles:'
}
temp_datadir = tempfile.mkdtemp()
saved_umask = os.umask(0o0077)
role_name = "test_role"
role_vars: dict = {'var1': "value1"}

kwargs = {
	'private_data_dir': temp_datadir,
	'roles_path': os.getcwd() + "/roles",
	'role': role_name,
	'role_vars': role_vars,
	'passwords': sshpass,
	'inventory': hosts,
	#'envvars': envvars,
	'cmdline': '--ask-pass',
	'verbosity': 2,
	'suppress_env_files':True,
}

try:
  r_result = ansible_runner.interface.run(**kwargs)
  stdout = r_result.stdout.read()
  events = list(r_result.events)
  stats = r_result.stats
  print(json.dumps(stats, indent=4))
finally:
  os.umask(saved_umask)
  shutil.rmtree(temp_datadir)
