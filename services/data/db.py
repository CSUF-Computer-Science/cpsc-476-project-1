import sqlite3, click, os.path
from flask import current_app, g
from flask.cli import with_appcontext

from cassandra.cluster import Cluster, NoHostAvailable

cluster = Cluster(['172.17.0.2'])

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_data_cmd)
    app.cli.add_command(init_db_cmd)
    app.cli.add_command(reset_db_cmd)


def get_db(service):
    return cluster.connect('blog')


def close_db(service, e=None):
    pass


def init_db():
    db = cluster.connect()
    with current_app.open_resource(f'data/schemas/blog.cql') as f:
        content = f.readlines()
        for line in content:
            print("Ran: ", line.decode('utf-8'))
            db.execute(line.decode('utf-8'))
    click.echo(f"Initialized database for blog")


def reset_db(service):
    if os.path.isfile(f"{service}.db"):
        os.remove(f"{service}.db")
    click.echo(f"Removed database for {service}")
    init_db(service)


@click.command('init-db')
@click.argument('service')
@with_appcontext
def init_db_cmd(service):
    init_db()

@click.command('reset-db')
@click.argument('service')
@with_appcontext
def reset_db_cmd(service):
    reset_db(service)
    init_db(service)


def init_service_data(service):
    with current_app.app_context():
        db = get_db(service)
    with current_app.open_resource(f'data/schemas/{service}.data.sql') as f:
        content = f.read().decode()
        db.executescript(content)
    db.commit()
    click.echo(f"Initialized data for {service}")


@click.command('init-data')
@click.argument('service')
@with_appcontext
def init_data_cmd(service):
    services = ["articles", "comments", "tags", "users"]
    if service == "all":
        for service in services:
            init_service_data(service)
    elif service in services:
        init_service_data(service)
    else:
        click.echo(f"{service} is not one of [comments, tags, users, articles, all]")