""" Generic modifiers module
"""
import rdflib
from eea.dexterity.rdfmarshaller.interfaces import ISurfResourceModifier
from OFS.interfaces import IFolder
from plone.api.portal import get_tool
from zope.component import adapts
from zope.interface import implementer


@implementer(ISurfResourceModifier)
class FolderPartsModifier(object):
    """IObject2Surf implemention for Folders"""

    adapts(IFolder)

    def __init__(self, context):
        self.context = context

    def run(self, resource, adapter, session, *args, **kwds):
        """ Folder to Surf """

        resource.dcterms_hasPart = []

        catalog = get_tool('portal_catalog')
        contentFilter = {
            'path': {'query': '/'.join(self.context.getPhysicalPath()),
                     'depth': 1}}
        urls = [b.getURL() for b in catalog(contentFilter,
                                            review_state='published',
                                            show_all=1,
                                            show_inactive=1)]

        resource.dcterms_hasPart = [rdflib.URIRef(url) for url in urls]
