import os
import sys

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(__file__))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brandfluence.settings')

# Import Django WSGI application
from brandfluence.wsgi import application

# Vercel expects 'app' variable
app = application

