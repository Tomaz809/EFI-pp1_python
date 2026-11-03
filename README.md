# API de Gestión Académica

Proyecto de la EFI de Práctica Profesionalizante I: Python (ITEC Río Cuarto). Expone una API REST modular para administrar alumnos, carreras, materias y las correlatividades entre materias, construida con FastAPI, SQLModel, SQLite y Alembic.

## Integrantes

- Juan Ignacio Andrada Guzman - [@juanignacioandrada20-gif](https://github.com/juanignacioandrada20-gif)
- Tomas Castelo - [@Tomaz809](https://github.com/Tomaz809)
- Lautaro Ocanto - [@laautisz](https://github.com/laautisz)
- Geronimo Martin Torasso - [@Gerot1234](https://github.com/Gerot1234)

## Requisitos Previos

- Python 3.12
- [uv](https://docs.astral.sh/uv/) (administrador de paquetes y entornos virtuales)
- Git

## Instalación y Ejecución

1. *Clonar el repositorio y ubicarse en la raíz del proyecto:*
   ```bash
   git clone https://github.com/Tomaz809/EFI-pp1_python
   cd EFI-pp1_python
   ```

2. *Sincronizar el entorno e instalar dependencias:*
   ```bash
   uv sync
   ```

3. *Aplicar las migraciones para generar la base de datos local:*
   ```bash
   uv run alembic upgrade head
   ```

4. *Iniciar el servidor de desarrollo:*
   ```bash
   uv run uvicorn src.main:app --reload
   ```

- La documentación interactiva (Swagger UI) se encuentra disponible en: <http://127.0.0.1:8000/docs>
- La especificación OpenAPI se encuentra disponible en: <http://127.0.0.1:8000/openapi.json>
- Los datos se almacenan de forma local en el archivo database.db (ignorado en el control de versiones).

## Características Técnicas

- *Framework:* FastAPI con validación estricta de esquemas mediante SQLModel y Pydantic v2.
- *Base de Datos:* SQLite local con relaciones 1:N y N:M con clave compuesta (Correlativa) y restricciones CheckConstraint.
- *Migraciones:* Control de versiones de esquema con Alembic (alembic/versions/).
- *Paginación:* Implementada en listados generales (GET /) mediante fastapi-pagination (Page[...] y paginate).
- *Manejo de Errores:* Respuestas HTTP normalizadas (200, 201, 204, 400 y 404 documentado en Swagger).
- *CORS Middleware:* Habilitado para permitir la integración con la SPA en React / Vite de la EFI de JavaScript (http://localhost:5173).

## Recursos de la API

Cada recurso implementa las operaciones CRUD completas (Crear, Listar con paginación, Consultar por ID con esquemas anidados Nested, Actualizar con PATCH y Eliminar con DELETE):

| Recurso | Prefijo | Operaciones soportadas | Descripción |
|---|---|---|---|
| Alumnos | /alumnos | POST, GET, GET /{id}, PATCH /{id}, DELETE /{id} | Gestión de alumnos con DNI, legajo y email únicos, con vínculo a Carrera. |
| Carreras | /carreras | POST, GET, GET /{id}, PATCH /{id}, DELETE /{id} | Gestión de carreras y visualización anidada de sus materias y alumnos. |
| Materias | /materias | POST, GET, GET /{id}, PATCH /{id}, DELETE /{id} | Materias vinculadas a carreras y consulta de sus correlativas requeridas. |
| Correlativas | /correlativas | POST, GET, DELETE /{materia_id}/{correlativa_id} | Vínculo N:M entre una materia y sus requisitos previos de cursado. |

## Diagrama Entidad-Relación

<p align="center">
  <img src="https://github.com/user-attachments/assets/abe71534-98e9-485f-af1d-2be56d66868d" width="470" alt="Base de datos EFI drawio">
</p>
