import pytest, os
from implementation.primaries.ExtractMetadata.classes.DataLayer.querylayer import QueryLayer
from implementation.primaries.ExtractMetadata.classes.DataLayer.musicdata import MusicData
from implementation.primaries.ExtractMetadata.classes.MusicManager import MusicManager
from implementation.primaries.ExtractMetadata.classes.hashdict import hashdict


@pytest.fixture()
def db():
    return "sqlite:///:memory:"


@pytest.fixture()
def qlayer(db):
    elem = QueryLayer(db)
    elem.setup()
    return elem


@pytest.fixture()
def mlayer(db):
    elem = MusicData(db)
    elem.setup()
    return elem

@pytest.fixture()
def manager_folder():
    return os.path.join(
            os.path.dirname(
                os.path.realpath(__file__)),
            "../test_files/manager_tests")

@pytest.fixture()
def manager(db, manager_folder):
    elem = MusicManager(None, folder=manager_folder, db=db)
    elem.setup()
    return elem


@pytest.fixture()
def insname():
    count = 0
    while True:
        yield "ins_{}".format(count)
        count += 1


@pytest.fixture()
def clef_in(clef_out):
    return {"name": clef_out}


@pytest.fixture()
def clef_out():
    return "treble"


@pytest.fixture()
def key_in(key_out):
    return {"name": key_out}


@pytest.fixture()
def key_out():
    return "C major"


@pytest.fixture()
def dummy():
    data = {"instruments": [{"name": "wibble"}],
            "clefs": {"wibble": [{"name": "treble"}]},
            "keys": {"wibble": [{"name": "C major"}]}}
    return data


@pytest.fixture()
def dummy_res():
    return {
        "keys": {
            'wibble': ['C major']}, "clefs": {
            'wibble': ['treble']}, "instruments": [
                hashdict(
                    chromatic=None, diatonic=None, name='wibble')]}
