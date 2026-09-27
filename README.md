
# StyleBook

Sistema web desarrollado en Flask para la gestión, reserva y administración de servicios profesionales y perfiles de usuario, integrado con Supabase como backend de base de datos.

---

## Características Principales (Features)

* **Autenticación y Registro:** Sistema de gestión de usuarios con soporte para inicio de sesión, registro y control de sesiones seguras.
* **Gestión de Perfiles:** Módulo para que los usuarios visualicen y editen la información de su perfil personal.
* **Directorio y Detalle de Profesionales:** Listado público de profesionales disponibles, con páginas de detalle individual y opciones de registro especializado.
* **Administración de Servicios:** Módulos para listar, crear, gestionar y solicitar servicios ofrecidos en la plataforma.
* **Panel de Administración:** Interfaz reservada para la supervisión y control global del sistema (usuarios, servicios y registros).
* **Base de Datos Relacional y Esquema SQL:** Estructura inicial y configuración gestionada mediante esquemas SQL compatibles con Supabase.

---

## Tecnologías Utilizadas

* **Python 3.13:** Lenguaje de programación principal para la lógica del backend.
* **Flask (v3.0.3):** Microframework web utilizado para estructurar rutas, vistas y la arquitectura modular mediante Blueprints.
* **Supabase (v2.7.4):** Plataforma backend como servicio (BaaS) utilizada para la persistencia de datos y gestión de base de datos.
* **Python-Dotenv (v1.0.1):** Librería para la gestión de variables de entorno de forma segura.
* **HTML5 / CSS3 / Jinja2:** Tecnologías de renderizado y diseño frontend para las plantillas y estilos personalizados (`estilos.css`).

---

## Arquitectura y Estructura de Directorios

El proyecto sigue una estructura modular basada en Flask Blueprints:

```text
stylebook-main/
│
└── stylebook/
    ├── blueprints/          # Módulos lógicos de la aplicación (Blueprints)
    │   ├── admin.py         # Panel y funciones de administración
    │   ├── auth.py          # Autenticación (Login / Registro)
    │   ├── perfil.py        # Visualización y edición de perfiles
    │   ├── profesionales.py # Listado, detalle y registro de profesionales
    │   └── servicios.py     # Gestión y listado de servicios
    ├── db/
    │   └── schema.sql       # Esquema y scripts de la base de datos
    ├── static/
    │   └── css/
    │       └── estilos.css  # Estilos CSS globales de la interfaz
    ├── templates/           # Plantillas HTML estructuradas por módulos
    │   ├── admin/           # Vistas del panel de administración
    │   ├── auth/            # Vistas de autenticación (login, registro)
    │   ├── perfil/          # Vistas de perfil de usuario
    │   ├── profesionales/   # Vistas de listado y detalle de profesionales
    │   ├── servicios/       # Vistas de gestión y formularios de servicios
    │   ├── base.html        # Plantilla base compartida
    │   └── index.html       # Página de inicio
    ├── app.py               # Archivo principal de inicialización de Flask
    ├── requirements.txt     # Dependencias del proyecto Python
    ├── supabase_client.py   # Configuración e inicialización del cliente de Supabase
    └── utilidades.py        # Funciones auxiliares y de soporte

```

---

## Instalación y Configuración (Prerrequisitos)

### Prerrequisitos

* Tener instalado **Python** (versión 3.13 recomendada).
* Tener instalado **pip** (gestor de paquetes de Python).
* Una cuenta y proyecto activo en **Supabase**.

### Pasos de Instalación

1. **Clonar el repositorio o descomprimir el proyecto:**
```bash
cd stylebook-main/stylebook

```


2. **Crear y activar un entorno virtual:**
* En Windows:
```bash
python -m venv venv
venv\Scripts\activate

```


* En macOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate

```




3. **Instalar las dependencias:**
```bash
pip install -r requirements.txt

```


4. **Configurar las Variables de Entorno:**
Crea un archivo `.env` en la carpeta raíz del proyecto (`stylebook/`) y define las credenciales de tu conexión con Supabase:
```env
SUPABASE_URL=tu_supabase_url_aqui
SUPABASE_KEY=tu_supabase_anon_key_aqui
SECRET_KEY=tu_flask_secret_key_aqui

```


5. **Configurar la Base de Datos:**
Ejecuta el script SQL ubicado en `db/schema.sql` dentro de tu consola SQL de Supabase para inicializar las tablas necesarias.

---

## Ejecución y Uso

### Modo Desarrollo

Para poner en marcha el servidor local de desarrollo con recarga automática:

```bash
python app.py

```

O bien utilizando el comando de Flask:

```bash
flask --app app run --debug

```

La aplicación estará disponible por defecto en `[http://127.0.0.1:5000](http://127.0.0.1:5000)`.

### Modo Producción

Para entornos de producción, se recomienda utilizar un servidor WSGI como Gunicorn:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app

```

---

## Guía de Contribución

¡Las contribuciones son bienvenidas! Si deseas reportar un error, sugerir una mejora o enviar una Pull Request, por favor sigue estos pasos:

1. Haz un Fork del repositorio.
2. Crea una rama nueva para tu característica (`git checkout -b feature/nueva-caracteristica`).
3. Realiza tus cambios y commitealos (`git commit -m 'Agrega nueva característica'`).
4. Sube los cambios a tu rama (`git push origin feature/nueva-caracteristica`).
5. Abre una Pull Request detallando los cambios introducidos.

---

## Licencia

# StyleBook

Sistema web desarrollado en Flask para la gestión, reserva y administración de servicios profesionales y perfiles de usuario, integrado con Supabase como backend de base de datos.

---

## Características Principales (Features)

* **Autenticación y Registro:** Sistema de gestión de usuarios con soporte para inicio de sesión, registro y control de sesiones seguras.
* **Gestión de Perfiles:** Módulo para que los usuarios visualicen y editen la información de su perfil personal.
* **Directorio y Detalle de Profesionales:** Listado público de profesionales disponibles, con páginas de detalle individual y opciones de registro especializado.
* **Administración de Servicios:** Módulos para listar, crear, gestionar y solicitar servicios ofrecidos en la plataforma.
* **Panel de Administración:** Interfaz reservada para la supervisión y control global del sistema (usuarios, servicios y registros).
* **Base de Datos Relacional y Esquema SQL:** Estructura inicial y configuración gestionada mediante esquemas SQL compatibles con Supabase.

---

## Tecnologías Utilizadas

* **Python 3.13:** Lenguaje de programación principal para la lógica del backend.
* **Flask (v3.0.3):** Microframework web utilizado para estructurar rutas, vistas y la arquitectura modular mediante Blueprints.
* **Supabase (v2.7.4):** Plataforma backend como servicio (BaaS) utilizada para la persistencia de datos y gestión de base de datos.
* **Python-Dotenv (v1.0.1):** Librería para la gestión de variables de entorno de forma segura.
* **HTML5 / CSS3 / Jinja2:** Tecnologías de renderizado y diseño frontend para las plantillas y estilos personalizados (`estilos.css`).

---

## Arquitectura y Estructura de Directorios

El proyecto sigue una estructura modular basada en Flask Blueprints:

```text
stylebook-main/
│
└── stylebook/
    ├── blueprints/          # Módulos lógicos de la aplicación (Blueprints)
    │   ├── admin.py         # Panel y funciones de administración
    │   ├── auth.py          # Autenticación (Login / Registro)
    │   ├── perfil.py        # Visualización y edición de perfiles
    │   ├── profesionales.py # Listado, detalle y registro de profesionales
    │   └── servicios.py     # Gestión y listado de servicios
    ├── db/
    │   └── schema.sql       # Esquema y scripts de la base de datos
    ├── static/
    │   └── css/
    │       └── estilos.css  # Estilos CSS globales de la interfaz
    ├── templates/           # Plantillas HTML estructuradas por módulos
    │   ├── admin/           # Vistas del panel de administración
    │   ├── auth/            # Vistas de autenticación (login, registro)
    │   ├── perfil/          # Vistas de perfil de usuario
    │   ├── profesionales/   # Vistas de listado y detalle de profesionales
    │   ├── servicios/       # Vistas de gestión y formularios de servicios
    │   ├── base.html        # Plantilla base compartida
    │   └── index.html       # Página de inicio
    ├── app.py               # Archivo principal de inicialización de Flask
    ├── requirements.txt     # Dependencias del proyecto Python
    ├── supabase_client.py   # Configuración e inicialización del cliente de Supabase
    └── utilidades.py        # Funciones auxiliares y de soporte

```

---

## Instalación y Configuración (Prerrequisitos)

### Prerrequisitos

* Tener instalado **Python** (versión 3.13 recomendada).
* Tener instalado **pip** (gestor de paquetes de Python).
* Una cuenta y proyecto activo en **Supabase**.

### Pasos de Instalación

1. **Clonar el repositorio o descomprimir el proyecto:**
```bash
cd stylebook-main/stylebook

```


2. **Crear y activar un entorno virtual:**
* En Windows:
```bash
python -m venv venv
venv\Scripts\activate

```


* En macOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate

```




3. **Instalar las dependencias:**
```bash
pip install -r requirements.txt

```


4. **Configurar las Variables de Entorno:**
Crea un archivo `.env` en la carpeta raíz del proyecto (`stylebook/`) y define las credenciales de tu conexión con Supabase:
```env
SUPABASE_URL=tu_supabase_url_aqui
SUPABASE_KEY=tu_supabase_anon_key_aqui
SECRET_KEY=tu_flask_secret_key_aqui

```


5. **Configurar la Base de Datos:**
Ejecuta el script SQL ubicado en `db/schema.sql` dentro de tu consola SQL de Supabase para inicializar las tablas necesarias.

---

## Ejecución y Uso

### Modo Desarrollo

Para poner en marcha el servidor local de desarrollo con recarga automática:

```bash
python app.py

```

O bien utilizando el comando de Flask:

```bash
flask --app app run --debug

```

La aplicación estará disponible por defecto en `[http://127.0.0.1:5000](http://127.0.0.1:5000)`.

### Modo Producción

Para entornos de producción, se recomienda utilizar un servidor WSGI como Gunicorn:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app

```

---

## Guía de Contribución

¡Las contribuciones son bienvenidas! Si deseas reportar un error, sugerir una mejora o enviar una Pull Request, por favor sigue estos pasos:

1. Haz un Fork del repositorio.
2. Crea una rama nueva para tu característica (`git checkout -b feature/nueva-caracteristica`).
3. Realiza tus cambios y commitealos (`git commit -m 'Agrega nueva característica'`).
4. Sube los cambios a tu rama (`git push origin feature/nueva-caracteristica`).
5. Abre una Pull Request detallando los cambios introducidos.

---

## Licencia


Este proyecto se encuentra bajo los términos de la licencia especificada en el repositorio. Consulta el archivo de licencia para más detalles.