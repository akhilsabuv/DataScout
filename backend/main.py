from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.database import get_sqlite_schema, get_mysql_schema, get_postgresql_schema, get_mssql_schema, init_db, save_connection_details, update_table_context, update_column_description, update_global_context, drop_internal_tables
from backend.models import DatabaseSchemaResponse, SQLiteConnection, DBConnection
from pydantic import BaseModel

app = FastAPI(title="DataScout API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For development, allow all. In production, specify domains.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ContextUpdate(BaseModel):
    context: str

class DescriptionUpdate(BaseModel):
    description: str

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/")
def read_root():
    return {"message": "DataScout Backend Running"}

@app.delete("/connection")
def delete_connection():
    success = drop_internal_tables()
    if not success:
        raise HTTPException(status_code=500, detail="Failed to drop tables")
    
    # Re-initialize tables
    init_db()
    return {"message": "Connection deleted and tables reset"}

@app.post("/connect/sqlite", response_model=DatabaseSchemaResponse)
def connect_sqlite(details: SQLiteConnection):
    try:
        schema = get_sqlite_schema(details.path)
        # Save details
        conn_id = save_connection_details("sqlite", details.dict(), schema)
        return {"connection_id": conn_id, "tables": schema}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error connecting to SQLite: {str(e)}")

@app.post("/connect/mysql", response_model=DatabaseSchemaResponse)
def connect_mysql(details: DBConnection):
    try:
        schema = get_mysql_schema(details.host, details.port, details.username, details.password, details.database)
        conn_id = save_connection_details("mysql", details.dict(), schema)
        return {"connection_id": conn_id, "tables": schema}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error connecting to MySQL: {str(e)}")

@app.post("/connect/postgresql", response_model=DatabaseSchemaResponse)
def connect_postgresql(details: DBConnection):
    try:
        schema = get_postgresql_schema(details.host, details.port, details.username, details.password, details.database)
        conn_id = save_connection_details("postgresql", details.dict(), schema)
        return {"connection_id": conn_id, "tables": schema}
    except Exception as e:
        print(f"DEBUG: PostgreSQL Connection Error: {e}")
        raise HTTPException(status_code=400, detail=f"Error connecting to PostgreSQL: {str(e)}")

@app.post("/connect/mssql", response_model=DatabaseSchemaResponse)
def connect_mssql(details: DBConnection):
    try:
        schema = get_mssql_schema(details.host, details.port, details.username, details.password, details.database)
        conn_id = save_connection_details("mssql", details.dict(), schema)
        return {"connection_id": conn_id, "tables": schema}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error connecting to MSSQL: {str(e)}")

@app.put("/schema/{connection_id}/table/{table_name}/context")
def update_table_context_endpoint(connection_id: int, table_name: str, update: ContextUpdate):
    success = update_table_context(connection_id, table_name, update.context)
    if not success:
        raise HTTPException(status_code=404, detail="Table or connection not found")
    return {"message": "Context updated"}

@app.put("/schema/{connection_id}/column/{table_name}/{column_name}/description")
def update_column_description_endpoint(connection_id: int, table_name: str, column_name: str, update: DescriptionUpdate):
    success = update_column_description(connection_id, table_name, column_name, update.description)
    if not success:
        raise HTTPException(status_code=404, detail="Column, table or connection not found")
    return {"message": "Description updated"}

@app.put("/schema/{connection_id}/global/context")
def update_global_context_endpoint(connection_id: int, update: ContextUpdate):
    success = update_global_context(connection_id, update.context)
    if not success:
        raise HTTPException(status_code=404, detail="Connection not found")
    return {"message": "Global context updated"}
