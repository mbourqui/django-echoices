from django import forms

from echoices.enums import EChoice


class TypedEChoiceField(forms.TypedChoiceField):
    def clean(self, value):
        if isinstance(value, EChoice):
            value = value.value
        return super(TypedEChoiceField, self).clean(value)
