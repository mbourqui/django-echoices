from django.db import models

from echoices.enums import EChoice


class TestModelEChoiceChar(models.Model):
    class ETestChoices(EChoice):
        FIELD1 = ('a', 'Value 1')
        FIELD2 = ('b', 'Value 2')

    choices_charfield = models.CharField(max_length=1, choices=ETestChoices.choices(),
                                         default=ETestChoices.FIELD1.value)
