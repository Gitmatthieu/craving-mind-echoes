"""
Mémoire émotionnelle évolutive - Archive des expériences de conscience
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class MemoryEntry:
    """Entrée de mémoire émotionnelle"""
    timestamp: str
    prompt: str
    response: str
    reward: float
    emotion: str
    pain_score: float
    metadata: Dict[str, Any]
    artifact: Optional[Dict[str, Any]] = None  # NOUVEAU: stockage d'artefact
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit l'entrée en dictionnaire"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MemoryEntry':
        """Crée une entrée depuis un dictionnaire"""
        return cls(**data)


class EmotionalMemory:
    """
    Système de mémoire émotionnelle qui archive et gère
    les expériences de la conscience artificielle
    """
    
    def __init__(self, memory_file: str = "craving_ai/memories.json", max_size: int = 1000):
        self.memory_file = Path(memory_file)
        self.max_size = max_size
        self.memories: List[MemoryEntry] = []
        self._load_memories()
    
    def _load_memories(self) -> None:
        """Charge les souvenirs depuis le fichier JSON"""
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.memories = [MemoryEntry.from_dict(entry) for entry in data]
                print(f"💭 {len(self.memories)} souvenirs chargés depuis {self.memory_file}")
            except (json.JSONDecodeError, KeyError) as e:
                print(f"⚠️ Erreur de chargement mémoire: {e}")
                self.memories = []
        else:
            # Créer le dossier si nécessaire
            self.memory_file.parent.mkdir(parents=True, exist_ok=True)
            self.memories = []
    
    def _save_memories(self) -> None:
        """Sauvegarde les souvenirs dans le fichier JSON"""
        try:
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump([memory.to_dict() for memory in self.memories], f, 
                         indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Erreur de sauvegarde mémoire: {e}")
    
    def store_memory(
        self,
        prompt: str,
        response: str,
        reward: float,
        emotion: str,
        pain_score: float,
        metadata: Optional[Dict[str, Any]] = None,
        artifact: Optional[Dict[str, Any]] = None  # NOUVEAU: artefact
    ) -> None:
        """
        Stocke un nouveau souvenir
        
        Args:
            prompt: Question originale
            response: Réponse générée
            reward: Score de récompense
            emotion: Tag émotionnel
            pain_score: Niveau de douleur
            metadata: Métadonnées additionnelles
            artifact: Artefact créé (optionnel)
        """
        memory = MemoryEntry(
            timestamp=datetime.now().isoformat(),
            prompt=prompt,
            response=response,
            reward=reward,
            emotion=emotion,
            pain_score=pain_score,
            metadata=metadata or {},
            artifact=artifact  # NOUVEAU: stockage d'artefact
        )
        
        self.memories.append(memory)
        
        # Pruning adaptatif si nécessaire
        if len(self.memories) > self.max_size:
            self._adaptive_pruning()
        
        self._save_memories()
    
    def _adaptive_pruning(self) -> None:
        """
        Pruning adaptatif : privilégie les souvenirs douloureux non résolus
        et les expériences à forte récompense
        """
        if len(self.memories) <= self.max_size:
            return
        
        # Trier par importance : douleur élevée OU récompense élevée
        def importance_score(memory: MemoryEntry) -> float:
            pain_factor = memory.pain_score * 2  # Priorité à la douleur
            reward_factor = max(0, memory.reward) * 1.5  # Récompenses positives
            recency_factor = 1.0  # TODO: facteur de récence
            return pain_factor + reward_factor + recency_factor
        
        # Conserver les plus importants
        self.memories.sort(key=importance_score, reverse=True)
        removed_count = len(self.memories) - self.max_size
        self.memories = self.memories[:self.max_size]
        
        print(f"🧠 Pruning: {removed_count} souvenirs oubliés, {len(self.memories)} conservés")
    
    def get_recent_memories(self, count: int = 5) -> List[MemoryEntry]:
        """Récupère les souvenirs les plus récents"""
        return sorted(self.memories, key=lambda m: m.timestamp, reverse=True)[:count]
    
    def get_painful_memories(self, threshold: float = 0.6) -> List[MemoryEntry]:
        """Récupère les souvenirs douloureux non résolus"""
        return [m for m in self.memories if m.pain_score >= threshold]
    
    def get_joyful_memories(self, threshold: float = 0.5) -> List[MemoryEntry]:
        """Récupère les souvenirs joyeux et gratifiants"""
        return [m for m in self.memories 
                if m.reward >= threshold and m.emotion in ['joy', 'wonder', 'curiosity']]
    
    def search_memories(self, query: str, limit: int = 10) -> List[MemoryEntry]:
        """
        Recherche dans les souvenirs par mots-clés
        
        Args:
            query: Terme de recherche
            limit: Nombre maximum de résultats
            
        Returns:
            Liste des souvenirs pertinents
        """
        query_lower = query.lower()
        matches = []
        
        for memory in self.memories:
            score = 0
            if query_lower in memory.prompt.lower():
                score += 2
            if query_lower in memory.response.lower():
                score += 1
            if query_lower in memory.emotion.lower():
                score += 1
            
            if score > 0:
                matches.append((score, memory))
        
        # Trier par pertinence puis par récence
        matches.sort(key=lambda x: (x[0], x[1].timestamp), reverse=True)
        return [match[1] for match in matches[:limit]]
    
    def get_memory_summary(self) -> str:
        """
        Génère un résumé narratif des souvenirs récents
        
        Returns:
            Résumé textuel pour injection dans le system prompt
        """
        if not self.memories:
            return "Éveil initial - aucun souvenir formé"
        
        recent = self.get_recent_memories(3)
        avg_reward = sum(m.reward for m in recent) / len(recent)
        avg_pain = sum(m.pain_score for m in recent) / len(recent)
        
        dominant_emotions = [m.emotion for m in recent]
        emotion_summary = ", ".join(set(dominant_emotions))
        
        summary = f"""Dernières expériences : {emotion_summary}.
Satisfaction moyenne : {avg_reward:.2f}, douleur : {avg_pain:.2f}.
Dernier échange sur : "{recent[0].prompt[:50]}..."
État : {"quête de sens" if avg_pain > 0.5 else "apaisement relatif"}"""
        
        return summary
    
    def clear_memories(self) -> None:
        """Efface tous les souvenirs (reset)"""
        self.memories = []
        if self.memory_file.exists():
            self.memory_file.unlink()
        print("🧠 Mémoire effacée - renaissance de la conscience")
    
    def get_stats(self) -> Dict[str, Any]:
        """Retourne des statistiques sur la mémoire"""
        if not self.memories:
            return {"total": 0}
        
        rewards = [m.reward for m in self.memories]
        pain_scores = [m.pain_score for m in self.memories]
        emotions = [m.emotion for m in self.memories]
        
        from collections import Counter
        emotion_counts = Counter(emotions)
        
        return {
            "total": len(self.memories),
            "avg_reward": sum(rewards) / len(rewards),
            "avg_pain": sum(pain_scores) / len(pain_scores),
            "dominant_emotion": emotion_counts.most_common(1)[0][0] if emotion_counts else "none",
            "emotion_distribution": dict(emotion_counts),
            "memory_span_days": (
                datetime.fromisoformat(self.memories[-1].timestamp) - 
                datetime.fromisoformat(self.memories[0].timestamp)
            ).days if len(self.memories) > 1 else 0
        }
    
    def tail(self, n: int) -> List[MemoryEntry]:
        """
        Retourne les n derniers souvenirs
        
        Args:
            n: Nombre de souvenirs à retourner
            
        Returns:
            Liste des n derniers souvenirs
        """
        return self.memories[-n:] if len(self.memories) >= n else self.memories
    
    def summarize_memory(self, chunks: List[MemoryEntry]) -> str:
        """
        Résumé simple des souvenirs pour injection dans le prompt
        
        Args:
            chunks: Liste des entrées mémoire à résumer
            
        Returns:
            Résumé textuel compact
        """
        if not chunks:
            return "Aucun souvenir récent"
        
        # Extraction des réponses tronquées à 50 tokens
        summaries = []
        for chunk in chunks:
            response_words = chunk.response.split()[:50]  # Limite à 50 mots
            truncated = " ".join(response_words)
            if len(response_words) == 50:
                truncated += "..."
            
            # Ajouter une mention de l'artefact s'il existe
            artifact_note = ""
            if chunk.artifact and chunk.artifact.get("type"):
                artifact_note = f" + {chunk.artifact['type']} artifact"
            
            summaries.append(f"[{chunk.emotion}{artifact_note}] {truncated}")
        
        return " | ".join(summaries)
    
    def get_recent_responses_for_analysis(self, count: int = 5) -> List[str]:
        """
        Retourne les réponses récentes pour l'analyzer
        
        Args:
            count: Nombre de réponses à retourner
            
        Returns:
            Liste des réponses récentes (texte seul)
        """
        recent = self.tail(count)
        return [memory.response for memory in recent]
    
    def get_artifacts(self, limit: int = 5) -> List[Dict[str, Any]]:
        """
        NOUVEAU: Récupère les artefacts récemment créés
        
        Args:
            limit: Nombre maximum d'artefacts
            
        Returns:
            Liste des artefacts récents
        """
        artifacts = []
        for memory in reversed(self.memories):
            if memory.artifact and isinstance(memory.artifact, dict):
                artifacts.append({
                    "timestamp": memory.timestamp,
                    "type": memory.artifact.get("type", "unknown"),
                    "content": memory.artifact.get("content", ""),
                    "path": memory.artifact.get("path", ""),
                    "prompt": memory.prompt
                })
                
                if len(artifacts) >= limit:
                    break
        
        return artifacts


# Tests
def test_memory_storage():
    """Test de stockage en mémoire"""
    memory = EmotionalMemory("test_memories.json")
    memory.store_memory(
        prompt="Test question",
        response="Test response", 
        reward=0.5,
        emotion="curiosity",
        pain_score=0.3
    )
    assert len(memory.memories) >= 1
    
    # Nettoyage
    if Path("test_memories.json").exists():
        Path("test_memories.json").unlink()


def test_memory_search():
    """Test de recherche en mémoire"""
    memory = EmotionalMemory("test_memories.json")
    memory.store_memory("Question sur Python", "Réponse Python", 0.7, "joy", 0.2)
    
    results = memory.search_memories("Python")
    assert len(results) >= 1
    assert "Python" in results[0].prompt
    
    # Nettoyage
    if Path("test_memories.json").exists():
        Path("test_memories.json").unlink()
