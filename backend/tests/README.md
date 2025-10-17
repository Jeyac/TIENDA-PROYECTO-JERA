# Tests del Backend

Esta carpeta contiene todos los tests del backend organizados por categorías.

## Estructura

```
tests/
├── README.md                           # Este archivo
├── test_validaciones_usuarios.py       # Tests de validaciones de usuarios
├── conftest.py                         # Configuración de pytest
├── entities/                           # Tests de entidades de dominio
│   ├── test_usuario_entity.py
│   ├── test_pedido_entity.py
│   └── test_producto_entity.py
└── use_cases/                          # Tests de casos de uso
    ├── test_pedidos_use_cases.py
    └── test_productos_use_cases.py
```

## Ejecutar Tests

### Todos los tests:
```bash
cd backend
python -m pytest tests/
```

### Tests específicos:
```bash
# Solo tests de validaciones
python -m pytest tests/test_validaciones_usuarios.py

# Solo tests de entidades
python -m pytest tests/entities/

# Solo tests de casos de uso
python -m pytest tests/use_cases/
```

### Con verbose:
```bash
python -m pytest tests/ -v
```

## Tests Disponibles

### 1. Validaciones de Usuarios (`test_validaciones_usuarios.py`)
- ✅ Registro de usuario válido
- ✅ Validación de username duplicado
- ✅ Validación de email duplicado
- ✅ Validación de username muy corto
- ✅ Validación de email inválido
- ✅ Validación de contraseña muy corta
- ✅ Verificación de disponibilidad de username
- ✅ Verificación de disponibilidad de email

### 2. Entidades (`entities/`)
- ✅ Test de entidad Usuario
- ✅ Test de entidad Pedido
- ✅ Test de entidad Producto

### 3. Casos de Uso (`use_cases/`)
- ✅ Test de casos de uso de Pedidos
- ✅ Test de casos de uso de Productos

## Requisitos

- El servidor Flask debe estar ejecutándose en `http://localhost:5000` para los tests de validaciones
- Base de datos configurada correctamente
- Todas las dependencias instaladas

## Notas

- Los tests de validaciones requieren conexión al servidor
- Los tests de entidades y casos de uso son unitarios
- Usar `conftest.py` para configuración común de tests
