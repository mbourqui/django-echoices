from django.db import models

from echoices.enums import EChoice
from echoices.fields import EChoiceCharField


class ETestCharChoices(EChoice):
    FIELD1 = ('v', 'Label 1')
    FIELD2 = ('w', 'Label 2')


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


class TestEChoiceCharFieldModel(models.Model):
    choice = EChoiceCharField(ETestCharChoices, default=ETestCharChoices.FIELD1)
