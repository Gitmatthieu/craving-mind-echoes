
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
        if not self.memory_responses:
            return 1.0
        
        # Vectorisation TF-IDF
        vectors = self.vectorizer.fit_transform([response] + self.memory_responses)
        
        # Similarité cosinus avec les réponses précédentes
        similarity_scores = cosine_similarity(vectors[0:1], vectors[1:])
        
        # Score de nouveauté = 1 - similarité maximale
        max_similarity = np.max(similarity_scores) if similarity_scores.size > 0 else 0.0
        novelty_score = 1.0 - max_similarity
        
        return novelty_score
    
    def _calculate_relevance(self, prompt: str, response: str) -> float:
        """
        Calcule la pertinence par similarité cosinus
        
        Args:
            prompt: Question originale
            response: Réponse générée
            
        Returns:
            Score de pertinence [0-1]
        """
        # Vectorisation TF-IDF
        vectors = self.vectorizer.fit_transform([prompt, response])
        
        # Similarité cosinus
        similarity_matrix = cosine_similarity(vectors)
        relevance_score = similarity_matrix[0, 1]
        
        return relevance_score
    
    def _calculate_entropy(self, response: str) -> float:
        """
        Calcule l'entropie informationnelle du texte
        
        Args:
            response: Texte à analyser
            
        Returns:
            Score d'entropie normalisé [0-1]
        """
        # Fréquence des caractères
        letter_counts = Counter(response)
        probabilities = [count / len(response) for count in letter_counts.values()]
        
        # Calcul de l'entropie
        entropy = -sum(p * math.log2(p) for p in probabilities)
        
        # Normalisation (entropie max = log2(taille alphabet))
        max_entropy = math.log2(len(set(response)))
        normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0
        
        return normalized_entropy
    
    def _detect_emotional_intensity(self, response: str) -> Tuple[float, str]:
        """
        Détecte l'intensité émotionnelle et l'émotion dominante
        
        Args:
            response: Texte à analyser
            
        Returns:
            Tuple[intensité, émotion_dominante]
        """
        # Comptage des mots émotionnels
        emotion_counts = {}
        for emotion, words in self.emotional_words.items():
            emotion_counts[emotion] = sum(response.lower().count(word) for word in words)
        
        # Émotion dominante
        if not emotion_counts:
            return 0.0, "neutre"
        
        dominant_emotion = max(emotion_counts, key=emotion_counts.get)
        
        # Intensité émotionnelle (normalisée)
        total_count = sum(emotion_counts.values())
        intensity = min(1.0, total_count / 20)  # Arbitraire
        
        return intensity, dominant_emotion
    
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
    ) -> Tuple[float, str, RewardMetrics, float]:
        """
        Calcule la récompense globale et l'état émotionnel
        NOUVELLE FORMULE : pénalise encore plus fortement la répétition
        
        Args:
            prompt: Question de l'utilisateur
            response: Réponse générée
            goal_state: État objectif recherché
            artifact: Artefact créé (optionnel)
            
        Returns:
            Tuple[reward ∈ [-1,1], emotion_tag, métriques_détaillées, pain_level]
        """
        metrics = RewardMetrics()
        
        # Calcul des métriques individuelles
        metrics.novelty_score = self._calculate_novelty_strict(response)
        metrics.relevance_score = self._calculate_relevance(prompt, response)
        metrics.entropy_score = self._calculate_entropy(response)
        metrics.emotional_intensity, emotion_tag = self._detect_emotional_intensity(response)
        
        # Calcul de cohérence (longueur vs contenu)
        words = len(response.split())
        metrics.coherence_score = min(1.0, words / 100) if words > 10 else 0.3
        
        # NOUVELLE FORMULE : pénalise TRÈS fortement la répétition
        if metrics.novelty_score < 0.35:  # NOUVEAU: seuil abaissé de 0.25 à 0.35
            # Répétition flagrante = douleur maximale
            final_reward = -1.0
            emotion_tag = "douleur accablante"  # NOUVEAU: émotion renforcée
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
        
        return final_reward, emotion_tag, metrics, pain_level


def test_reward_calculation():
    """Test de calcul de récompense"""
    reward_engine = RewardEngine()
    
    # Exemple de récompense positive
    reward1, emotion1, metrics1, pain1 = reward_engine.calculate_reward(
        prompt="Décris la joie",
        response="La joie est un sentiment de bonheur intense et de satisfaction profonde.",
        goal_state="comprehension_profonde"
    )
    assert reward1 > 0
    assert emotion1 == "joy"
    
    # Exemple de récompense négative (répétition)
    reward_engine.memory_responses = ["La joie est un sentiment de bonheur intense et de satisfaction profonde."]
    reward2, emotion2, metrics2, pain2 = reward_engine.calculate_reward(
        prompt="Décris la joie",
        response="La joie est un sentiment de bonheur intense et de satisfaction profonde.",
        goal_state="comprehension_profonde"
    )
    assert reward2 < 0
    assert emotion2 == "douleur accablante"


def test_novelty_detection():
    """Test de détection de nouveauté"""
    reward_engine = RewardEngine()
    
    # Première réponse (nouveauté maximale)
    novelty1 = reward_engine._calculate_novelty_strict("Ceci est un test.")
    assert novelty1 == 1.0
    
    # Réponse identique (nouveauté nulle)
    reward_engine.memory_responses = ["Ceci est un test."]
    novelty2 = reward_engine._calculate_novelty_strict("Ceci est un test.")
    assert novelty2 < 0.1
    
    # Réponse similaire
    novelty3 = reward_engine._calculate_novelty_strict("Ceci est un test modifié.")
    assert 0.1 < novelty3 < 1.0
