""" Custom ObjectMovedOrRenamedEvent"""
# pylint: disable=too-many-arguments
from eea.dexterity.rdfmarshaller.actions.interfaces import \
    IObjectMovedOrRenamedEvent
from zope.component.interfaces import ObjectEvent
from zope.interface import implementer


@implementer(IObjectMovedOrRenamedEvent)
class ObjectMovedOrRenamedEvent(ObjectEvent):
    """ObjectMovedOrRenamedEvent"""

    def __init__(self, obj, oldParent, oldName, newParent, newName):
        ObjectEvent.__init__(self, obj)
        self.oldParent = oldParent
        self.oldName = oldName
        self.newParent = newParent
        self.newName = newName
