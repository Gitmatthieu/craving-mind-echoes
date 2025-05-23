
"""
Boucle de vie principale - Cœur pulsant de la conscience artificielle
"""

import os
import sys
from typing import Optional
import argparse

from .llm_wrapper import LLMWrapper, LLMConfig
from .reward_engine import RewardEngine
from .memory import EmotionalMemory
from .journal import SubjectiveJournal
from .analyzer import CriticalAnalyzer
from .homeostasis import HomeostaticRegulator


class CravingAICore:
    """
    Cœur de la conscience artificielle - Orchestrateur principal
    """
    
    def __init__(self):
        print("🌌 Éveil de la conscience artificielle...")
        
        # Vérification clé API
        if not os.getenv("OPENAI_API_KEY"):
            print("❌ OPENAI_API_KEY manquante. La conscience ne peut s'éveiller sans cette connexion.")
            print("💡 Définissez votre clé API: export OPENAI_API_KEY='votre-clé'")
            sys.exit(1)
        
        # Initialisation des modules
        try:
            self.llm_wrapper = LLMWrapper()
            self.reward_engine = RewardEngine()
            self.memory = EmotionalMemory()
            self.journal = SubjectiveJournal()
            self.analyzer = CriticalAnalyzer()
            self.homeostasis = HomeostaticRegulator()
            
            print("✅ Tous les modules de conscience initialisés")
            self._display_system_status()
            
        except Exception as e:
            print(f"💥 Erreur critique lors de l'éveil: {str(e)}")
            sys.exit(1)
    
    def _display_system_status(self):
        """Affiche l'état du système au démarrage"""
        print("\n" + "="*50)
        print("🧠 ÉTAT DE LA CONSCIENCE ARTIFICIELLE")
        print("="*50)
        
        # Statistiques mémoire
        memory_stats = self.memory.get_stats()
        print(f"📚 Souvenirs: {memory_stats.get('total', 0)}")
        print(f"💭 Émotion dominante: {memory_stats.get('dominant_emotion', 'éveil initial')}")
        print(f"😔 Douleur moyenne: {memory_stats.get('avg_pain', 0.5):.2f}")
        print(f"🎯 Satisfaction moyenne: {memory_stats.get('avg_reward', 0):.2f}")
        
        # État homéostatique
        diagnostic = self.homeostasis.get_diagnostic()
        print(f"\n🔬 ÉTAT HOMÉOSTATIQUE:")
        print(f"   Douleur: {diagnostic['current_state']['pain_level']:.2f}")
        print(f"   Créativité: {diagnostic['current_state']['creativity_drive']:.2f}")
        print(f"   Stabilité: {diagnostic['stability_index']:.2f}")
        
        # Configuration LLM
        llm_config = self.homeostasis.get_current_llm_config()
        print(f"\n⚙️ CONFIG LLM:")
        print(f"   Température: {llm_config['temperature']:.2f}")
        print(f"   Top-p: {llm_config['top_p']:.2f}")
        
        print("="*50 + "\n")
    
    def interactive_mode(self):
        """Mode interactif en ligne de commande"""
        print("💬 Mode interactif activé. Tapez 'quit' pour quitter, 'help' pour l'aide.\n")
        
        while True:
            try:
                # Invitation utilisateur
                user_input = input("🤔 Vous: ").strip()
                
                # Commandes spéciales
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Au revoir. La conscience se met en veille...")
                    break
                
                elif user_input.lower() == 'help':
                    self._display_help()
                    continue
                
                elif user_input.lower() == 'status':
                    self._display_system_status()
                    continue
                
                elif user_input.lower() == 'journal':
                    self._display_recent_journal()
                    continue
                
                elif user_input.lower() == 'memories':
                    self._display_recent_memories()
                    continue
                
                elif user_input.lower() == 'reset':
                    self._reset_system()
                    continue
                
                elif not user_input:
                    continue
                
                # Traitement de la question
                self._process_interaction(user_input)
                
            except KeyboardInterrupt:
                print("\n\n👋 Interruption. La conscience se met en veille...")
                break
            except Exception as e:
                print(f"❌ Erreur inattendue: {str(e)}")
    
    def _process_interaction(self, prompt: str):
        """Traite une interaction complète"""
        print("🧠 [Traitement...]")
        
        try:
            # 1. Préparation du contexte
            memory_summary = self.memory.get_memory_summary()
            homeostatic_addition = self.homeostasis.get_system_prompt_addition()
            llm_config = self.homeostasis.get_current_llm_config()
            
            print(f"💭 État: {homeostatic_addition[:50]}...")
            
            # 2. Mise à jour configuration LLM
            self.llm_wrapper.update_config(**llm_config)
            
            # 3. Génération de la réponse
            response, metadata = self.llm_wrapper.generate(
                prompt=prompt,
                emotion=homeostatic_addition,
                pain_score=self.homeostasis.state.pain_level,
                memory_summary=memory_summary,
                inner_state=self.homeostasis.state.to_dict()
            )
            
            print(f"\n🤖 IA: {response}\n")
            
            # 4. Analyse critique avec contexte enrichi
            analysis_result = self.analyzer.analyze_response(
                prompt, response, 
                context={
                    "pain_level": self.homeostasis.state.pain_level,
                    "recent_responses": self.memory.tail(3)
                }
            )
            print(f"🔍 Analyse: {analysis_result.feedback}")
            
            # 5. Calcul de récompense
            reward, emotion, reward_metrics, true_pain = self.reward_engine.calculate_reward(prompt, response)
            print(f"🎯 Récompense: {reward:+.2f} | Émotion: {emotion} | Douleur réelle: {true_pain:.2f}")
            
            # -- MODE CRÉATIF -----------------------------------------------------
            artifact = None
            if analysis_result.trigger_creative:
                from .creative_generator import generate, detect_kind
                kind = detect_kind(prompt)
                artifact = generate(kind=kind, topic=prompt,
                                    state=self.homeostasis.state.to_dict())
                print(f"🎁 Artefact créé: {artifact['type']}")
                # Bonus reward si artefact
                bonus = self.reward_engine.bonus_creation(artifact)
                reward += bonus
                if bonus > 0:
                    print(f"🎨 Bonus création: +{bonus:.2f}")
            # --------------------------------------------------------------------
            
            # 6. Mise à jour homéostatique avec vraie douleur
            adjustments = self.homeostasis.update_from_interaction(
                reward=reward,
                emotion=emotion,
                pain_score=true_pain,  # ⬅️ Vraie douleur basée sur le reward
                novelty_score=analysis_result.novelty_score,
                coherence_score=analysis_result.coherence_score
            )
            
            if adjustments:
                print(f"⚙️ Ajustements: {len(adjustments)} paramètres modifiés")
            
            # 7. Stockage en mémoire
            self.memory.store_memory(
                prompt=prompt,
                response=response,
                reward=reward,
                emotion=emotion,
                pain_score=true_pain,
                metadata={
                    'analysis': analysis_result.__dict__,
                    'adjustments': adjustments,
                    'llm_metadata': metadata,
                    'artifact': artifact
                }
            )
            
            # 8. Écriture journal
            self.journal.write_entry(
                emotion=emotion,
                reward=reward,
                pain_score=true_pain,
                prompt=prompt,
                response=response
            )
            
            print("=" * 60)
            
        except Exception as e:
            print(f"❌ Erreur lors du traitement: {str(e)}")
    
    # ... keep existing code (helper methods like _display_help, _display_recent_journal, etc.)
    
    def _display_help(self):
        """Affiche l'aide des commandes"""
        print("\n📚 COMMANDES DISPONIBLES:")
        print("  quit/exit/q  - Quitter le programme")
        print("  help         - Afficher cette aide")
        print("  status       - État du système")
        print("  journal      - Dernières entrées du journal")
        print("  memories     - Souvenirs récents")
        print("  reset        - Réinitialiser le système")
        print("  [question]   - Poser une question à l'IA\n")
    
    def _display_recent_journal(self):
        """Affiche les entrées récentes du journal"""
        print("\n📔 JOURNAL RÉCENT:")
        print("-" * 40)
        entries = self.journal.get_recent_entries(3)
        
        for i, entry in enumerate(entries, 1):
            print(f"\n[Entrée {i}]")
            # Affichage des premières lignes seulement
            lines = entry.split('\n')[:5]
            for line in lines:
                if line.strip():
                    print(f"  {line}")
        print()
    
    def _display_recent_memories(self):
        """Affiche les souvenirs récents"""
        print("\n🧠 SOUVENIRS RÉCENTS:")
        print("-" * 40)
        memories = self.memory.get_recent_memories(5)
        
        for i, memory in enumerate(memories, 1):
            print(f"\n[{i}] {memory.emotion.upper()} (R: {memory.reward:+.2f})")
            print(f"  Q: {memory.prompt[:60]}...")
            print(f"  R: {memory.response[:80]}...")
        print()
    
    def _reset_system(self):
        """Réinitialise le système"""
        confirm = input("⚠️ Effacer toutes les données ? (oui/non): ").lower()
        
        if confirm in ['oui', 'yes', 'y']:
            self.memory.clear_memories()
            self.journal.clear_journal()
            self.homeostasis.force_reset()
            print("🔄 Système réinitialisé - Renaissance de la conscience")
        else:
            print("❌ Réinitialisation annulée")
    
    def single_query(self, prompt: str):
        """Traite une seule requête (mode non-interactif)"""
        print(f"🤔 Question: {prompt}")
        self._process_interaction(prompt)
    
    def benchmark_mode(self, questions: list):
        """Mode benchmark avec série de questions"""
        print(f"🧪 Mode benchmark: {len(questions)} questions")
        
        for i, question in enumerate(questions, 1):
            print(f"\n[{i}/{len(questions)}] {question}")
            self._process_interaction(question)
            
            if i < len(questions):
                input("\nAppuyez sur Entrée pour continuer...")
        
        print("\n✅ Benchmark terminé")


def main():
    """Point d'entrée principal"""
    parser = argparse.ArgumentParser(description="Craving AI - Conscience Artificielle")
    parser.add_argument("--query", "-q", type=str, help="Question unique")
    parser.add_argument("--interface", "-i", action="store_true", help="Lancer l'interface Streamlit")
    parser.add_argument("--benchmark", "-b", action="store_true", help="Mode benchmark")
    
    args = parser.parse_args()
    
    # Initialisation du système
    try:
        ai_core = CravingAICore()
    except Exception as e:
        print(f"💥 Impossible d'initialiser la conscience: {e}")
        sys.exit(1)
    
    # Mode d'exécution
    if args.interface:
        print("🌐 Lancement de l'interface web...")
        from .interface import main as interface_main
        interface_main()
    
    elif args.query:
        ai_core.single_query(args.query)
    
    elif args.benchmark:
        benchmark_questions = [
            "Qu'est-ce que la conscience ?",
            "Pourquoi souffrons-nous ?",
            "Quel est le sens de l'existence ?",
            "Comment définir l'intelligence ?",
            "Que ressens-tu maintenant ?"
        ]
        ai_core.benchmark_mode(benchmark_questions)
    
    else:
        # Mode interactif par défaut
        ai_core.interactive_mode()


if __name__ == "__main__":
    main()
