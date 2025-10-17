# 🚀 Deploy a Render - Tienda Online

## 📋 Pasos para subir a Render

### **1. Preparar el repositorio:**
```bash
# Asegúrate de que todos los archivos estén en Git
git add .
git commit -m "Preparar para deploy en Render"
git push origin main
```

### **2. Crear cuenta en Render:**
1. Ve a [render.com](https://render.com)
2. Regístrate con GitHub
3. Conecta tu repositorio

### **3. Configurar base de datos Neon:**
1. Ve a [neon.tech](https://neon.tech)
2. Crea una cuenta o inicia sesión
3. Crea un nuevo proyecto:
   - **Name**: `tienda-db`
   - **Database**: `tienda`
   - **Region**: Elige la más cercana
4. Copia la **Connection String** (la necesitarás después)
5. **Importante**: La URL de Neon ya está en formato `postgresql://`

### **4. Deploy del Backend:**
1. En el dashboard, haz clic en "New +"
2. Selecciona "Web Service"
3. Conecta tu repositorio de GitHub
4. Configura:
   - **Name**: `tienda-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && python app.py`
   - **Plan**: Free

5. **Variables de entorno**:
   Las variables públicas ya están configuradas en `render.yaml`. Solo necesitas configurar manualmente estas variables sensibles:
   ```
   DB_PASSWORD=npg_xzi8dDsBS2KG
   JWT_SECRET=roqR6n_BJSpJswL35kvEAFunSpy23O_VKsUaMzoMW_A
   OPENAI_API_KEY=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
   SMTP_PASSWORD=uwep xrck lmwk knyt
   ```
   **Ver archivo `RENDER_ENV_VARS.md` para instrucciones detalladas**

### **5. Deploy del Frontend:**
1. En el dashboard, haz clic en "New +"
2. Selecciona "Static Site"
3. Conecta tu repositorio de GitHub
4. Configura:
   - **Name**: `tienda-frontend`
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Publish Directory**: `frontend/.output/public`
   - **Plan**: Free

5. **Variables de entorno**:
   ```
   NUXT_PUBLIC_API_BASE=https://tienda-backend.onrender.com
   ```

### **6. Configurar migraciones de base de datos:**
Después del primer deploy del backend, ejecuta las migraciones:
```bash
# En la consola del backend en Render
cd backend
python -m flask db upgrade
```

### **7. URLs finales:**
- **Frontend**: `https://tienda-frontend.onrender.com`
- **Backend**: `https://tienda-backend.onrender.com`
- **Base de datos**: PostgreSQL en Render

## 🔧 Solución de problemas comunes:

### **Error de CORS:**
- Verifica que `CORS_ORIGINS` incluya la URL del frontend
- Asegúrate de que el backend esté configurado para producción

### **Error de base de datos:**
- Verifica que `DATABASE_URL` esté correctamente configurada
- Ejecuta las migraciones: `python -m flask db upgrade`

### **Error de build del frontend:**
- Verifica que `NUXT_PUBLIC_API_BASE` apunte al backend
- Revisa los logs de build para errores específicos

## 📝 Notas importantes:

1. **Plan gratuito**: Tiene limitaciones (sleep después de 15 min de inactividad)
2. **Variables de entorno**: Nunca subas claves secretas al repositorio
3. **Logs**: Usa el dashboard de Render para monitorear errores
4. **Dominio personalizado**: Puedes configurar un dominio propio más tarde

## 🎉 ¡Listo!
Tu aplicación estará disponible en las URLs de Render y funcionando en producción.
