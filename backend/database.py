from sqlalchemy import create_engine, text, inspect
from sqlalchemy.engine import Engine
from typing import List, Dict, Any

def get_schema_from_engine(engine: Engine) -> List[Dict[str, Any]]:
    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    schema = []
    for table_name in table_names:
        columns = inspector.get_columns(table_name)
        # columns is a list of dicts with keys: name, type, nullable, default, autoincrement, primary_key
        column_details = []
        for col in columns:
            column_details.append({
                "name": col["name"],
                "type": str(col["type"]),
                "nullable": col.get("nullable", True),
                "primary_key": col.get("primary_key", False)
            })
        schema.append({
            "name": table_name,
            "columns": column_details
        })
    return schema

def get_sqlite_schema(path: str):
    # Handle both absolute paths and relative paths if needed, but user usually provides absolute or we handle it.
    # If path doesn't start with /, it might be relative.
    # For safety, let's assume the user knows what they are doing or we prepend sqlite:///
    if not path.startswith("sqlite"):
        url = f"sqlite:///{path}"
    else:
        url = path
    engine = create_engine(url)
    return get_schema_from_engine(engine)

def get_mysql_schema(host, port, user, password, db):
    # using pymysql
    url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}"
    engine = create_engine(url)
    return get_schema_from_engine(engine)

def get_postgresql_schema(host, port, user, password, db):
    # using psycopg2
    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
    engine = create_engine(url)
    return get_schema_from_engine(engine)

def get_mssql_schema(host, port, user, password, db):
    # using pymssql
    url = f"mssql+pymssql://{user}:{password}@{host}:{port}/{db}"
    engine = create_engine(url)
    return get_schema_from_engine(engine)

# Internal DataScout Database Logic
from sqlalchemy.orm import sessionmaker
from backend.models import Base, SavedConnection, SavedSchema

# Internal DB Credentials (hardcoded for now as per plan)
INTERNAL_DB_URL = "postgresql+psycopg2://postgres:postgres@localhost:5433/DataScout"

def get_internal_db_engine():
    try:
        engine = create_engine(INTERNAL_DB_URL)
        return engine
    except Exception as e:
        print(f"Error creating internal DB engine: {e}")
        return None

def init_db():
    engine = get_internal_db_engine()
    if engine:
        # Create database if not exists is tricky with sqlalchemy alone usually requires connecting to default db
        # For now assuming DB exists or we let it fail if not. 
        # Actually, let's try to create tables.
        try:
            Base.metadata.create_all(bind=engine)
            print("Internal database tables initialized.")
        except Exception as e:
            print(f"Error initializing internal database tables: {e}")

def save_connection_details(db_type: str, connection_data: Dict[str, Any], schema_data: List[Dict[str, Any]]) -> int:
    engine = get_internal_db_engine()
    if not engine:
        print("Cannot save details: Internal DB engine not available.")
        return None

    Session = sessionmaker(bind=engine)
    session = Session()
    connection_id = None

    try:
        # Create SavedConnection
        new_conn = SavedConnection(
            db_type=db_type,
            host=connection_data.get("host"),
            port=connection_data.get("port"),
            database=connection_data.get("database"),
            username=connection_data.get("username"),
            password=connection_data.get("password"),
            file_path=connection_data.get("path")
        )
        session.add(new_conn)
        session.flush() # Get ID
        connection_id = new_conn.id

        # Create SavedSchemas
        for table in schema_data:
            new_schema = SavedSchema(
                connection_id=new_conn.id,
                table_name=table["name"],
                columns_json=table["columns"]
            )
            session.add(new_schema)
        
        session.commit()
        print(f"Successfully saved connection and schema for {db_type} with ID {connection_id}")
        return connection_id
    except Exception as e:
        session.rollback()
        print(f"Error saving connection details: {e}")
        return None
    finally:
        session.close()

def update_table_context(connection_id: int, table_name: str, context: str):
    engine = get_internal_db_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        schema = session.query(SavedSchema).filter_by(connection_id=connection_id, table_name=table_name).first()
        if schema:
            schema.table_context = context
            session.commit()
            return True
        return False
    except Exception as e:
        print(f"Error updating table context: {e}")
        return False
    finally:
        session.close()

def update_column_description(connection_id: int, table_name: str, column_name: str, description: str):
    engine = get_internal_db_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        schema = session.query(SavedSchema).filter_by(connection_id=connection_id, table_name=table_name).first()
        if schema:
            # Update JSON blob
            columns = schema.columns_json
            updated = False
            for col in columns:
                if col['name'] == column_name:
                    col['description'] = description
                    updated = True
                    break
            
            if updated:
                # Force update of JSON column
                schema.columns_json = list(columns) 
                session.commit()
                return True
        return False
    except Exception as e:
        print(f"Error updating column description: {e}")
        return False
    finally:
        session.close()

def update_global_context(connection_id: int, context: str):
    engine = get_internal_db_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        conn = session.query(SavedConnection).filter_by(id=connection_id).first()
        if conn:
            conn.global_context = context
            session.commit()
            return True
        return False
    except Exception as e:
        print(f"Error updating global context: {e}")
        return False
    finally:
        session.close()

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from backend.models import Base, SavedConnection, SavedSchema
import json
from typing import List, Dict, Any

# ... (existing code) ...

def drop_internal_tables():
    engine = get_internal_db_engine()
    if not engine:
        return False
    
    try:
        # Using raw SQL for dropping to be sure
        with engine.connect() as connection:
            connection.execute(text("DROP TABLE IF EXISTS saved_schemas CASCADE"))
            connection.execute(text("DROP TABLE IF EXISTS saved_connections CASCADE"))
            connection.commit()
        print("Internal tables dropped.")
        return True
    except Exception as e:
        print(f"Error dropping internal tables: {e}")
        return False
