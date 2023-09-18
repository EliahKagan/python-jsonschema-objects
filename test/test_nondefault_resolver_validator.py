import pytest  # noqa
import referencing
import json
import referencing.jsonschema
import referencing.exceptions
import python_jsonschema_objects as pjo


def test_custom_spec_validator(markdown_examples):
    # This schema shouldn't be valid under DRAFT-03
    schema = {
        "$schema": "http://json-schema.org/draft-04/schema",
        "title": "other",
        "oneOf": [{"type": "string"}, {"type": "number"}],
    }
    builder = pjo.ObjectBuilder(
        schema,
        specification_uri="http://json-schema.org/draft-03/schema",
        resolved=markdown_examples,
    )
    klasses = builder.build_classes()
    a = klasses.Other("foo")
    assert a == "foo"


def test_non_default_resolver_finds_refs():
    registry = referencing.Registry()

    remote_schema = {
        "$schema": "http://json-schema.org/draft-04/schema",
        "type": "number",
    }
    registry = registry.with_resource(
        "https://example.org/schema/example",
        referencing.Resource.from_contents(remote_schema),
    )

    schema = {
        "$schema": "http://json-schema.org/draft-04/schema",
        "title": "other",
        "type": "object",
        "properties": {
            "local": {"type": "string"},
            "remote": {"$ref": "https://example.org/schema/example"},
        },
    }

    builder = pjo.ObjectBuilder(
        schema,
        registry=registry,
    )
    builder.build_classes()
