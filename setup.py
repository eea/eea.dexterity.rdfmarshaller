""" EEA Dexterity RDF Marshaller Installer
"""
import os

from setuptools import find_packages, setup

name = "eea.dexterity.rdfmarshaller"
path = name.split('.') + ['version.txt']
version = open(os.path.join(*path)).read().strip()

setup(name=name,
      version=version,
      description="Dexterity RDF marshaller for Plone",
      long_description_content_type="text/x-rst",
      long_description=open("README.rst").read() + "\n" +
      open(os.path.join("docs", "HISTORY.txt")).read(),
      # https://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Framework :: Zope2",
          "Framework :: Plone",
          "Framework :: Plone :: 5.2",
          "Programming Language :: Zope",
          "Programming Language :: Python",
          "Programming Language :: Python :: 3.7",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "License :: OSI Approved :: GNU General Public License (GPL)",
      ],
      keywords='EEA Add-ons Plone Zope',
      author='European Environment Agency: IDM2 A-Team',
      author_email='eea-edw-a-team-alerts@googlegroups.com',
      url='https://github.com/eea/eea.dexterity.rdfmarshaller',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['eea', 'eea.dexterity'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Unidecode',
          'surf>=3.0.b3',
          'rdflib>=4.2.2',
          'chardet',
          'eventlet',
          'rdflib_jsonld>=0.4.0',
          'collective.z3cform.datagridfield',
          'plone.formwidget.contenttree',
          'eea.rabbitmq.plone>=1.2',
      ],
      extras_require={
          'test': [
              'plone.app.testing',
              'plone.app.robotframework',
              'collective.z3cform.datagridfield',
          ]
      },
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
