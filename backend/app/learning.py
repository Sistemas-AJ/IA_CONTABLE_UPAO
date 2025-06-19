import re
from datetime import datetime, timedelta
from sqlalchemy import func
from .db import Session, conversations_table, user_context_table, learned_knowledge_table
from .embedding_utils import generar_embeddings
import numpy as np

class LearningSystem:
    def __init__(self):
        self.similarity_threshold = 0.8
        self.confidence_threshold = 0.7
        self.example_similarity_threshold = 0.7
        
        # Crear tabla de ejemplos si no existe
        self._ensure_examples_table()
    
    def _ensure_examples_table(self):
        """Asegurar que la tabla de ejemplos existe"""
        from sqlalchemy import Table, Column, Integer, String, Text, DateTime, Float
        from .db import metadata, engine
        
        # Solo crear si no existe
        if 'examples' not in metadata.tables:
            self.examples_table = Table(
                "examples", metadata,
                Column("id", Integer, primary_key=True, autoincrement=True),
                Column("session_id", String, nullable=False, index=True),
                Column("url_source", String, nullable=True),
                Column("example_type", String, nullable=False),
                Column("content", Text, nullable=False),
                Column("related_question", Text, nullable=True),
                Column("usage_count", Integer, default=0),
                Column("effectiveness_score", Float, default=0.5),
                Column("created_at", DateTime, default=datetime.utcnow),
                Column("last_used", DateTime, default=datetime.utcnow),
                extend_existing=True
            )
            metadata.create_all(engine)
        else:
            self.examples_table = metadata.tables['examples']
    
    def save_conversation(self, session_id: str, question: str, answer: str, context_used: str = None):
        """Guarda una conversación para aprendizaje futuro"""
        db = Session()
        try:
            db.execute(
                conversations_table.insert().values(
                    session_id=session_id,
                    question=question,
                    answer=answer,
                    context_used=context_used,
                    feedback='neutral',
                    usefulness_score=0.5
                )
            )
            db.commit()
        finally:
            db.close()
    
    def update_feedback(self, conversation_id: int, feedback: str, score: float):
        """Actualiza el feedback de una conversación"""
        db = Session()
        try:
            db.execute(
                conversations_table.update().where(
                    conversations_table.c.id == conversation_id
                ).values(
                    feedback=feedback,
                    usefulness_score=score
                )
            )
            db.commit()
        finally:
            db.close()
    
    def extract_user_context(self, session_id: str, question: str, answer: str):
        """Extrae contexto del usuario de la conversación"""
        context_patterns = {
            'empresa_tipo': [
                r'(?:soy|tengo|trabajo en|empresa|negocio)\s+(?:una\s+)?(\w+)',
                r'(?:sociedad|s\.a\.|s\.r\.l\.|eirl|empresa individual)'
            ],
            'sector': [
                r'(?:sector|rubro|industria|dedicamos a|negocio de)\s+(\w+)',
                r'(?:comercio|servicios|manufactura|construcción|minería)'
            ],
            'experiencia': [
                r'(?:soy|tengo experiencia|trabajo como|años en)\s+(\w+)',
                r'(?:contador|estudiante|empresario|gerente)'
            ]
        }
        
        db = Session()
        try:
            for context_key, patterns in context_patterns.items():
                for pattern in patterns:
                    match = re.search(pattern, question.lower())
                    if match:
                        value = match.group(1) if match.lastindex else match.group(0)
                        # Actualizar o insertar contexto
                        existing = db.execute(
                            user_context_table.select().where(
                                (user_context_table.c.session_id == session_id) &
                                (user_context_table.c.context_key == context_key)
                            )
                        ).first()
                        
                        if existing:
                            db.execute(
                                user_context_table.update().where(
                                    user_context_table.c.id == existing.id
                                ).values(
                                    context_value=value,
                                    updated_at=datetime.utcnow()
                                )
                            )
                        else:
                            db.execute(
                                user_context_table.insert().values(
                                    session_id=session_id,
                                    context_key=context_key,
                                    context_value=value
                                )
                            )
            db.commit()
        finally:
            db.close()
    
    def get_user_context(self, session_id: str) -> dict:
        """Obtiene el contexto conocido del usuario"""
        db = Session()
        try:
            rows = db.execute(
                user_context_table.select().where(
                    user_context_table.c.session_id == session_id
                )
            ).fetchall()
            return {row.context_key: row.context_value for row in rows}
        finally:
            db.close()
    
    def find_similar_questions(self, question: str, limit: int = 5) -> list:
        """Encuentra preguntas similares en el historial"""
        db = Session()
        try:
            # Obtener conversaciones exitosas (feedback positivo)
            rows = db.execute(
                conversations_table.select().where(
                    conversations_table.c.usefulness_score > 0.6
                ).order_by(conversations_table.c.usefulness_score.desc()).limit(50)
            ).fetchall()
            
            if not rows:
                return []
            
            # Calcular similitud semántica
            question_emb = generar_embeddings(question)
            similar_convs = []
            
            for row in rows:
                conv_emb = generar_embeddings(row.question)
                similarity = np.dot(question_emb, conv_emb) / (
                    np.linalg.norm(question_emb) * np.linalg.norm(conv_emb)
                )
                
                if similarity > self.similarity_threshold:
                    similar_convs.append({
                        'id': row.id,
                        'question': row.question,
                        'answer': row.answer,
                        'similarity': similarity,
                        'context_used': row.context_used
                    })
            
            # Ordenar por similitud
            similar_convs.sort(key=lambda x: x['similarity'], reverse=True)
            return similar_convs[:limit]
            
        finally:
            db.close()
    
    def learn_from_pattern(self, session_id: str, question: str, answer: str):
        """Aprende un patrón de pregunta-respuesta"""
        # Simplificar pregunta a patrón
        pattern = self._extract_question_pattern(question)
        
        db = Session()
        try:
            existing = db.execute(
                learned_knowledge_table.select().where(
                    learned_knowledge_table.c.question_pattern == pattern
                )
            ).first()
            
            if existing:
                # Actualizar conocimiento existente
                new_confidence = min(1.0, existing.confidence + 0.1)
                db.execute(
                    learned_knowledge_table.update().where(
                        learned_knowledge_table.c.id == existing.id
                    ).values(
                        confidence=new_confidence,
                        usage_count=existing.usage_count + 1,
                        last_used=datetime.utcnow()
                    )
                )
            else:
                # Crear nuevo conocimiento
                db.execute(
                    learned_knowledge_table.insert().values(
                        question_pattern=pattern,
                        answer_template=answer,
                        confidence=0.6,
                        usage_count=1,
                        created_from_session=session_id
                    )
                )
            db.commit()
        finally:
            db.close()
    
    def _extract_question_pattern(self, question: str) -> str:
        """Extrae patrón de una pregunta"""
        # Convertir a minúsculas y limpiar
        pattern = question.lower().strip()
        
        # Reemplazar números específicos con placeholders
        pattern = re.sub(r'\d+', '[NUM]', pattern)
        
        # Reemplazar nombres propios con placeholders
        pattern = re.sub(r'\b[A-Z][a-z]+\b', '[NOMBRE]', pattern)
        
        # Extraer palabras clave importantes
        keywords = re.findall(r'\b(?:asiento|contabilizar|registrar|cuenta|debe|haber|pcge|constitución|empresa|impuesto|igv|renta)\b', pattern)
        
        if keywords:
            return ' '.join(keywords)
        
        return pattern[:100]  # Limitar longitud
    
    def save_correction(self, session_id: str, original_question: str, correction: str, corrected_answer: str):
        """Guarda una corrección del usuario para aprendizaje"""
        db = Session()
        try:
            # Buscar la conversación original
            original_conv = db.execute(
                conversations_table.select().where(
                    (conversations_table.c.session_id == session_id) &
                    (conversations_table.c.question.like(f"%{original_question[:50]}%"))
                ).order_by(conversations_table.c.id.desc())
            ).first()
            
            if original_conv:
                # Marcar como incorrecta
                db.execute(
                    conversations_table.update().where(
                        conversations_table.c.id == original_conv.id
                    ).values(
                        feedback='negative',
                        usefulness_score=0.1
                    )
                )
            
            # Guardar la corrección como nueva conversación
            db.execute(
                conversations_table.insert().values(
                    session_id=session_id,
                    question=f"CORRECCIÓN: {original_question}",
                    answer=corrected_answer,
                    context_used=f"Corrección del usuario: {correction}",
                    feedback='positive',
                    usefulness_score=0.9
                )
            )
            
            # Aprender el patrón corregido
            self.learn_from_pattern(session_id, original_question, corrected_answer)
            
            db.commit()
        finally:
            db.close()
    
    def detect_correction(self, message: str) -> dict:
        """Detecta si un mensaje es una corrección"""
        correction_patterns = [
            r"está?\s+mal",
            r"incorrecto",
            r"no\s+es\s+correcto",
            r"debes?\s+usar",
            r"la\s+cuenta\s+es",
            r"debería\s+ser",
            r"en\s+realidad",
            r"provision"
        ]
        
        for pattern in correction_patterns:
            if re.search(pattern, message.lower()):
                return {
                    "is_correction": True,
                    "pattern": pattern,
                    "confidence": 0.8
                }
        
        return {"is_correction": False}
    
    def save_example_from_url(self, session_id: str, url: str, content: str, related_question: str):
        """Guarda un ejemplo extraído de una URL"""
        db = Session()
        try:
            # Detectar tipo de ejemplo
            example_type = self._detect_example_type(content, related_question)
            
            # Verificar si ya existe un ejemplo similar
            existing = self._find_existing_example(content)
            
            if not existing:
                db.execute(
                    self.examples_table.insert().values(
                        session_id=session_id,
                        url_source=url,
                        example_type=example_type,
                        content=content,
                        related_question=related_question,
                        usage_count=1,
                        effectiveness_score=0.7,
                    )
                )
                db.commit()
                print(f"DEBUG: Ejemplo guardado: {example_type} de {url}")
        finally:
            db.close()
    
    def find_similar_examples(self, question: str, limit: int = 3) -> list:
        """Encuentra ejemplos similares a la pregunta"""
        db = Session()
        try:
            # Obtener ejemplos con buena efectividad
            rows = db.execute(
                self.examples_table.select().where(
                    self.examples_table.c.effectiveness_score > 0.5
                ).order_by(self.examples_table.c.effectiveness_score.desc()).limit(20)
            ).fetchall()
            
            if not rows:
                return []
            
            # Calcular similitud semántica
            question_emb = generar_embeddings(question)
            similar_examples = []
            
            for row in rows:
                # Comparar con el contenido y la pregunta relacionada
                combined_text = f"{row.content} {row.related_question or ''}"
                example_emb = generar_embeddings(combined_text)
                
                similarity = np.dot(question_emb, example_emb) / (
                    np.linalg.norm(question_emb) * np.linalg.norm(example_emb)
                )
                
                if similarity > self.example_similarity_threshold:
                    similar_examples.append({
                        'id': row.id,
                        'content': row.content,
                        'type': row.example_type,
                        'url_source': row.url_source,
                        'similarity': similarity,
                        'effectiveness': row.effectiveness_score
                    })
            
            # Ordenar por similitud y efectividad
            similar_examples.sort(key=lambda x: (x['similarity'], x['effectiveness']), reverse=True)
            return similar_examples[:limit]
            
        finally:
            db.close()
    
    def _detect_example_type(self, content: str, question: str) -> str:
        """Detecta el tipo de ejemplo basándose en el contenido"""
        content_lower = content.lower()
        question_lower = question.lower()
        
        if any(kw in content_lower for kw in ["asiento", "debe", "haber", "cuenta"]):
            return "asiento_contable"
        elif any(kw in question_lower for kw in ["prestamo", "préstamo"]):
            return "prestamo_bancario"
        elif any(kw in content_lower for kw in ["metodologia", "procedimiento", "pasos"]):
            return "metodologia"
        elif any(kw in content_lower for kw in ["constitucion", "sociedad", "empresa"]):
            return "constitucion_empresa"
        else:
            return "general"
    
    def _find_existing_example(self, content: str) -> bool:
        """Verifica si ya existe un ejemplo similar"""
        db = Session()
        try:
            # Comparación simple por longitud y palabras clave
            content_words = set(content.lower().split())
            
            rows = db.execute(self.examples_table.select()).fetchall()
            
            for row in rows:
                existing_words = set(row.content.lower().split())
                # Si tiene más del 70% de palabras en común, considerar como existente
                intersection = len(content_words & existing_words)
                union = len(content_words | existing_words)
                
                if union > 0 and intersection / union > 0.7:
                    return True
            
            return False
        finally:
            db.close()
    
    def mark_example_as_used(self, example_id: int, effectiveness: float = None):
        """Marca un ejemplo como usado y actualiza su efectividad"""
        db = Session()
        try:
            update_values = {
                'usage_count': self.examples_table.c.usage_count + 1,
                'last_used': datetime.utcnow()
            }
            
            if effectiveness is not None:
                update_values['effectiveness_score'] = effectiveness
            
            db.execute(
                self.examples_table.update().where(
                    self.examples_table.c.id == example_id
                ).values(**update_values)
            )
            db.commit()
        finally:
            db.close()
    
    def get_best_examples_by_type(self, example_type: str, limit: int = 5) -> list:
        """Obtiene los mejores ejemplos de un tipo específico"""
        db = Session()
        try:
            rows = db.execute(
                self.examples_table.select().where(
                    self.examples_table.c.example_type == example_type
                ).order_by(self.examples_table.c.effectiveness_score.desc()).limit(limit)
            ).fetchall()
            
            return [{
                'id': row.id,
                'content': row.content,
                'url_source': row.url_source,
                'effectiveness': row.effectiveness_score,
                'usage_count': row.usage_count
            } for row in rows]
        finally:
            db.close()

# 🆕 CREAR INSTANCIA GLOBAL PARA EXPORTAR
learning_system = LearningSystem()