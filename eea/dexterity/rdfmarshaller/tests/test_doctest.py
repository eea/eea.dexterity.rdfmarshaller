""" Doc tests
"""
import doctest
import unittest
from plone.testing import layered
from eea.dexterity.rdfmarshaller.testing import FUNCTIONAL_TESTING
from eea.dexterity.rdfmarshaller.testing import FunctionalTestCase
from Testing.ZopeTestCase import FunctionalDocFileSuite


OPTIONFLAGS = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)


def test_suite():
    """ Suite
    """
    suite = unittest.TestSuite()
    suite.addTests([
        layered(
            FunctionalDocFileSuite(
                'marshall.txt',
                optionflags=OPTIONFLAGS,
                package='eea.dexterity.rdfmarshaller',
                test_class=FunctionalTestCase),
            layer=FUNCTIONAL_TESTING),
    ])
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
