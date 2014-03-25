#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Example: pretty_all_xml.py /opt/git/npo5-devel
"""

import os
import sys
from xmlutil import pretty_parse

repo_path = sys.argv[1]

for root, dirs, files in os.walk(repo_path):
    for file in files:
        if file.endswith('.xml'):
            file_path = os.path.join(root,file)
            pretty_parse(file_path)
