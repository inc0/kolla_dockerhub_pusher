# -*- coding: utf-8 -*-

import click

from . import tarballs
from . import registry
from . import utils


@click.command()
@click.option('--base', help='base OS')
@click.option('--type', help='Type of installation', type=click.Choice(
    ['binary', 'source']))
@click.option('--release', help='OpenStack release')
@click.option('--tarball-url', help='URL to tared registry',
        default="http://tarballs.openstack.org/kolla/images/")
@click.option('--local-path', help='Path to extract contents of tarball',
        default='/tmp/kolla/')
def main(base, type, release, tarball_url, local_path):
    click.echo("{} {} {}".format(base, type, release))
    tb = tarballs.TarFile(base, type, release, tarball_url, local_path)
    #tb.download()
    tb.extract()
    tb.rename_lokolla()

    reg_dirname = utils.get_file_name(base, type, release)[:-7]
    reg = registry.Registry(local_path, reg_dirname)
    reg.setup()

if __name__ == "__main__":
    main()
