# Compatibility shim for Python 3.12+ where distutils is removed.
# Only exposes what Django 3.1 imports: distutils.version.LooseVersion
from .version import LooseVersion  # noqa: F401
