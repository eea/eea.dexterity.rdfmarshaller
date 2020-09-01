""" testing  """
import logging
import sys
import unittest
from Products.CMFPlone.log import logger
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE \
    as PLONE_FIXTURE
from plone.app.testing import (setRoles, FunctionalTesting, TEST_USER_ID,
                               IntegrationTesting, PloneSandboxLayer)


class Fixture(PloneSandboxLayer):
    """ Fixture """

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """ Set up Zope """
        # Load ZCML
        import eea.dexterity.rdfmarshaller
        import plone.dexterity
        import plone.app.textfield
        import collective.z3cform.datagridfield
        import plone.formwidget.contenttree

        # needed for Dexterity FTI
        self.loadZCML(package=plone.dexterity)

        # needed for DublinCore behavior
        self.loadZCML(package=plone.app.dexterity)

        # needed to support RichText in testpage
        self.loadZCML(package=plone.app.textfield)
        self.loadZCML(package=plone.app.multilingual)
        self.loadZCML(package=collective.z3cform.datagridfield)
        self.loadZCML(package=plone.formwidget.contenttree)

        self.loadZCML(package=eea.dexterity.rdfmarshaller)
        self.loadZCML(package=eea.dexterity.rdfmarshaller.licenses,
                      name="licenseviewlet.zcml")

        self.loadZCML(package=eea.dexterity.rdfmarshaller, name='testing.zcml')

    def setUpPloneSite(self, portal):
        """ Set up Plone site """
        self.applyProfile(portal, 'collective.z3cform.datagridfield:default')
        self.applyProfile(portal, 'eea.dexterity.rdfmarshaller:default')
        self.applyProfile(portal, 'plone.formwidget.contenttree:default')
        self.applyProfile(portal, 'plone.app.multilingual:default')
        self.applyProfile(portal,
                          'eea.dexterity.rdfmarshaller:dexterity_testfixture')
        from zope.component import queryUtility
        from plone.dexterity.interfaces import IDexterityFTI
        import transaction
        for factory in ['testpage']:
            fti = queryUtility(IDexterityFTI, name=factory)
            behavior_list = [a for a in fti.behaviors]
            behavior_list.append('plone.translatable')
            fti.behaviors = tuple(behavior_list)
        transaction.commit()


FIXTURE = Fixture()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='eea.dexterity.rdfmarshaller:Integration',
)
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name='eea.dexterity.rdfmarshaller:Functional',
)


class FunctionalTestCase(unittest.TestCase):
    """ Functional Test Case """

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        """ After setup """
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def enableDebugLog(self):
        """ Enable context.plone_log() output from Python scripts """
        logger.root.setLevel(logging.WARN)
        logger.root.addHandler(logging.StreamHandler(sys.stdout))
