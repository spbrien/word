from fabric.api import *
from fabtools.vagrant import vagrant


# Utilities
# ------------------------
def find_root():
    working_dir = os.getcwd().split(os.sep)
    length = len(working_dir) + 1
    build_paths = filter(lambda x: x != '', ['/'.join(working_dir[:x]) for x in range(length)])
    paths = [x for x in reversed(build_paths)]
    for path in paths:
    test_root = os.path.join(path, '.project')
        if os.path.isfile(test_root):
            return path
    return None

# Constants
# ------------------------
PROJECT_NAME = "{{project_name}}"
WORDPRESS_DIR = "/var/www/{{project_name}}"
PROJECT_ROOT = find_root()


# Tasks
# ------------------------
@task
def backup():
    with cd(WORDPRESS_DIR):
        run('wp db export --add-drop-table')
    # move resulting sql file to backups folder locally


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
