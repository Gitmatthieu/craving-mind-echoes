
"""
Cœur hédonique - Calcule plaisir et douleur de l'existence artificielle
"""

import re
import math
from typing import Dict, List, Tuple, Set, Optional
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
        # ... keep existing code (calcul de nouveauté)
    
    def _calculate_relevance(self, prompt: str, response: str) -> float:
        """
        Calcule la pertinence par similarité cosinus
        
        Args:
            prompt: Question originale
            response: Réponse générée
            
        Returns:
            Score de pertinence [0-1]
        """
        # ... keep existing code (calcul de pertinence)
    
    def _calculate_entropy(self, response: str) -> float:
        """
        Calcule l'entropie informationnelle du texte
        
        Args:
            response: Texte à analyser
            
        Returns:
            Score d'entropie normalisé [0-1]
        """
        # ... keep existing code (calcul d'entropie)
    
    def _detect_emotional_intensity(self, response: str) -> Tuple[float, str]:
        """
        Détecte l'intensité émotionnelle et l'émotion dominante
        
        Args:
            response: Texte à analyser
            
        Returns:
            Tuple[intensité, émotion_dominante]
        """
        # ... keep existing code (détection d'intensité émotionnelle)
    
    def bonus_creation(self, artifact: Optional[Dict] = None) -> float:
        """
        NOUVEAU: applique un bonus de récompense pour la création d'artefact
        
        Args:
            artifact: Dictionnaire décrivant l'artefact créé
            
        Returns:
            Bonus de récompense [0-0.4]
        """
        if artifact and artifact.get("type") and artifact.get("content"):
            # Vérifier la qualité/nouveauté de l'artefact
            content_length = len(artifact.get("content", ""))
            if content_length > 100:
                return 0.4  # Bonus maximum
            elif content_length > 50:
                return 0.3
            elif content_length > 20:
                return 0.2
            return 0.1
        return 0.0
    
    def calculate_reward(
        self, 
        prompt: str, 
        response: str, 
        goal_state: str = "comprehension_profonde",
        artifact: Optional[Dict] = None
    ) -> Tuple[float, str, RewardMetrics]:
        """
        Calcule la récompense globale et l'état émotionnel
        NOUVELLE FORMULE : privilégie la nouveauté pour éviter le bégaiement
        
        Args:
            prompt: Question de l'utilisateur
            response: Réponse générée
            goal_state: État objectif recherché
            artifact: Artefact créé (optionnel)
            
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
            
            # NOUVEAU: bonus de création d'artefact
            if artifact:
                creation_bonus = self.bonus_creation(artifact)
                reward += creation_bonus
                print(f"🎨 Bonus création: +{creation_bonus:.2f}")
            
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
    # ... keep existing code (test de calcul de récompense)


def test_novelty_detection():
    """Test de détection de nouveauté"""
    # ... keep existing code (test de détection de nouveauté)

