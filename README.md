# Tienda – Proyecto Final (Nuxt 3 + Flask)

Aplicación full‑stack de e‑commerce con panel de administración y atención al cliente, chat en tiempo real, tickets de soporte, catálogo, carrito y analíticas.

## Tecnologías
- Frontend: Nuxt 3 (Vue 3, TypeScript), Pinia, Bootstrap 5
- Backend: Flask, SQLAlchemy, Alembic/Flask‑Migrate, Flask‑SocketIO
- Realtime: Socket.IO
- Base de datos: PostgreSQL (Neon)
- Autenticación: JWT

## Estructura del proyecto
```
./
├─ backend/                      # API Flask + Socket.IO + Migrations
│  ├─ funcionalidades/           # Módulos (auth, productos, tickets, etc.)
│  ├─ migrations/                # Alembic/Flask‑Migrate
│  ├─ app.py                     # Entry point Flask (application)
│  ├─ config_production.py       # Configuración por variables de entorno
│  └─ requirements.txt           # Dependencias del backend
├─ frontend/                     # Nuxt 3
│  ├─ layouts/, pages/, plugins/, assets/, public/
│  ├─ stores/, middleware/, composables/
│  ├─ nuxt.config.ts             # Configuración Nuxt
│  └─ package.json               # Dependencias del frontend
├─ uploads/                      # Archivos subidos (imágenes de productos)
```

## Requisitos
- Node.js 18+ y npm 9+
- Python 3.11 (recomendado)
- PostgreSQL (Neon u otro proveedor)
- Git

## Variables de entorno
Configura estas variables en el entorno de producción y desarrollo. En desarrollo puedes usar un archivo `frontend/.env` para el frontend; para el backend, variables en tu shell o `.env` (si usas python‑dotenv).

Backend (Flask):
- ENVIRONMENT=production|development
- DB_NAME
- DB_USER
- DB_PASSWORD
- DB_HOST
- DB_PORT=5432
- JWT_SECRET
- JWT_EXPIRES_MINUTES (ej. 3)
- JWT_REFRESH_EXPIRES_MINUTES (ej. 60)
- OPENAI_API_KEY (opcional si usas RAG)
- SMTP_SERVER=smtp.gmail.com
- SMTP_PORT=587
- SMTP_USERNAME
- SMTP_PASSWORD
- FROM_EMAIL
- FRONTEND_URL=https://tu‑frontend
- CORS_ORIGINS=lista de orígenes separados por coma (ej. https://tu‑frontend)

Frontend (Nuxt):
- NUXT_PUBLIC_API_BASE=https://tu‑backend
- NUXT_PUBLIC_WS_URL=wss/https de tu backend si se usa explícito (opcional)

Notas:
- `config_production.py` construye `DATABASE_URL` a partir de DB_* si `DATABASE_URL` no está presente y aplica `sslmode=require`.
- `CORS_ORIGINS` acepta múltiples orígenes separados por coma; si no se define, toma `FRONTEND_URL`.

## Puesta en marcha local (desarrollo)

1) Backend
```
cd backend
python -m venv .venv
. .venv/bin/activate    # En Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

# Exporta variables mínimas para desarrollo
export ENVIRONMENT=development
export DB_NAME=...
export DB_USER=...
export DB_PASSWORD=...
export DB_HOST=localhost
export DB_PORT=5432
export JWT_SECRET=devsecret
export FRONTEND_URL=http://localhost:3000

# Migraciones (primera vez)
flask db upgrade

# Ejecutar backend
python app.py          # o: gunicorn app:application
```

2) Frontend
```
cd frontend
npm install
# Crea frontend/.env con, por ejemplo:
# NUXT_PUBLIC_API_BASE=http://localhost:8000
npm run dev
```

El backend escucha en puerto dinámico (si PORT está presente) o en el puerto configurado en `app.py`. En producción se usa `gunicorn app:application`.

## Migraciones de base de datos
```
cd backend
flask db migrate -m "mensaje"
flask db upgrade
```

## Socket.IO
- Cliente: inicializado mediante un plugin Nuxt (p. ej., `plugins/socket.client.js`) o con `socket.io-client` desde componentes.
- Servidor: `Flask-SocketIO` con CORS permitido a tus orígenes. Verifica `cors_allowed_origins` y proxy WebSocket en producción.
- En Nginx/PAAS necesitarás que el path `/socket.io/` se proxyee como WebSocket (en Nuxt cliente: `{ path: '/socket.io/' }`).

## Despliegue en Render (Blueprint)
Archivo: `render.yaml`.

Backend (tipo web, Python):
- `rootDir: backend`
- `buildCommand: pip install -r requirements.txt`
- `startCommand: gunicorn app:application`
- `pythonVersion: 3.11.9`
- Configurar variables de entorno indicadas arriba.

Frontend (tipo static):
- `buildCommand: cd frontend && npm install && npm run build`
- `staticPublishPath: frontend/.output/public`
- Definir `NUXT_PUBLIC_API_BASE` apuntando al backend público.

Pasos:
1. Subir el repo a GitHub.
2. En Render: New → Blueprint → seleccionar el repo → Apply.
3. Completar variables sensibles no versionadas (DB_PASSWORD, JWT_SECRET, SMTP_PASSWORD, OPENAI_API_KEY, etc.).
4. Deploy y revisar logs.

Problemas comunes:
- Error `Cannot import 'setuptools.build_meta'`: fija versión de Python en `render.yaml` y añade `setuptools` y `wheel` en `backend/requirements.txt`.
- CORS: define `CORS_ORIGINS` o `FRONTEND_URL` con el dominio del frontend.
- WebSockets: usa URL HTTPS del backend y `path: '/socket.io/'` en el cliente.

## Despliegue en DigitalOcean App Platform
- Crear App → conectar repositorio.
- Servicio backend (Python):
  - Directorio: `backend`
  - Build: `pip install -r requirements.txt`
  - Run: `gunicorn app:application`
  - Variables de entorno: mismas del backend arriba.
- Servicio frontend (Static Site):
  - Directorio: `frontend`
  - Build: `npm install && npm run build`
  - Public: `.output/public`
  - Variables: `NUXT_PUBLIC_API_BASE` con la URL pública del backend.
- Asegurar soporte WebSocket y CORS correctos.

## Buenas prácticas de proyecto
- No subir `node_modules/` (raíz y frontend) al repositorio; usa `.gitignore`.
- Mantener `uploads/` en la raíz para archivos de productos. Si usas un bucket en producción, configura almacenamiento externo.
- Evitar URLs hardcodeadas; usa variables de entorno (`useRuntimeConfig()` en Nuxt, variables en Flask).
- Revisar logs en cada despliegue para diagnosticar rápidamente.

## Scripts útiles
Backend:
- Ejecutar migraciones: `flask db upgrade`
- Ejecutar servidor dev: `python app.py`
- Producción: `gunicorn app:application`

Frontend:
- Dev: `npm run dev`
- Build: `npm run build`
- Preview (si aplica): `npm run preview`

## Licencia
Uso académico/educativo. Ajusta según tus necesidades.
