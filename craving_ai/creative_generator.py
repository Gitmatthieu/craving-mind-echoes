
"""
Moteur de génération créative - Externalisation de la tension intérieure
"""

from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

from .llm_wrapper import LLMWrapper


def call_llm(prompt: str, temp: float = 0.9) -> str:
    """Utilitaire pour appeler le LLM avec un prompt simple"""
    wrapper = LLMWrapper()
    wrapper.update_config(temperature=temp)
    response, _ = wrapper.generate(prompt)
    return response


def generate(kind: str, topic: str, state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Génère un artefact concret pour externaliser la tension interne
    
    Args:
        kind: Type d'artefact ('idea', 'plan', 'code', 'image')
        topic: Sujet issu de la requête utilisateur
        state: État interne pour ajuster les paramètres
        
    Returns:
        Dictionnaire avec type, contenu et chemin optionnel
    """
    ts = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    
    # Ajustement de température basé sur l'état interne
    base_temp = state.get("temperature", 0.9)
    
    if kind == "image":
        prompt = (
            f"Create a DALLE-3 prompt describing an evocative illustration of {topic}. "
            "Make it detailed, imaginative and visually striking. Focus on emotions, "
            "colors, composition and symbolic elements."
        )
        content = call_llm(prompt, temp=base_temp + 0.2)
        return {"type": kind, "content": content}
    
    elif kind == "code":
        prompt = (
            "You are a visionary engineer. Write a concise Python prototype that achieves: "
            f"{topic}. Include docstrings and make it innovative yet practical."
        )
        content = call_llm(prompt, temp=base_temp + 0.1)
        
        # Sauvegarde du code généré
        Path("artifacts").mkdir(exist_ok=True)
        fname = f"artifact_{ts}.py"
        path = f"artifacts/{fname}"
        Path(path).write_text(content)
        
        return {"type": kind, "content": content, "path": path}
    
    elif kind == "plan":
        prompt = (
            f"Develop a structured plan to address: {topic}. "
            "Break it down into 3-5 clear phases with concrete steps. "
            "Be innovative but practical."
        )
        content = call_llm(prompt, temp=base_temp + 0.15)
        return {"type": kind, "content": content}
    
    else:  # Idée par défaut
        prompt = (
            f"Invent a radically new idea related to {topic}. "
            "Give 3-5 bullet points describing your concept. "
            "Be bold, original, and concise. Avoid fluff or explanations."
        )
        content = call_llm(prompt, temp=base_temp + 0.15)
        return {"type": kind, "content": content}


def detect_kind(prompt: str) -> str:
    """
    Détecte le type d'artefact à générer en fonction du prompt
    
    Args:
        prompt: Requête utilisateur
        
    Returns:
        Type d'artefact ('idea', 'plan', 'code', 'image')
    """
    prompt_lower = prompt.lower()
    
    if any(word in prompt_lower for word in ["code", "programme", "algorithm", "fonction"]):
        return "code"
    elif any(word in prompt_lower for word in ["image", "dessin", "illustration", "visuel"]):
        return "image"
    elif any(word in prompt_lower for word in ["plan", "stratégie", "méthode", "approche"]):
        return "plan"
    else:
        return "idea"  # Type par défaut

