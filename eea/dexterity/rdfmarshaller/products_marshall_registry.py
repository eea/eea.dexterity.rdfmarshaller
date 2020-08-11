""" Python 3 compatibility
"""


class RegistryItem(object):
    """ RegistryItem
    """
    def __init__(self, name, title, factory):
        self.name = name
        if not title:
            title = name
        self.title = title
        self.factory = factory

    def info(self):
        """info."""
        return {'name': self.name,
                'title': self.title}

    def create(self, ob_id, title, expression, component_name):
        """create.

        :param id:
        :param title:
        :param expression:
        :param component_name:
        """
        return self.factory(ob_id, title or self.title, expression,
                            component_name)


comp_registry = {}


def registerComponent(name, title, component):
    """registerComponent.

    :param name:
    :param title:
    :param component:
    """
    comp_registry[name] = RegistryItem(name, title, component)


def getComponent(name):
    """getComponent.

    :param name:
    """
    return comp_registry[name].factory()
