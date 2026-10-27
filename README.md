# API de Gestión Académica

Proyecto de la EFI de Práctica Profesionalizante I: Python. Expone una API REST para administrar alumnos, carreras, materias y las correlatividades entre materias, construida con FastAPI, SQLModel, SQLite y Alembic.

## Integrantes

- Juan Ignacio Andrada Guzman - [juanignacioandrada20-gif]
- Tomas Castelo - [Tomaz809]
- Lautaro Ocanto - [laautisz]
- Geronimo Martin Torasso - [Gerot1234]

## Requisitos

- Python 3.12
- [uv](https://docs.astral.sh/uv/)

## Instalación y ejecución

1. Clonar el repositorio y ubicarse en la raíz del proyecto.
2. Sincronizar el entorno e instalar dependencias: uv sync
3. Aplicar las migraciones para crear la base de datos local: uv run alembic upgrade head
4. Iniciar el servidor de desarrollo: uv run uvicorn src.main:app --reload

* La documentación interactiva (Swagger) se encuentra disponible en: <http://127.0.0.1:8000/docs>
* Los datos se almacenan de forma local en el archivo database.db.

## Recursos de la API

Cada recurso implementa las operaciones CRUD completas (Crear, Listar con paginación, Consultar por ID, Actualizar y Eliminar):

| Recurso | Prefijo | Descripción |
|---|---|---|
| Alumnos | /alumnos | Gestión de alumnos con DNI y email únicos. |
| Carreras | /carreras | Gestión de carreras y materias asociadas. |
| Materias | /materias | Materias vinculadas a carreras y sus correlativas. |
| Correlativas | /correlativas | Relación entre una materia y sus requisitos de cursado. |

## Diagrama Entidad-Relación

<p align="center">
  <img src="https://github.com/user-attachments/assets/abe71534-98e9-485f-af1d-2be56d66868d" width="470" alt="Base de datos EFI drawio">
</p>
