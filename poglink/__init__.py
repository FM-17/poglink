from importlib.metadata import PackageNotFoundError, version

from . import cogs

try:
    __version__ = version("poglink")
except PackageNotFoundError:
    pass
