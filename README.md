# Stack

Boilerplate para aplicaciones web con **Django**, **Next.js** y **Docker**. Incluye autenticación completa con JWT (cookies httpOnly) y login con Google, listo para levantar con un solo comando.

## Stack tecnológico

| Tecnología | Versión | Rol |
|-----------|---------|-----|
| Django | 6.0 | API REST (DRF + SimpleJWT) |
| Next.js | 16 | Frontend (App Router, TypeScript) |
| PostgreSQL | 18 | Base de datos |
| Docker Compose | - | Orquestación |
| Tailwind CSS | 4 | Estilos |
| shadcn/ui | - | Componentes UI |

## Funcionalidades incluidas

- **JWT con cookies httpOnly** — sin localStorage, refresh token rotation con blacklist
- **Login con Google** — Google Identity Services en frontend, verificación de ID token en backend
- **Interceptor con retry queue** — refresh automático y transparente de tokens expirados
- **Auth context con redirect** — protección de rutas en el frontend
- **Docker Compose** — backend, frontend y PostgreSQL en un solo comando
- **Hot reload** — cambios reflejados al instante en desarrollo

## Inicio rápido

```bash
# 1. Clonar
git clone git@github.com:ssantss/stack.git
cd stack

# 2. Configurar variables de entorno
cp .env.example .env

# 3. Levantar
make up
```

El backend corre en `http://localhost:8200` y el frontend en `http://localhost:3200`.

## Crear usuario

```bash
make createsuperuser
```

## Estructura del proyecto

```
stack/
├── docker-compose.yml
├── Makefile
├── .env.example
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── manage.py
│   └── stack_api/
│       ├── settings.py
│       ├── urls.py
│       ├── views.py            # login, logout, me, refresh, google_auth
│       ├── authentication.py   # CookieJWTAuthentication
│       ├── wsgi.py
│       └── asgi.py
└── frontend/
    ├── package.json
    ├── next.config.ts
    └── src/
        ├── types/index.ts
        ├── lib/utils.ts
        ├── components/ui/       # shadcn/ui (button, card, input, label)
        └── app/
            ├── layout.tsx
            ├── page.tsx         # Dashboard
            ├── providers.tsx    # GoogleOAuthProvider + AuthProvider
            ├── login/page.tsx
            ├── contexts/AuthContext.tsx
            └── services/api.ts  # Axios + interceptor refresh
```

## Endpoints API

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/health/` | Health check |
| POST | `/api/auth/login/` | Login con usuario y contraseña |
| POST | `/api/auth/logout/` | Logout (blacklist refresh token) |
| GET | `/api/auth/me/` | Usuario autenticado |
| POST | `/api/auth/refresh/` | Renovar access token |
| POST | `/api/auth/google/` | Login con Google |

## Comandos Make

| Comando | Descripción |
|---------|-------------|
| `make up` | Levantar todos los servicios |
| `make down` | Bajar todos los servicios |
| `make build` | Rebuild de imágenes |
| `make logs` | Ver logs de todos los servicios |
| `make migrate` | Correr migraciones |
| `make createsuperuser` | Crear superusuario |
| `make shell` | Shell de Django |

## Login con Google

1. Crear un proyecto en [Google Cloud Console](https://console.cloud.google.com/)
2. Configurar OAuth 2.0 y obtener el Client ID
3. Agregar las variables en `.env`:

```
GOOGLE_CLIENT_ID=tu-client-id
NEXT_PUBLIC_GOOGLE_CLIENT_ID=tu-client-id
```

## Licencia

MIT
