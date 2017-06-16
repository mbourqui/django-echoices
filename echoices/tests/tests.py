# -*- coding: utf-8 -*-

import warnings
from distutils.version import StrictVersion

from django import forms
from django import get_version as django_version
from django.contrib.auth.models import User
from django.db import models
from django.template import Context, Template
from django.test import TestCase

from echoices.fields import make_echoicefield
from echoices.tests.models import ETestAutoChoices
from echoices.tests.models import ETestBoolChoices
from echoices.tests.models import ETestCharChoices, ETestStrChoices
from echoices.tests.models import ETestCharOrderedChoices, ETestStrOrderedChoices, ETestIntOrderedChoices
from echoices.tests.models import ETestIntChoices, ETestFloatChoices
from echoices.tests.models import TestAutoChoicesModel
from echoices.tests.models import TestBoolChoicesDefaultModel
from echoices.tests.models import TestCharChoicesDefaultModel, TestStrChoicesDefaultModel, TestIntChoicesDefaultModel
from echoices.tests.models import TestCharChoicesModel, TestStrChoicesModel, TestIntChoicesModel
from echoices.tests.models import TestCharOrderedChoicesModel, TestStrOrderedChoicesModel, TestIntOrderedChoicesModel
from echoices.tests.models import TestEChoiceCharFieldEStrOrderedChoicesModel
from echoices.tests.models import TestEChoiceFieldDefaultEBoolChoicesModel
from echoices.tests.models import TestEChoiceFieldEFloatChoicesModel, TestEChoiceFieldDefaultEFloatChoicesModel
from echoices.tests.models import TestEChoiceFieldEIntChoicesModel, TestEChoiceFieldDefaultEIntChoicesModel
from echoices.tests.models import TestEChoiceFieldEStrChoicesModel, TestEChoiceFieldDefaultEStrChoicesModel
from echoices.tests.models import TestFloatChoicesModel, TestFloatChoicesDefaultModel
from echoices.tests.models import TestNamedEChoiceFieldEStrChoicesModel

warnings.simplefilter("always")


class EChoiceTest(TestCase):

    def test_name(self):
        self.assertEqual(ETestCharChoices.FIELD1.name, 'FIELD1')
        self.assertEqual(ETestStrChoices.FIELD1.name, 'FIELD1')
        self.assertEqual(ETestIntChoices.FIELD1.name, 'FIELD1')

    def test_label(self):
        self.assertEqual(ETestCharChoices.FIELD1.label, 'Label 1')
        self.assertEqual(ETestStrChoices.FIELD1.label, 'Label 1')
        self.assertEqual(ETestIntChoices.FIELD1.label, 'Label 1')

    def test_values(self):
        self.assertEqual(ETestCharChoices.values(), ('u', 'v'))
        self.assertEqual(ETestStrChoices.values(), ('value1', 'value2'))
        self.assertEqual(ETestIntChoices.values(), (10, 20))

    def test_maxvaluelength(self):
        self.assertEqual(ETestCharChoices.max_value_length(), 1)
        self.assertEqual(ETestStrChoices.max_value_length(), 6)

    def test_choices(self):
        self.assertEqual(ETestCharChoices.choices(), (('u', 'Label 1'), ('v', 'Label 2')))
        self.assertEqual(ETestStrChoices.choices(), (('value1', 'Label 1'), ('value2', 'Label 2')))
        self.assertEqual(ETestIntChoices.choices(), ((10, 'Label 1'), (20, 'Label 2')))

    def test_fromvalue(self):
        self.assertIs(ETestCharChoices.from_value('u'), ETestCharChoices.FIELD1)
        self.assertIs(ETestStrChoices.from_value('value1'), ETestStrChoices.FIELD1)
        self.assertIs(ETestIntChoices.from_value(10), ETestIntChoices.FIELD1)
        self.assertRaises(KeyError, ETestCharChoices.from_value, 'a')
        self.assertRaises(KeyError, ETestStrChoices.from_value, 'foobar')
        self.assertRaises(KeyError, ETestIntChoices.from_value, -66)

    def test_getitem(self):
        self.assertEqual(ETestCharChoices.__getitem__('u'), ETestCharChoices.FIELD1)
        self.assertIs(ETestCharChoices['u'], ETestCharChoices.FIELD1)
        self.assertRaises(KeyError, ETestCharChoices.__getitem__, 'a')

    def test_get(self):
        self.assertIs(ETestCharChoices.get('u'), ETestCharChoices.FIELD1)
        self.assertIsNone(ETestCharChoices.get('a'))
        self.assertTrue(ETestCharChoices.get('a', default=True))

    def test_call(self):
        self.assertIs(ETestCharChoices.FIELD1('name'), ETestCharChoices.FIELD1.name)
        self.assertEqual(ETestCharChoices.FIELD1('name'), 'FIELD1')
        self.assertIs(ETestCharChoices.FIELD1('value'), ETestCharChoices.FIELD1.value)
        self.assertEqual(ETestCharChoices.FIELD1('value'), 'u')
        self.assertIs(ETestCharChoices.FIELD1('label'), ETestCharChoices.FIELD1.label)
        self.assertEqual(ETestCharChoices.FIELD1('label'), 'Label 1')
        self.assertEqual(ETestCharChoices.FIELD1('__str__'), str(ETestCharChoices.FIELD1))

    def test_duplicate_value(self):
        def init_duplicated():
            from echoices.enums import EChoice

            class EDuplicatedChoices(EChoice):
                FIELD1 = ('u', 'Label 1')
                FIELD2 = ('u', 'Label 2')

        self.assertRaises(AttributeError, init_duplicated)

    def test_mixed_values(self):
        def init_mixed():
            from echoices.enums import EChoice

            class EMixedChoices(EChoice):
                FIELD1 = ('u', 'Label 1')
                FIELD2 = (2, 'Label 2')

        self.assertRaises(TypeError, init_mixed)

    def test_create_empty_instances(self):
        TestCharChoicesModel.objects.create()
        TestCharChoicesDefaultModel.objects.create()
        TestStrChoicesModel.objects.create()
        TestStrChoicesDefaultModel.objects.create()
        TestIntChoicesModel.objects.create()
        TestIntChoicesDefaultModel.objects.create()
        TestFloatChoicesModel.objects.create()
        TestFloatChoicesDefaultModel.objects.create()
        # NULL is not supported by BooleanField, but NullBooleanField does
        TestBoolChoicesDefaultModel.objects.create()


class EOrderedChoiceTest(TestCase):
    def test_label(self):
        self.assertEqual(ETestCharOrderedChoices.FIELD1.label, 'Label 1')
        self.assertEqual(ETestStrOrderedChoices.FIELD1.label, 'Label 1')
        self.assertEqual(ETestIntOrderedChoices.FIELD1.label, 'Label 1')

    def test_values(self):
        self.assertEqual(ETestCharOrderedChoices.values(), ('w', 'u', 'v'))
        self.assertEqual(ETestStrOrderedChoices.values(), ('value3', 'value1', 'value2'))
        self.assertEqual(ETestIntOrderedChoices.values(), (30, 10, 20))

    def test_maxvaluelength(self):
        self.assertEqual(ETestCharOrderedChoices.max_value_length(), 1)
        self.assertEqual(ETestStrOrderedChoices.max_value_length(), 6)

    def test_fromvalue(self):
        self.assertIs(ETestCharOrderedChoices.from_value('v'), ETestCharOrderedChoices.FIELD3)
        self.assertIs(ETestStrOrderedChoices.from_value('value2'), ETestStrOrderedChoices.FIELD3)
        self.assertIs(ETestIntOrderedChoices.from_value(20), ETestIntOrderedChoices.FIELD3)

    def test_choices(self):
        self.assertEqual(ETestCharOrderedChoices.choices(), (('w', 'Label 1'), ('u', 'Label 2'), ('v', 'Label 3')))
        self.assertEqual(ETestCharOrderedChoices.choices('sorted'),
                         (('u', 'Label 2'), ('v', 'Label 3'), ('w', 'Label 1')))
        self.assertEqual(ETestCharOrderedChoices.choices('reverse'),
                         (('w', 'Label 1'), ('v', 'Label 3'), ('u', 'Label 2')))
        self.assertEqual(ETestCharOrderedChoices.choices('natural'), ETestCharOrderedChoices.choices())
        self.assertRaises(AssertionError, ETestCharOrderedChoices.choices, 'foobar')

        self.assertEqual(ETestStrOrderedChoices.choices(),
                         (('value3', 'Label 1'), ('value1', 'Label 2'), ('value2', 'Label 3')))
        self.assertEqual(ETestStrOrderedChoices.choices('sorted'),
                         (('value1', 'Label 2'), ('value2', 'Label 3'), ('value3', 'Label 1')))
        self.assertEqual(ETestStrOrderedChoices.choices('reverse'),
                         (('value3', 'Label 1'), ('value2', 'Label 3'), ('value1', 'Label 2')))
        self.assertEqual(ETestStrOrderedChoices.choices('natural'),
                         (('value3', 'Label 1'), ('value1', 'Label 2'), ('value2', 'Label 3')))
        self.assertEqual(ETestStrOrderedChoices.choices('natural'), ETestStrOrderedChoices.choices())
        self.assertRaises(AssertionError, ETestCharOrderedChoices.choices, 'foobar')

        self.assertEqual(ETestIntOrderedChoices.choices(), ((30, 'Label 1'), (10, 'Label 2'), (20, 'Label 3')))
        self.assertEqual(ETestIntOrderedChoices.choices('sorted'), ((10, 'Label 2'), (20, 'Label 3'), (30, 'Label 1')))
        self.assertEqual(ETestIntOrderedChoices.choices('reverse'), ((30, 'Label 1'), (20, 'Label 3'), (10, 'Label 2')))
        self.assertEqual(ETestIntOrderedChoices.choices('natural'), ((30, 'Label 1'), (10, 'Label 2'), (20, 'Label 3')))
        self.assertEqual(ETestIntOrderedChoices.choices('natural'), ETestIntOrderedChoices.choices())
        self.assertRaises(AssertionError, ETestIntOrderedChoices.choices, 'foobar')

    def test_getitem(self):
        self.assertEqual(ETestCharOrderedChoices.__getitem__('u'), ETestCharOrderedChoices.FIELD2)
        self.assertIs(ETestCharOrderedChoices['u'], ETestCharOrderedChoices.FIELD2)
        self.assertRaises(KeyError, ETestCharOrderedChoices.__getitem__, 'a')

    def test_get(self):
        self.assertIs(ETestCharOrderedChoices.get('u'), ETestCharOrderedChoices.FIELD2)
        self.assertIsNone(ETestCharOrderedChoices.get('a'))
        self.assertTrue(ETestCharOrderedChoices.get('a', default=True))

    def test_ordering(self):
        self.assertTrue(ETestCharOrderedChoices.FIELD1 > ETestCharOrderedChoices.FIELD2)
        self.assertTrue(ETestStrOrderedChoices.FIELD1 > ETestStrOrderedChoices.FIELD2)
        self.assertTrue(ETestIntOrderedChoices.FIELD1 > ETestIntOrderedChoices.FIELD2)

    def test_create_empty_instances(self):
        TestCharOrderedChoicesModel.objects.create()
        TestStrOrderedChoicesModel.objects.create()
        TestIntOrderedChoicesModel.objects.create()


class EAutoChoiceTest(TestCase):
    def test_label(self):
        self.assertEqual(ETestAutoChoices.FIELD1.label, 'Label 1')

    def test_values(self):
        self.assertEqual(ETestAutoChoices.values(), (1, 2, 3))

    def test_fromvalue(self):
        self.assertIs(ETestAutoChoices[2], ETestAutoChoices.FIELD2)

    def test_get(self):
        self.assertIs(ETestAutoChoices.get(2), ETestAutoChoices.FIELD2)
        self.assertIsNone(ETestAutoChoices.get(4))
        self.assertTrue(ETestAutoChoices.get(4, default=True))

    def test_choices(self):
        self.assertEqual(ETestAutoChoices.choices(), ((1, 'Label 1'), (2, 'Label 2'), (3, 'Label 3')))
        self.assertEqual(ETestAutoChoices.choices('sorted'), ((1, 'Label 1'), (2, 'Label 2'), (3, 'Label 3')))
        self.assertEqual(ETestAutoChoices.choices('reverse'), ((3, 'Label 3'), (2, 'Label 2'), (1, 'Label 1')))
        self.assertEqual(ETestAutoChoices.choices('natural'), ((1, 'Label 1'), (2, 'Label 2'), (3, 'Label 3')))
        self.assertEqual(ETestAutoChoices.choices('natural'), ETestAutoChoices.choices())
        self.assertRaises(AssertionError, ETestAutoChoices.choices, 'foobar')

    def test_ordering(self):
        self.assertTrue(ETestAutoChoices.FIELD1 < ETestAutoChoices.FIELD2)
        self.assertTrue(ETestAutoChoices.FIELD2 < ETestAutoChoices.FIELD3)

    def test_create_empty_instances(self):
        TestAutoChoicesModel.objects.create()


class ChoiceCharFieldTest(TestCase):
    def test_create_empty_instance(self):
        TestEChoiceFieldEStrChoicesModel.objects.create()
        TestNamedEChoiceFieldEStrChoicesModel.objects.create()
        TestEChoiceFieldDefaultEStrChoicesModel.objects.create()

    def test_create_instance(self):
        instance = TestEChoiceFieldEStrChoicesModel.objects.create(choice=ETestStrChoices.FIELD1)
        choice = instance.choice
        self.assertIsInstance(choice, ETestStrChoices)
        self.assertIs(choice, ETestStrChoices.FIELD1)
        self.assertEqual(choice.value, 'value1')
        self.assertEqual(choice.label, 'Label 1')
        if StrictVersion(django_version()) < StrictVersion('1.9.0'):
            self.assertEqual(instance._meta.fields[1].__class__.__name__, 'EChoiceField')
        else:
            self.assertEqual(instance._meta.fields[1].__class__.__name__, 'ETestStrChoicesField')
        self.assertEqual(instance._meta.fields[1].choices, ETestStrChoices.choices())
        self.assertIs(instance._meta.fields[1].default, models.fields.NOT_PROVIDED)
        self.assertEqual(instance._meta.fields[1].get_default(), '')
        instance.delete()

    def test_create_instance_named(self):
        instance = TestNamedEChoiceFieldEStrChoicesModel.objects.create(choice=ETestStrChoices.FIELD1)
        choice = instance.choice
        self.assertIsInstance(choice, ETestStrChoices)
        self.assertIs(choice, ETestStrChoices.FIELD1)
        self.assertEqual(choice.value, 'value1')
        self.assertEqual(choice.label, 'Label 1')
        if StrictVersion(django_version()) < StrictVersion('1.9.0'):
            self.assertEqual(instance._meta.fields[1].__class__.__name__, 'EChoiceField')
        else:
            self.assertEqual(instance._meta.fields[1].__class__.__name__, 'MyEnumFieldName')
        self.assertEqual(instance._meta.fields[1].choices, ETestStrChoices.choices())
        self.assertIs(instance._meta.fields[1].default, models.fields.NOT_PROVIDED)
        self.assertEqual(instance._meta.fields[1].get_default(), '')
        instance.delete()

    def test_create_instance_default(self):
        instance = TestEChoiceFieldDefaultEStrChoicesModel.objects.create(choice=ETestStrChoices.FIELD1)
        choice = instance.choice
        self.assertIsInstance(choice, ETestStrChoices)
        self.assertIs(choice, ETestStrChoices.FIELD1)
        self.assertEqual(choice.value, 'value1')
        self.assertEqual(choice.label, 'Label 1')
        if StrictVersion(django_version()) < StrictVersion('1.9.0'):
            self.assertEqual(instance._meta.fields[1].__class__.__name__, 'EChoiceField')
        else:
            self.assertEqual(instance._meta.fields[1].__class__.__name__, 'ETestStrChoicesField')
        self.assertEqual(instance._meta.fields[1].choices, ETestStrChoices.choices())
        self.assertIs(instance._meta.fields[1].default, ETestStrChoices.FIELD1.value)
        self.assertIs(instance._meta.fields[1].get_default(), ETestStrChoices.FIELD1)
        instance.delete()

    def test_update(self):
        instance = TestEChoiceFieldEStrChoicesModel.objects.create(choice=ETestStrChoices.FIELD1)
        choice = instance.choice
        self.assertIsInstance(choice, ETestStrChoices)
        self.assertIs(choice, ETestStrChoices.FIELD1)
        instance.choice = ETestStrChoices.FIELD2
        instance.save()
        instance = TestEChoiceFieldEStrChoicesModel.objects.get(pk=1)
        choice = instance.choice
        self.assertIsInstance(choice, ETestStrChoices)
        self.assertIs(choice, ETestStrChoices.FIELD2)
        instance.delete()


class ChoiceIntFieldTest(TestCase):
    def test_create_empty_instance(self):
        TestEChoiceFieldEIntChoicesModel.objects.create()
        TestEChoiceFieldDefaultEIntChoicesModel.objects.create()

    def test_create_instance(self):
        instance = TestEChoiceFieldEIntChoicesModel.objects.create(choice=ETestIntChoices.FIELD1)
        choice = instance.choice
        self.assertIsInstance(choice, ETestIntChoices)
        self.assertIs(choice, ETestIntChoices.FIELD1)
        self.assertEqual(choice.value, 10)
        self.assertEqual(choice.label, 'Label 1')
        if StrictVersion(django_version()) < StrictVersion('1.9.0'):
            self.assertEqual(instance._meta.fields[1].__class__.__name__, 'EChoiceField')
        else:
            self.assertEqual(instance._meta.fields[1].__class__.__name__, 'ETestIntChoicesField')
        self.assertEqual(instance._meta.fields[1].choices, ETestIntChoices.choices())
        self.assertIs(instance._meta.fields[1].default, models.fields.NOT_PROVIDED)
        self.assertIsNone(instance._meta.fields[1].get_default())
        instance.delete()

    def test_create_instance_default(self):
        instance = TestEChoiceFieldDefaultEIntChoicesModel.objects.create(choice=ETestIntChoices.FIELD1)
        choice = instance.choice
        self.assertIsInstance(choice, ETestIntChoices)
        self.assertIs(choice, ETestIntChoices.FIELD1)
        self.assertEqual(choice.value, 10)
        self.assertEqual(choice.label, 'Label 1')
        if StrictVersion(django_version()) < StrictVersion('1.9.0'):
            self.assertEqual(instance._meta.fields[1].__class__.__name__, 'EChoiceField')
        else:
            self.assertEqual(instance._meta.fields[1].__class__.__name__, 'ETestIntChoicesField')
        self.assertEqual(instance._meta.fields[1].choices, ETestIntChoices.choices())
        self.assertIs(instance._meta.fields[1].default, ETestIntChoices.FIELD1.value)
        self.assertIs(instance._meta.fields[1].get_default(), ETestIntChoices.FIELD1)
        instance.delete()


class ChoiceFloatFieldTest(TestCase):
    def test_create_empty_instance(self):
        TestEChoiceFieldEFloatChoicesModel.objects.create()
        TestEChoiceFieldDefaultEFloatChoicesModel.objects.create()

    def test_create_instance(self):
        instance = TestEChoiceFieldEFloatChoicesModel.objects.create(choice=ETestFloatChoices.FIELD1)
        choice = instance.choice
        self.assertIsInstance(choice, ETestFloatChoices)
        self.assertIs(choice, ETestFloatChoices.FIELD1)
        self.assertEqual(choice.value, 1.0)
        self.assertEqual(choice.label, 'Label 1')
        if StrictVersion(django_version()) < StrictVersion('1.9.0'):
            self.assertEqual(instance._meta.fields[1].__class__.__name__, 'EChoiceField')
        else:
            self.assertEqual(instance._meta.fields[1].__class__.__name__, 'ETestFloatChoicesField')
        self.assertEqual(instance._meta.fields[1].choices, ETestFloatChoices.choices())
        self.assertIs(instance._meta.fields[1].default, models.fields.NOT_PROVIDED)
        self.assertIs(instance._meta.fields[1].get_default(), None)
        instance.delete()

    def test_create_instance_default(self):
        instance = TestEChoiceFieldDefaultEFloatChoicesModel.objects.create(choice=ETestFloatChoices.FIELD1)
        choice = instance.choice
        self.assertIsInstance(choice, ETestFloatChoices)
        self.assertIs(choice, ETestFloatChoices.FIELD1)
        self.assertEqual(choice.value, 1.0)
        self.assertEqual(choice.label, 'Label 1')
        if StrictVersion(django_version()) < StrictVersion('1.9.0'):
            self.assertEqual(instance._meta.fields[1].__class__.__name__, 'EChoiceField')
        else:
            self.assertEqual(instance._meta.fields[1].__class__.__name__, 'ETestFloatChoicesField')
        self.assertEqual(instance._meta.fields[1].choices, ETestFloatChoices.choices())
        self.assertIs(instance._meta.fields[1].default, ETestFloatChoices.FIELD1.value)
        self.assertIs(instance._meta.fields[1].get_default(), ETestFloatChoices.FIELD1)
        instance.delete()


class ChoiceBoolFieldTest(TestCase):
    def test_create_empty_instance(self):
        TestEChoiceFieldDefaultEBoolChoicesModel.objects.create()

    def test_create_instance(self):
        instance = TestEChoiceFieldDefaultEBoolChoicesModel.objects.create(choice=ETestBoolChoices.FIELD1)
        choice = instance.choice
        self.assertIsInstance(choice, ETestBoolChoices)
        self.assertIs(choice, ETestBoolChoices.FIELD1)
        self.assertTrue(choice.value)
        self.assertEqual(choice.label, 'Label 1')
        if StrictVersion(django_version()) < StrictVersion('1.9.0'):
            self.assertEqual(instance._meta.fields[1].__class__.__name__, 'EChoiceField')
        else:
            self.assertEqual(instance._meta.fields[1].__class__.__name__, 'ETestBoolChoicesField')
        self.assertEqual(instance._meta.fields[1].choices, ETestBoolChoices.choices())
        self.assertTrue(instance._meta.fields[1].default)
        self.assertIs(instance._meta.fields[1].get_default(), ETestBoolChoices.FIELD1)
        instance.delete()


class ChoiceComplexFieldTest(TestCase):
    def test_create_empty_instance(self):
        def create():
            from echoices.enums import EChoice

            class ETestComplexChoices(EChoice):
                FIELD1 = (1 + 1j, 'Label 1')
                FIELD2 = (2 + 1j, 'Label 2')

            from django.db import models
            class TestEChoiceFieldEComplexChoicesModel(models.Model):
                from echoices.fields import make_echoicefield
                choice = make_echoicefield(ETestComplexChoices, default=ETestComplexChoices.FIELD1)

        self.assertRaises(NotImplementedError, create)


class ChoiceMixedDefaultFieldTest(TestCase):
    def test_create_empty_instance(self):
        def create():
            from django.db import models

            class TestEChoiceFieldMixedDefaultModel(models.Model):
                from echoices.fields import make_echoicefield
                choice = make_echoicefield(ETestCharChoices, default=ETestIntChoices.FIELD1)

        self.assertRaises(AttributeError, create)


class OrderedChoiceCharFieldTest(TestCase):
    def test_create_empty_instance(self):
        TestEChoiceCharFieldEStrOrderedChoicesModel.objects.create()

    def test_create_instance(self):
        instance = TestEChoiceCharFieldEStrOrderedChoicesModel.objects.create(choice=ETestStrOrderedChoices.FIELD1)
        choice = instance.choice
        self.assertIs(choice, ETestStrOrderedChoices.FIELD1)
        self.assertEqual(choice.value, 'value3')
        self.assertEqual(choice.label, 'Label 1')
        if StrictVersion(django_version()) < StrictVersion('1.9.0'):
            self.assertEqual(instance._meta.fields[1].__class__.__name__, 'EChoiceField')
        else:
            self.assertEqual(instance._meta.fields[1].__class__.__name__, 'ETestStrOrderedChoicesField')
        self.assertEqual(instance._meta.fields[1].choices, ETestStrOrderedChoices.choices())
        self.assertIs(instance._meta.fields[1].default, ETestStrOrderedChoices.FIELD1.value)
        self.assertIs(instance._meta.fields[1].get_default(), ETestStrOrderedChoices.FIELD1)
        instance.delete()


class TemplateTest(TestCase):
    def test_simple(self):
        tpl = Template("""
<div class="echoices">
{{ echoices }}
</div>
<div class="echoices.FIELD1">
{{ echoices.FIELD1 }}
</div>
<div class="echoices.FIELD1.value">
{{ echoices.FIELD1.value }}
</div>
<div class="echoices.FIELD1.label">
{{ echoices.FIELD1.label }}
</div>
""")
        ctx = Context(dict(echoices=ETestCharChoices))
        rendered = tpl.render(ctx)
        rendered = str(rendered.strip())
        self.assertIn(ETestCharChoices.FIELD1.name, rendered)
        self.assertIn(ETestCharChoices.FIELD1.value, rendered)
        self.assertIn(ETestCharChoices.FIELD1.label, rendered)

    def test_iteration(self):
        tpl = Template("""
{% for e in echoices %}
    <div class="e">
    {{ e }}
    </div>
    <div class="e.value">
    {{ e.value }}
    </div>
    <div class="e.label">
    {{ e.label }}
    </div>
{% endfor %}
""")
        ctx = Context(dict(echoices=ETestCharChoices))
        rendered = tpl.render(ctx)
        rendered = str(rendered.strip())
        for e in ETestCharChoices:
            self.assertIn(e.name, rendered)
            self.assertIn(e.value, rendered)
            self.assertIn(e.label, rendered)


class AdminTest(TestCase):
    def setUp(self):
        User.objects.create_superuser('admin', 'admin@tests.com', 'admin')
        self.client.login(username='admin', password='admin')

    def test_admin(self):
        self.assertEqual(self.client.get('/admin/').status_code, 200)
        self.assertEqual(self.client.get('/admin/tests/').status_code, 200)

    def test_admin_testcharchoicesmodel_list(self):
        TestCharChoicesModel.objects.create(choice=ETestCharChoices.FIELD1.value)
        for param in ['', '?choice__exact=u']:
            response = self.client.get('/admin/tests/testcharchoicesmodel/' + param)
            self.assertEqual(response.status_code, 200)
            self.assertInHTML('<p class="paginator">1 test char choices model</p>', response.rendered_content)

    def test_admin_testcharchoicesmodel_change(self):
        TestCharChoicesModel.objects.create(choice=ETestCharChoices.FIELD1.value)
        response = self.client.get('/admin/tests/testcharchoicesmodel/1/change/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertInHTML('<option value="u" selected="selected">Label 1</option>', response.rendered_content)


class FormTest(TestCase):
    def test_form(self):
        # SEE: https://docs.djangoproject.com/en/stable/ref/forms/api/#using-forms-to-validate-data
        class SimpleForm(forms.Form):
            choice = make_echoicefield(ETestCharChoices).formfield()

        f = SimpleForm(dict(choice=ETestCharChoices.FIELD1))
        self.assertTrue(f.is_valid())

        f = SimpleForm(dict(choice=ETestCharChoices.FIELD1.value))
        self.assertTrue(f.is_valid())

        f = SimpleForm(dict(choice=''))
        self.assertFalse(f.is_valid())

    def test_modelform_testcharchoicesmodel(self):
        from django.forms import ModelForm

        class TestCharChoicesModelForm(ModelForm):
            class Meta:
                model = TestCharChoicesModel
                fields = '__all__'

        f = TestCharChoicesModelForm(dict(choice=ETestCharChoices.FIELD1.value))
        self.assertTrue(f.save())

    def test_modelform_testechoicefieldestrchoicesmodel(self):
        from django.forms import ModelForm

        class TestEChoiceFieldEStrChoicesModelForm(ModelForm):
            class Meta:
                model = TestEChoiceFieldEStrChoicesModel
                fields = '__all__'

        f = TestEChoiceFieldEStrChoicesModelForm(dict(choice=ETestStrChoices.FIELD1))
        self.assertTrue(f.save())
        instance = TestEChoiceFieldEStrChoicesModel.objects.get(pk=1)
        f = TestEChoiceFieldEStrChoicesModelForm(instance=instance)
        self.assertInHTML('<option value="value1" selected="selected">Label 1</option>', str(f))
