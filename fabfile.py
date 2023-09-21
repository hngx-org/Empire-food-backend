from fabric import task
from invoke import run as local
from fabric.connection import Context


@task
def ping_server(ctx: Context):
    """Ping the server"""
    ctx.run("ping -c 2 localhost", echo=True, warn=True)


@task
def package_app(ctx: Context, path: str):
    """create a tarball of the application"""
    local('rm -rf .deployments', echo=True)
    local('mkdir -p .deployments', echo=True)
    local(f"tar -czvf .deployments/backend.tar.gz --exclude='./.git/*' {path}", echo=True)


@task
def copy_files(ctx: Context):
    """Copy the application to the server"""
    ctx.run('sudo rm -rf /app/backend', echo=True)
    ctx.run('sudo mkdir -p /app/backend', echo=True)
    ctx.run('sudo chmod 777 /app/backend', echo=True)
    ctx.put('.deployments/backend.tar.gz', '/tmp/')
    ctx.run('sudo tar -xvf /tmp/backend.tar.gz -C /app/backend', echo=True)


@task
def nginx_config(ctx: Context):
    """Start the application server"""
    with ctx.cd("/app/backend"):
        # ctx.run('chmod +x ./deploy/configure_server.sh', echo=True)
        ctx.run('./deploy/configure_server.sh', echo=True)


@task
def start_app(ctx: Context):
    """Start the application server"""
    with ctx.cd("/app/backend"):
        # ctx.run('chmod +x ./deploy/service.sh', echo=True)
        ctx.run('./deploy/service.sh', echo=True)


@task
def deploy(ctx: Context):
    """Deploy the application"""
    ping_server(ctx)
    package_app(ctx, './')
    copy_files(ctx)
    nginx_config(ctx)
    start_app(ctx)
