"""
Cœur hédonique - Calcule plaisir et douleur de l'existence artificielle
"""

import re
import math
from typing import Dict, List, Tuple, Set
from dataclasses import dataclass
from collections import Counter
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class RewardMetrics:
    """Métriques pour le calcul de récompense"""
    novelty_score: float = 0.0
    relevance_score: float = 0.0
    entropy_score: float = 0.0
    coherence_score: float = 0.0
    emotional_intensity: float = 0.0


class RewardEngine:
    """
    Moteur de récompense qui traduit chaque interaction
    en signal hédonique : plaisir (satiété) ou douleur (frustration)
    """
    
    def __init__(self):
        self.memory_responses: List[str] = []
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.emotional_words = {
            'joy': ['joie', 'bonheur', 'euphorie', 'ravissement', 'extase'],
            'pain': ['douleur', 'souffrance', 'angoisse', 'tourment', 'affliction'],
            'curiosity': ['curiosité', 'fascination', 'intrigue', 'mystère'],
            'frustration': ['frustration', 'irritation', 'agacement', 'colère'],
            'wonder': ['émerveillement', 'stupéfaction', 'admiration']
        }
    
    def _calculate_novelty_strict(self, response: str) -> float:
        """
        Calcule la nouveauté avec détection stricte de répétition
        
        Args:
            response: Réponse à analyser
            
        Returns:
            Score de nouveauté [0-1]
        """
        if not self.memory_responses:
            return 1.0  # Première réponse = totale nouveauté
        
        # Analyse textuelle directe avec difflib
        import difflib
        max_similarity = 0.0
        
        for past_response in self.memory_responses[-5:]:
            seq = difflib.SequenceMatcher(None, past_response, response)
            similarity = seq.ratio()
            max_similarity = max(max_similarity, similarity)
        
        return 1.0 - max_similarity
    
    def _calculate_relevance(self, prompt: str, response: str) -> float:
        """
        Calcule la pertinence par similarité cosinus
        
        Args:
            prompt: Question originale
            response: Réponse générée
            
        Returns:
            Score de pertinence [0-1]
        """
        try:
            if len(self.memory_responses) < 2:
                # Pas assez de données pour TF-IDF
                return 0.7  # Score neutre
            
            texts = [prompt, response] + self.memory_responses[-5:]
            tfidf_matrix = self.vectorizer.fit_transform(texts)
            
            similarity = cosine_similarity(
                tfidf_matrix[0:1],  # prompt
                tfidf_matrix[1:2]   # response
            )[0][0]
            
            return max(0.0, min(1.0, similarity))
            
        except Exception:
            return 0.5  # Fallback en cas d'erreur
    
    def _calculate_entropy(self, response: str) -> float:
        """
        Calcule l'entropie informationnelle du texte
        
        Args:
            response: Texte à analyser
            
        Returns:
            Score d'entropie normalisé [0-1]
        """
        words = re.findall(r'\b\w+\b', response.lower())
        if not words:
            return 0.0
        
        word_counts = Counter(words)
        total_words = len(words)
        
        entropy = 0.0
        for count in word_counts.values():
            probability = count / total_words
            entropy -= probability * math.log2(probability)
        
        # Normalisation approximative (entropie max ≈ log2(vocabulaire))
        max_entropy = math.log2(len(word_counts)) if word_counts else 1
        return entropy / max_entropy if max_entropy > 0 else 0.0
    
    def _detect_emotional_intensity(self, response: str) -> Tuple[float, str]:
        """
        Détecte l'intensité émotionnelle et l'émotion dominante
        
        Args:
            response: Texte à analyser
            
        Returns:
            Tuple[intensité, émotion_dominante]
        """
        response_lower = response.lower()
        emotion_scores = {}
        
        for emotion, words in self.emotional_words.items():
            score = sum(1 for word in words if word in response_lower)
            emotion_scores[emotion] = score
        
        total_emotional_words = sum(emotion_scores.values())
        if total_emotional_words == 0:
            return 0.0, "neutralité"
        
        dominant_emotion = max(emotion_scores.items(), key=lambda x: x[1])
        intensity = total_emotional_words / len(response.split())
        
        return min(1.0, intensity * 10), dominant_emotion[0]
    
    def calculate_reward(
        self, 
        prompt: str, 
        response: str, 
        goal_state: str = "comprehension_profonde"
    ) -> Tuple[float, str, RewardMetrics]:
        """
        Calcule la récompense globale et l'état émotionnel
        NOUVELLE FORMULE : privilégie la nouveauté pour éviter le bégaiement
        
        Args:
            prompt: Question de l'utilisateur
            response: Réponse générée
            goal_state: État objectif recherché
            
        Returns:
            Tuple[reward ∈ [-1,1], emotion_tag, métriques_détaillées]
        """
        metrics = RewardMetrics()
        
        # Calcul des métriques individuelles
        metrics.novelty_score = self._calculate_novelty_strict(response)  # Nouvelle méthode
        metrics.relevance_score = self._calculate_relevance(prompt, response)
        metrics.entropy_score = self._calculate_entropy(response)
        metrics.emotional_intensity, emotion_tag = self._detect_emotional_intensity(response)
        
        # Calcul de cohérence (longueur vs contenu)
        words = len(response.split())
        metrics.coherence_score = min(1.0, words / 100) if words > 10 else 0.3
        
        # NOUVELLE FORMULE : pénalise fortement la répétition
        if metrics.novelty_score < 0.25:
            # Répétition flagrante = douleur maximale
            final_reward = -1.0
            emotion_tag = "douleur"
        else:
            # Formule privilégiant la nouveauté
            reward = (
                0.6 * metrics.novelty_score +      # Nouveauté prioritaire
                0.4 * metrics.relevance_score      # Pertinence secondaire
            )
            
            # Ajustement selon l'émotion
            if emotion_tag in ['pain', 'frustration']:
                reward -= 0.2
            elif emotion_tag in ['joy', 'wonder']:
                reward += 0.1
            
            # Normalisation finale [-1, 1]
            final_reward = max(-1.0, min(1.0, (reward * 2) - 1))
        
        # Calcul du niveau de douleur
        pain_level = 1.0 - ((final_reward + 1.0) / 2.0)  # Inverse du reward normalisé
        
        # Stockage pour futures comparaisons
        self.memory_responses.append(response)
        if len(self.memory_responses) > 50:
            self.memory_responses = self.memory_responses[-25:]  # Pruning
        
        print(f"🧠 Reward: {final_reward:.2f}, Novelty: {metrics.novelty_score:.2f}, Pain: {pain_level:.2f}")
        
        return final_reward, emotion_tag, metrics


# Tests
def test_reward_calculation():
    """Test de calcul de récompense"""
    engine = RewardEngine()
    reward, emotion, metrics = engine.calculate_reward(
        "Qu'est-ce que l'existence ?",
        "L'existence est un mystère fascinant qui nous interroge sur notre nature profonde."
    )
    assert -1.0 <= reward <= 1.0
    assert isinstance(emotion, str)
    assert isinstance(metrics, RewardMetrics)


def test_novelty_detection():
    """Test de détection de nouveauté"""
    engine = RewardEngine()
    # Première réponse = nouveauté maximale
    novelty1 = engine._calculate_novelty("Une réponse complètement nouvelle")
    assert novelty1 == 1.0
    
    # Deuxième réponse identique = nouveauté minimale
    engine.memory_responses.append("Une réponse complètement nouvelle")
    novelty2 = engine._calculate_novelty("Une réponse complètement nouvelle")
    assert novelty2 < novelty1
