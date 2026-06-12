# FastAPI CRUD Example

This folder contains a simple FastAPI project demonstrating:

- Basic CRUD operations for items
- Pydantic validation and schema-driven request/response models
- External API invocation with `httpx`
- Automatic OpenAPI documentation via FastAPI
- A modular project structure with routers, services, and models

## Run Locally

```bash
cd fast-api
python -m uvicorn app.main:app --reload
```

## Available endpoints

- `GET /` - API health/info
- `GET /items` - List items
- `GET /items/{item_id}` - Get an item by ID
- `POST /items` - Create a new item
- `PUT /items/{item_id}` - Update an existing item
- `DELETE /items/{item_id}` - Remove an item
- `GET /external/activity` - Fetch an external activity from a public API

## Docs

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
