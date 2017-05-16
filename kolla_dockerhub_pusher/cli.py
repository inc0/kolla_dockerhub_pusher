# -*- coding: utf-8 -*-
from subprocess import call

import click

from . import tarballs
from . import registry
from . import utils


@click.group(help="Toolset to manage Kolla registry")
def main():
    pass


@click.command(help="Downloads built registry tarball and sets it up locally")
@click.option('--base', help='base OS')
@click.option('--type', help='Type of installation', type=click.Choice(
    ['binary', 'source']))
@click.option('--release', help='OpenStack release')
@click.option('--tarball-url', help='URL to tared registry',
        default="http://tarballs.openstack.org/kolla/images/")
@click.option('--local-path', help='Path to extract contents of tarball',
        default='/tmp/kolla/')
def download(base, type, release, tarball_url, local_path):
    click.echo("Downloading {} {} {}".format(base, type, release))
    tb = tarballs.TarFile(base, type, release, tarball_url, local_path)
    tb.download()
    tb.extract()
    tb.rename_lokolla()

    reg = registry.Registry(local_path)
    reg.setup()


@click.command(help="Lists all images available in registry")
@click.option('--local-path', help='Path to extract contents of tarball',
        default='/tmp/kolla/')
def ls(local_path):
    reg = registry.Registry(local_path)
    for img in reg.ls():
        click.echo(img)


@click.command(help="Pulls all images from registry")
@click.option('--local-path', help='Path to extract contents of tarball',
        default='/tmp/kolla/')
def pull(local_path):
    lreg = registry.Registry(local_path)
    lreg.pull_all()



main.add_command(download)
main.add_command(ls)
main.add_command(pull)

if __name__ == "__main__":
    main()
