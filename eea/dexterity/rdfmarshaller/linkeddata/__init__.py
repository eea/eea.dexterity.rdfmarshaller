""" LinkedData module
"""
# pylint: disable=too-many-locals
from __future__ import print_function
import rdflib
import surf
from eea.dexterity.rdfmarshaller.interfaces import ILinkedData
from eea.dexterity.rdfmarshaller.interfaces import ILinkedDataHomepage
from eea.dexterity.rdfmarshaller.linkeddata.interfaces import \
    ILinkedDataHomepageData
from persistent import Persistent
from plone.api import portal
from Products.CMFCore.interfaces import IContentish
from zope.annotation.factory import factory
from zope.component import adapts
from zope.interface import implementer


def schematize(store):
    """ Schematize
    """
    graph = store.reader.graph
    triples = list(graph)

    res = [(s, p, v)
           for (s, p, v) in triples

           if (
               v.startswith('http://schema.org') or
               p.startswith('http://schema.org')
    )]
    s = surf.Store(reader='rdflib', writer='rdflib', rdflib_store='IOMemory')

    for triple in res:
        s.add_triple(*triple)

    return s


@implementer(ILinkedData)
class GenericLinkedData(object):
    """ Generic ILinkedData implemention
    """

    adapts(IContentish)

    def __init__(self, context):
        self.context = context

    def get_jsonld_context(self):
        """ Get jsonld context
        """
        context = {
            surf.ns.SCHEMA['Image']: surf.ns.SCHEMA['ImageObject'],
            surf.ns.SCHEMA['productID']: surf.ns.SCHEMA['about'],
        }

        return context

    def get_site(self):
        """ Get site
        """
        site = portal.get()
        ldsite = self.context

        while not ILinkedDataHomepage.providedBy(ldsite):
            try:
                ldsite = ldsite.aq_parent
            except AttributeError:
                ldsite = None

                break

        if ldsite is None:
            return site

        return ldsite

    def modify(self, obj2surf):
        """ Modify
        """
        resource = obj2surf.resource
        session = resource.session

        resource.rdf_type.append(surf.ns.SCHEMA['WebPage'])
        resource.update()

        image = resource.foaf_depiction.first

        site = self.get_site()
        site_url = site.absolute_url()
        base_url = self.context.absolute_url()

        Article = session.get_class(surf.ns.SCHEMA['Article'])
        Person = session.get_class(surf.ns.SCHEMA['Person'])

        article = Article(base_url + "#article")
        article.schema_mainEntityOfPage = resource.subject

        headline = resource.dcterms_title.first
        if headline:
            headline = headline.value
        else:
            headline = resource.dcterms_abstract
        article.schema_headline = headline

        published = resource.dcterms_issued.first
        published = published if published else resource.dcterms_created.first
        article.schema_datePublished = str(published)

        modified = resource.dcterms_modified.first
        modified = modified if modified else published
        article.schema_dateModified = str(modified)

        name = resource.dcterms_creator.first

        if name:
            name = name.value
        else:
            name = "admin"
        author = Person(site_url + "#author:" + name)
        author.schema_name = name

        article.schema_author = author
        article.schema_description = resource.dcterms_abstract

        if image:
            image.schema_url = str(image.subject)

            article.schema_image = image.subject
            image.update()

        author.update()
        article.update()
        resource.update()

        article.schema_publisher = rdflib.term.URIRef(
            site_url + "#organization"
        )
        article.update()

    def serialize(self, obj2surf):
        """ Folder to Surf
        """

        self.modify(obj2surf)

        store = obj2surf.session.default_store
        store = schematize(store)

        context = self.get_jsonld_context()
        data = store.reader.graph.serialize(format='json-ld', context=context)

        return data


class HomepageLinkedData(GenericLinkedData):
    """ ILinkedData implemention for homepages
    """

    adapts(ILinkedDataHomepage)

    def get_jsonld_context(self):
        """ Get jsonld context
        """
        context = {
            surf.ns.SCHEMA['Image']: surf.ns.SCHEMA['ImageObject'],
            surf.ns.SCHEMA['productID']: surf.ns.SCHEMA['about'],
        }

        return context

    def modify(self, obj2surf):
        """ Modify
        """
        print("This is a homepage")


@implementer(ILinkedDataHomepageData)
class LinkedDataHomepageData(Persistent):
    """ LinkedDataHomepageData
    """
    adapts(ILinkedDataHomepage)


KEY = 'LinkedDataHomepage'

linked_data_annotation = factory(LinkedDataHomepageData, key=KEY)
