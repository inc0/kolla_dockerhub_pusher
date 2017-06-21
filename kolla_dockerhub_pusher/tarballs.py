import os
import shutil
import tarfile

import click
import requests
from tqdm import tqdm

from . import utils


class TarFile(object):
    def __init__(self, base, type, release, tarball_url, local_path):
        self.base = base
        self.type = type
        self.release = release
        self.tarball_url = tarball_url
        self.local_path = local_path
        self.fname = utils.get_file_name(base, type, release)

    def _get_url(self):
        return self.tarball_url + self.fname

    def download(self):
        url = self._get_url()
        click.echo("Downloading tarball")
        r = requests.get(url, stream=True)

        # Total size in bytes.
        total_size = int(r.headers.get('content-length', 0));
        total_size = int(total_size / (1024 * 1024))

        if not os.path.exists(self.local_path):
            os.makedirs(self.local_path)

        with open(self.local_path + self.fname, 'wb') as f:
            for data in tqdm(r.iter_content(chunk_size=1024*1024), total=total_size, unit='MB'):
                f.write(data)

    def extract(self):
        click.echo("Extracting to " + self.local_path + "registry")
        tar = tarfile.open(self.local_path + self.fname, "r:gz")
        tar.extractall(path=self.local_path + "registry", numeric_owner=True)
        tar.close()

    def rename_lokolla(self):
        os.chmod(self.local_path + "registry", 0o700)
        dirname = self.local_path + "registry" + "/docker/registry/v2/repositories/"
        shutil.move(dirname + "lokolla", dirname + "kolla")


