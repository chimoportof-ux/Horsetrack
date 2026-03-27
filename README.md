# HorseTrack con Django + Docker

Proyecto web para gestión de caballos, entrenamientos, salud y eventos.

## Incluye
- Django
- SQLite3
- Docker y docker-compose
- Panel de administración de Django
- Login/logout
- CRUD de caballos
- Registros de salud
- Entrenamientos
- Eventos y recordatorios
- Dashboard con próximos eventos

## Cómo arrancarlo

```bash
docker compose up --build
```

Después abre:
- App: http://localhost:8000
- Admin: http://localhost:8000/admin

## Usuario administrador por defecto
- Usuario: `admin`
- Contraseña: `admin1234`

Puedes cambiarlos en `docker-compose.yml`.

## Comandos útiles

Crear migraciones manualmente:
```bash
docker compose exec web python manage.py makemigrations
```

Crear otro superusuario:
```bash
docker compose exec web python manage.py createsuperuser
```

## Estructura
- `horsetrack_project/`: configuración principal del proyecto
- `horses/`: app principal
- `templates/`: plantillas HTML
- `static/`: CSS y JS

## Notas
- La base de datos es SQLite (`db.sqlite3`).
- Se puede gestionar desde el panel de administración de Django.
- Los datos se conservan en el archivo del proyecto mientras mantengas la carpeta.
