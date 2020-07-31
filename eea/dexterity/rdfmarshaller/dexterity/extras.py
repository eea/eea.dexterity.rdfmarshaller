""" extras """

import sys
import six

try:
    from collective.cover.interfaces import ICover
except ImportError:
    from zope.interface import Interface

    class ICover(Interface):
        """ Dummy replacement interface
        """

from zope.component import adapts
from zope.interface import implementer

from eea.dexterity.rdfmarshaller.dexterity.modifiers import BaseFileModifier
from eea.dexterity.rdfmarshaller.interfaces import ISurfResourceModifier
from plone.app.contenttypes.interfaces import IFile, IImage
from Products.CMFPlone import log


@implementer(ISurfResourceModifier)
class CoverTilesModifier(object):
    """Adds tiles information to rdf resources
    """

    adapts(ICover)

    def __init__(self, context):
        self.context = context

    def run(self, resource, *args, **kwds):
        """Change the rdf resource
        """
        uids = self.context.list_tiles()
        value = ''

        for uid in uids:
            tile = self.context.get_tile(uid)
            text = tile.data.get('text', None)

            if text:
                # convert to unicode

                if not isinstance(text.output, six.text_type):
                    value += six.text_type(text.output, 'utf-8')
                else:
                    value += text.output

        if value:
            try:
                setattr(resource, '%s_%s' % ("eea", "cover_tiles"),
                        [value])
            except Exception:
                log.log('RDF marshaller error for context[tiles]'
                        '"%s[": \n%s: %s' %
                        (self.context.absolute_url(),
                         sys.exc_info()[0], sys.exc_info()[1]),
                        severity=log.logging.WARN)

        return resource


class ImageModifier(BaseFileModifier):
    """ ImageModifier """
    adapts(IImage)

    field = 'image'


class FileModifier(BaseFileModifier):
    """ FileModifier """
    adapts(IFile)

    field = 'file'
