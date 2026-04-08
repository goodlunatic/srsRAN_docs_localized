# -*- coding: utf-8 -*-

import os
from datetime import date

year = str(date.today().year)

extensions = [
    'sphinxcontrib.seqdiag',
    'sphinxcontrib.blockdiag',
    'sphinx_copybutton',
    'hoverxref.extension',
    'sphinx.ext.todo',
    'sphinx.ext.intersphinx',
]

templates_path = ['../source/.templates']
source_suffix = '.rst'
master_doc = 'index'

intersphinx_mapping = {
    "project": ("https://docs.srsran.com/projects/project/en/latest/", None),
    "4g": ("https://docs.srsran.com/projects/4g/en/latest/", None),
}

hoverxref_auto_ref = True
hoverxref_role_types = {
    'hoverxref': 'tooltip',
    'ref': 'tooltip',
}

if os.environ.get('READTHEDOCS') != 'True':
    hoverxref_api_host = 'https://readthedocs.org'

project = u'srsRAN'
copyright = u'2021-' + year + ', Software Radio Systems.'
author = u'Software Radio Systems'
language = 'zh_CN'
exclude_patterns = []
pygments_style = 'sphinx'
todo_include_todos = False

html_theme = 'sphinx_rtd_theme'

html_context = {
    "sidebar_external_links_caption": "链接",
    "sidebar_external_links": [
        (
            '<i class="web-icon"></i> 官网',
            "https://www.srsran.com",
        ),
        (
            '<i class="fa fa-github fa-fw"></i> 项目仓库',
            "https://github.com/srsran/",
        ),
        (
            '<i class="fa fa-twitter fa-fw"></i> Twitter',
            "https://twitter.com/srsRANProject",
        ),
    ],
    "sidebar_permanent_nav_caption": "文档导航",
    "sidebar_permanent_nav": [
        (
            'srsRAN Project',
            "https://docs.srsran.com/projects/project/en/latest/",
        ),
        (
            'srsRAN 4G',
            "https://docs.srsran.com/projects/4g/en/latest/",
        ),
    ],
}

html_theme_options = {
    "collapse_navigation": False,
    "prev_next_buttons_location": 'both'
}

html_logo = '../source/.imgs/logo.png'
html_favicon = '../source/.imgs/favicon.png'
html_static_path = ['../source/.static']
html_css_files = [
    'css/custom.css',
]
