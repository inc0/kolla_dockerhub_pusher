import json
import os
import subprocess
from io import StringIO
from multiprocessing import Pool

import click
import requests
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


def push_worker(image):
    try:
        devnull = open(os.devnull, 'w')
        subprocess.call(
                ["docker", "push", "docker.io/" + image],
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

    def get_tags_from_dockerhub(self, image, namespace):
        url = "https://registry.hub.docker.com/v1/repositories/" + namespace + "/" + image + "/tags"
        resp = requests.get(url)
        if not resp.ok:
            return []
        resp = resp.content
        tags = json.loads(resp.decode('utf-8'))
        return tags

    def get_next_incremental(self, image, release, namespace):
        for tag in self.get_tags_from_dockerhub(image, namespace):
            if not tag:
                break
            if tag['name'].startswith(release + "-"):
                incr = tag['name'].split("-")[1]
                try:
                    incr = str(int(incr) + 1)
                    return incr
                except ValueError:
                    continue
        return "1"

    def retag(self, release, namespace):
        images = self.ls()
        new_images = []
        for image in tqdm(images, unit="image"):
            tags = {'old': "127.0.0.1:5000/kolla/" + image, 'new': []}
            image_name = image.split(":")[0]
            incremental = self.get_next_incremental(image_name, release, namespace)
            tags['new'].append("docker.io/" + namespace + "/" + image_name + ":" + release)
            tags['new'].append("docker.io/" + namespace + "/" + image_name + ":" + release +"-" + incremental)
            new_images.append(tags)
            for newtag in tags['new']:
                subprocess.call(["docker", "tag", tags['old'], newtag])
        return new_images

    def push(self, release, namespace):
        proc = subprocess.Popen(["docker", "images"], stdout=subprocess.PIPE)
        images = proc.stdout.read()
        imgs_to_push = []
        for i in images.decode("utf-8").split("\n"):
            img = [s for s in i.split(" ") if s]
            if img and img[0].startswith(namespace) and img[1].startswith(release):
                imgs_to_push.append(img[0] + ":" +img[1])

        with Pool() as pool:
            pulls = pool.imap_unordered(push_worker, imgs_to_push)
            for img, err in tqdm(pulls, total=len(imgs_to_push), unit="image"):
                if err:
                    print(img, type(err), err)
