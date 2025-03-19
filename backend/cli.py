import asyncio
import os
import sys
import click
from flask import Flask
from werkzeug.serving import run_simple

from config.database import init_db
from config.settings import settings
from app import create_app

def setup_environment(env: str) -> None:
    """设置环境变量
    
    Args:
        env: 环境名称（development/production/testing）
    """
    os.environ["ENV"] = env
    
    # 设置配置文件路径
    config_path = f"config/{env}.yaml"
    if os.path.exists(config_path):
        os.environ["CONFIG_PATH"] = config_path
    else:
        os.environ["CONFIG_PATH"] = "config/default.yaml"

def run_async_command(f):
    """装饰器：运行异步命令"""
    @click.pass_context
    def wrapper(ctx, *args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return wrapper

@click.group()
def cli():
    """AI Demo 后端管理工具"""
    pass

@cli.command()
@click.option(
    "--env",
    type=click.Choice(["development", "production", "testing"]),
    default="development",
    help="运行环境",
)
@click.option(
    "--host",
    default="0.0.0.0",
    help="主机地址",
)
@click.option(
    "--port",
    default=8000,
    type=int,
    help="端口号",
)
@click.option(
    "--debug",
    is_flag=True,
    default=True,
    help="是否启用调试模式",
)
def run(env: str, host: str, port: int, debug: bool) -> None:
    """运行应用服务器"""
    setup_environment(env)
    
    # 创建应用实例
    app = create_app()
    
    if debug:
        # 使用 Werkzeug 的开发服务器，支持热重载
        run_simple(
            host,
            port,
            app,
            use_reloader=True,
            use_debugger=True,
            threaded=True,
            processes=1
        )
    else:
        # 生产环境使用 Flask 的开发服务器
        app.run(
            host=host,
            port=port,
            debug=False,
            use_reloader=False
        )

@cli.command(name="init")
@click.option(
    "--env",
    type=click.Choice(["development", "production", "testing"]),
    default="development",
    help="运行环境",
)
@run_async_command
async def init_db_command(env: str) -> None:
    """初始化数据库"""
    setup_environment(env)
    
    try:
        # 导入并运行初始化脚本
        from scripts.init_db import init_db
        await init_db()
        click.echo("数据库初始化成功")
    except Exception as e:
        click.echo(f"数据库初始化失败：{str(e)}", err=True)
        raise click.Abort()

@cli.command()
@run_async_command
async def shell() -> None:
    """启动异步 Python Shell"""
    # 导入常用模块和对象
    from main import app
    from config.database import AsyncSessionLocal
    from models.user import User
    
    # 创建异步会话
    async with AsyncSessionLocal() as session:
        # 设置 Python Shell 环境
        import IPython
        IPython.embed(
            header=f"AI Demo Async Shell (Python {sys.version.split()[0]})\n"
                  f"可用对象: app, session, User\n"
                  "注意：这是一个异步环境，请使用 await 调用异步函数",
            user_ns={
                "app": app,
                "session": session,
                "User": User,
                "asyncio": asyncio,
            }
        )

if __name__ == "__main__":
    cli() 