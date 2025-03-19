import asyncio
import os
import sys
import click
from hypercorn.config import Config
from hypercorn.asyncio import serve
from typing import Optional

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
    "--workers",
    default=1,
    type=int,
    help="工作进程数",
)
@click.option(
    "--reload",
    is_flag=True,
    default=False,
    help="是否启用热重载",
)
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="是否启用调试模式",
)
def run(env: str, host: str, port: int, workers: int, reload: bool, debug: bool) -> None:
    """运行应用服务器"""
    setup_environment(env)
    
    # 创建应用实例
    app = create_app()
    
    # 配置 Hypercorn
    config = Config()
    config.bind = [f"{host}:{port}"]
    config.workers = workers
    config.use_reloader = reload
    config.accesslog = "-"  # 输出到标准输出
    config.errorlog = "-"   # 输出到标准错误
    config.loglevel = "debug" if debug or env != "production" else "info"
    
    # 启动异步服务器
    asyncio.run(serve(app, config))

@cli.command()
@click.option(
    "--env",
    type=click.Choice(["development", "production", "testing"]),
    default="development",
    help="运行环境",
)
@run_async_command
async def init(env: str) -> None:
    """初始化数据库"""
    setup_environment(env)
    
    # 运行异步初始化函数
    from scripts.init_db import init_app
    await init_app()
    click.echo("数据库初始化完成")

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