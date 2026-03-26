# API REST - Sistema de Gestión de Usuarios Avanzado

Este es un proyecto backend de nivel profesional construido con **Django** y **Django REST Framework (DRF)**. Proporciona una API robusta, documentada y segura para la gestión integral de usuarios.

## 🛡️ Características Principales

- **Seguridad de Vanguardia (JWT + RSA):** Autenticación mediante JSON Web Tokens firmados con algoritmos asimétricos (RS256 con claves pública y privada).
- **Protección CSRF:** Mitigación de ataques de falsificación de peticiones entre sitios combinando Session Authentication con JWT.
- **Autorización Basada en Roles (RBAC):** Inyección automática de los `grupos` y `permisos` del usuario en el payload del Access Token.
- **Control de Acceso Riguroso:** Operaciones CRUD limitadas estrictamente a usuarios Administradores (`IsAdminUser`).
- **Blacklisting de Tokens:** Cierre de sesión seguro mediante la invalidación de Refresh Tokens.
- **Documentación Interactiva:** Interfaces Swagger UI y ReDoc generadas automáticamente con `drf-spectacular`.

## 🚀 Tecnologías Utilizadas

- Python 3.x
- Django 5.x / 6.x
- Django REST Framework
- SimpleJWT (con soporte RS256)
- Cryptography
- DRF Spectacular (OpenAPI 3.0)

## ⚙️ Estructura y Funcionamiento

El proyecto utiliza una estrategia de generación de llaves RSA automática. Al iniciar el servidor por primera vez, se generarán los archivos `private.pem` y `public.pem` en la raíz del proyecto, asegurando un entorno *plug-and-play* seguro sin configuraciones manuales complejas.

## 📖 Documentación de la API

Una vez que el servidor esté en ejecución, puedes explorar los *endpoints* interactivos en:
- **Swagger UI:** `/docs/api/schema/swagger-ui/`
- **ReDoc:** `/docs/api/schema/redoc/`

## 🛠️ Instalación y Uso

Consulta el archivo COMANDOS.md para ver la guía paso a paso sobre cómo inicializar y ejecutar este proyecto.

Para conocer en detalle las decisiones de arquitectura y flujos de seguridad, revisa la DOCUMENTACION_TECNICA.md.
