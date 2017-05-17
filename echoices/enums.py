from abc import ABCMeta
from enum import Enum
from types import DynamicClassAttribute


class EChoice(Enum):
    """
    Custom Enum to ease the usage of choices outside the model.
    
    Works by overriding the default _value_ field. This is done to offer a harmonized interface 
    when using auto-generated numeric values.
    By the way, `value` is now the actual value to be stored in the DB.
    
    Notes
    -----
    Interface differs slightly from the Enum:
    `EChoice.value` returns the actual value to be stored in the DB, while the legacy `Enum.value`
    would return the whole tuple used when defining the enumeration item.

    See Also
    --------
    http://stackoverflow.com/a/24105344

    """
    __metaclass__ = ABCMeta

    def __new__(cls, value, label, *args, **kwargs):
        if value in [c.value for c in list(cls)]:
            raise AttributeError(
                "Duplicate value: '{}'. Only unique values are supported in {}.".format(value, EChoice))
        obj = object.__new__(cls)
        obj._value_ = value  # Overrides default _value_
        obj._label_ = label
        return obj

    @DynamicClassAttribute
    def label(self):
        """The label of the Enum member."""
        return self._label_

    @classmethod
    def values(cls):
        """
        
        Returns
        -------
        tuple
            of all the values of this Enum
        
        """
        if not hasattr(cls, '__values_'):
            cls.__values_ = tuple([c.value for c in list(cls)])
        return cls.__values_

    @classmethod
    def max_value_length(cls):
        """
        Not to be used when using numeric values.
        
        Returns
        -------
        int
            the maximal length required by this Enum to be stored in the database

        """
        if not hasattr(cls, '__max_value_length_'):
            cls.__max_value_length_ = max([len(c.value) for c in list(cls)])
        return cls.__max_value_length_

    @classmethod
    def choices(cls):
        """
        Generate the choices as required by Django models.

        Returns
        -------
        tuple

        """
        # "natural" order, aka as given when instantiating
        if not hasattr(cls, '__choices_'):
            cls.__choices_ = tuple([(c.value, c.label) for c in list(cls)])
        return cls.__choices_

    @classmethod
    def from_value(cls, value):
        """
        Return the EChoice object associated with this value, if any.

        Parameters
        ----------
        value
            In the type of the `value` field, as set when instantiating this EChoice.

        Returns
        -------
        EChoice

        Raises
        ------
        KeyError
            if `value` does not exist in any element

        """
        try:
            # Should always be there (at least in Python 3.5)
            return cls._value2member_map_[value]
        except AttributeError:
            value2member_map_ = {}
            for echoice in list(cls):
                value2member_map_[echoice.value] = echoice
            cls._value2member_map_ = value2member_map_
            return cls._value2member_map_[value]


class EOrderedChoice(EChoice):
    """Provide ordering of the elements"""
    __metaclass__ = ABCMeta

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

    @classmethod
    def choices(cls, order='natural'):
        """
        Generate the choices as required by Django models.

        Parameters
        ----------
        order : str
            in which the elements should be returned. Possible values are:
            * 'sorted', the elements will be sorted by `value`
            * 'reverse', the elements will be sorted by `value` as if each comparison were 
                reversed
            * 'natural' (default), the elements are ordered as when instantiated in the enumeration
                
        Returns
        -------
        iterable of tuple

        """
        INC, DEC, NAT = 'sorted', 'reverse', 'natural'
        assert order in [INC, DEC, NAT], "Sorting order not recognized: {}".format(order)
        if order in [INC, DEC]:
            reverse = order == DEC
            if reverse:
                attr = '__choices_reverse_'
            else:
                attr = '__choices_sorted_'
            if not hasattr(cls, attr):
                setattr(cls, attr, tuple([(c.value, c.label) for c in sorted(list(cls), reverse=reverse)]))
            return getattr(cls, attr)
        else:
            return super(EOrderedChoice, cls).choices()


class EAutoChoice(EOrderedChoice):
    """
    Auto-generated numeric `value`s. Thus support sorting by `value`.

    See Also
    --------
    https://docs.python.org/3.5/library/enum.html#autonumber

    """
    __metaclass__ = ABCMeta

    def __new__(cls, label, *args, **kwargs):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        obj._label_ = label
        return obj
