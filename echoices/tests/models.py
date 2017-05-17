from django.db import models

from echoices.enums import EChoice, EOrderedChoice, EAutoChoice
from echoices.fields import EChoiceCharField


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


class TestCharChoicesModel(models.Model):
    choice = models.CharField(max_length=ETestCharChoices.max_value_length(),
                              choices=ETestCharChoices.choices(),
                              default=ETestCharChoices.FIELD1.value)


class TestStrChoicesModel(models.Model):
    choice = models.CharField(max_length=ETestStrChoices.max_value_length(),
                              choices=ETestStrChoices.choices(),
                              default=ETestStrChoices.FIELD1.value)


class TestIntChoicesModel(models.Model):
    choice = models.IntegerField(choices=ETestIntChoices.choices(), default=ETestIntChoices.FIELD1.value)


class TestEChoiceCharFieldEStrChoicesModel(models.Model):
    choice = EChoiceCharField(ETestStrChoices, default=ETestStrChoices.FIELD1)


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


class TestEChoiceCharFieldEStrOrderedChoicesModel(models.Model):
    choice = EChoiceCharField(ETestStrOrderedChoices, default=ETestStrOrderedChoices.FIELD1)


# ==========
# EAutoChoice

class ETestAutoChoices(EAutoChoice):
    FIELD1 = 'Label 1'
    FIELD2 = 'Label 2'
    FIELD3 = 'Label 3'


class TestAutoChoicesModel(models.Model):
    choice = models.IntegerField(choices=ETestAutoChoices.choices(), default=ETestAutoChoices.FIELD1.value)

# TODO: derive EChoice
