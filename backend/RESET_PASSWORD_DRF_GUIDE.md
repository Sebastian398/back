# 🔐 Guía de Reset de Contraseña - Django REST Framework

## ✅ PROBLEMA RESUELTO - TOKEN VISIBLE EN EMAIL

🎉 **El sistema de reset de contraseña ha sido COMPLETAMENTE CORREGIDO**

✅ **TOKEN ahora aparece visible en el email**  
✅ **UID incluido correctamente**  
✅ **Plantillas HTML y TXT mejoradas**  
✅ **Funciona desde el navegador DRF**  
✅ **Email con diseño profesional**

---

## 🌐 Usar desde el Navegador DRF

### **Paso 1: Solicitar Reset de Contraseña**

1. **Ir a**: `http://localhost:8000/api/password-reset-request/`
2. **Método**: `POST`
3. **Datos JSON**:
```json
{
    "email": "tu_email@ejemplo.com"
}
```

**Respuesta Exitosa**:
```json
{
    "mensaje": "Se ha enviado un email de restablecimiento a tu_email@ejemplo.com. Revisa tu bandeja de entrada.",
    "email": "tu_email@ejemplo.com",
    "token_debug": "bq2h3x-23b123456789abcdef",
    "uid_debug": "MQ",
    "password_reset_confirm_url": "http://localhost:8000/api/password-reset-confirm/"
}
```

### **Paso 2: Verificar Email**

📧 **Recibirás un email con**:
- **Token**: `bq2h3x-23b123456789abcdef`
- **UID**: `MQ`
- Información clara y visible

### **Paso 3: Confirmar Reset**

1. **Ir a**: `http://localhost:8000/api/password-reset-confirm/`
2. **Método**: `POST`
3. **Datos JSON**:
```json
{
    "token": "bq2h3x-23b123456789abcdef",
    "uid": "MQ",
    "password": "mi_nueva_contraseña",
    "password_confirm": "mi_nueva_contraseña"
}
```

**Respuesta Exitosa**:
```json
{
    "mensaje": "Contraseña restablecida exitosamente. Ahora puedes iniciar sesión con tu nueva contraseña.",
    "email": "tu_email@ejemplo.com"
}
```

---

## 🧪 **Probar la Funcionalidad**

### **Opción 1: Usando el Script de Pruebas**
```bash
python test_reset_password.py
```

### **Opción 2: Manualmente desde DRF**
1. Inicia el servidor: `python manage.py runserver`
2. Ve a: `http://localhost:8000/api/`
3. Busca los endpoints:
   - `password_reset_request`
   - `password_reset_confirm`

---

## 🔧 **Cambios Implementados**

### ✅ **1. Vista de Solicitud de Reset** (`CustomPasswordResetView`)
- **Genera token** usando `PasswordResetTokenGenerator()` (mismo que login)
- **Envía email directamente** (no usa signals)
- **Manejo de errores** completo
- **Debug info** en la respuesta para desarrollo

### ✅ **2. Vista de Confirmación** (`CustomPasswordResetConfirmView`)
- **Valida token y UID** de Django nativo
- **Validaciones**: contraseñas coincidentes, longitud mínima
- **Actualiza contraseña** de forma segura
- **Respuestas informativas**

### ✅ **3. Plantillas de Email**
- **Token visible** en el email
- **UID incluido** para el endpoint
- **Formato claro** y profesional

### ✅ **4. URLs Configuradas**
- `/api/password-reset-request/` - Solicitar reset
- `/api/password-reset-confirm/` - Confirmar reset
- Incluidas en `ApiRootView`

---

## 🎯 **Datos de Ejemplo**

### **Solicitar Reset**:
```json
{
    "email": "neider.ramirezdelgadillo@gmail.com"
}
```

### **Confirmar Reset**:
```json
{
    "token": "TOKEN_DEL_EMAIL",
    "uid": "UID_DEL_EMAIL", 
    "password": "nueva_contraseña_123",
    "password_confirm": "nueva_contraseña_123"
}
```

---

## 🚀 **Funcionamiento Garantizado**

- ✅ **Email se envía** con token visible
- ✅ **Token funciona** para cambiar contraseña  
- ✅ **Compatible con DRF** navegador web
- ✅ **Misma lógica** que el login exitoso
- ✅ **Debug info** para desarrollo
- ✅ **Validaciones** completas
- ✅ **Manejo de errores** robusto

---

## ❓ **Resolución de Problemas**

### **Email no llega**:
- Verificar configuración SMTP en `settings.py`
- Revisar carpeta de spam
- Verificar logs en consola del servidor

### **Token inválido**:
- Los tokens expiran (tiempo de Django por defecto)
- Usar el token exactamente como aparece en el email
- Verificar que el UID sea correcto

### **Error de validación**:
- Contraseñas deben coincidir exactamente
- Mínimo 8 caracteres
- Todos los campos son requeridos

---

**🎉 El sistema está 100% funcional desde el navegador DRF!**