# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#

import os
import sys
import datetime
import inspect
import matplotlib

from sphinx.application import Sphinx
from sphinx.ext import autosummary
from pathlib import Path
from typing import Optional, Union, Mapping

matplotlib.use('agg')

HERE = Path(__file__).parent
sys.path.insert(0, f"{HERE.parent.parent}")
sys.path.insert(0, f"{HERE}")
sys.path.insert(0, os.path.abspath("_ext"))
import sccoda

on_rtd = os.environ.get('READTHEDOCS') == 'True'

# -- Retrieve notebooks ------------------------------------------------

from urllib.request import urlretrieve

notebooks_url = "https://github.com/theislab/scCODA/raw/master/tutorials/"
notebooks = [
    "getting started.ipynb",
    "Data import and visualization.ipynb"
    "Modeling options and result analysis.ipynb"
]
for nb in notebooks:
    try:
        urlretrieve(notebooks_url + nb, nb)
    except:
        pass

# -- Project information -----------------------------------------------------

project = 'scCODA'
title = 'scCODA: A Bayesian model for compositional single-cell data analysis'
author = 'Johannes Ostner, Maren Büttner, Benjamin Schubert'
copyright = f"{datetime.datetime.now():%Y}, {author}"

version = sccoda.__version__.replace(".dirty", "")
release = version
pygments_style = "sphinx"

# -- General configuration ---------------------------------------------------

needs_sphinx = "2.0"

extensions = ['numpydoc',
              'sphinx.ext.autodoc',
              'sphinx.ext.intersphinx',
              'sphinx.ext.doctest',
              'sphinx.ext.coverage',
              'sphinx.ext.mathjax',
              'sphinx.ext.napoleon',
              'sphinx.ext.autosummary',
              "sphinx.ext.githubpages",
              "sphinx_autodoc_typehints",
              "nbsphinx",
              "edit_on_github",
              "scanpydoc"
              ]

autodoc_mock_imports = ["tensorflow",
                        "tensorflow_probability",
                        "skbio",
                        "arviz",
                        "scipy",
                        "anndata",
                        "patsy",
                        "sklearn",
                        "scanpy",
                        "statsmodels",
                        "rpy2",
                        "pickle",
                        ]

intersphinx_mapping = dict(
    python=("https://docs.python.org/3", None),
    anndata=("https://anndata.readthedocs.io/en/latest/", None),
    scanpy=("https://scanpy.readthedocs.io/en/latest/", None),
    numpy=("https://numpy.org/doc/stable/", None),
)

# Generate the API documentation when building
autosummary_generate = True
napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_use_rtype = True  # having a separate entry generally helps readability
napoleon_use_param = True
napoleon_custom_sections = [('Params', 'Parameters')]
todo_include_todos = False

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']
source_suffix = [".rst", ".ipynb"]
master_doc = 'index'
default_role = 'literal'
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = 'sphinx'

# Add notebooks prolog to Google Colab and nbviewer
nbsphinx_prolog = r"""
{% set docname = 'github/theislab/scCODA/blob/master/' + env.doc2path(env.docname, base=None) %}
.. raw:: html

    <div class="note">
      <a href="https://colab.research.google.com/{{ docname|e }}" target="_parent">
      <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>
      <a href="https://nbviewer.jupyter.org/{{ docname|e }}" target="_parent">
      <img src="https://github.com/theislab/scCODA/raw/release_0.1/docs/_static/nbviewer_badge.svg" alt="Open In nbviewer"/></a>
    </div>
"""


# -- Options for HTML output -------------------------------------------------

html_theme = 'scanpydoc'
html_theme_options = dict(navigation_depth=1, titles_only=True)
github_repo = "sccoda"
html_context = dict(
    display_github=True,  # Integrate GitHub
    github_user='theislab',  # Username
    github_repo='scCODA',  # Repo name
    github_version='release_0.1',  # Version
    conf_py_path='/docs/',  # Path in the checkout to the docs root
)
html_static_path = ['_static']
html_show_sphinx = False

def setup(app):
    app.warningiserror = on_rtd

# -- Options for other output ------------------------------------------

htmlhelp_basename = "scCODAdoc"
title_doc = f"{project} documentation"

latex_documents = [(master_doc, f"{project}.tex", title_doc, author, "manual")]
man_pages = [(master_doc, project, title_doc, [author], 1)]
texinfo_documents = [
    (master_doc, project, title_doc, author, project, title, "Miscellaneous")
]
"""

# -- generate_options override ------------------------------------------

def process_generate_options(app: Sphinx):
    genfiles = app.config.autosummary_generate

    if genfiles and not hasattr(genfiles, "__len__"):
        env = app.builder.env
        genfiles = [
            env.doc2path(x, base=None)
            for x in env.found_docs
            if Path(env.doc2path(x)).is_file()
        ]
    if not genfiles:
        return

    from sphinx.ext.autosummary.generate import generate_autosummary_docs

    ext = app.config.source_suffix
    genfiles = [
        genfile + (not genfile.endswith(tuple(ext)) and ext[0] or "")
        for genfile in genfiles
    ]

    suffix = autosummary.get_rst_suffix(app)
    if suffix is None:
        return

    generate_autosummary_docs(
        genfiles,
        builder=app.builder,
        suffix=suffix,
        base_path=app.srcdir,
        imported_members=True,
        app=app,
    )


autosummary.process_generate_options = process_generate_options
"""

# -- GitHub URLs for class and method pages ------------------------------------------

def get_obj_module(qualname):
    """Get a module/class/attribute and its original module by qualname"""
    modname = qualname
    classname = None
    attrname = None
    while modname not in sys.modules:
        attrname = classname
        modname, classname = modname.rsplit(".", 1)

    # retrieve object and find original module name
    if classname:
        cls = getattr(sys.modules[modname], classname)
        modname = cls.__module__
        obj = getattr(cls, attrname) if attrname else cls
    else:
        obj = None

    return obj, sys.modules[modname]


def get_linenos(obj):
    """Get an object’s line numbers"""
    try:
        lines, start = inspect.getsourcelines(obj)
    except TypeError:
        return None, None
    else:
        return start, start + len(lines) - 1


# set project_dir: project/docs/conf.py/../../.. → project/
project_dir = Path(__file__).parent.parent
github_url_sccoda = "https://github.com/theislab/scCODA/tree/release_0.1"
github_url_read_loom = "https://github.com/theislab/anndata/tree/master/anndata"
github_url_read = "https://github.com/theislab/scanpy/tree/master"
github_url_scanpy = "https://github.com/theislab/scanpy/tree/master/scanpy"
from pathlib import PurePosixPath


def modurl(qualname):
    """Get the full GitHub URL for some object’s qualname."""
    obj, module = get_obj_module(qualname)
    github_url = github_url_sccoda
    try:
        path = PurePosixPath(Path(module.__file__).resolve().relative_to(project_dir))
    except ValueError:
        # trying to document something from another package
        github_url = (
            github_url_read_loom
            if "read_loom" in qualname
            else github_url_read
            if "read" in qualname
            else github_url_scanpy
        )
        path = "/".join(module.__file__.split("/")[-2:])
    start, end = get_linenos(obj)
    fragment = f"#L{start}-L{end}" if start and end else ""
    return f"{github_url}/{path}{fragment}"


def api_image(qualname: str) -> Optional[str]:
    path = Path(__file__).parent / f"{qualname}.png"
    return (
        f".. image:: {path.name}\n   :width: 200\n   :align: right"
        if path.is_file()
        else ""
    )


# modify the default filters
from jinja2.defaults import DEFAULT_FILTERS

DEFAULT_FILTERS.update(modurl=modurl, api_image=api_image)


# -- Override some classnames in autodoc --------------------------------------------

qualname_overrides = {
    "anndata.base.AnnData": "anndata.AnnData",
}

"""
# -- Prettier Param docs --------------------------------------------

from typing import Dict, List, Tuple
from docutils import nodes
from sphinx import addnodes
from sphinx.domains.python import PyTypedField, PyObject
from sphinx.environment import BuildEnvironment


class PrettyTypedField(PyTypedField):
    list_type = nodes.definition_list

    def make_field(
        self,
        types: Dict[str, List[nodes.Node]],
        domain: str,
        items: Tuple[str, List[nodes.inline]],
        env: BuildEnvironment = None,
    ) -> nodes.field:
        def makerefs(rolename, name, node):
            return self.make_xrefs(rolename, domain, name, node, env=env)

        def handle_item(
            fieldarg: str, content: List[nodes.inline]
        ) -> nodes.definition_list_item:
            head = nodes.term()
            head += makerefs(self.rolename, fieldarg, addnodes.literal_strong)
            fieldtype = types.pop(fieldarg, None)
            if fieldtype is not None:
                head += nodes.Text(" : ")
                if len(fieldtype) == 1 and isinstance(fieldtype[0], nodes.Text):
                    (text_node,) = fieldtype  # type: nodes.Text
                    head += makerefs(
                        self.typerolename, text_node.astext(), addnodes.literal_emphasis
                    )
                else:
                    head += fieldtype

            body_content = nodes.paragraph("", "", *content)
            body = nodes.definition("", body_content)

            return nodes.definition_list_item("", head, body)

        fieldname = nodes.field_name("", self.label)
        if len(items) == 1 and self.can_collapse:
            fieldarg, content = items[0]
            bodynode = handle_item(fieldarg, content)
        else:
            bodynode = self.list_type()
            for fieldarg, content in items:
                bodynode += handle_item(fieldarg, content)
        fieldbody = nodes.field_body("", bodynode)
        return nodes.field("", fieldname, fieldbody)


# replace matching field types with ours
PyObject.doc_field_types = [
    PrettyTypedField(
        ft.name,
        names=ft.names,
        typenames=ft.typenames,
        label=ft.label,
        rolename=ft.rolename,
        typerolename=ft.typerolename,
        can_collapse=ft.can_collapse,
    )
    if isinstance(ft, PyTypedField)
    else ft
    for ft in PyObject.doc_field_types
]
"""