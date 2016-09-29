{% raw %}from fabric.api import *
from fabtools.vagrant import vagrant

@task
def uname():
    run('uname -a'){% endraw %}
