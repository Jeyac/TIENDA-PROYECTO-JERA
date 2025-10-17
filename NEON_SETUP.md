# 🗄️ Configuración de Neon Database

## 📋 Pasos para configurar Neon

### **1. Crear cuenta en Neon:**
1. Ve a [neon.tech](https://neon.tech)
2. Haz clic en "Sign Up"
3. Conecta con GitHub o crea cuenta con email

### **2. Crear nuevo proyecto:**
1. Haz clic en "Create Project"
2. Configura:
   - **Name**: `tienda-database`
   - **Database Name**: `tienda`
   - **Region**: Elige la más cercana (ej: `us-east-1`)
   - **PostgreSQL Version**: `15` (recomendado)

### **3. Obtener Connection String:**
1. En el dashboard de Neon, ve a "Connection Details"
2. Copia la **Connection String** que se ve así:
   ```
   postgresql://username:password@ep-xxx-xxx.us-east-1.aws.neon.tech/tienda?sslmode=require
   ```

### **4. Configurar en Render:**
1. En el dashboard de Render, ve a tu servicio backend
2. Ve a "Environment"
3. Agrega la variable:
   - **Key**: `DATABASE_URL`
   - **Value**: `postgresql://username:password@ep-xxx-xxx.us-east-1.aws.neon.tech/tienda?sslmode=require`

## 🔧 Ventajas de usar Neon:

### **✅ Beneficios:**
- **Gratuito**: Plan gratuito generoso
- **Serverless**: Se escala automáticamente
- **Rápido**: Conexiones instantáneas
- **Seguro**: SSL por defecto
- **Fácil**: Configuración simple

### **🆚 vs PostgreSQL de Render:**
- **Neon**: Más rápido, serverless, mejor para desarrollo
- **Render PostgreSQL**: Integrado, pero más lento para conectar

## 🚀 Migraciones con Neon:

### **Ejecutar migraciones:**
```bash
# En la consola del backend en Render
cd backend
python -m flask db upgrade
```

### **Crear migraciones:**
```bash
# En local (si necesitas crear nuevas migraciones)
cd backend
python -m flask db migrate -m "Descripción del cambio"
python -m flask db upgrade
```

## 🔍 Verificar conexión:

### **En los logs de Render:**
Busca mensajes como:
```
✅ Database connected successfully
✅ Tables created/updated
```

### **En Neon Dashboard:**
1. Ve a "Queries"
2. Ejecuta: `SELECT * FROM information_schema.tables;`
3. Deberías ver las tablas de tu aplicación

## ⚠️ Notas importantes:

1. **SSL**: Neon requiere SSL (`sslmode=require`)
2. **Conexiones**: Neon maneja las conexiones automáticamente
3. **Backup**: Neon hace backups automáticos
4. **Límites**: Plan gratuito tiene límites de uso (suficiente para desarrollo)

## 🎉 ¡Listo!
Tu base de datos Neon estará funcionando con Render.

