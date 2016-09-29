# -*- coding: utf-8 -*-

import os
import subprocess

from jinja2 import Environment, PackageLoader

from settings import *

# Set up vars
env = Environment(loader=PackageLoader('word', 'templates'))


def create_template(project_name, template_name):
    template = env.get_template(template_name)
    return template.render(project_name=project_name)


def clone_vagrant_setup(project_name):
    # clone the vagrant repo
    project_dir = os.path.join(os.getcwd(), project_name)
    clone_cmd = "git clone %s %s" % (VAGRANT_CONFIG_REPO, project_dir)
    subprocess.call(clone_cmd.split())

    # remove the git directory
    clean_cmd = "rm -rf %s/.git" % project_dir
    subprocess.call(clean_cmd.split())

    config = create_template(project_name, 'site.yml')
    with open("%s/site.yml" % project_dir, "w") as f:
        f.write(config)


def install_vagrant_environment(project_name):
    project_dir = os.path.join(os.getcwd(), project_name)
    install_cmd = "vagrant up"
    run = subprocess.Popen(
        install_cmd.split(),
        cwd=project_dir
    )
    run.wait()

def clone_basetheme(project_name):
    # Clone the theme repo
    project_dir = os.path.join(os.getcwd(), project_name)
    theme_dir = os.path.join(project_dir, 'www/%s/wp-content/themes/%s' % (project_name, project_name))
    clone_cmd = "git clone %s %s" % (BASETHEME_REPO, theme_dir)
    subprocess.call(clone_cmd.split())

    # remove the git directory
    clean_cmd = "rm -rf %s/.git" % theme_dir
    subprocess.call(clean_cmd.split())

    config = create_template(project_name, 'setup.php')
    with open("%s/lib/setup.php" % theme_dir, "w") as f:
        f.write(config) 

    config = create_template(project_name, 'manifest.json')
    with open("%s/assets/manifest.json" % theme_dir, "w") as f:
        f.write(config)


def cleanup(project_name):
    project_dir = os.path.join(os.getcwd(), project_name)
    cmd = "git init"
    run = subprocess.Popen(
        cmd.split(),
        cwd=project_dir
    )
    run.wait()
