from importlib.metadata import version, PackageNotFoundError
from . import cogs

try:
    __version__ = version("poglink")
except PackageNotFoundError:
    pass