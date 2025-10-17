# 🔐 Variables de Entorno para Render

## 📋 Variables que debes configurar manualmente en Render:

### **🔑 Variables sensibles (sync: false):**
Estas variables contienen información sensible y debes configurarlas manualmente en el dashboard de Render:

```
DB_PASSWORD=npg_xzi8dDsBS2KG
JWT_SECRET=roqR6n_BJSpJswL35kvEAFunSpy23O_VKsUaMzoMW_A
OPENAI_API_KEY=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
SMTP_PASSWORD=uwep xrck lmwk knyt
```

## 🚀 Pasos para configurar en Render:

### **1. Después del deploy inicial:**
1. Ve al dashboard de Render
2. Selecciona tu servicio backend (`arrozales-backend`)
3. Ve a la pestaña "Environment"
4. Haz clic en "Add Environment Variable"

### **2. Agregar cada variable:**
```
Key: DB_PASSWORD
Value: npg_xzi8dDsBS2KG

Key: JWT_SECRET
Value: roqR6n_BJSpJswL35kvEAFunSpy23O_VKsUaMzoMW_A

Key: OPENAI_API_KEY
Value: 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

Key: SMTP_PASSWORD
Value: uwep xrck lmwk knyt
```

### **3. Reiniciar el servicio:**
Después de agregar todas las variables, haz clic en "Manual Deploy" para reiniciar el servicio.

## ✅ Variables ya configuradas automáticamente:

Estas variables ya están configuradas en `render.yaml` y se aplicarán automáticamente:

```
ENVIRONMENT=production
DB_NAME=neondb
DB_USER=neondb_owner
DB_HOST=ep-broad-violet-ad1tmk0n-pooler.c-2.us-east-1.aws.neon.tech
DB_PORT=5432
JWT_EXPIRES_MINUTES=3
JWT_REFRESH_EXPIRES_MINUTES=60
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=jacevedoj@miumg.edu.gt
FROM_EMAIL=jacevedoj@miumg.edu.gt
FRONTEND_URL=https://arrozales-frontend.onrender.com
```

## 🔍 Verificar configuración:

### **En los logs de Render:**
Busca mensajes como:
```
✅ Database connected successfully
✅ JWT configuration loaded
✅ SMTP configuration loaded
✅ OpenAI API key loaded
```

### **URL de conexión construida:**
La aplicación construirá automáticamente esta URL:
```
postgresql://neondb_owner:npg_xzi8dDsBS2KG@ep-broad-violet-ad1tmk0n-pooler.c-2.us-east-1.aws.neon.tech:5432/neondb?sslmode=require
```

## ⚠️ Notas de seguridad:

1. **Nunca subas** estas variables al repositorio
2. **Usa sync: false** para variables sensibles
3. **Rota las claves** periódicamente
4. **Monitorea** el acceso a las APIs

## 🎉 ¡Listo!
Una vez configuradas todas las variables, tu aplicación estará completamente funcional en Render.
