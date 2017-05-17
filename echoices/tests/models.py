from django.db import models

from echoices.enums import EChoice


class ETestCharChoices(EChoice):
    FIELD1 = ('v', 'Label 1')
    FIELD2 = ('w', 'Label 2')


class ETestStrChoices(EChoice):
    FIELD1 = ('value1', 'Label 1')
    FIELD2 = ('value2', 'Label 2')


class ETestIntChoices(EChoice):
    FIELD1 = (10, 'Label 1')
    FIELD2 = (20, 'Label 2')


class TestModelEChoiceChar(models.Model):
    choices_charfield = models.CharField(max_length=ETestCharChoices.max_value_length(),
                                         choices=ETestCharChoices.choices(),
                                         default=ETestCharChoices.FIELD1.value)


class TestModelEChoiceStr(models.Model):
    choices_charfield = models.CharField(max_length=ETestStrChoices.max_value_length(),
                                         choices=ETestStrChoices.choices(),
                                         default=ETestStrChoices.FIELD1.value)


class TestModelEChoiceInt(models.Model):
    choices_charfield = models.IntegerField(choices=ETestIntChoices.choices(), default=ETestIntChoices.FIELD1.value)
