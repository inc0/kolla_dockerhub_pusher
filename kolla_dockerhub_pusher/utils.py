import os


def get_file_name(base, type, release):
    fname = "{base}-{type}-registry-{release}.tar.gz".format(
        base = base,
        type = type,
        release = release)
    return fname


def get_list_of_images(local_path):
    registry_path = local_path + "/registry/docker/registry/v2/repositories/kolla"
    images = os.listdir(registry_path)
    imgs = []
    for image in images:
        tag = os.listdir(registry_path + "/" + image + "/_manifests/tags")[0]
        imgs.append(image + ":" + tag)
    return imgs

