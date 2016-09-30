# -*- coding: utf-8 -*-

import os
import subprocess

from jinja2 import Environment, PackageLoader

from settings import *

# Set up vars
env = Environment(loader=PackageLoader('word', 'templates'))


# Utility Functions
# -------------------------------

def create_template(project_name, out_dir, template_name):
    template = env.get_template(template_name)
    data = template.render(project_name=project_name)
    with open("%s/%s" % (out_dir, template_name), "w") as f:
        f.write(data)


def create_dir(parent, name):
    new = os.path.join(parent, name)
    if not os.path.exists(new):
        os.makedirs(new)


def create_file(parent, name):
    new = os.path.join(parent, name)
    if not os.path.exists(new):
        open(new, 'w').close()


# Making all the things
# -------------------------------

def clone_vagrant_setup(project_name):
    # clone the vagrant repo
    project_dir = os.path.join(os.getcwd(), project_name)
    clone_cmd = "git clone %s %s" % (VAGRANT_CONFIG_REPO, project_dir)
    subprocess.call(clone_cmd.split())

    # remove the git directory
    clean_cmd = "rm -rf %s/.git" % project_dir
    subprocess.call(clean_cmd.split())

    # Create basic default configs
    create_template(project_name, project_dir, 'site.yml')
    create_template(project_name, project_dir, 'fabfile.py')
    create_template(project_name, project_dir, '.gitignore')

    # Make some additional files and folders
    create_dir(project_dir, 'backups')
    create_file(project_dir, '.project')


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

    clean_ignore_cmd = "rm -rf %s/.gitignore" % theme_dir
    subprocess.call(clean_ignore_cmd.split())

    create_template(project_name, os.path.join(theme_dir, 'lib'), 'setup.php')
    create_template(project_name, os.path.join(theme_dir, 'assets'), 'manifest.json')


def cleanup(project_name):
    project_dir = os.path.join(os.getcwd(), project_name)
    cmd = "git init"
    run = subprocess.Popen(
        cmd.split(),
        cwd=project_dir
    )
    run.wait()
