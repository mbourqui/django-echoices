from django.db import models
from django.utils.translation import ugettext_lazy as _

from .enums import EChoice


class EChoiceCharField(models.CharField):
    """
    Specialized field for single choices
    
    Internally uses CharField. 'max_length' is deducted from the `echoices`.
    
    Parameters
    ----------
    echoices : sublcass of EChoice
        The choices this field supports.
    * args
        Are passed to models.CharField
    * kwargs
        Are passed to models.CharField
    
    """
    description = _("An enhanced CharField supporting enumerated choices")

    def __init__(self, echoices, *args, **kwargs):
        assert issubclass(echoices, EChoice)
        self.echoices = echoices
        kwargs['choices'] = self.echoices.choices()
        kwargs['max_length'] = self.echoices.max_value_length()
        default = kwargs.get('default')
        if default:
            kwargs['default'] = default.value
        super(EChoiceCharField, self).__init__(*args, **kwargs)

    def get_default(self):
        default = super(EChoiceCharField, self).get_default()
        if self.has_default():
            return self.echoices.from_value(default)
        return default

    def from_db_value(self, value, *args):
        if value is None:
            return value
        return self.echoices.from_value(value)

    def to_python(self, value):
        if isinstance(value, self.echoices) or value is None:
            return value
        return self.echoices.from_value(value)

    def get_prep_value(self, value):
        return str(value.value)

    def deconstruct(self):
        name, path, args, kwargs = super(EChoiceCharField, self).deconstruct()
        kwargs['echoices'] = self.echoices
        del kwargs['choices']
        del kwargs['max_length']
        if self.has_default():
            kwargs['default'] = self.get_default()
        return name, path, args, kwargs

# TODO: EChoiceIntegerField

# TODO: MultipleEChoiceField

# TODO: merge EChoiceCharField and EChoiceIntegerField into EChoiceField
