from rest_framework import serializers
from openbudget.apps.international.utilities import translated_fields
from openbudget.apps.entities import models


class EntityMin(serializers.HyperlinkedModelSerializer):
    """A minimal serializer for use as a nested entity representation."""

    class Meta:
        model = models.Entity
        fields = ['id', 'url']


class DivisionMin(serializers.HyperlinkedModelSerializer):
    """A minimal serializer for use as a nested division representation."""

    class Meta:
        model = models.Division
        fields = ['id', 'url']


class EntityBase(serializers.HyperlinkedModelSerializer):
    """The default serialized representation of entities."""

    parent = EntityMin()
    division = DivisionMin()

    class Meta:
        model = models.Entity
        fields = ['id', 'url', 'name', 'description', 'code', 'parent',
                  'division', 'sheets', 'created_on', 'last_modified']\
                 + translated_fields(model)


class DivisionBase(serializers.HyperlinkedModelSerializer):
    """The default serialized representation of divisions."""

    class Meta:
        model = models.Division
        fields = ['id', 'url', 'name', 'index', 'budgeting', 'domain',
                  'created_on', 'last_modified'] + translated_fields(model)


class DomainBase(serializers.HyperlinkedModelSerializer):
    """The default serialized representation of domains."""

    class Meta:
        model = models.Domain
        fields = ['id', 'url', 'name', 'measurement_system',
                  'ground_surface_unit', 'currency', 'created_on',
                  'last_modified', 'divisions'] + translated_fields(model)


class DomainDetail(DomainBase):
    """A detailed, related representation of domain."""

    divisions = DivisionBase()


class DivisionDetail(DivisionBase):
    """Used to represent a full relational map of a division."""

    domain = DomainBase()
    # don't show self again on nested objects
    del domain.fields['divisions']

    class Meta(DivisionBase.Meta):
        fields = DivisionBase.Meta.fields + ['entities']


class EntityDetail(EntityBase):
    """A detailed, related representation of entities."""
    # preventing circular import
    from openbudget.apps.sheets.serializers import SheetBase
    sheets = SheetBase()
