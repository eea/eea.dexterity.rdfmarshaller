""" eea.dexterity.rdfmarshaller package """

from eea.dexterity.rdfmarshaller import marshaller
from eea.dexterity.rdfmarshaller.products_marshall_registry import \
    registerComponent

registerComponent('surfrdf', 'RDF Marshaller',
                  marshaller.RDFMarshaller)

registerComponent('surfrdfs', 'RDF Schema Marshaller',
                  marshaller.RDFMarshaller)
