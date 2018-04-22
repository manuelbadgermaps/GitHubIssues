# -*- coding: utf-8 -*-
from reporter_service import Reporter

import sys

arguments = sys.argv

if len(arguments) > 3:
    reporter = Reporter(arguments[1])
    print reporter.run(arguments[2],arguments[3])
else:
    print("Usage: python reporter.py github_username github_password list_of_repositories")
