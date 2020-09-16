""" Surf conversion classes """

from DateTime.DateTime import DateTime
from rdflib import URIRef
from zope.component import adapts, queryAdapter
from zope.interface import implementer, Interface
from eea.dexterity.rdfmarshaller.interfaces import IValue2Surf
from plone.app.textfield.value import RichTextValue
import six


@implementer(IValue2Surf)
class Value2Surf(object):
    """Base implementation of IValue2Surf
    """
    adapts(Interface)

    def __init__(self, value):
        self.value = value

    def __call__(self, *args, **kwds):
        if self.value:
            language = kwds['language']
            if isinstance(self.value, six.text_type):
                return (self.value, language)
            try:
                value = (six.text_type(self.value, 'utf-8', 'replace'),
                         language)
            except TypeError:
                value = (str(self.value), language)
            return value


class URIRef2Surf(Value2Surf):
    """ Value2Surf implementation for URIRef
    """
    adapts(URIRef)

    def __call__(self, *args, **kwargs):
        return self.value


class Tuple2Surf(Value2Surf):
    """IValue2Surf implementation for tuples.
    """
    adapts(tuple)

    def __call__(self, *args, **kwds):
        return list(self.value)


class List2Surf(Value2Surf):
    """IValue2Surf implementation for tuples.
    """
    adapts(list)

    def __call__(self, *args, **kwds):
        adapted = []
        for val in self.value:
            valueAdapter = queryAdapter(val, IValue2Surf)
            if valueAdapter:
                val = valueAdapter(val, language=kwds['language'])
            adapted.append(val)
        return adapted


class Set2Surf(Value2Surf):
    """IValue2Surf implementation for sets.
    """
    adapts(set)

    def __call__(self, *args, **kwds):
        return list(self.value)


class RichValue2Surf(Value2Surf):
    """ RichTextValue adaptor """
    adapts(RichTextValue)

    def __init__(self, value):
        super(RichValue2Surf, self).__init__(value.output)


class DateTime2Surf(Value2Surf):
    """IValue2Surf implementation for DateTime """

    adapts(DateTime)

    def __call__(self, *args, **kwds):
        return (self.value.HTML4(), None,
                'http://www.w3.org/2001/XMLSchema#dateTime')
