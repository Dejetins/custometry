"""Consumer rejects hostile/partial archives before exposing an executable payload."""

import stat
import zipfile
from pathlib import Path

import pytest

from tools.custometry_quality.delivery_consumer import ConsumerError, unpack


def archive(path: Path, names: list[str], mode: int = stat.S_IFREG | 0o600) -> None:
    with zipfile.ZipFile(path, "w") as stream:
        for name in names:
            info = zipfile.ZipInfo(name)
            info.external_attr = mode << 16
            stream.writestr(info, b"payload")


@pytest.mark.parametrize(
    "name", ["../outside", "/absolute", "a/../../outside", "a\\b", "a//b", "./file"]
)
def test_escape_does_not_create_destination(tmp_path: Path, name: str) -> None:
    source, target = tmp_path / "input.zip", tmp_path / "output"
    archive(source, ["valid", name])
    with pytest.raises(ConsumerError):
        unpack(source, target)
    assert not target.exists()
    assert not (tmp_path / "outside").exists()


def test_symlink_and_duplicate_reject(tmp_path: Path) -> None:
    for number, names, mode in [
        (1, ["link"], stat.S_IFLNK | 0o777),
        (2, ["A", "a"], stat.S_IFREG | 0o600),
    ]:
        source, target = tmp_path / f"{number}.zip", tmp_path / f"out{number}"
        archive(source, names, mode)
        with pytest.raises(ConsumerError):
            unpack(source, target)
        assert not target.exists()


def test_truncated_payload_never_promotes(tmp_path: Path) -> None:
    source, target = tmp_path / "input.zip", tmp_path / "output"
    archive(source, ["first", "second"])
    raw = bytearray(source.read_bytes())
    position = raw.find(b"payload", raw.find(b"payload") + 1)
    raw[position] ^= 1
    source.write_bytes(raw)
    with pytest.raises(zipfile.BadZipFile):
        unpack(source, target)
    assert not target.exists()
    assert list(tmp_path.iterdir()) == [source]


def test_size_limit_and_existing_identity(tmp_path: Path) -> None:
    source, target = tmp_path / "input.zip", tmp_path / "output"
    archive(source, ["file"])
    with pytest.raises(ConsumerError):
        unpack(source, target, limit=1)
    unpack(source, target)
    with pytest.raises(ConsumerError):
        unpack(source, target)
    assert (target / "file").read_bytes() == b"payload"
