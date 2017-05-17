# -*- coding: utf-8 -*-

from django.test import TestCase

from echoices.tests.models import ETestCharChoices, ETestStrChoices, ETestIntChoices
from echoices.tests.models import TestCharChoicesModel, TestStrChoicesModel, TestIntChoicesModel
from echoices.tests.models import TestEChoiceCharFieldModel


class EChoiceTest(TestCase):
    def test_echoices(self):
        self.assertEqual(ETestCharChoices.values(), ('v', 'w'))
        self.assertEqual(ETestCharChoices.max_value_length(), 1)
        self.assertEqual(ETestCharChoices.choices(), (('v', 'Label 1'), ('w', 'Label 2')))
        self.assertEqual(ETestCharChoices.FIELD1.label, 'Label 1')
        self.assertIs(ETestCharChoices.from_value('v'), ETestCharChoices.FIELD1)

        self.assertEqual(ETestStrChoices.values(), ('value1', 'value2'))
        self.assertEqual(ETestStrChoices.max_value_length(), 6)
        self.assertEqual(ETestStrChoices.choices(), (('value1', 'Label 1'), ('value2', 'Label 2')))
        self.assertEqual(ETestStrChoices.FIELD1.label, 'Label 1')
        self.assertIs(ETestStrChoices.from_value('value1'), ETestStrChoices.FIELD1)

        self.assertEqual(ETestIntChoices.values(), (10, 20))
        self.assertEqual(ETestIntChoices.choices(), ((10, 'Label 1'), (20, 'Label 2')))
        self.assertEqual(ETestIntChoices.FIELD1.label, 'Label 1')
        self.assertIs(ETestIntChoices.from_value(10), ETestIntChoices.FIELD1)

    def test_create_empty_instances(self):
        TestCharChoicesModel.objects.create()
        TestStrChoicesModel.objects.create()
        TestIntChoicesModel.objects.create()


# TODO: same tests for EOrderedChoice

# TODO: same tests for EAutoChoice

class ChoiceCharFieldTest(TestCase):
    def test_create_empty_instance(self):
        TestEChoiceCharFieldModel.objects.create()

    def test_create_instance(self):
        instance = TestEChoiceCharFieldModel.objects.create(choice=ETestCharChoices.FIELD1)
        choice = instance.choice
        self.assertIs(choice, ETestCharChoices.FIELD1)
        self.assertEqual(choice.value, 'v')
        self.assertEqual(choice.label, 'Label 1')
        self.assertEqual(instance._meta.fields[1].choices, ETestCharChoices.choices())
        self.assertIs(instance._meta.fields[1].default, ETestCharChoices.FIELD1.value)
        self.assertIs(instance._meta.fields[1].get_default(), ETestCharChoices.FIELD1)
        instance.delete()
