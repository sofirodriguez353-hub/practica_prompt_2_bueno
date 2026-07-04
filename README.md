# FamilyBank

FamilyBank es una aplicación Django para la gestión y control de cuentas bancarias de una unidad familiar.

Objetivo
 - Proveer un feed cronológico tipo "blog" donde se registren movimientos financieros (ingresos, gastos y transferencias).
 - Ofrecer un dashboard claro y responsive para visualizar saldos, cuentas y categorías.

Stack
 - Backend: Python 3.10+, Django 4.2+
 - Frontend: HTML5, CSS3 (variables para temas), JavaScript vanilla

Estructura del proyecto
 - `familybank/` - configuración del proyecto Django
 - `bankapp/` - app principal con modelos, vistas, templates y static
 - `static/` - CSS/JS e imágenes
 - `media/` - uploads (no versionado)

Instrucciones rápidas para desarrollo (Windows PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Buenas prácticas
 - Mantén `DEBUG=False` y `SECRET_KEY` en variables de entorno para producción.
 - No comitees archivos en `media/` ni `*.env`.

Licencia
 - Este repositorio incluye una licencia MIT (archivo `LICENSE`).

Contribuir
 - Crea un fork o una rama `feat/*` y abre un Pull Request.

