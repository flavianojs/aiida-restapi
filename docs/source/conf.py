# -*- coding: utf-8 -*-
#
# Sphinx configuration for aiida-restapi
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import os
import sys
import time

import reentry

# run reentry before importing aiida
reentry.manager.scan()

from aiida.manage.configuration import load_documentation_profile

import aiida_restapi

# -- AiiDA-related setup --------------------------------------------------

# Load the dummy profile even if we are running locally, this way the documentation will succeed even if the current
# default profile of the AiiDA installation does not use a Django backend.
load_documentation_profile()

extensions = [
    "myst_parser",
    "sphinx_external_toc",
    "sphinx_panels",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "aiida_restapi.graphql.sphinx_ext",
]

# General information about the project.
project = "aiida-restapi"
copyright_first_year = "2021"
copyright_owners = "The AiiDA Team"
show_authors = True
current_year = str(time.localtime().tm_year)
copyright_year_string = (
    current_year
    if current_year == copyright_first_year
    else "{}-{}".format(copyright_first_year, current_year)
)
# pylint: disable=redefined-builtin
copyright = u"{}, {}. All rights reserved".format(
    copyright_year_string, copyright_owners
)

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The full version, including alpha/beta/rc tags.
release = aiida_restapi.__version__
# The short X.Y version.
version = ".".join(release.split(".")[:2])

myst_enable_extensions = ["replacements", "deflist", "colon_fence", "linkify"]

pygments_style = "sphinx"

html_theme = "sphinx_book_theme"
html_theme_options = {
    "home_page_in_toc": True,
    "extra_navbar": "",
    "show_navbar_depth": 2,
    "path_to_docs": "docs/source",
}
html_title = "REST API"
html_logo = "images/AiiDA_transparent_logo.png"
html_use_opensearch = "http://aiida-restapi.readthedocs.io"
html_search_language = "en"

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "aiida": ("https://aiida-core.readthedocs.io/en/latest", None),
    # note pydantic and fastapi are not on sphinx
    "graphql": ("https://graphql-core-3.readthedocs.io/en/latest", None),
    "graphene": ("https://docs.graphene-python.org/en/latest", None),
}
autodoc_typehints = "none"
nitpick_ignore = [
    ("py:class", name)
    for name in [
        "pydantic.main.BaseModel",
        "pydantic.types.Json",
        "graphene.types.generic.GenericScalar",
        "graphene.types.objecttype.ObjectType",
        "graphene.types.mutation.Mutation",
        "graphene.types.scalars.String",
        "aiida_restapi.aiida_db_mappings.Config",
        "aiida_restapi.models.Config",
        "aiida_restapi.routers.auth.Config",
        "aiida_restapi.graphql.orm_factories.AiidaOrmObjectType",
        "aiida_restapi.graphql.nodes.LinkObjectType",
        "aiida_restapi.graphql.orm_factories.multirow_cls_factory.<locals>.AiidaOrmRowsType",
    ]
]

suppress_warnings = ["etoc.toctree"]


def run_apidoc(_):
    """Runs sphinx-apidoc when building the documentation.

    Needs to be done in conf.py in order to include the APIdoc in the
    build on readthedocs.

    See also https://github.com/rtfd/readthedocs.org/issues/1139
    """
    source_dir = os.path.abspath(os.path.dirname(__file__))
    apidoc_dir = os.path.join(source_dir, "apidoc")
    package_dir = os.path.join(source_dir, os.pardir, os.pardir, "aiida_restapi")

    # In #1139, they suggest the route below, but this ended up
    # calling sphinx-build, not sphinx-apidoc
    # from sphinx.apidoc import main
    # main([None, '-e', '-o', apidoc_dir, package_dir, '--force'])

    import subprocess

    cmd_path = "sphinx-apidoc"
    if hasattr(sys, "real_prefix"):  # Check to see if we are in a virtualenv
        # If we are, assemble the path manually
        cmd_path = os.path.abspath(os.path.join(sys.prefix, "bin", "sphinx-apidoc"))

    options = [
        "-o",
        apidoc_dir,
        package_dir,
        "--private",
        "--force",
        "--no-toc",
    ]

    # See https://stackoverflow.com/a/30144019
    env = os.environ.copy()
    env[
        "SPHINX_APIDOC_OPTIONS"
    ] = "members,special-members,private-members,undoc-members,show-inheritance"
    subprocess.check_call([cmd_path] + options, env=env)


def setup(app):
    app.connect("builder-inited", run_apidoc)
