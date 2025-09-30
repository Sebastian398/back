# Documentación - Reset de Contraseña PlantIQ

## Funcionalidades Implementadas

### 1. Signal Mejorado
- **Archivo**: `irrigation/signals.py`
- **Función**: Envío automático de email con token cuando se solicita reset de contraseña
- **Mejoras**: Token explícito en el contexto, manejo de errores, información detallada del usuario

### 2. Plantillas de Email Profesionales
- **HTML**: `irrigation/templates/email/user_reset_password.html` - Email con formato profesional y responsive
- **Texto**: `irrigation/templates/email/user_reset_password.txt` - Versión de texto plano

### 3. Configuración de Email
- **Archivo**: `backend/settings.py`
- **Configuraciones añadidas**:
  - `EMAIL_BACKEND`
  - `DJANGO_REST_PASSWORDRESET_TOKEN_CONFIG`
  - Configuraciones de timeout y SSL

### 4. Vistas Personalizadas
- **CustomPasswordResetView**: Solicitar reset de contraseña
- **CustomPasswordResetConfirmView**: Confirmar reset con token

### 5. Serializers
- **PasswordResetSerializer**: Validar email
- **PasswordResetConfirmSerializer**: Validar token y nuevas contraseñas

## Endpoints Disponibles

### 1. Solicitar Reset de Contraseña
```
POST /api/password-reset-request/
Content-Type: application/json

{
    "email": "usuario@ejemplo.com"
}
```

**Respuesta Exitosa:**
```json
{
    "mensaje": "Se ha enviado un email de restablecimiento a usuario@ejemplo.com. Revisa tu bandeja de entrada.",
    "token_info": "Token generado para debug: abc123xyz..."
}
```

### 2. Confirmar Reset con Token
```
POST /api/password-reset-confirm/
Content-Type: application/json

{
    "token": "abc123xyz...",
    "password": "nueva_contraseña",
    "password_confirm": "nueva_contraseña"
}
```

**Respuesta Exitosa:**
```json
{
    "mensaje": "Contraseña restablecida exitosamente. Ahora puedes iniciar sesión con tu nueva contraseña."
}
```

### 3. Reset usando django-rest-passwordreset (Método Original)
```
POST /api/password_reset/
Content-Type: application/json

{
    "email": "usuario@ejemplo.com"
}
```

## Pasos para Probar

### 1. Iniciar el servidor
```bash
python manage.py runserver
```

### 2. Crear un usuario de prueba (si no existe)
```bash
python manage.py shell
```
```python
from django.contrib.auth.models import User
user = User.objects.create_user(
    username='test_user',
    email='tu_email@ejemplo.com',  # Usa tu email real
    password='contraseña_antigua',
    first_name='Usuario',
    last_name='Prueba'
)
user.is_active = True
user.save()
```

### 3. Probar Solicitud de Reset
**Con cURL:**
```bash
curl -X POST http://localhost:8000/api/password-reset-request/ \
  -H "Content-Type: application/json" \
  -d '{"email": "tu_email@ejemplo.com"}'
```

**Con Postman/Insomnia:**
- URL: `POST http://localhost:8000/api/password-reset-request/`
- Body (JSON): `{"email": "tu_email@ejemplo.com"}`

### 4. Verificar Email
- Revisa tu email (incluyendo spam)
- El email debe mostrar:
  - Token de restablecimiento claramente visible
  - URL completa para reset
  - Diseño profesional y responsive

### 5. Probar Reset con Token
Usa el token recibido en el email:

```bash
curl -X POST http://localhost:8000/api/password-reset-confirm/ \
  -H "Content-Type: application/json" \
  -d '{
    "token": "TOKEN_DEL_EMAIL",
    "password": "nueva_contraseña_123",
    "password_confirm": "nueva_contraseña_123"
  }'
```

### 6. Verificar Login
Intenta hacer login con la nueva contraseña:

```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "tu_email@ejemplo.com",
    "password": "nueva_contraseña_123"
  }'
```

## Características del Email

### Contenido del Email:
- ✅ **Saludo personalizado** con el nombre del usuario
- ✅ **Token visible** en una sección destacada
- ✅ **URL completa** para reset
- ✅ **Información de seguridad** (expiración, advertencias)
- ✅ **Diseño responsive** que funciona en móviles
- ✅ **Versión HTML y texto plano**

### Información de Seguridad:
- ✅ Token expira en 24 horas
- ✅ Un token por usuario (se eliminan tokens previos)
- ✅ Token se elimina después del uso
- ✅ Validación de email existente

## Debugging

### Ver logs de email en consola:
Los signals ahora muestran información de debug en la consola:
```
Email de reset enviado exitosamente a usuario@ejemplo.com con token: abc123...
```

### Verificar tokens en base de datos:
```python
from django_rest_passwordreset.models import ResetPasswordToken
tokens = ResetPasswordToken.objects.all()
for token in tokens:
    print(f"Usuario: {token.user.email}, Token: {token.key}, Creado: {token.created_at}")
```

### Posibles Errores:
1. **Email no llega**: Verificar configuración SMTP en `settings.py`
2. **Token inválido**: El token puede haber expirado o ya fue usado
3. **Error de autenticación SMTP**: Verificar credenciales de Gmail

## URLs del API Root
Visita `http://localhost:8000/api/` para ver todos los endpoints disponibles, incluyendo los nuevos endpoints de reset de contraseña.