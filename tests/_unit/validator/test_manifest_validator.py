from anki_note_types.validator.manifest_validator import ManifestValidator


def test_note_type_manifest_accepts_the_documented_contract():
    diagnostics = ManifestValidator().validate_note_type(
        {"schemaVersion": 1, "name": "Vocabulary", "stylesheet": "common.css", "fields": ["Word"]}
    )

    assert diagnostics == ()


def test_template_manifest_reports_unknown_and_missing_fields():
    diagnostics = ManifestValidator().validate_template({"schemaVersion": 1, "unused": True})

    assert {item.code for item in diagnostics} == {"invalid-manifest-field", "unknown-manifest-field"}
