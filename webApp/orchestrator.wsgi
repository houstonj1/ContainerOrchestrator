# Orchestrator wsgi
import sys

#Expand Python classes path with your app's path
from orchestrator import app as application
application.secret_key = "ThisIScontainerOrchestrator\x1c02\xbbh\xba\xd8$\xe9d(\xa5\xe0Wb\xff\x1a\x8a\xd391\x1a(N\x8c"
application.debug = True

#Put logging code (and imports) here ...

#Initialize WSGI app object
