import json
from django.conf import settings

class ViteMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if b"</head>" in response.content:
            # Usar lógica diferente para desarrollo y producción
            if settings.DEBUG:
                # En desarrollo, apuntar al servidor de Vite
                vite_script = b'<script type="module" src="http://localhost:5173/src/js/main.js"></script>'
                vite_style = b'<link rel="stylesheet" href="http://localhost:5173/src/styles/app.css">'
                vite_script_preload = b'<link rel="preload" href="http://localhost:5173/src/styles/app.css" as="style">'
            else:
                # En producción, usar los archivos estáticos generados por Vite
                manifest = self.get_manifest()
                try:
                    js_file = manifest["src/js/main.js"]["file"]
                    css_file = manifest["src/styles/app.css"]["file"]

                    vite_script_preload = f'<link rel="preload" href="/static/dist/{css_file}" as="style">'.encode()
                    vite_script = f'<script type="module" src="/static/dist/{js_file}"></script>'.encode()
                    vite_style = f'<link rel="stylesheet" href="/static/dist/{css_file}">'.encode()

                except KeyError:
                    vite_script = b""
                    vite_style = b""
                    vite_script_preload = b""

            # Inyectar los enlaces al head
            response.content = response.content.replace(
                b"</head>",
                vite_script_preload + vite_script + vite_style + b"</head>"
            )
        return response

    def get_manifest(self):
        # Asegúrate de que la ruta del manifiesto sea correcta
        manifest_path = settings.BASE_DIR / 'static/dist/.vite/manifest.json'
        try:
            with open(manifest_path) as f:
                return json.load(f)
        except FileNotFoundError:
            return {}