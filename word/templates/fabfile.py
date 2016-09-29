{% raw %}from fabric.api import env, local, run

def vagrant():
    env.user = "vagrant"
    env.hosts = ['127.0.0.1:2222']

    result = local('vagrant ssh_config | grep IdentityFile', capture=True)
    env.key_filename = result.split()[1]

def uname():
    run('uname -a'){% endraw %}
