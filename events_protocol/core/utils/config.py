import os
import typing
import glob

from decouple import Config, RepositoryEnv, Undefined

def config(
    config_name: str,
    default: typing.Any = None,
    cast: typing.Type = None,
    env_file=os.environ.get("APPLICATION_ENVIRONMENT") or "dev"
):
    try:
        available_env_files = glob.glob("./**/*.env", recursive=True)
        env_file_path = [file for file in available_env_files if file.endswith(f'/{env_file}.env')][0]
        _config = Config(RepositoryEnv(env_file_path))
    except IndexError as ex:
        raise FileNotFoundError(f'Can\'t find environment file {env_file}.env')
    except Exception as ex:
        raise OSError(f'Can\'t parse env file {env_file}.env: {ex}')
    
    cfg = None
    try:
        cfg = _config(config_name, default=default or Undefined(), cast=cast or Undefined())
    except Exception:
        cfg = cast(default) if cast else default
    return cfg
