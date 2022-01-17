import os
import tempfile

import pytest

from poglink.utils import parse_bool, rotate_backups


@pytest.fixture(scope="module")
def tmpdir():
    with tempfile.TemporaryDirectory() as tmp:
        yield tmp


@pytest.fixture
def main_filename(tmpdir):
    filename = os.path.join(tmpdir, "file.txt")
    return filename


def test_rotate_backup(tmpdir, main_filename):
    # Starting with empty directory
    assert len(os.listdir(tmpdir)) == 0

    # Check single file is rotated
    with open(os.path.join(tmpdir, "file.txt"), "w") as f:
        f.write("2")
    rotate_backups(main_filename, 3)
    assert ["file.txt.1"] == os.listdir(tmpdir)

    # Check two files are rotated
    with open(os.path.join(tmpdir, "file.txt"), "w") as f:
        f.write("2")
    rotate_backups(main_filename, 3)
    assert {"file.txt.2", "file.txt.1"} == set(os.listdir(tmpdir))

    # Check 3rd file is discarded
    with open(os.path.join(tmpdir, "file.txt"), "w") as f:
        f.write("3")
    rotate_backups(main_filename, 3)
    assert {"file.txt.2", "file.txt.1"} == set(os.listdir(tmpdir))

    # Check that rotation still works without base file
    rotate_backups(main_filename, 3)
    assert ["file.txt.2"] == os.listdir(tmpdir)
    with open(os.path.join(tmpdir, "file.txt.2")) as f:
        assert "3" == f.read()


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("1", True),
        ("1", True),
        (0, False),
        (-1, False),
        (2, False),
        ("0", False),
        ("true", True),
        ("True", True),
        ("TRUE", True),
        ("y", True),
        ("Y", True),
        ("yes", True),
        ("Yes", True),
        ("YES", True),
        ("f", False),
        ("F", False),
        ("false", False),
        ("False", False),
        ("FALSE", False),
        ("apple", False),
    ],
)
def test_parse_bool(test_input, expected):
    assert parse_bool(test_input) == expected
