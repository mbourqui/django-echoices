[![Python](https://img.shields.io/badge/Python-3.4,3.5,3.6-blue.svg?style=flat-square)](/)
[![Django](https://img.shields.io/badge/Django-1.9,1.10,1.11-blue.svg?style=flat-square)](/)
[![License](https://img.shields.io/badge/License-GPLv3-blue.svg?style=flat-square)](/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/django_echoices.svg?style=flat-square)](https://pypi.python.org/pypi/django-echoices)
[![Build Status](https://travis-ci.org/mbourqui/django-echoices.svg?branch=master)](https://travis-ci.org/mbourqui/django-echoices)
[![Coverage Status](https://coveralls.io/repos/github/mbourqui/django-echoices/badge.svg?branch=master)](https://coveralls.io/github/mbourqui/django-echoices?branch=master)


# Django-EChoices, choices for Django model fields as enumeration


## Features

* Specialized [enum types](#enum)
* Specialized [model fields](#modelfield)
* Accessible in [templates](#templages)


## Requirements

* Django >= 1.9.13


## Installation

1. Run `pip install django-echoices`


## Usage

### Enumeration
First, define your choices enumeration (in your `models.py` for example):
```
from echoices.enums import EChoice

class EStates(EChoice):
    # format is: (value -> char or str or int, label -> str)
    CREATED = ('c', 'Created')
    SUBMITTED = ('s', 'Submitted')

```

### Model field
#### Regular model field
Then, either use a regular model field:
```
from django.db import models

class MyModel(models.Model):
    state = models.CharField(max_length=EStates.max_value_length(),
                             choices=EStates.choices(),
                             default=EStates.CREATED.value)
```

**Note**: If your value is an `int`, you can use `models.IntegerField` instead.

#### Specialized field
You can also use specialized field. Using such a field, you will then only handle `Echoice` instances.
```
from django.db import models
from echoices.fields import make_echoicefield

class MyModel(models.Model):
    # `max_length` is set automatically
    state = make_echoicefield(EStates, default=EStates.CREATED)
```

**Note**: `MyModel.state` will be `Estates` instance stored in a `EStatesField` field. See [documentation](#modelfield)
for more details.

**WARNING**: requires special handling of migrations. Read more in the [doc](#migrations).

### Derivation

You can add your own fields to the `value` and `label` ones. To do so, you have to override the __init__() and your
signature must look like: `self, value, label, *args` where you replace `*args` with your own positional arguments, as
you would do when defining a custom Enum. Do *not* call the super().__init__(), as `value` and `label` are already set
internally by `EChoice`.

As when dealing with a derived Enum, you can also add your own methods.
```
from echoices.enums import EChoice

class EMyChoices(EChoice):
    """Another variant of EChoice with additionnal content"""

    MY_CHOICE = (1, 'First choice', 'my additional value')

    def __init__(self, value, label, my_arg):
        self.my_arg = my_arg
        # Note: super().__init__() shall *not* be called!

    def show_myarg(self):
        """Used as: EMyChoices.MY_CHOICE.show_myarg()"""
        print(self.my_arg)

    @classmethod
    def show_all(cls):
        """Used as: EMyChoices.show_all()"""
        print(", ".join([e.my_arg for e in list(cls)]))
```

### In templates
Assume a `Context(dict(estates=myapp.models.EStates))` is provided to the following templates.

* Fields of the `EChoice` can be accessed in the templates as:
    ```
    {{ estates.CREATED.value }}
    {{ estates.CREATED.label }}
    ```

* `EChoice` can also be enumerated:
    ```
    {% for state in estates %}
        {{ state.value }}
        {{ state.label }}
    {% endfor %}
    ```

## Short documentation

### <a name="enum"></a>Specialized enum types

#### `enums.EChoice`
Base enum type. Each enum element is a tuple `(value, label)`, where <cite>[t]he first element
in each tuple is the actual value to be set on the model, and the second element is the human-readable name</cite>&nbsp;
<sup>[doc](https://docs.djangoproject.com/en/1.11/ref/models/fields/#choices)</sup>. Values **must** be unique. Can be
derived for further customization.

#### `enums.EOrderedChoice`
Supports ordering of elements. `EOrderedChoice.choices()` takes an extra optional argument,
`order`, which supports three values: 'sorted', 'reverse' or 'natural' (default). If `sorted`, the choices are ordered
according to their value. If `reverse`, the choices are ordered according to their value as if each comparison were
reversed. If `natural`, the order is the one used when instantiating the enumeration.

#### `enums.EAutoChoice`
Generates auto-incremented numeric values. It's then used like:
```
from echoices.enums import EAutoChoice

class EStates(EAutoChoice):
    # format is: label -> str
    CREATED = 'Created'
    SUBMITTED = 'Submitted'
```

#### API
##### Overriden EnumMeta methods
* `EChoice.__getitem__()`, such that you can retrieve an `EChoice` instance using `EChoice['my_value']`

##### Additional classmethods
* `choices()` generates the choices as expected by a Django model field
* `max_value_length()` returns the max length for the Django model field, if the values are strings
* `values()` returns a list of all the values
* `get(value, default=None)` returns the EChoice instance having that value, else returns the default

### <a name="modelfield"></a>Specialized model fields

#### `fields.EChoiceField` via `fields.make_echoicefield()`
Deal directly with the enum instances instead of their DB storage value. The specialized field will be derived from a
`models.Field` subclass, the internal representation is deduced from the value type. So for example if the values are
strings, then the the `EChoiceField` will subclass `models.CharField`; and if the values are integers then it will be
`models.IntegerField`. Actually supports `str`, `int`, `float` and (non-null) `bool` as enum values.

`make_echoicefield()` will return an instance of `EChoiceField` which subclasses a field type from `models.CharField`.
The exact name of the field type will be `MyEnumNameField` in Django >= 1.9, note the suffixed 'Field'. For earlier
versions of Django, it will be `EChoiceField`.

Thus, `MyModel.my_echoice_field` will be an `EChoice` instance stored in an `EChoiceField` field.

##### <a name="migrations"></a>Migrations
Since the field is generated with the help of a factory function, it does not exist as is as a field class in
`echoices.fields`. But, when generating a migration file, Django will set the class of the field as the resulting class
from `make_echoicefield()`, which does not exist in `echoices.fields`. This will cause the Django server to crash, as
an `AttributeError: module 'echoices.fields' has no attribute 'MyEnumNameField'` exception will be raised.

To prevent this, you have to edit the migration file and replace the instantiation of the non-existing class with a call
to `make_echoicefield()`, with the same parameters as when defining the field in your model.

For example, assume you have the following model defined in `models.py`:
```
from django.db import models
from echoices.fields import make_echoicefield

class MyModel(models.Model):
    state = make_echoicefield(EStates, default=EStates.CREATED)
```

Then you would replace the generated field instantiation statement in `migrations/0001_initial.py`
```
migrations.CreateModel(
    name='MyModel',
    fields=[
        # Replace the statement below
        ('state', echoices.fields.EStatesField(
                        echoices=app.models.EStates,
                        default=app.models.EStates(1))
        ),
    ],
```

with
```
        ('state', echoices.fields.make_echoicefield(
                        echoices=app.models.EStates,
                        default=app.models.EStates.CREATED)
        ),
```

#### `fields.MultipleEChoiceField`
Similar to previous fields, but supports multiple values to be selected.
[**Not yet implemented**](#3).

### <a name="templates"></a>Usage in templates
Assume a `Context(dict(estates=myapp.models.EStates))` is provided to the following templates.

* Fields of the `EChoice` can be accessed in the templates as:
    ```
    {{ estates.CREATED.value }}
    {{ estates.CREATED.label }}
    ```

* `EChoice` can also be enumerated:
    ```
    {% for state in estates %}
        {{ state.value }}
        {{ state.label }}
    {% endfor %}
    ```
