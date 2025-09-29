import sys, os

# Agrega la ruta a tu app Django
sys.path.insert(0, os.path.dirname(__file__) + "/hermes")

from passenger_wsgi import application