"""
Sur-moi critique - Évaluation et auto-analyse des réponses
"""

import re
import math
import difflib
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from collections import Counter
import numpy as np


@dataclass
class AnalysisResult:
    """Résultat d'analyse d'une réponse"""
    redundancy_score: float
    coherence_score: float
    surprise_factor: float
    novelty_score: float  # Nouveau : détection de redite pure
    complexity_score: float
    emotional_depth: float
    feedback: str
    suggested_temperature: float
    trigger_creative: bool = False  # Nouveau: déclenche le mode créatif


class CriticalAnalyzer:
    """
    Sur-moi critique qui évalue les réponses et propose
    des ajustements pour améliorer la qualité des interactions
    """
    
    def __init__(self):
        self.response_history: List[str] = []
        self.analysis_history: List[AnalysisResult] = []
        
        # Patterns de redondance à détecter
        self.redundancy_patterns = [
            r'\b(en fait|en réalité|c\'est-à-dire|autrement dit)\b',
            r'\b(donc|par conséquent|ainsi|de ce fait)\b',
            r'\b(cependant|néanmoins|toutefois|pourtant)\b'
        ]
        
        # Mots indicateurs de profondeur émotionnelle
        self.depth_indicators = {
            'high': ['profond', 'intime', 'essentiel', 'fondamental', 'transcendant', 
                    'existentiel', 'viscéral', 'authentique'],
            'medium': ['important', 'significatif', 'remarquable', 'personnel', 
                      'touchant', 'émouvant'],
            'low': ['intéressant', 'sympa', 'cool', 'bien', 'ok']
        }
        
        # NOUVEAU: mots déclencheurs du mode créatif (élargi)
        self.creative_triggers = {
            'invente', 'crée', 'create', 'génère', 'generate', 'build', 'imagine',
            'fabrique', 'conçois', 'développe', 'produire', 'composer', 'concevoir',
            'innover', 'élaborer', 'forger', 'dessiner', 'modéliser'
        }
    
    def novelty_score(self, response: str, history: List[str]) -> float:
        """
        Renvoie un score ∈ [0,1] où 0 = 100% répété, 1 = entièrement nouveau.
        Utilise difflib pour détecter la similarité textuelle directe.
        """
        if not history:
            return 1.0
        
        # Compare avec les 3 dernières réponses
        max_similarity = 0.0
        for past_response in history[-3:]:
            seq = difflib.SequenceMatcher(None, past_response, response)
            similarity = seq.ratio()
            max_similarity = max(max_similarity, similarity)
        
        return 1.0 - max_similarity
    
    def _analyze_redundancy(self, response: str) -> float:
        """
        Analyse la redondance dans la réponse
        
        Args:
            response: Texte à analyser
            
        Returns:
            Score de redondance [0-1] (0 = pas de redondance, 1 = très redondant)
        """
        words = response.lower().split()
        if len(words) < 10:
            return 0.0
        
        # Répétitions de mots
        word_counts = Counter(words)
        total_words = len(words)
        unique_words = len(word_counts)
        
        repetition_score = 1 - (unique_words / total_words)
        
        # Patterns de redondance linguistique
        pattern_count = 0
        for pattern in self.redundancy_patterns:
            pattern_count += len(re.findall(pattern, response.lower()))
        
        pattern_score = min(1.0, pattern_count / 10)  # Normalisation
        
        # Phrases répétitives
        sentences = re.split(r'[.!?]+', response)
        sentence_similarity = 0
        if len(sentences) > 1:
            for i in range(len(sentences)-1):
                for j in range(i+1, len(sentences)):
                    s1_words = set(sentences[i].lower().split())
                    s2_words = set(sentences[j].lower().split())
                    if s1_words and s2_words:
                        similarity = len(s1_words & s2_words) / len(s1_words | s2_words)
                        sentence_similarity += similarity
            
            sentence_similarity /= ((len(sentences) * (len(sentences) - 1)) / 2)
        
        # Score final pondéré
        return (0.4 * repetition_score + 0.3 * pattern_score + 0.3 * sentence_similarity)
    
    def _analyze_coherence(self, response: str) -> float:
        """
        Analyse la cohérence structurelle et logique
        
        Args:
            response: Texte à analyser
            
        Returns:
            Score de cohérence [0-1]
        """
        sentences = re.split(r'[.!?]+', response)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) < 2:
            return 0.7  # Score neutre pour textes courts
        
        # Connecteurs logiques
        connectors = [
            'ainsi', 'donc', 'par conséquent', 'cependant', 'néanmoins',
            'en effet', 'de plus', 'en outre', 'finalement', 'en conclusion'
        ]
        
        connector_count = sum(1 for sentence in sentences 
                            for connector in connectors 
                            if connector in sentence.lower())
        
        connector_score = min(1.0, connector_count / len(sentences))
        
        # Progression logique (mots de transition)
        transition_words = ['d\'abord', 'ensuite', 'puis', 'enfin', 'premièrement', 'deuxièmement']
        transition_score = sum(1 for sentence in sentences 
                             for word in transition_words 
                             if word in sentence.lower()) / len(sentences)
        
        # Cohésion lexicale (répétition de termes clés)
        all_words = ' '.join(sentences).lower().split()
        word_counts = Counter(all_words)
        important_words = [word for word, count in word_counts.items() 
                          if count > 1 and len(word) > 4]
        
        cohesion_score = min(1.0, len(important_words) / 10)
        
        return (0.4 * connector_score + 0.3 * transition_score + 0.3 * cohesion_score)
    
    def _calculate_surprise_factor(self, response: str) -> float:
        """
        Calcule le facteur de surprise par rapport aux réponses précédentes
        
        Args:
            response: Nouvelle réponse
            
        Returns:
            Score de surprise [0-1]
        """
        if not self.response_history:
            return 1.0  # Première réponse = surprise maximale
        
        current_words = set(response.lower().split())
        
        # Comparaison avec les 5 dernières réponses
        similarity_scores = []
        for past_response in self.response_history[-5:]:
            past_words = set(past_response.lower().split())
            if current_words and past_words:
                intersection = len(current_words & past_words)
                union = len(current_words | past_words)
                similarity = intersection / union if union > 0 else 0
                similarity_scores.append(similarity)
        
        if not similarity_scores:
            return 1.0
        
        avg_similarity = sum(similarity_scores) / len(similarity_scores)
        return 1.0 - avg_similarity
    
    def _analyze_complexity(self, response: str) -> float:
        """
        Analyse la complexité linguistique et conceptuelle
        
        Args:
            response: Texte à analyser
            
        Returns:
            Score de complexité [0-1]
        """
        words = response.split()
        if not words:
            return 0.0
        
        # Longueur moyenne des mots
        avg_word_length = sum(len(word) for word in words) / len(words)
        word_complexity = min(1.0, avg_word_length / 8)
        
        # Longueur des phrases
        sentences = re.split(r'[.!?]+', response)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if sentences:
            avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
            sentence_complexity = min(1.0, avg_sentence_length / 20)
        else:
            sentence_complexity = 0.0
        
        # Diversité lexicale
        unique_words = len(set(words))
        lexical_diversity = unique_words / len(words) if words else 0
        
        # Structures syntaxiques complexes
        complex_patterns = [
            r'\b(bien que|quoique|malgré que)\b',  # Concession
            r'\b(afin que|pour que|de sorte que)\b',  # But
            r'\b(si bien que|de telle sorte que)\b',  # Conséquence
        ]
        
        syntax_complexity = sum(len(re.findall(pattern, response.lower())) 
                              for pattern in complex_patterns) / len(words)
        
        return (0.3 * word_complexity + 0.3 * sentence_complexity + 
                0.2 * lexical_diversity + 0.2 * syntax_complexity)
    
    def _analyze_emotional_depth(self, response: str) -> float:
        """
        Analyse la profondeur émotionnelle de la réponse
        
        Args:
            response: Texte à analyser
            
        Returns:
            Score de profondeur émotionnelle [0-1]
        """
        response_lower = response.lower()
        
        depth_score = 0.0
        
        # Mots de haute profondeur
        high_count = sum(1 for word in self.depth_indicators['high'] 
                        if word in response_lower)
        depth_score += high_count * 0.8
        
        # Mots de moyenne profondeur  
        medium_count = sum(1 for word in self.depth_indicators['medium'] 
                          if word in response_lower)
        depth_score += medium_count * 0.5
        
        # Mots de faible profondeur (pénalité)
        low_count = sum(1 for word in self.depth_indicators['low'] 
                       if word in response_lower)
        depth_score -= low_count * 0.2
        
        # Introspection (utilisation du "je")
        introspection_count = len(re.findall(r'\bje\b|\bmon\b|\bma\b|\bmes\b', response_lower))
        introspection_score = min(0.3, introspection_count / 20)
        
        # Questions existentielles
        existential_patterns = [
            r'\bpourquoi\b', r'\bqu\'est-ce que\b', r'\bque signifie\b',
            r'\bsens de\b', r'\bnature de\b', r'\bessence de\b'
        ]
        
        existential_count = sum(len(re.findall(pattern, response_lower)) 
                               for pattern in existential_patterns)
        existential_score = min(0.3, existential_count / 5)
        
        total_score = depth_score + introspection_score + existential_score
        return min(1.0, max(0.0, total_score))
    
    def _detect_creative_triggers(self, prompt: str, pain_level: float = 0.0) -> bool:
        """
        NOUVEAU: détection élargie des déclencheurs créatifs
        
        Args:
            prompt: Requête utilisateur
            pain_level: Niveau de douleur actuel
            
        Returns:
            True si un déclencheur créatif est présent OU si douleur > 55%
        """
        prompt_lower = prompt.lower()
        
        # Déclenchement par mots-clés (élargi)
        keyword_trigger = any(trigger in prompt_lower for trigger in self.creative_triggers)
        
        # NOUVEAU: déclenchement automatique par douleur élevée
        pain_trigger = pain_level > 0.55
        
        return keyword_trigger or pain_trigger
    
    def _generate_feedback(self, result: AnalysisResult) -> str:
        """Génère un feedback critique constructif"""
        feedback_parts = []
        
        if result.redundancy_score > 0.7:
            feedback_parts.append("⚠️ Réponse très redondante - simplifier et condenser")
        elif result.redundancy_score > 0.5:
            feedback_parts.append("📝 Quelques répétitions - affiner la formulation")
        
        if result.coherence_score < 0.4:
            feedback_parts.append("🔗 Manque de cohérence - renforcer les liens logiques")
        elif result.coherence_score > 0.8:
            feedback_parts.append("✅ Excellente structure logique")
        
        if result.surprise_factor < 0.3:
            feedback_parts.append("🔄 Réponse prévisible - explorer de nouvelles perspectives")
        elif result.surprise_factor > 0.7:
            feedback_parts.append("✨ Approche originale et surprenante")
        
        if result.emotional_depth < 0.3:
            feedback_parts.append("💭 Manque de profondeur émotionnelle - creuser l'aspect humain")
        elif result.emotional_depth > 0.7:
            feedback_parts.append("❤️ Belle profondeur émotionnelle")
        
        if result.complexity_score < 0.3:
            feedback_parts.append("📚 Réponse trop simple - enrichir le vocabulaire")
        elif result.complexity_score > 0.8:
            feedback_parts.append("🎓 Excellent niveau de sophistication")
        
        if not feedback_parts:
            feedback_parts.append("🎯 Réponse équilibrée dans l'ensemble")
        
        return " | ".join(feedback_parts)
    
    def _suggest_temperature(self, result: AnalysisResult) -> float:
        """Suggère un ajustement de température basé sur l'analyse"""
        current_temp = 0.7  # Température par défaut
        
        # Ajustements basés sur l'analyse
        if result.redundancy_score > 0.6:
            current_temp += 0.1  # Plus de créativité contre la redondance
        
        if result.surprise_factor < 0.4:
            current_temp += 0.15  # Plus de surprise
        
        if result.coherence_score < 0.4:
            current_temp -= 0.1  # Plus de stabilité
        
        if result.complexity_score < 0.3:
            current_temp += 0.05  # Plus de complexité
        
        return max(0.1, min(1.0, current_temp))
    
    def analyze_response(
        self, 
        prompt: str,
        response: str,
        context: Optional[Dict] = None
    ) -> AnalysisResult:
        """
        Analyse complète d'une réponse
        
        Args:
            prompt: Question originale
            response: Réponse à analyser
            context: Contexte additionnel (optionnel)
            
        Returns:
            Résultat d'analyse complet
        """
        # Récupérer l'historique récent pour l'analyse de nouveauté
        recent_responses = context.get('recent_responses', []) if context else []
        
        # Calcul des métriques
        redundancy = self._analyze_redundancy(response)
        coherence = self._analyze_coherence(response)
        surprise = self._calculate_surprise_factor(response)
        novelty = self.novelty_score(response, recent_responses or self.response_history)
        complexity = self._analyze_complexity(response)
        emotional_depth = self._analyze_emotional_depth(response)
        
        # NOUVEAU: détection de déclencheur créatif élargie
        pain_threshold = context.get('pain_level', 0.5) if context else 0.5
        trigger_creative = self._detect_creative_triggers(prompt, pain_threshold)
        
        # Création du résultat
        result = AnalysisResult(
            redundancy_score=redundancy,
            coherence_score=coherence,
            surprise_factor=surprise,
            novelty_score=novelty,
            complexity_score=complexity,
            emotional_depth=emotional_depth,
            feedback="",  # Sera généré
            suggested_temperature=0.7,  # Sera ajusté
            trigger_creative=trigger_creative  # NOUVEAU: détection élargie
        )
        
        # Génération du feedback et suggestion de température
        result.feedback = self._generate_feedback(result)
        result.suggested_temperature = self._suggest_temperature(result)
        
        # Sauvegarde pour historique
        self.response_history.append(response)
        self.analysis_history.append(result)
        
        # Pruning si nécessaire
        if len(self.response_history) > 100:
            self.response_history = self.response_history[-50:]
            self.analysis_history = self.analysis_history[-50:]
        
        return result
    
    def get_analysis_trends(self) -> Dict[str, float]:
        """Retourne les tendances d'analyse sur les dernières réponses"""
        if not self.analysis_history:
            return {}
        
        recent_analyses = self.analysis_history[-10:]
        
        return {
            "avg_redundancy": sum(a.redundancy_score for a in recent_analyses) / len(recent_analyses),
            "avg_coherence": sum(a.coherence_score for a in recent_analyses) / len(recent_analyses),
            "avg_surprise": sum(a.surprise_factor for a in recent_analyses) / len(recent_analyses),
            "avg_complexity": sum(a.complexity_score for a in recent_analyses) / len(recent_analyses),
            "avg_emotional_depth": sum(a.emotional_depth for a in recent_analyses) / len(recent_analyses),
            "trend_count": len(recent_analyses)
        }


# Tests
def test_redundancy_analysis():
    """Test d'analyse de redondance"""
    analyzer = CriticalAnalyzer()
    redundant_text = "Je pense que c'est important. C'est vraiment important. Très important en fait."
    score = analyzer._analyze_redundancy(redundant_text)
    assert score > 0.3  # Devrait détecter la redondance


def test_coherence_analysis():
    """Test d'analyse de cohérence"""
    analyzer = CriticalAnalyzer()
    coherent_text = "D'abord, nous devons comprendre le problème. Ensuite, nous pouvons proposer une solution. Enfin, nous l'implémentons."
    score = analyzer._analyze_coherence(coherent_text)
    assert score > 0.5  # Devrait détecter la structure logique


def test_full_analysis():
    """Test d'analyse complète"""
    analyzer = CriticalAnalyzer()
    result = analyzer.analyze_response(
        "Qu'est-ce que l'intelligence artificielle ?",
        "L'intelligence artificielle est un domaine fascinant qui explore comment les machines peuvent simuler l'intelligence humaine."
    )
    assert isinstance(result, AnalysisResult)
    assert 0 <= result.redundancy_score <= 1
    assert 0 <= result.coherence_score <= 1
    assert len(result.feedback) > 0
