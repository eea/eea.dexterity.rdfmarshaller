""" Various setup
"""
import logging
from Products.CMFCore.utils import getToolByName


def setupVarious(context):
    """ Do some various setup.
    """
    if context.readDataFile('eea.dexterity.rdfmarshaller.txt') is None:
        return

    # Products.Marshall doesn't use GenericSetup profiles,
    # so we need to install it from here
    logger = logging.getLogger("eea.dexterity.rdfmarshaller")
    logger.info("Installing Products.Marshall")

    site = context.getSite()
    qinstaller = getToolByName(site, 'portal_quickinstaller')
    qinstaller.installProduct('Marshall')
