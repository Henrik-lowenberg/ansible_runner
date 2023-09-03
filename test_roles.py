#!/usr/bin/env python3

import ansible_runner
import getpass
import os
import json
import tempfile
import shutil

sshpass = getpass.getpass('Enter SSH password: ')
pwd_dict: dict = { r'SSH [pP]assword:\s*$': sshpass }
hosts = {
    "local": {
        "hosts": {
            "localhost": {
                'ansible_connection': 'local'
			},
        },
    }
}

envvars = {
	'ansible_ssh_common_args': '-o StrictHostKeyChecking=no',
	'ansible_user': 'root',
	'ansible_timeout': 10,
}

temp_datadir = tempfile.mkdtemp()
saved_umask = os.umask(0o0077)

kwargs = {
	'private_data_dir': temp_datadir,
	'roles_path': os.getcwd() + "/roles",
	'role': "test_role",
	'role_vars': {'var1': "value1"},
	'passwords': sshpass,
	'inventory': hosts,
	'envvars': envvars,
	'verbosity': 5,
	'suppress_env_files':True,
}

r_result = ansible_runner.interface.run(**kwargs)
stdout = r_result.stdout.read()
events = list(r_result.events)
stats = r_result.stats
print(json.dumps(stats, indent=4))

os.umask(saved_umask)
shutil.rmtree(temp_datadir)
