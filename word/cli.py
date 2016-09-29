# -*- coding: utf-8 -*-

import click
from word import *

@click.command()
@click.argument('project_name')
def main(project_name):
    """Wordpress Tools"""
    clone_vagrant_setup(project_name)
    install_vagrant_environment(project_name)
    clone_basetheme(project_name)
    cleanup(project_name)


if __name__ == "__main__":
    main()
