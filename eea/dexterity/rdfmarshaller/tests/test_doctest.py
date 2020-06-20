""" Doc tests
"""
import doctest
import unittest
from eea.dexterity.rdfmarshaller.tests.base import FunctionalTestCase
from Testing.ZopeTestCase import FunctionalDocFileSuite


OPTIONFLAGS = (
    doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)


def test_suite():
    """ Suite
    """

    return unittest.TestSuite((
        FunctionalDocFileSuite(
            'marshall.txt',
            optionflags=OPTIONFLAGS,
            package='eea.dexterity.rdfmarshaller',
            test_class=FunctionalTestCase),
    ))


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
