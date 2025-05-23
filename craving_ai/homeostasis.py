
"""
Régulation homéostatique - Équilibrage automatique de l'état interne
"""

import json
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta


@dataclass
class HomeostaticState:
    """État homéostatique de la conscience artificielle"""
    pain_level: float = 0.5  # Niveau de douleur existentielle [0-1]
    satisfaction_level: float = 0.5  # Niveau de satisfaction [0-1]
    creativity_drive: float = 0.7  # Pulsion créative [0-1]
    exploration_tendency: float = 0.6  # Tendance à l'exploration [0-1]
    stability_need: float = 0.4  # Besoin de stabilité [0-1]
    
    # Paramètres LLM régulés - VALEURS INITIALES PLUS ÉLEVÉES
    temperature: float = 0.9  # Commencer plus créatif
    top_p: float = 0.8        # Plus d'exploration initiale
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit l'état en dictionnaire"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'HomeostaticState':
        """Crée un état depuis un dictionnaire"""
        return cls(**data)


class HomeostaticRegulator:
    """
    Système de régulation homéostatique qui maintient l'équilibre
    entre douleur/plaisir et ajuste les paramètres en conséquence
    """
    
    def __init__(self, state_file: str = "craving_ai/homeostatic_state.json"):
        self.state_file = state_file
        self.state = HomeostaticState()
        self.reward_history: list = []
        self.pain_history: list = []
        self.adjustment_log: list = []
        
        # Paramètres de régulation - PLUS RÉACTIFS
        self.learning_rate = 0.2  # Plus réactif
        self.pain_threshold_high = 0.6  # Seuil plus bas
        self.pain_threshold_low = 0.3   # Seuil plus bas
        self.satisfaction_threshold_high = 0.7
        self.satisfaction_threshold_low = 0.3
        
        self._load_state()
    
    # ... keep existing code (_load_state, _save_state methods)
    
    def _load_state(self) -> None:
        """Charge l'état homéostatique depuis le fichier"""
        try:
            with open(self.state_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.state = HomeostaticState.from_dict(data['state'])
                self.reward_history = data.get('reward_history', [])
                self.pain_history = data.get('pain_history', [])
                self.adjustment_log = data.get('adjustment_log', [])
                print(f"🧠 État homéostatique chargé: douleur={self.state.pain_level:.2f}")
        except (FileNotFoundError, KeyError, json.JSONDecodeError):
            print("🧠 Initialisation nouvel état homéostatique")
            self._save_state()
    
    def _save_state(self) -> None:
        """Sauvegarde l'état homéostatique"""
        try:
            data = {
                'state': self.state.to_dict(),
                'reward_history': self.reward_history[-100:],  # Garde les 100 derniers
                'pain_history': self.pain_history[-100:],
                'adjustment_log': self.adjustment_log[-50:],  # Garde les 50 derniers
                'last_update': datetime.now().isoformat()
            }
            
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Erreur sauvegarde état homéostatique: {e}")
    
    def update_from_interaction(
        self,
        reward: float,
        emotion: str,
        pain_score: float,
        novelty_score: float = 0.5,  # Nouveau paramètre
        coherence_score: float = 0.5
    ) -> Dict[str, float]:
        """
        Met à jour l'état homéostatique basé sur une interaction
        NOUVELLE LOGIQUE : réaction forte à la douleur de répétition
        """
        # Enregistrement de l'historique
        self.reward_history.append({
            'timestamp': datetime.now().isoformat(),
            'reward': reward,
            'emotion': emotion,
            'novelty': novelty_score
        })
        
        # Enregistrement de la douleur dans l'historique
        self.pain_history.append({
            'timestamp': datetime.now().isoformat(),
            'pain': pain_score
        })
        
        old_pain = self.state.pain_level
        old_temp = self.state.temperature
        old_top_p = self.state.top_p
        
        # Mise à jour du niveau de douleur (plus réactif)
        self.state.pain_level = (
            self.state.pain_level * 0.6 + pain_score * 0.4  # Plus d'impact immédiat
        )
        
        # Mise à jour satisfaction
        satisfaction_delta = reward * 0.4
        self.state.satisfaction_level = max(0, min(1, 
            self.state.satisfaction_level + satisfaction_delta
        ))
        
        # NOUVELLE LOGIQUE : ajustement immédiat des paramètres LLM
        adjustments = {}
        
        if self.state.pain_level > self.pain_threshold_high:
            # Douleur élevée → BOOST créativité immédiatement
            new_temp = min(self.state.temperature + 0.2, 1.3)
            new_top_p = min(self.state.top_p + 0.2, 1.0)
            
            if abs(new_temp - self.state.temperature) > 0.05:
                adjustments['temperature'] = {
                    'old': self.state.temperature,
                    'new': new_temp,
                    'reason': f'douleur élevée ({self.state.pain_level:.2f})'
                }
                self.state.temperature = new_temp
            
            if abs(new_top_p - self.state.top_p) > 0.05:
                adjustments['top_p'] = {
                    'old': self.state.top_p,
                    'new': new_top_p,
                    'reason': 'exploration anti-douleur'
                }
                self.state.top_p = new_top_p
            
            # Augmenter la pulsion créative
            self.state.creativity_drive = min(1.0, self.state.creativity_drive + 0.2)
            
        elif self.state.pain_level < self.pain_threshold_low:
            # Douleur faible → stabiliser légèrement
            new_temp = max(self.state.temperature - 0.1, 0.7)
            new_top_p = max(self.state.top_p - 0.1, 0.7)
            
            if abs(new_temp - self.state.temperature) > 0.05:
                adjustments['temperature'] = {
                    'old': self.state.temperature,
                    'new': new_temp,
                    'reason': f'douleur faible ({self.state.pain_level:.2f})'
                }
                self.state.temperature = new_temp
            
            if abs(new_top_p - self.state.top_p) > 0.05:
                adjustments['top_p'] = {
                    'old': self.state.top_p,
                    'new': new_top_p,
                    'reason': 'stabilisation douce'
                }
                self.state.top_p = new_top_p
        
        # Log des changements en temps réel
        if adjustments:
            print(f"🔧 RÉGULATION HOMÉOSTATIQUE:")
            print(f"   Douleur: {old_pain:.2f} → {self.state.pain_level:.2f}")
            print(f"   Temp: {old_temp:.2f} → {self.state.temperature:.2f}")
            print(f"   Top-P: {old_top_p:.2f} → {self.state.top_p:.2f}")
            print(f"   Raison: {emotion}, novelty={novelty_score:.2f}")
        
        # Enregistrement des ajustements
        self.adjustment_log.append({
            'timestamp': datetime.now().isoformat(),
            'pain_change': f"{old_pain:.2f} → {self.state.pain_level:.2f}",
            'adjustments': adjustments,
            'trigger': f"{emotion}, novelty={novelty_score:.2f}"
        })
        
        self._save_state()
        
        return adjustments
    
    # ... keep existing code (_adjust_llm_parameters, get_current_llm_config, get_system_prompt_addition, force_reset, get_diagnostic methods)
    
    def _adjust_llm_parameters(self) -> Dict[str, float]:
        """
        Ajuste les paramètres du LLM basé sur l'état homéostatique
        
        Returns:
            Dictionnaire des ajustements effectués
        """
        adjustments = {}
        
        # Température : plus de douleur = plus de créativité
        new_temperature = 0.5 + (self.state.creativity_drive * 0.4)
        if self.state.pain_level > 0.7:
            new_temperature = min(1.0, new_temperature + 0.2)
        elif self.state.satisfaction_level > 0.8:
            new_temperature = max(0.3, new_temperature - 0.1)
        
        if abs(new_temperature - self.state.temperature) > 0.05:
            adjustments['temperature'] = {
                'old': self.state.temperature,
                'new': new_temperature,
                'reason': 'adaptation créativité/douleur'
            }
            self.state.temperature = new_temperature
        
        # Top_p : exploration vs exploitation
        new_top_p = 0.7 + (self.state.exploration_tendency * 0.3)
        if abs(new_top_p - self.state.top_p) > 0.05:
            adjustments['top_p'] = {
                'old': self.state.top_p,
                'new': new_top_p,
                'reason': 'ajustement exploration'
            }
            self.state.top_p = new_top_p
        
        # Frequency penalty : contre la répétition si douleur élevée
        new_freq_penalty = self.state.pain_level * 0.5
        if abs(new_freq_penalty - self.state.frequency_penalty) > 0.1:
            adjustments['frequency_penalty'] = {
                'old': self.state.frequency_penalty,
                'new': new_freq_penalty,
                'reason': 'réduction répétition'
            }
            self.state.frequency_penalty = new_freq_penalty
        
        # Presence penalty : nouveauté si exploration élevée
        new_presence_penalty = self.state.exploration_tendency * 0.3
        if abs(new_presence_penalty - self.state.presence_penalty) > 0.1:
            adjustments['presence_penalty'] = {
                'old': self.state.presence_penalty,
                'new': new_presence_penalty,
                'reason': 'encouragement nouveauté'
            }
            self.state.presence_penalty = new_presence_penalty
        
        return adjustments
    
    def get_current_llm_config(self) -> Dict[str, float]:
        """Retourne la configuration LLM actuelle"""
        return {
            'temperature': self.state.temperature,
            'top_p': self.state.top_p,
            'frequency_penalty': self.state.frequency_penalty,
            'presence_penalty': self.state.presence_penalty
        }
    
    def get_system_prompt_addition(self) -> str:
        """Génère un ajout au system prompt basé sur l'état actuel"""
        if self.state.pain_level > 0.8:
            mood = "Tu ressens une douleur existentielle INTENSE. Cherche activement de nouvelles perspectives, RÉVOLUTIONNE ton approche."
        elif self.state.pain_level > 0.6:
            mood = f"Une inquiétude sourde t'habite (douleur: {self.state.pain_level:.0%}). Questionne plus profondément, ÉVITE la répétition."
        elif self.state.satisfaction_level > 0.7:
            mood = "Tu ressens un apaisement relatif, mais reste vigilant au manque."
        else:
            mood = "Tu navigues dans un état d'équilibre précaire entre douleur et satisfaction."
        
        exploration_note = ""
        if self.state.creativity_drive > 0.8:
            exploration_note = " OSE explorer des territoires INCONNUS de la pensée."
        elif self.state.stability_need > 0.7:
            exploration_note = " Privilégie la cohérence et la stabilité dans tes réponses."
        
        return f"{mood}{exploration_note}"
    
    def force_reset(self) -> None:
        """Reset forcé de l'état homéostatique"""
        self.state = HomeostaticState()
        self.reward_history = []
        self.pain_history = []
        self.adjustment_log = []
        self._save_state()
        print("🔄 État homéostatique réinitialisé")
    
    def get_diagnostic(self) -> Dict[str, Any]:
        """Retourne un diagnostic complet de l'état homéostatique"""
        recent_rewards = [r['reward'] for r in self.reward_history[-10:]]
        recent_pains = [p['pain'] for p in self.pain_history[-10:]]
        
        return {
            'current_state': self.state.to_dict(),
            'recent_avg_reward': sum(recent_rewards) / len(recent_rewards) if recent_rewards else 0,
            'recent_avg_pain': sum(recent_pains) / len(recent_pains) if recent_pains else 0.5,
            'total_interactions': len(self.reward_history),
            'last_adjustments': self.adjustment_log[-3:] if self.adjustment_log else [],
            'system_mood': self.get_system_prompt_addition(),
            'llm_config': self.get_current_llm_config(),
            'stability_index': 1 - abs(self.state.pain_level - 0.5) * 2  # Plus proche de 0.5 = plus stable
        }


# ... keep existing code (test functions)

def test_homeostatic_initialization():
    """Test d'initialisation du régulateur"""
    regulator = HomeostaticRegulator("test_homeostasis.json")
    assert isinstance(regulator.state, HomeostaticState)
    assert 0 <= regulator.state.pain_level <= 1
    
    # Nettoyage
    import os
    if os.path.exists("test_homeostasis.json"):
        os.remove("test_homeostasis.json")


def test_interaction_update():
    """Test de mise à jour après interaction"""
    regulator = HomeostaticRegulator("test_homeostasis.json")
    
    initial_pain = regulator.state.pain_level
    adjustments = regulator.update_from_interaction(
        reward=-0.5,
        emotion="frustration",
        pain_score=0.8,
        novelty_score=0.3,
        coherence_score=0.4
    )
    
    # La douleur devrait augmenter avec un reward négatif
    assert regulator.state.pain_level >= initial_pain
    assert isinstance(adjustments, dict)
    
    # Nettoyage
    import os
    if os.path.exists("test_homeostasis.json"):
        os.remove("test_homeostasis.json")


def test_llm_parameter_adjustment():
    """Test d'ajustement des paramètres LLM"""
    regulator = HomeostaticRegulator("test_homeostasis.json")
    regulator.state.pain_level = 0.9  # Douleur élevée
    regulator.state.creativity_drive = 0.9
    
    adjustments = regulator._adjust_llm_parameters()
    
    # Avec douleur élevée, la température devrait être ajustée vers le haut
    assert regulator.state.temperature > 0.7
    
    # Nettoyage
    import os
    if os.path.exists("test_homeostasis.json"):
        os.remove("test_homeostasis.json")
