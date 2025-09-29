import sys
import os

# Agregar la carpeta de tu proyecto Django al path
PROJECT_ROOT = os.path.join(os.path.dirname(__file__), "hermes")
sys.path.insert(0, PROJECT_ROOT)

# Establecer settings de Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'hermes.settings'

# Activar virtualenv si lo tenés en el host
activate_this = os.path.join(os.path.dirname(__file__), 'venv/bin/activate_this.py')
if os.path.exists(activate_this):
    with open(activate_this) as f:
        exec(f.read(), {'__file__': activate_this})

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
