# FastAPI Boilerplate

This project provides a simple FastAPI server with a build notes API demonstrating full CRUD functionality. It uses SQLite via SQLAlchemy and includes unit tests.

## Setup

1. (Optional) Create and activate a virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the development server:

   ```bash
   uvicorn app.main:app --reload
   ```

4. Open [http://localhost:8000/docs](http://localhost:8000/docs) to view the Swagger UI and interact with the API.

## Testing

Run unit tests with:

```bash
pytest
```
