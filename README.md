# Gestión de Proyectos - Django App

## Descripción
Aplicación web para gestión de proyectos desarrollada con Django.

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/RafaelMarcelliniB/GESTION-PROYECTOS.git
cd GESTION-PROYECTOS
```

2. Crear entorno virtual:
```bash
python3 -m venv env
source env/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Ejecutar migraciones:
```bash
python manage.py migrate
```

5. Crear superusuario:
```bash
python manage.py createsuperuser
```

6. Ejecutar servidor:
```bash
python manage.py runserver
```

## Tecnologías
- Python 3.10
- Django
- SQLite
