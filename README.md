# ⚽ Premier League Manager — Secure Web Application

Aplicación web desarrollada con **Flask + Dash** para gestionar equipos de fútbol.

El proyecto demuestra un despliegue seguro utilizando:

- Docker
- Jenkins (CI/CD)
- API REST
- Tests con Postman
- Seguridad basada en OWASP Top 10

---

# 🏗 Arquitectura

La aplicación se ejecuta mediante contenedores Docker.


Usuario
↓
Flask + Dash (web)
↓
API REST
↓
MariaDB

CI/CD:

GitHub → Jenkins → Docker → Tests


---

# 🚀 Ejecución rápida

## 1️⃣ Clonar el repositorio


git clone https://github.com/usuario/trabajoFinal.git

cd trabajoFinal


---

## 2️⃣ Crear archivo `.env`


MARIADB_DATABASE=trabajoFinal
MARIADB_USER=trabajoFinal
MARIADB_PASSWORD=trabajoFinal
MARIADB_ROOT_PASSWORD=rootpassword

DATABASE_URL=mysql+pymysql://trabajoFinal:trabajoFinal@db:3306/trabajoFinal
API_BASE_URL=http://127.0.0.1:5000/api


---

## 3️⃣ Ejecutar con Docker


docker compose up --build


Esto iniciará:

| Servicio | Descripción |
|--------|-------------|
| web | aplicación Flask + Dash |
| db | base de datos MariaDB |

---

## 4️⃣ Abrir la aplicación


http://localhost:5000


---

# 👤 Usuarios disponibles

La base de datos se inicializa automáticamente con:

| Usuario | Password | Rol |
|------|------|------|
| admin | admin123 | administrador |
| user | user123 | usuario |

---

# 📊 Funcionalidades

### Administrador
- ver equipos
- crear equipos
- editar equipos
- eliminar equipos

### Usuario normal
- ver equipos

---

# 🔌 API REST

Endpoints principales:

| Método | Endpoint | Descripción |
|------|------|------|
| GET | /api/health | comprobar API |
| POST | /api/auth/login | login |
| POST | /api/auth/logout | logout |
| GET | /api/teams | listar equipos |
| POST | /api/teams | crear equipo (admin) |
| PUT | /api/teams/{id} | editar equipo (admin) |
| DELETE | /api/teams/{id} | eliminar equipo (admin) |

---

# 🧪 Tests con Postman

Se incluye una colección Postman para probar la API.

Tests incluidos:

- health check
- login admin
- login user
- control de permisos
- CRUD de equipos

Para ejecutarlos:

1. Importar la colección en **Postman**
2. Ejecutar **Collection Runner**

Resultado esperado:


All tests passed


---

# ⚙ CI/CD con Jenkins

El proyecto incluye automatización con Jenkins.

Pipeline definido en:


Jenkinsfile


El pipeline realiza:

1. Checkout del repositorio
2. Build de contenedores Docker
3. Inicialización de base de datos
4. Ejecución de tests
5. Despliegue de la aplicación

Cada **push en GitHub** activa el pipeline automáticamente.

---

# 🐳 Docker

Docker permite ejecutar la aplicación en un entorno reproducible.

Contenedores utilizados:

| Contenedor | Función |
|-----------|---------|
| web | aplicación Flask |
| db | base de datos MariaDB |

Ventajas:

- aislamiento
- despliegue sencillo
- entorno reproducible

---

# 🌿 Control de versiones

Se ha utilizado Git con:
- rama main
- ramas de desarrollo para nuevas funcionalidades
- merge posterior mediante pull requests

---

# 🔐 Seguridad (OWASP Top 10)

Se aplican varias prácticas de seguridad:

A01 — Broken Access Control

        Descripción

        Ocurre cuando los usuarios pueden acceder a recursos o acciones para las que no tienen permisos.

        Implementación en el proyecto

        Se ha implementado control de roles:

        admin

        user

        Solo los administradores pueden:

        crear equipos

        editar equipos

        eliminar equipos

        Dónde se aplica

        Archivo:

        app/security.py

        Decorador utilizado:

        @admin_required

        También se valida en la interfaz web (dashapp.py) ocultando los controles de administración a usuarios normales.

A02 — Cryptographic Failures

        Descripción

        Ocurre cuando información sensible (como contraseñas) se almacena sin protección.

        Implementación en el proyecto

        Las contraseñas se almacenan utilizando hash seguro con bcrypt.

        Esto evita almacenar contraseñas en texto plano.

        Dónde se aplica

        Archivo:

        app/models.py

        Método utilizado:

        bcrypt.hash(password)

        Verificación de contraseña:

        bcrypt.verify(password, self.password_hash)

A03 — Injection

        Descripción

        Ataques como SQL Injection ocurren cuando el usuario puede inyectar código SQL en consultas.

        Implementación en el proyecto

        La aplicación utiliza SQLAlchemy ORM, que evita la construcción manual de consultas SQL.

        Esto previene ataques de inyección.

        Dónde se aplica

        Archivo:

        app/models.py

        Ejemplo:

        Team.query.filter_by(id=id).first()

A05 — Security Misconfiguration

        Descripción

        Errores de configuración del servidor o del entorno que pueden exponer la aplicación.

        Implementación en el proyecto

        La aplicación se ejecuta en contenedores Docker, lo que permite:

        aislar servicios

        controlar dependencias

        reproducir el entorno

        Dónde se aplica

        Archivos:

        Dockerfile
        docker-compose.yml

        Servicios definidos:

        contenedor web

        contenedor base de datos

A07 — Identification and Authentication Failures

        Descripción

        Problemas en la gestión de autenticación de usuarios.

        Implementación en el proyecto

        Se utiliza Flask-Login para gestionar sesiones de usuario de forma segura.

        Características implementadas:

        login

        logout

        control de sesión

        usuario autenticado

        Dónde se aplica

        Archivo:

        app/auth.py

        Funciones utilizadas:

        login_user(user)
        logout_user()
        current_user

A09 — Security Logging and Monitoring Failures

        Descripción

        Falta de registros que permitan detectar problemas de seguridad.

        Implementación en el proyecto

        Se utilizan logs en:

        Jenkins

        Docker

        Flask

        Esto permite registrar:

        ejecuciones de pipeline

        errores

        builds fallidos

        Dónde se aplica

        Archivos:

        Jenkinsfile
        docker-compose.yml

        Además Jenkins registra cada ejecución del pipeline.

También se han aplicado buenas prácticas de seguridad en la API:
- autenticación en endpoints
- control de permisos
- validación de datos

---

# 📂 Tests automáticos

El proyecto incluye tests unitarios con pytest.


pytest


Ubicación:


tests/

---

## Tests de API con Postman

Se incluye una colección de Postman en:

postman/trabajoFinal_postman_collection.json

### Importar la colección

1. Abrir Postman
2. Pulsar **Import**
3. Seleccionar el archivo JSON
4. Ejecutar la colección con **Collection Runner**

La colección incluye tests para:

- Health check
- Login
- Crear equipo
- Modificar equipo
- Borrar equipo
- Tests de seguridad

---

# 👨‍💻 Autor

Proyecto desarrollado para la asignatura **Puesta en Producción Segura**.

Autor: **José Manuel Oliver**