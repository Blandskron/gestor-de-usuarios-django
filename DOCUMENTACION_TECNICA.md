# Arquitectura y Documentación Técnica

Este documento detalla las decisiones arquitectónicas y el modelo de seguridad implementado en el **Gestor de Usuarios API REST**.

---

## 1. Arquitectura de Autenticación y Seguridad

Hemos abandonado la autenticación básica o por tokens opacos en favor de un enfoque *Stateless* robusto basado en **JSON Web Tokens (JWT) asimétricos**.

### 1.1 Firmas Asimétricas (RS256)
En lugar de utilizar el algoritmo tradicional HS256 (que usa una única clave secreta), empleamos **RS256**.
- **Cómo funciona:** El servidor utiliza una llave privada (`private.pem`) para firmar los tokens emitidos en el Login.
- **Ventaja técnica:** Permite que en el futuro un sistema externo (como un microservicio de frontend o un gateway de API) valide la autenticidad del token utilizando **únicamente la llave pública** (`public.pem`), sin necesidad de conocer los secretos de nuestra aplicación.
- **Automatización:** El archivo `core/settings.py` incluye un script con la librería `cryptography` que detecta la ausencia de estas llaves y las genera dinámicamente en formato *TraditionalOpenSSL* a 2048 bits en el primer arranque.

### 1.2 Mitigación de Vulnerabilidades (CSRF)
Al enviar tokens a clientes web (navegadores), existe riesgo de ataques XSS y CSRF.
Para mitigar esto, en la vista de Login (`LoginView`), el servidor devuelve el JWT, pero también acopla la petición con `SessionAuthentication` nativo de Django, configurando una cookie `csrftoken`. 
Esto asegura que las solicitudes posteriores desde un navegador requieran pasar el chequeo de origen cruzado de Django.

### 1.3 Blacklisting de Tokens en Logout
Debido a que los JWT son *stateless* (sin estado), por defecto no pueden ser destruidos en el servidor antes de su fecha de expiración. 
Implementamos el módulo `token_blacklist` de SimpleJWT. Durante el proceso de *Logout*, el Refresh Token suministrado por el cliente se introduce en una base de datos de tokens en lista negra, cortando inmediatamente cualquier intento futuro de obtener nuevos accesos con esa sesión.

---

## 2. Inyección de Claims (RBAC)

Hemos personalizado el serializador `MyTokenObtainPairSerializer` para enriquecer el payload del Access Token. Cuando un cliente decodifica el token en Base64, observará lo siguiente:

```json
{
  "token_type": "access",
  "exp": 1711000000,
  "user_id": 1,
  "username": "admin",
  "grupos": ["Editores", "Auditores"],
  "permisos": ["users.add_user", "users.change_user"]
}
```
*Nota: Si el usuario es un cliente estándar sin roles administrativos, el sistema devuelve proactivamente `grupos: []` y `permisos: []` para evitar errores de `undefined` en el parseo del lado del Frontend.*

---

## 3. Estructura de Endpoints

| Endpoint | Método | Descripción | Permisos |
|----------|--------|-------------|----------|
| `/api/users/login/` | `POST` | Emite Access y Refresh tokens. | Público |
| `/api/users/logout/` | `POST` | Invalida el Refresh token. | Autenticado |
| `/api/users/token/refresh/` | `POST` | Renueva el Access token usando el Refresh. | Público (Requiere Token) |
| `/api/users/crud/` | `GET`, `POST` | Lista o crea nuevos usuarios. | Administrador |
| `/api/users/crud/<id>/` | `GET`, `PUT`, `DELETE`| Modifica un usuario específico. | Administrador |

Todo el CRUD se expone a través del poderoso `ModelViewSet` y está completamente documentado con el estándar **OpenAPI 3.0** servido vía Swagger/ReDoc.