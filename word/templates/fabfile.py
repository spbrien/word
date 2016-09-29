from fabric.api import *
from fabtools.vagrant import vagrant

# Set up constants
PROJECT_NAME = "{{project_name}}"
WORDPRESS_DIR = "/var/www/{{project_name}}"


@task
def backup():
    with cd(WORDPRESS_DIR):
        run('wp db export --add-drop-table')


@task
def update():
    with cd(WORDPRESS_DIR):
        run('wp core update')
        run('wp core update-db')


@task
def regenerate_media():
    with cd(WORDPRESS_DIR):
        run('wp media regenerate --yes')


@task
def replace(old, new):
    with cd(WORDPRESS_DIR):
        run('wp search-replace "%s" "%s"' % (old, new))
