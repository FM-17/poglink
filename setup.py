# TODO: Transition to setup.cfg https://setuptools.pypa.io/en/latest/userguide/quickstart.html#transitioning-from-setup-py-to-setup-cfg
import os

from setuptools import setup

# If PYTHON_PACKAGE_VERSION variable is provided, use this instead of automatically grabbing from SCM.
version = os.getenv("PYTHON_PACKAGE_VERSION")

kwargs = {"setup_requires": ["setuptools_scm"]}
if version:
    kwargs["version"] = version
elif os.getenv("CI") == "true":
    # the local scheme is overridden because pypi doesn't support commit hashes in version numbers
    kwargs["use_scm_version"] = {"local_scheme": "no-local-version"}
else:
    kwargs["use_scm_version"] = True

setup(**kwargs)
