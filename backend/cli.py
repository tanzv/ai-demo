import click
from flask import Flask
from config.database import init_db
from scripts.init_db import init_postgres_db, create_admin_user
from config.settings import settings

@click.group()
def cli():
    """AI Demo 管理工具"""
    pass

@cli.command()
def init():
    """初始化数据库和创建管理员用户"""
    click.echo("正在初始化数据库...")
    if init_postgres_db():
        click.echo("数据库创建成功")
        
        app = Flask(__name__)
        app.config.update(
            SECRET_KEY=settings.get('auth.secret_key'),
            SQLALCHEMY_DATABASE_URI=settings.database_url,
            SQLALCHEMY_TRACK_MODIFICATIONS=False
        )
        
        init_db(app)
        create_admin_user(app)
        click.echo("数据库初始化完成")
    else:
        click.echo("数据库初始化失败")

@cli.command()
@click.option('--host', default='0.0.0.0', help='服务器主机地址')
@click.option('--port', default=8000, help='服务器端口')
@click.option('--debug/--no-debug', default=True, help='是否启用调试模式')
def run(host, port, debug):
    """启动应用服务器"""
    from app import create_app
    app = create_app()
    app.run(host=host, port=port, debug=debug)

@cli.command()
def shell():
    """启动交互式 Python shell"""
    from app import create_app
    app = create_app()
    with app.app_context():
        import code
        code.InteractiveConsole(locals=globals()).interact()

if __name__ == '__main__':
    cli() 