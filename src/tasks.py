import importlib
import marshal
import os 
import pip
import types

from celery import Celery
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)

redis_url = os.environ.get("REDIS_HOST", "redis")

app = Celery(
    "tasks",
    broker=f"redis://{redis_url}",
    backend=f"redis://{redis_url}",
)
app.conf.task_serializer = "pickle"
app.conf.accept_content = ["pickle", "json"]


def install(package):
    # https://stackoverflow.com/a/15950647

    warnings.simplefilter("ignore")
    pip_main = pip.main if hasattr(pip, "main") else pip._internal.main
    pip_main(["install", package])


@app.task
def exec_func(
    code_string: str,
    requirements: dict = None,
    args: tuple = None,
    kwargs: dict = None,
):
    """
    code_string - code of function to execute.
    requirements - dict with info about used modules. Key is module and value is package.
    args - tuple of args for executable function.
    kwargs - dict of named args for executable function.

    returns: result of function.

    for usage see example.py for
    """
    requirements = requirements or {}

    for module, package in requirements.items():
        try:
            mod = importlib.import_module(module)
        except ImportError as e:
            logger.debug(f"Installing module {module} from package {package}")
            install(package)
            mod = importlib.import_module(module)
        finally:
            globals()[module] = mod

    args = args or ()
    kwargs = kwargs or {}
    code = marshal.loads(code_string)
    fn = types.FunctionType(code, globals(), "fn")

    result = fn(*args, **kwargs)
    return result
