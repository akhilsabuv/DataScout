from pydantic import BaseModel
from typing import List, Dict, Any

class ColumnSchema(BaseModel):
    name: str
    type: str
    nullable: bool
    primary_key: bool

class TableSchema(BaseModel):
    name: str
    columns: List[ColumnSchema]

class DatabaseSchemaResponse(BaseModel):
    connection_id: int = None
    tables: List[TableSchema]

class SQLiteConnection(BaseModel):
    path: str

class DBConnection(BaseModel):
    host: str
    port: int
    database: str
    username: str
    password: str

# SQLAlchemy ORM Models
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, JSON, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class SavedConnection(Base):
    __tablename__ = "saved_connections"

    id = Column(Integer, primary_key=True, index=True)
    db_type = Column(String, index=True)
    host = Column(String, nullable=True)
    port = Column(Integer, nullable=True)
    database = Column(String, nullable=True)
    username = Column(String, nullable=True)
    password = Column(String, nullable=True) # Storing plain text for now as requested
    file_path = Column(String, nullable=True) # For SQLite
    global_context = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    schemas = relationship("SavedSchema", back_populates="connection")

class SavedSchema(Base):
    __tablename__ = "saved_schemas"

    id = Column(Integer, primary_key=True, index=True)
    connection_id = Column(Integer, ForeignKey("saved_connections.id"))
    table_name = Column(String)
    table_context = Column(Text, nullable=True)
    columns_json = Column(JSON) # Storing full column details as JSON
    created_at = Column(DateTime, default=datetime.utcnow)

    connection = relationship("SavedConnection", back_populates="schemas")
