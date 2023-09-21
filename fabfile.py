from os import getenv
import sys

from fabric import task
from invoke import run as local
from fabric.connection import Context


DEPLOY_DIR = "/app/backend"
USER = getenv("REMOTE_USER", "mypythtesting")


@task
def ping_server(ctx: Context):
    """Ping the server"""
    ctx.run("ping -c 2 localhost", echo=True, warn=True)


@task
def package_app(ctx: Context, path: str):
    """create a tarball of the application"""
    local('rm -rf .deployments', echo=True)
    local('mkdir -p .deployments', echo=True)
    local(f"tar -czvf .deployments/backend.tar.gz --exclude='./.git/*' --exclude='Pipfile*' --exclude='env.sample' --exclude='.vscode' --exclude='*__pycache__*' {path}", echo=True)


@task
def copy_files(ctx: Context):
    """Copy the application to the server"""
    ctx.run(f'sudo rm -rf {DEPLOY_DIR}', echo=True)
    ctx.run(f'sudo mkdir -p {DEPLOY_DIR}', echo=True)
    ctx.put('.deployments/backend.tar.gz', '/tmp/')
    ctx.run(f'sudo tar -xvf /tmp/backend.tar.gz -C {DEPLOY_DIR}', echo=True)
    ctx.run(f'sudo chown -R {USER}:{USER} {DEPLOY_DIR}', echo=True)


@task
def nginx_config(ctx: Context):
    """Start the application server"""
    with ctx.cd(f"{DEPLOY_DIR}"):
        ctx.run('./deploy/configure_server.sh', echo=True)


@task
def start_app(ctx: Context):
    """Start the application server"""
    with ctx.cd(f"{DEPLOY_DIR}"):
        ctx.run('./deploy/service.sh', echo=True)


@task
def deploy(ctx: Context):
    """Deploy the application"""
    ping_server(ctx)
    package_app(ctx, './')
    copy_files(ctx)
    nginx_config(ctx)
    start_app(ctx)
