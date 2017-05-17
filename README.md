[![Python](https://img.shields.io/badge/Python-3.4,3.5,3.6-blue.svg?style=flat-square)](/)
[![Django](https://img.shields.io/badge/Django-1.8,1.9,1.10-blue.svg?style=flat-square)](/)
[![License](https://img.shields.io/badge/License-GPLv3-blue.svg?style=flat-square)](/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/django_echoices.svg?style=flat-square)](https://pypi.python.org/pypi/django-echoices)
[![Build Status](https://travis-ci.org/mbourqui/django-echoices.svg?branch=master)](https://travis-ci.org/mbourqui/django-echoices)
[![Coverage Status](https://coveralls.io/repos/github/mbourqui/django-echoices/badge.svg?branch=master)](https://coveralls.io/github/mbourqui/django-echoices?branch=master)


# Django-EChoices, choices for Django model fields as enumeration


## Features

### Specialized enum types

* `enums.EChoice` is the base enum type. Each enum element is a tuple `(value, label)`, where <cite>[t]he first element
in each tuple is the actual value to be set on the model, and the second element is the human-readable name</cite>&nbsp;
<sup>[doc](https://docs.djangoproject.com/en/1.11/ref/models/fields/#choices)</sup>. Values **must** be unique. Can be
derived for further customization.
* `enums.EOrderedChoice` supports ordering of elements. `EOrderedChoice.choices()` takes an extra optional argument,
`order`, which supports three values: 'sorted', 'reverse' or 'natural' (default). If `sorted`, the choices are ordered
according to their value. If `reverse`, the choices are ordered according to their value as if each comparison were
reversed. If `natural`, the order is the one used when instantiating the enumeration.
* `enums.EAutoChoice`, generates auto-incremented numeric values. It's then used like
    ```
    class EStates(EAutoChoice):
        # format is: label -> str
        CREATED = 'Created'
        SUBMITTED = 'Submitted'
    ```

### Specialized model fields

* `fields.EChoiceCharField` deals directly with the enum instances instead of their value. Internal representation is
using CharField, thus only works for textual labels.
* `fields.EChoiceIntegerField`, same as `EChoiceCharField` but using IntegerField, thus only works for numeric labels.
[**Not yet implemented**](#1).
* `fields.MultipleEChoiceField`, similar to previous fields, but supports multiple values to be selected.
[**Not yet implemented**](#3).


## Requirements

* Django >= 1.8.18


## Installation

1. Run `pip install django-echoices`


## Usage
First, define your choices enumeration (in your `models.py` for example):
```
from enum import unique
from echoices.enums import EChoice

@unique
class EStates(EChoice):
    # format is: (value -> char or str or int, label -> str)
    CREATED = ('c', 'Created')
    SUBMITTED = ('s', 'Submitted')

```

Then, either use a regular model field:
```
from django.db import models

class MyModel(models.Model):
    state = models.CharField(max_length=EStates.max_value_length(),
                             choices=EStates.choices(),
                             default=EStates.CREATED.value)
```
**Note**: If your value is an `int`, you can use `models.IntegerField` instead.

or a specialized field:
```
from django.db import models
from echoices.fields import EChoiceCharField

class MyModel(models.Model):
    # `max_length` is set automatically
    state = EChoiceCharField(EStates, default=EStates.CREATED)
```

### Derivation
```
from echoices.enums import EChoice

class EMyChoice(EChoice):
    """
    You can add your own fields to the `value` and `label` ones. To do so, you have to override the
    __init__() and your signature must look like: `self, value, label, *args` where you replace `*args`
    with your own positional arguments, as you would do when defining a custom Enum.
    Do *not* call the super().__init__(), as `value` and `label` are already set by `EChoice`.

    As when dealing with a derived Enum, you can also add your own methods.

    """

    MY_CHOICE = (1, 'First choice', 'my value')

    def __init__(self, value, label, my_arg):
        self.my_arg = my_arg
        # Note: super().__init__() shall *not* be called!

```
