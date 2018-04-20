# -*- coding: utf-8 -*-
from reporter_service import Reporter

import sys

arguments = sys.argv

if len(arguments) > 1:
    reporter=Reporter(arguments[1])
    reporter.run()
else:
    print("Usage python reporter.py list_of_repositories")
