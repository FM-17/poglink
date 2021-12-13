# TODO: Transition to setup.cfg https://setuptools.pypa.io/en/latest/userguide/quickstart.html#transitioning-from-setup-py-to-setup-cfg
from setuptools import setup
import os

# If PYTHON_PACKAGE_VERSION variable is provided, use this instead of automatically grabbing from SCM.
version = os.getenv("PYTHON_PACKAGE_VERSION")

# the local scheme is overridden because pypi doesn't support commit hashes in version numbers
if version:
    use_scm_version = False
elif os.getenv("CI") == "true":
    use_scm_version = {"local_scheme": "no-local-version"}
else:
    use_scm_version = True

setup(
    version=version,
    use_scm_version=use_scm_version,
    setup_requires=["setuptools_scm"],
)
