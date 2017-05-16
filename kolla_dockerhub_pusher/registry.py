import os
from multiprocessing import Pool
import subprocess
from io import StringIO

import click
from tqdm import tqdm


def pull_worker(image):
    try:
        devnull = open(os.devnull, 'w')
        subprocess.call(
                ["docker", "pull", "127.0.0.1:5000/kolla/" + image],
                stdout=devnull)
        return image, None
    except Exception as e:
        return image, e


class Registry(object):
    def __init__(self, local_path, registry_name="kolla-registry"):
        self.local_path = local_path
        self.registry_name = registry_name

    def setup(self):
        resp = os.system(
                ("docker run -d -p 5000:5000 -v "
                    "{}:/var/lib/registry --name {} registry:2").format(
                    self.local_path + "/registry/",
                    self.registry_name,
                )
            )

    def ls(self):
        registry_path = self.local_path + "/registry/docker/registry/v2/repositories/kolla"
        images = os.listdir(registry_path)
        imgs = []
        for image in images:
            tag = os.listdir(registry_path + "/" + image + "/_manifests/tags")[0]
            imgs.append(image + ":" + tag)
        return imgs

    def pull_all(self):
        images = self.ls()
        with Pool() as pool:
            pulls = pool.imap_unordered(pull_worker, images)
            for img, err in tqdm(pulls, total=len(images), unit="image"):
                if err:
                    print(img, type(err), err)





