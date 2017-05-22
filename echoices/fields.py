from distutils.version import StrictVersion

from django import get_version as django_version
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .enums import EChoice


def make_echoicefield(echoices, *args, **kwargs):
    """
    Construct a derived `models.Field` specific to the type of the `EChoice` values.
    
    Parameters
    ----------
    echoices
    args
    kwargs

    Returns
    -------
    EChoiceField
        For Django>=1.9, the exact name of the returned Field is based on the name of the `echoices` with a suffixed
        'Field'. For older Django, the returned name of the class is `EChoiceField`.

    """
    assert issubclass(echoices, EChoice)
    value_type = echoices.__getvaluetype__()
    if value_type is str:
        cls_ = models.CharField
    elif value_type is int:
        cls_ = models.IntegerField
    elif value_type is float:
        cls_ = models.FloatField
    elif value_type is bool:
        cls_ = models.BooleanField
    else:
        raise NotImplementedError("Please open an issue if you wish your value type to be supported: "
                                  "https://github.com/mbourqui/django-echoices/issues/new")
    d = dict(cls_.__dict__)
    d.update(dict(EChoiceField.__dict__))
    if StrictVersion(django_version()) >= StrictVersion('1.9.0'):
        cls_name = "{}Field".format(echoices.__name__)
    else:
        cls_name = EChoiceField.__name__
    return type(cls_name, (cls_,), d)(echoices, *args, **kwargs)


class EChoiceField(models.Field):
    """
    Specialized field for single choices. Not intended to be called directly but instantiated via
    `make_echoicefield()`.
    
    Internally uses a derived `models.Field`.
    In the case of a `models.CharField`, 'max_length' is deduced directly from the `echoices`.
    
    Parameters
    ----------
    echoices : sublcass of EChoice
        The choices this field supports.
    * args
        Are passed to the derived models.Field
    * kwargs
        Are passed to the derived models.Field
    
    """
    description = _("A derived Field supporting enumerated choices")

    def __init__(self, echoices, *args, **kwargs):
        self.echoices = echoices
        kwargs['choices'] = self.echoices.choices()
        default = kwargs.get('default')
        if default:
            kwargs['default'] = default.value
        # Parameters specific to some fields
        if issubclass(self.__class__, models.CharField):
            kwargs['max_length'] = echoices.max_value_length()
        super(self.__class__, self).__init__(*args, **kwargs)

    def get_default(self):
        default = super(self.__class__, self).get_default()
        if self.has_default():
            return self.echoices[default]
        return default

    def from_db_value(self, value, *args):
        if value is None:
            return value
        return self.echoices[value]

    def to_python(self, value):
        if isinstance(value, self.echoices) or value is None:
            return value
        return self.echoices[value]

    def get_prep_value(self, value):
        if value:
            return value.value
        return value

    def deconstruct(self):
        name, path, args, kwargs = super(self.__class__, self).deconstruct()
        # Drop the parameters set by our field
        del kwargs['choices']
        if issubclass(self.__class__, models.CharField):
            del kwargs['max_length']
        # Set the parameters in our non-trivial formats
        kwargs['echoices'] = self.echoices
        if self.has_default():
            kwargs['default'] = self.get_default()
        return name, path, args, kwargs

# TODO: MultipleEChoiceField
