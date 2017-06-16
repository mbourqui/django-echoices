import warnings
from distutils.version import StrictVersion

from django import get_version as django_version
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .enums import EChoice
from .forms import TypedEChoiceField


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
            if not isinstance(default, self.echoices):
                raise AttributeError(
                    "Illegal default value: {}. Must be an instance of {}".format(default, self.echoices))
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
        if isinstance(value, self.echoices):
            return value.value
        assert value in self.echoices.values() or value in ['', None]
        return value

    def formfield(self, **kwargs):
        defaults = {'choices_form_class': TypedEChoiceField}
        defaults.update(kwargs)
        return super(self.__class__, self).formfield(**defaults)

    def validate(self, value, model_instance):
        """
        Validates value and throws ValidationError. Subclasses should override
        this to provide validation logic.
        """
        return super(self.__class__, self).validate(value.value, model_instance)

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


def make_echoicefield(echoices, *args, klass_name=None, **kwargs):
    """
    Construct a subclass of a derived `models.Field` specific to the type of the `EChoice` values.

    Parameters
    ----------
    echoices : subclass of EChoice
    args
        Passed to the derived `models.Field`
    klass_name : str
        Give a specific name to the returned class.
        By default for Django < 1.9, the name will be 'EChoiceField'.
        By default for Django >= 1.9, the name will be the name of the enum appended with 'Field'.
    kwargs
        Passed to the derived `models.Field`

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
    if klass_name and StrictVersion(django_version()) < StrictVersion('1.9.0'):
        warnings.warn("Django < 1.9 throws an 'ImportError' if the class name is not defined in the module. "
                      "The provided klass_name will be replaced by {}".format(EChoiceField.__name__), RuntimeWarning)
    klass_name = EChoiceField.__name__ if StrictVersion(django_version()) < StrictVersion('1.9.0') else \
        klass_name if klass_name else "{}Field".format(echoices.__name__)
    d = dict(cls_.__dict__)
    d.update(dict(EChoiceField.__dict__))
    return type(klass_name, (cls_,), d)(echoices, *args, **kwargs)

# TODO: MultipleEChoiceField
