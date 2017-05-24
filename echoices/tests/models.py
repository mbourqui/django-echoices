from django.db import models

from echoices.enums import EChoice, EOrderedChoice, EAutoChoice
from echoices.fields import make_echoicefield


# ==========
# EChoice

class ETestCharChoices(EChoice):
    FIELD1 = ('u', 'Label 1')
    FIELD2 = ('v', 'Label 2')


class ETestStrChoices(EChoice):
    FIELD1 = ('value1', 'Label 1')
    FIELD2 = ('value2', 'Label 2')


class ETestIntChoices(EChoice):
    FIELD1 = (10, 'Label 1')
    FIELD2 = (20, 'Label 2')


class ETestFloatChoices(EChoice):
    FIELD1 = (1.0, 'Label 1')
    FIELD2 = (2.0, 'Label 2')


class ETestBoolChoices(EChoice):
    FIELD1 = (True, 'Label 1')
    FIELD2 = (False, 'Label 2')


class TestCharChoicesModel(models.Model):
    choice = models.CharField(max_length=ETestCharChoices.max_value_length(),
                              choices=ETestCharChoices.choices())


class TestCharChoicesDefaultModel(models.Model):
    choice = models.CharField(max_length=ETestCharChoices.max_value_length(),
                              choices=ETestCharChoices.choices(),
                              default=ETestCharChoices.FIELD1.value)


class TestStrChoicesModel(models.Model):
    choice = models.CharField(max_length=ETestStrChoices.max_value_length(),
                              choices=ETestStrChoices.choices())


class TestStrChoicesDefaultModel(models.Model):
    choice = models.CharField(max_length=ETestStrChoices.max_value_length(),
                              choices=ETestStrChoices.choices(),
                              default=ETestStrChoices.FIELD1.value)


class TestIntChoicesModel(models.Model):
    choice = models.IntegerField(choices=ETestIntChoices.choices(), null=True)


class TestIntChoicesDefaultModel(models.Model):
    choice = models.IntegerField(choices=ETestIntChoices.choices(), default=ETestIntChoices.FIELD1.value)


class TestFloatChoicesModel(models.Model):
    choice = models.FloatField(choices=ETestFloatChoices.choices(), null=True)


class TestFloatChoicesDefaultModel(models.Model):
    choice = models.FloatField(choices=ETestFloatChoices.choices(), default=ETestFloatChoices.FIELD1.value)


class TestBoolChoicesDefaultModel(models.Model):
    # NULL is not supported by BooleanField, but NullBooleanField does
    choice = models.BooleanField(choices=ETestBoolChoices.choices(), default=ETestBoolChoices.FIELD1.value)


# ==========
# EOrderedChoice

class ETestCharOrderedChoices(EOrderedChoice):
    FIELD1 = ('w', 'Label 1')
    FIELD2 = ('u', 'Label 2')
    FIELD3 = ('v', 'Label 3')


class ETestStrOrderedChoices(EOrderedChoice):
    FIELD1 = ('value3', 'Label 1')
    FIELD2 = ('value1', 'Label 2')
    FIELD3 = ('value2', 'Label 3')


class ETestIntOrderedChoices(EOrderedChoice):
    FIELD1 = (30, 'Label 1')
    FIELD2 = (10, 'Label 2')
    FIELD3 = (20, 'Label 3')


class TestCharOrderedChoicesModel(models.Model):
    choice = models.CharField(max_length=ETestCharOrderedChoices.max_value_length(),
                              choices=ETestCharOrderedChoices.choices(),
                              default=ETestCharOrderedChoices.FIELD1.value)


class TestStrOrderedChoicesModel(models.Model):
    choice = models.CharField(max_length=ETestStrOrderedChoices.max_value_length(),
                              choices=ETestStrOrderedChoices.choices(),
                              default=ETestStrOrderedChoices.FIELD1.value)


class TestIntOrderedChoicesModel(models.Model):
    choice = models.IntegerField(choices=ETestIntOrderedChoices.choices(), default=ETestIntOrderedChoices.FIELD1.value)


# ==========
# EAutoChoice

class ETestAutoChoices(EAutoChoice):
    FIELD1 = 'Label 1'
    FIELD2 = 'Label 2'
    FIELD3 = 'Label 3'


class TestAutoChoicesModel(models.Model):
    choice = models.IntegerField(choices=ETestAutoChoices.choices(), default=ETestAutoChoices.FIELD1.value)


# ==========
# EChoiceField

class TestEChoiceFieldEStrChoicesModel(models.Model):
    choice = make_echoicefield(ETestStrChoices)


class TestNamedEChoiceFieldEStrChoicesModel(models.Model):
    choice = make_echoicefield(ETestStrChoices, klass_name='MyEnumFieldName')


class TestEChoiceFieldDefaultEStrChoicesModel(models.Model):
    choice = make_echoicefield(ETestStrChoices, default=ETestStrChoices.FIELD1)


class TestEChoiceFieldEIntChoicesModel(models.Model):
    choice = make_echoicefield(ETestIntChoices, null=True)


class TestEChoiceFieldDefaultEIntChoicesModel(models.Model):
    choice = make_echoicefield(ETestIntChoices, default=ETestIntChoices.FIELD1)


class TestEChoiceFieldEFloatChoicesModel(models.Model):
    choice = make_echoicefield(ETestFloatChoices, null=True)


class TestEChoiceFieldDefaultEFloatChoicesModel(models.Model):
    choice = make_echoicefield(ETestFloatChoices, default=ETestFloatChoices.FIELD1)


class TestEChoiceFieldDefaultEBoolChoicesModel(models.Model):
    # NULL is not supported by BooleanField, but NullBooleanField does
    choice = make_echoicefield(ETestBoolChoices, default=ETestBoolChoices.FIELD1)


class TestEChoiceCharFieldEStrOrderedChoicesModel(models.Model):
    choice = make_echoicefield(ETestStrOrderedChoices, default=ETestStrOrderedChoices.FIELD1)

# TODO: derive EChoice
