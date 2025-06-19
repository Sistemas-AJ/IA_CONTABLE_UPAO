"""
Servicio de feedback y mejora continua del sistema
"""
import json
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, asdict
from ..config import DATA_DIR

@dataclass
class FeedbackEntry:
    """Entrada de feedback del usuario"""
    id: str
    session_id: str
    query: str
    response: str
    rating: int  # 1-5
    feedback_text: Optional[str]
    categories: List[str]
    timestamp: str
    user_id: Optional[str] = None
    response_time: Optional[float] = None
    query_type: Optional[str] = None

@dataclass
class SystemMetrics:
    """Métricas del sistema"""
    period_start: str
    period_end: str
    total_queries: int
    avg_rating: float
    avg_response_time: float
    query_types: Dict[str, int]
    common_issues: List[Dict]
    improvement_suggestions: List[str]

class FeedbackService:
    """Servicio para manejo de feedback y métricas"""
    
    def __init__(self):
        self.feedback_dir = Path(DATA_DIR) / "feedback"
        self.feedback_dir.mkdir(parents=True, exist_ok=True)
        self.feedback_file = self.feedback_dir / "feedback.json"
        self.metrics_file = self.feedback_dir / "metrics.json"
        
        # Cargar feedback existente
        self.feedback_data = self._load_feedback_data()
    
    def _load_feedback_data(self) -> List[Dict]:
        """Carga datos de feedback existentes"""
        try:
            if self.feedback_file.exists():
                with open(self.feedback_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"Error cargando feedback: {e}")
            return []
    
    def _save_feedback_data(self) -> None:
        """Guarda datos de feedback"""
        try:
            with open(self.feedback_file, 'w', encoding='utf-8') as f:
                json.dump(self.feedback_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando feedback: {e}")
    
    def submit_feedback(self, session_id: str, query: str, response: str,
                       rating: int, feedback_text: str = None,
                       categories: List[str] = None, user_id: str = None,
                       response_time: float = None, query_type: str = None) -> Dict:
        """Registra feedback del usuario"""
        try:
            # Validar rating
            if not 1 <= rating <= 5:
                return {"success": False, "error": "Rating debe estar entre 1 y 5"}
            
            # Crear entrada de feedback
            feedback_entry = FeedbackEntry(
                id=self._generate_feedback_id(),
                session_id=session_id,
                query=query[:500],  # Limitar longitud
                response=response[:1000],  # Limitar longitud
                rating=rating,
                feedback_text=feedback_text[:500] if feedback_text else None,
                categories=categories or [],
                timestamp=datetime.now().isoformat(),
                user_id=user_id,
                response_time=response_time,
                query_type=query_type
            )
            
            # Agregar a datos
            self.feedback_data.append(asdict(feedback_entry))
            
            # Guardar
            self._save_feedback_data()
            
            # Analizar si es feedback negativo para alertas
            if rating <= 2:
                self._handle_negative_feedback(feedback_entry)
            
            return {
                "success": True,
                "message": "Feedback registrado correctamente",
                "feedback_id": feedback_entry.id
            }
            
        except Exception as e:
            return {"success": False, "error": f"Error registrando feedback: {str(e)}"}
    
    def _generate_feedback_id(self) -> str:
        """Genera ID único para feedback"""
        import hashlib
        timestamp = datetime.now().isoformat()
        return hashlib.md5(timestamp.encode()).hexdigest()[:12]
    
    def _handle_negative_feedback(self, feedback: FeedbackEntry) -> None:
        """Maneja feedback negativo para alertas"""
        try:
            # Log para monitoreo
            print(f"🚨 FEEDBACK NEGATIVO - Rating: {feedback.rating}, Query: {feedback.query[:100]}...")
            
            # En implementación real, podría enviar alertas por email/Slack
            # Guardar en archivo de alertas
            alerts_file = self.feedback_dir / "alerts.json"
            
            alert_data = {
                "timestamp": feedback.timestamp,
                "type": "negative_feedback",
                "rating": feedback.rating,
                "query": feedback.query,
                "feedback_text": feedback.feedback_text,
                "session_id": feedback.session_id
            }
            
            alerts = []
            if alerts_file.exists():
                with open(alerts_file, 'r', encoding='utf-8') as f:
                    alerts = json.load(f)
            
            alerts.append(alert_data)
            
            with open(alerts_file, 'w', encoding='utf-8') as f:
                json.dump(alerts, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"Error manejando feedback negativo: {e}")
    
    def get_feedback_stats(self, days: int = 30) -> Dict:
        """Obtiene estadísticas de feedback"""
        try:
            # Filtrar por período
            cutoff_date = datetime.now() - timedelta(days=days)
            recent_feedback = [
                f for f in self.feedback_data
                if datetime.fromisoformat(f["timestamp"]) >= cutoff_date
            ]
            
            if not recent_feedback:
                return {"message": "No hay feedback en el período especificado"}
            
            # Calcular estadísticas
            total_feedback = len(recent_feedback)
            ratings = [f["rating"] for f in recent_feedback]
            avg_rating = sum(ratings) / len(ratings)
            
            # Distribución de ratings
            rating_distribution = {}
            for rating in range(1, 6):
                count = ratings.count(rating)
                rating_distribution[f"{rating}_stars"] = {
                    "count": count,
                    "percentage": round((count / total_feedback) * 100, 1)
                }
            
            # Tipos de consulta más comunes
            query_types = {}
            for f in recent_feedback:
                if f.get("query_type"):
                    qt = f["query_type"]
                    query_types[qt] = query_types.get(qt, 0) + 1
            
            # Categorías de problemas más comunes
            problem_categories = {}
            for f in recent_feedback:
                if f.get("categories"):
                    for category in f["categories"]:
                        problem_categories[category] = problem_categories.get(category, 0) + 1
            
            # Feedback negativo reciente
            negative_feedback = [f for f in recent_feedback if f["rating"] <= 2]
            
            return {
                "period_days": days,
                "total_feedback": total_feedback,
                "average_rating": round(avg_rating, 2),
                "rating_distribution": rating_distribution,
                "query_types": dict(sorted(query_types.items(), key=lambda x: x[1], reverse=True)),
                "problem_categories": dict(sorted(problem_categories.items(), key=lambda x: x[1], reverse=True)),
                "negative_feedback_count": len(negative_feedback),
                "satisfaction_rate": round((len([f for f in recent_feedback if f["rating"] >= 4]) / total_feedback) * 100, 1)
            }
            
        except Exception as e:
            return {"error": f"Error obteniendo estadísticas: {str(e)}"}
    
    def get_recent_feedback(self, limit: int = 10, min_rating: int = None) -> List[Dict]:
        """Obtiene feedback reciente"""
        try:
            # Filtrar por rating si se especifica
            filtered_feedback = self.feedback_data
            if min_rating is not None:
                filtered_feedback = [f for f in filtered_feedback if f["rating"] >= min_rating]
            
            # Ordenar por timestamp (más reciente primero)
            sorted_feedback = sorted(
                filtered_feedback,
                key=lambda x: x["timestamp"],
                reverse=True
            )
            
            # Limitar cantidad
            recent = sorted_feedback[:limit]
            
            # Limpiar datos sensibles para respuesta
            cleaned_feedback = []
            for f in recent:
                cleaned = {
                    "id": f["id"],
                    "rating": f["rating"],
                    "feedback_text": f.get("feedback_text"),
                    "categories": f.get("categories", []),
                    "timestamp": f["timestamp"],
                    "query_type": f.get("query_type"),
                    "query_preview": f["query"][:100] + "..." if len(f["query"]) > 100 else f["query"]
                }
                cleaned_feedback.append(cleaned)
            
            return cleaned_feedback
            
        except Exception as e:
            return [{"error": f"Error obteniendo feedback reciente: {str(e)}"}]
    
    def generate_improvement_report(self, days: int = 30) -> Dict:
        """Genera reporte de mejoras sugeridas"""
        try:
            # Obtener feedback del período
            cutoff_date = datetime.now() - timedelta(days=days)
            recent_feedback = [
                f for f in self.feedback_data
                if datetime.fromisoformat(f["timestamp"]) >= cutoff_date
            ]
            
            if not recent_feedback:
                return {"message": "No hay suficiente feedback para generar reporte"}
            
            # Analizar problemas comunes
            negative_feedback = [f for f in recent_feedback if f["rating"] <= 2]
            common_issues = self._analyze_common_issues(negative_feedback)
            
            # Sugerencias de mejora basadas en análisis
            suggestions = self._generate_improvement_suggestions(common_issues, recent_feedback)
            
            # Métricas de rendimiento
            response_times = [f.get("response_time") for f in recent_feedback if f.get("response_time")]
            avg_response_time = sum(response_times) / len(response_times) if response_times else 0
            
            return {
                "report_period": f"Últimos {days} días",
                "generated_at": datetime.now().isoformat(),
                "summary": {
                    "total_feedback": len(recent_feedback),
                    "average_rating": round(sum(f["rating"] for f in recent_feedback) / len(recent_feedback), 2),
                    "negative_feedback_count": len(negative_feedback),
                    "avg_response_time": round(avg_response_time, 2) if avg_response_time else None
                },
                "common_issues": common_issues,
                "improvement_suggestions": suggestions,
                "priority_actions": self._identify_priority_actions(common_issues)
            }
            
        except Exception as e:
            return {"error": f"Error generando reporte de mejoras: {str(e)}"}
    
    def _analyze_common_issues(self, negative_feedback: List[Dict]) -> List[Dict]:
        """Analiza problemas comunes en feedback negativo"""
        issues = []
        
        # Analizar texto de feedback
        issue_keywords = {
            "respuesta_incorrecta": ["incorrecto", "error", "equivocado", "mal"],
            "no_entiende": ["no entiende", "no comprende", "confuso"],
            "lento": ["lento", "demora", "tardó"],
            "incompleto": ["incompleto", "falta", "más información"],
            "no_ayuda": ["no ayuda", "inútil", "no sirve"]
        }
        
        issue_counts = {}
        for feedback in negative_feedback:
            text = (feedback.get("feedback_text") or "").lower()
            query = feedback["query"].lower()
            combined_text = f"{text} {query}"
            
            for issue_type, keywords in issue_keywords.items():
                if any(keyword in combined_text for keyword in keywords):
                    issue_counts[issue_type] = issue_counts.get(issue_type, 0) + 1
        
        # Convertir a lista ordenada
        for issue_type, count in sorted(issue_counts.items(), key=lambda x: x[1], reverse=True):
            issues.append({
                "issue_type": issue_type.replace("_", " ").title(),
                "count": count,
                "percentage": round((count / len(negative_feedback)) * 100, 1) if negative_feedback else 0
            })
        
        return issues
    
    def _generate_improvement_suggestions(self, common_issues: List[Dict], all_feedback: List[Dict]) -> List[str]:
        """Genera sugerencias de mejora basadas en análisis"""
        suggestions = []
        
        # Sugerencias basadas en problemas comunes
        for issue in common_issues:
            issue_type = issue["issue_type"].lower()
            
            if "respuesta incorrecta" in issue_type:
                suggestions.append("Mejorar la precisión del modelo con más entrenamiento en casos específicos")
                suggestions.append("Implementar validación cruzada de respuestas críticas")
            
            elif "no entiende" in issue_type:
                suggestions.append("Ampliar el sistema de detección de intención de consultas")
                suggestions.append("Agregar más ejemplos de reformulación de preguntas")
            
            elif "lento" in issue_type:
                suggestions.append("Optimizar el sistema de cache para consultas frecuentes")
                suggestions.append("Implementar respuestas parciales en tiempo real")
            
            elif "incompleto" in issue_type:
                suggestions.append("Expandir la base de conocimientos con más documentación")
                suggestions.append("Implementar seguimiento automático para consultas que requieren más información")
        
        # Sugerencias generales basadas en métricas
        avg_rating = sum(f["rating"] for f in all_feedback) / len(all_feedback)
        if avg_rating < 3.5:
            suggestions.append("Revisar y actualizar la base de conocimientos general")
            suggestions.append("Implementar sistema de escalamiento a expertos humanos")
        
        return list(set(suggestions))  # Eliminar duplicados
    
    def _identify_priority_actions(self, common_issues: List[Dict]) -> List[Dict]:
        """Identifica acciones prioritarias basadas en impacto"""
        priority_actions = []
        
        for issue in common_issues[:3]:  # Top 3 problemas
            if issue["percentage"] > 20:  # Si afecta a más del 20% del feedback negativo
                priority_actions.append({
                    "issue": issue["issue_type"],
                    "impact": "Alto" if issue["percentage"] > 40 else "Medio",
                    "recommended_action": self._get_recommended_action(issue["issue_type"]),
                    "estimated_effort": self._estimate_effort(issue["issue_type"])
                })
        
        return priority_actions
    
    def _get_recommended_action(self, issue_type: str) -> str:
        """Obtiene acción recomendada para un tipo de problema"""
        actions = {
            "Respuesta Incorrecta": "Revisar y actualizar base de conocimientos contables",
            "No Entiende": "Mejorar sistema de procesamiento de lenguaje natural",
            "Lento": "Optimizar infraestructura y sistema de cache",
            "Incompleto": "Ampliar documentación y contexto disponible",
            "No Ayuda": "Revisar flujo de conversación y respuestas predeterminadas"
        }
        return actions.get(issue_type, "Analizar caso específico")
    
    def _estimate_effort(self, issue_type: str) -> str:
        """Estima esfuerzo necesario para resolver un problema"""
        efforts = {
            "Respuesta Incorrecta": "Medio (1-2 semanas)",
            "No Entiende": "Alto (3-4 semanas)", 
            "Lento": "Bajo (3-5 días)",
            "Incompleto": "Medio (1-2 semanas)",
            "No Ayuda": "Bajo (1 semana)"
        }
        return efforts.get(issue_type, "Por determinar")
    
    def export_feedback_data(self, format: str = "json", days: int = None) -> Dict:
        """Exporta datos de feedback"""
        try:
            # Filtrar por período si se especifica
            feedback_to_export = self.feedback_data
            if days:
                cutoff_date = datetime.now() - timedelta(days=days)
                feedback_to_export = [
                    f for f in self.feedback_data
                    if datetime.fromisoformat(f["timestamp"]) >= cutoff_date
                ]
            
            if format.lower() == "json":
                export_file = self.feedback_dir / f"feedback_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(export_file, 'w', encoding='utf-8') as f:
                    json.dump(feedback_to_export, f, indent=2, ensure_ascii=False)
                
                return {
                    "success": True,
                    "message": f"Datos exportados a {export_file}",
                    "records_exported": len(feedback_to_export)
                }
            
            elif format.lower() == "csv":
                import pandas as pd
                
                # Aplanar datos para CSV
                flattened_data = []
                for f in feedback_to_export:
                    flattened = {
                        "id": f["id"],
                        "timestamp": f["timestamp"],
                        "rating": f["rating"],
                        "query": f["query"],
                        "feedback_text": f.get("feedback_text", ""),
                        "query_type": f.get("query_type", ""),
                        "response_time": f.get("response_time", "")
                    }
                    flattened_data.append(flattened)
                
                df = pd.DataFrame(flattened_data)
                export_file = self.feedback_dir / f"feedback_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                df.to_csv(export_file, index=False, encoding='utf-8')
                
                return {
                    "success": True,
                    "message": f"Datos exportados a {export_file}",
                    "records_exported": len(feedback_to_export)
                }
            
            else:
                return {"success": False, "error": "Formato no soportado. Use 'json' o 'csv'"}
                
        except Exception as e:
            return {"success": False, "error": f"Error exportando datos: {str(e)}"}

# Instancia global del servicio
feedback_service = FeedbackService()