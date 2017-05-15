import os

import click



class Registry(object):
    def __init__(self, local_path, dirname, registry_name="kolla-registry"):
        self.local_path = local_path
        self.registry_name = registry_name
        self.dirname = dirname

    def setup(self):
        resp = os.system(
                ("docker run -d -p 5000:5000 -v "
                    "{}:/var/lib/registry --name {} registry:2").format(
                    self.local_path + self.dirname,
                    self.registry_name,
                )
            )
