from anki_note_types.model import Catalog


def test_catalog_copies_the_input_mapping():
    source = {"one": 1}

    catalog = Catalog(source)
    source["two"] = 2

    assert len(catalog) == 1
    assert catalog.require("one") == 1
