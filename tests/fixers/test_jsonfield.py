from __future__ import annotations

from django_upgrade.data import Settings
from tests.fixers.tools import check_noop
from tests.fixers.tools import check_transformed

settings = Settings(target_version=(3, 1))


def test_no_deprecated_alias():
    check_noop(
        """\
        from django.contrib.postgres.fields import IntegerRangeField
        """,
        settings,
    )


def test_unrecognized_import_format():
    check_noop(
        """\
        from django.contrib.postgres import fields

        fields.JSONField()
        """,
        settings,
    )


def test_untransformed_in_migration_file():
    check_noop(
        """\
        from django.contrib.postgres.fields import (
            JSONField, KeyTransform,  KeyTextTransform,
        )
        """,
        settings,
        filename="example/core/migrations/0001_initial.py",
    )


def test_full():
    check_transformed(
        """\
        from django.contrib.postgres.fields import (
            JSONField, KeyTransform,  KeyTextTransform,
        )
        """,
        """\
        from django.db.models import JSONField
        from django.db.models.fields.json import KeyTextTransform, KeyTransform
        """,
        settings,
    )


def test_model_field():
    check_transformed(
        """\
        from django.contrib.postgres.fields import JSONField
        """,
        """\
        from django.db.models import JSONField
        """,
        settings,
    )


def test_model_field_indented():
    check_transformed(
        """\
        def f():
            from django.contrib.postgres.fields import JSONField, bla
        """,
        """\
        def f():
            from django.db.models import JSONField
            from django.contrib.postgres.fields import bla
        """,
        settings,
    )


def test_model_field_submodule():
    check_transformed(
        """\
        from django.contrib.postgres.fields.jsonb import JSONField
        """,
        """\
        from django.db.models import JSONField
        """,
        settings,
    )


def test_form_field():
    check_transformed(
        """\
        from django.contrib.postgres.forms import JSONField
        """,
        """\
        from django.forms import JSONField
        """,
        settings,
    )


def test_form_field_submodule():
    check_transformed(
        """\
        from django.contrib.postgres.forms.jsonb import JSONField
        """,
        """\
        from django.forms import JSONField
        """,
        settings,
    )


def test_transforms():
    check_transformed(
        """\
        from django.contrib.postgres.fields import KeyTextTransform
        yada = 1
        from django.contrib.postgres.fields.jsonb import KeyTransform
        """,
        """\
        from django.db.models.fields.json import KeyTextTransform
        yada = 1
        from django.db.models.fields.json import KeyTransform
        """,
        settings,
    )
