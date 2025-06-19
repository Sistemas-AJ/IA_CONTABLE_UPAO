from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, DateTime, Float
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from .config import DATABASE_URL

engine   = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata = MetaData()
Session  = sessionmaker(bind=engine)

# Tabla existente de chunks
chunks_table = Table(
    "chunks", metadata,
    Column("id",      Integer, primary_key=True, autoincrement=True),
    Column("source",  String,  nullable=False),
    Column("content", Text,    nullable=False),
)

# Tabla existente de archivos
files_table = Table(
    "files", metadata,
    Column("id",         Integer, primary_key=True, autoincrement=True),
    Column("session_id", String,  nullable=False, index=True),
    Column("filename",   String,  nullable=False),
)

# 🆕 NUEVA: Tabla para aprendizaje de conversaciones
conversations_table = Table(
    "conversations", metadata,
    Column("id",         Integer, primary_key=True, autoincrement=True),
    Column("session_id", String,  nullable=False, index=True),
    Column("question",   Text,    nullable=False),
    Column("answer",     Text,    nullable=False),
    Column("feedback",   String,  nullable=True),  # 'positive', 'negative', 'neutral'
    Column("context_used", Text,  nullable=True),  # Contexto que se usó para responder
    Column("created_at", DateTime, default=datetime.utcnow),
    Column("usefulness_score", Float, default=0.5),  # Score de utilidad 0-1
)

# 🆕 NUEVA: Tabla para contexto persistente por usuario
user_context_table = Table(
    "user_context", metadata,
    Column("id",         Integer, primary_key=True, autoincrement=True),
    Column("session_id", String,  nullable=False, index=True),
    Column("context_key", String, nullable=False),  # 'empresa_tipo', 'sector', 'preferencias'
    Column("context_value", Text, nullable=False),
    Column("updated_at", DateTime, default=datetime.utcnow),
)

# 🆕 NUEVA: Tabla para conocimiento aprendido
learned_knowledge_table = Table(
    "learned_knowledge", metadata,
    Column("id",          Integer, primary_key=True, autoincrement=True),
    Column("question_pattern", String, nullable=False),  # Patrón de pregunta
    Column("answer_template", Text,   nullable=False),   # Template de respuesta
    Column("confidence",  Float,     default=0.5),       # Nivel de confianza
    Column("usage_count", Integer,   default=0),         # Veces que se ha usado
    Column("last_used",   DateTime,  default=datetime.utcnow),
    Column("created_from_session", String, nullable=True),
)

# 🆕 NUEVA: Tabla para ejemplos extraídos
examples_table = Table(
    "examples", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("session_id", String, nullable=False, index=True),
    Column("url_source", String, nullable=True),
    Column("example_type", String, nullable=False),  # 'asiento_contable', 'metodologia', etc.
    Column("content", Text, nullable=False),
    Column("related_question", Text, nullable=True),
    Column("usage_count", Integer, default=0),
    Column("effectiveness_score", Float, default=0.5),
    Column("created_at", DateTime, default=datetime.utcnow),
    Column("last_used", DateTime, default=datetime.utcnow),
)

metadata.create_all(engine)

# Historial en memoria (existente)
chat_histories: dict[str, list[dict]] = {}
file_names:     dict[str, str]     = {}
