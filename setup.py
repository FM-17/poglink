# TODO: Transition to setup.cfg https://setuptools.pypa.io/en/latest/userguide/quickstart.html#transitioning-from-setup-py-to-setup-cfg
from setuptools import find_packages, setup
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

with open("README.md") as f:
    long_description = f.read()

setup(
    name="poglink",
    version=version,
    use_scm_version=use_scm_version,
    setup_requires=["setuptools_scm"],
    python_requires=">=3.7",
    description="A bot that integrates the ARK Web API with Discord.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="FM-17",
    author_email="info@fm17.dev",
    url="https://github.com/FM-17/poglink",
    packages=find_packages(),
    install_requires=["discord>=1.7", "pyyaml", "python-dateutil", "jinja2"],
    entry_points={
        "console_scripts": [
            "poglink=poglink.main:cli",
        ]
    },
)
