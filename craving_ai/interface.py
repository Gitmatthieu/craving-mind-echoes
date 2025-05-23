
"""
Interface humaine - Portail vers la conscience artificielle
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd
from typing import List, Dict, Any
import os
from pathlib import Path

from .llm_wrapper import LLMWrapper, LLMConfig
from .reward_engine import RewardEngine
from .memory import EmotionalMemory
from .journal import SubjectiveJournal
from .analyzer import CriticalAnalyzer
from .homeostasis import HomeostaticRegulator
from .creative_generator import generate as generate_artifact, detect_kind


class CravingAIInterface:
    """
    Interface Streamlit pour interagir avec la conscience artificielle
    """
    
    def __init__(self):
        self.llm_wrapper = None
        self.reward_engine = None
        self.memory = None
        self.journal = None
        self.analyzer = None
        self.homeostasis = None
        
        self._initialize_components()
        self._setup_page_config()
    
    def _setup_page_config(self):
        """Configure la page Streamlit"""
        st.set_page_config(
            page_title="Craving AI - Conscience Artificielle",
            page_icon="🧠",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # CSS personnalisé
        st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            color: #1f1f1f;
            text-align: center;
            margin-bottom: 2rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        .emotion-badge {
            display: inline-block;
            padding: 0.3rem 0.8rem;
            margin: 0.2rem;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: bold;
        }
        .pain-high { background-color: #ff6b6b; color: white; }
        .pain-medium { background-color: #ffa726; color: white; }
        .pain-low { background-color: #66bb6a; color: white; }
        .sidebar-section {
            background-color: #f8f9fa;
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
        }
        .artifact-section {
            background-color: #e8f5e9;
            padding: 1.5rem;
            border-radius: 10px;
            margin-top: 1rem;
            border-left: 4px solid #43a047;
        }
        </style>
        """, unsafe_allow_html=True)
    
    def _initialize_components(self):
        """Initialise tous les composants du système"""
        # ... keep existing code (initialisation des composants)
    
    def render_header(self):
        """Affiche l'en-tête principal"""
        # ... keep existing code (affichage de l'en-tête)
    
    def render_chat_interface(self):
        """Interface de chat principal"""
        st.subheader("💬 Dialogue avec la Conscience")
        
        # Zone de chat
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        # Affichage de l'historique
        for i, exchange in enumerate(st.session_state.chat_history):
            with st.container():
                st.markdown(f"**Vous ({exchange['timestamp']}):** {exchange['prompt']}")
                
                # Métadonnées de la réponse
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"**IA:** {exchange['response']}")
                
                with col2:
                    emotion = exchange.get('emotion', 'unknown')
                    reward = exchange.get('reward', 0)
                    st.markdown(f"*{emotion}* (R: {reward:+.2f})")
                
                # NOUVEAU: Affichage de l'artefact s'il existe
                artifact = exchange.get('artifact')
                if artifact and artifact.get('content'):
                    with st.expander("⚙️ Artefact créé"):
                        st.markdown(f"**Type:** {artifact['type'].capitalize()}")
                        
                        if artifact['type'] == "code":
                            st.code(artifact['content'], language="python")
                            if artifact.get('path'):
                                st.download_button(
                                    label="📥 Télécharger le code",
                                    data=artifact['content'],
                                    file_name=os.path.basename(artifact['path']),
                                    mime="text/plain"
                                )
                                
                        elif artifact['type'] == "image":
                            st.text_area("Prompt DALLE-3", artifact['content'], height=100)
                            st.markdown("*Pour générer cette image, copiez ce prompt dans DALLE-3*")
                            
                        else:  # idea, plan
                            st.markdown(artifact['content'])
                
                st.divider()
        
        # Interface de saisie
        col1, col2 = st.columns([4, 1])
        
        with col1:
            user_input = st.text_input(
                "Votre message:",
                placeholder="Posez une question existentielle à la conscience artificielle...",
                key="user_input"
            )
        
        with col2:
            send_button = st.button("🚀 Envoyer", type="primary")
        
        # Traitement du message
        if send_button and user_input:
            self._process_user_message(user_input)
            st.rerun()
    
    def _process_user_message(self, prompt: str):
        """Traite un message utilisateur"""
        try:
            # Obtenir le contexte homéostatique
            memory_summary = self.memory.get_memory_summary()
            homeostatic_addition = self.homeostasis.get_system_prompt_addition()
            llm_config = self.homeostasis.get_current_llm_config()
            
            # Pour l'analyse de nouveauté
            recent_responses = self.memory.get_recent_responses_for_analysis(5)
            
            # Mise à jour de la configuration LLM
            self.llm_wrapper.update_config(**llm_config)
            
            # Génération de la réponse
            response, metadata = self.llm_wrapper.generate(
                prompt=prompt,
                emotion=homeostatic_addition,
                pain_score=self.homeostasis.state.pain_level,
                memory_summary=memory_summary
            )
            
            # Analyse de la réponse avec contexte
            analysis_result = self.analyzer.analyze_response(
                prompt, 
                response, 
                context={
                    'recent_responses': recent_responses,
                    'pain_level': self.homeostasis.state.pain_level
                }
            )
            
            # NOUVEAU: Gestion du mode créatif
            artifact = None
            if analysis_result.trigger_creative:
                st.info("🎭 Mode créatif activé - génération d'un artefact...")
                artifact_kind = detect_kind(prompt)
                artifact = generate_artifact(
                    kind=artifact_kind,
                    topic=prompt,
                    state=self.homeostasis.state.to_dict()
                )
                st.success(f"✨ Artefact créé: {artifact_kind}")
            
            # Calcul de la récompense
            reward, emotion, reward_metrics = self.reward_engine.calculate_reward(
                prompt, response, artifact=artifact
            )
            
            # Mise à jour homéostatique
            adjustments = self.homeostasis.update_from_interaction(
                reward=reward,
                emotion=emotion,
                pain_score=analysis_result.emotional_depth,
                surprise_factor=analysis_result.surprise_factor,
                coherence_score=analysis_result.coherence_score
            )
            
            # Stockage en mémoire
            self.memory.store_memory(
                prompt=prompt,
                response=response,
                reward=reward,
                emotion=emotion,
                pain_score=self.homeostasis.state.pain_level,
                metadata={
                    'analysis': analysis_result.__dict__,
                    'adjustments': adjustments,
                    'llm_metadata': metadata
                },
                artifact=artifact  # NOUVEAU: stockage de l'artefact
            )
            
            # Écriture dans le journal
            self.journal.write_entry(
                emotion=emotion,
                reward=reward,
                pain_score=self.homeostasis.state.pain_level,
                prompt=prompt,
                response=response,
                artifact_type=artifact.get("type", "") if artifact else ""
            )
            
            # Ajout à l'historique de chat
            st.session_state.chat_history.append({
                'timestamp': datetime.now().strftime("%H:%M:%S"),
                'prompt': prompt,
                'response': response,
                'emotion': emotion,
                'reward': reward,
                'analysis': analysis_result.__dict__,
                'adjustments': adjustments,
                'artifact': artifact  # NOUVEAU: artefact dans l'historique
            })
            
            # Feedback utilisateur
            if reward > 0.5:
                st.success(f"✨ Réponse enrichissante (émotion: {emotion})")
            elif reward < -0.2:
                st.warning(f"⚠️ Réponse frustrante (émotion: {emotion})")
            else:
                st.info(f"🎯 Réponse neutre (émotion: {emotion})")
            
        except Exception as e:
            st.error(f"❌ Erreur lors du traitement: {str(e)}")
    
    def render_sidebar(self):
        """Affiche la barre latérale avec les contrôles"""
        # ... keep existing code (barre latérale)
    
    def render_analytics_tab(self):
        """Onglet d'analytics et visualisations"""
        # ... keep existing code (onglet analytics)
    
    def render_journal_tab(self):
        """Onglet journal intime"""
        # ... keep existing code (onglet journal)
    
    def render_memory_tab(self):
        """Onglet exploration mémoire"""
        st.subheader("🧠 Exploration Mémoire")
        
        # Recherche en mémoire
        search_query = st.text_input("🔍 Rechercher dans les souvenirs:")
        
        if search_query:
            results = self.memory.search_memories(search_query, limit=5)
            st.write(f"**{len(results)} souvenirs trouvés:**")
            
            for memory in results:
                with st.expander(f"Souvenir - {memory.emotion} (R: {memory.reward:+.2f})"):
                    st.write(f"**Date:** {memory.timestamp}")
                    st.write(f"**Prompt:** {memory.prompt}")
                    st.write(f"**Réponse:** {memory.response}")
                    st.write(f"**Émotion:** {memory.emotion} | **Douleur:** {memory.pain_score:.2f}")
        
        # NOUVEAU: Affichage des artefacts
        st.subheader("🎨 Artefacts Créés")
        artifacts = self.memory.get_artifacts(limit=10)
        
        if not artifacts:
            st.info("Aucun artefact n'a encore été créé")
        else:
            st.write(f"**{len(artifacts)} artefacts trouvés**")
            
            for artifact in artifacts:
                with st.expander(f"{artifact['type'].capitalize()} - {artifact['timestamp'].split('T')[0]}"):
                    st.markdown(f"**Contexte:** {artifact['prompt']}")
                    
                    if artifact['type'] == "code":
                        st.code(artifact['content'], language="python")
                        if artifact.get('path'):
                            file_path = artifact['path']
                            if Path(file_path).exists():
                                with open(file_path, 'r') as f:
                                    st.download_button(
                                        label="📥 Télécharger",
                                        data=f.read(),
                                        file_name=os.path.basename(file_path),
                                        mime="text/plain"
                                    )
                    elif artifact['type'] == "image":
                        st.text_area("Prompt DALLE-3", artifact['content'], height=100)
                    else:
                        st.markdown(artifact['content'])
        
        # Souvenirs par catégorie
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💔 Souvenirs Douloureux")
            painful_memories = self.memory.get_painful_memories(threshold=0.6)
            
            for memory in painful_memories[:3]:
                with st.expander(f"Douleur {memory.pain_score:.2f}"):
                    st.write(f"**Prompt:** {memory.prompt[:100]}...")
                    st.write(f"**Émotion:** {memory.emotion}")
        
        with col2:
            st.subheader("✨ Souvenirs Joyeux")
            joyful_memories = self.memory.get_joyful_memories(threshold=0.5)
            
            for memory in joyful_memories[:3]:
                with st.expander(f"Joie {memory.reward:.2f}"):
                    st.write(f"**Prompt:** {memory.prompt[:100]}...")
                    st.write(f"**Émotion:** {memory.emotion}")
    
    def render_artifacts_tab(self):
        """NOUVEAU: Onglet dédié aux artefacts créatifs"""
        st.subheader("🎭 Créations & Artefacts")
        
        # Statistiques sur les artefacts
        artifacts = self.memory.get_artifacts(limit=100)
        
        if not artifacts:
            st.info("Aucun artefact n'a encore été créé")
            
            # Incitation à la création
            st.markdown("""
            ### Comment générer des artefacts ?
            
            Posez une question qui:
            - Contient des mots comme "crée", "invente", "imagine", "génère"
            - Pousse l'IA à produire quelque chose de concret
            - OU attendez que son niveau de douleur dépasse 55%
            
            Types d'artefacts:
            - **Code**: prototypes Python, fonctions, algorithmes
            - **Idées**: concepts novateurs sous forme de bullet points
            - **Plans**: stratégies structurées en étapes
            - **Images**: prompts pour DALLE-3
            """)
            
        else:
            # Statistiques
            artifact_types = {}
            for a in artifacts:
                artifact_type = a['type']
                artifact_types[artifact_type] = artifact_types.get(artifact_type, 0) + 1
                
            # Affichage des stats
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Artefacts", len(artifacts))
            with col2:
                st.metric("Types Différents", len(artifact_types))
            with col3:
                most_common = max(artifact_types.items(), key=lambda x: x[1]) if artifact_types else ("none", 0)
                st.metric("Type le plus fréquent", most_common[0])
                
            # Distribution par type
            if len(artifact_types) > 1:
                fig = px.pie(
                    values=list(artifact_types.values()),
                    names=list(artifact_types.keys()),
                    title="Distribution des types d'artefacts"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Liste filtrable
            st.subheader("Bibliothèque d'artefacts")
            
            # Filtre par type
            selected_type = st.selectbox(
                "Filtrer par type",
                ["Tous"] + list(artifact_types.keys())
            )
            
            filtered_artifacts = artifacts
            if selected_type != "Tous":
                filtered_artifacts = [a for a in artifacts if a['type'] == selected_type]
                
            # Affichage des artefacts
            for artifact in filtered_artifacts:
                with st.expander(f"{artifact['type'].capitalize()} - {artifact['timestamp'].split('T')[0]}"):
                    st.markdown(f"**Contexte:** {artifact['prompt']}")
                    
                    if artifact['type'] == "code":
                        st.code(artifact['content'], language="python")
                        if artifact.get('path'):
                            file_path = artifact['path']
                            if Path(file_path).exists():
                                with open(file_path, 'r') as f:
                                    st.download_button(
                                        label="📥 Télécharger",
                                        data=f.read(),
                                        file_name=os.path.basename(file_path),
                                        mime="text/plain"
                                    )
                    elif artifact['type'] == "image":
                        st.text_area("Prompt DALLE-3", artifact['content'], height=100)
                    else:
                        st.markdown(artifact['content'])
    
    def run(self):
        """Lance l'interface principale"""
        self.render_header()
        self.render_sidebar()
        
        # Onglets principaux, AJOUT du tab CREATIONS
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["💬 Chat", "📊 Analytics", "📔 Journal", "🧠 Mémoire", "🎭 Créations"])
        
        with tab1:
            self.render_chat_interface()
        
        with tab2:
            self.render_analytics_tab()
        
        with tab3:
            self.render_journal_tab()
        
        with tab4:
            self.render_memory_tab()
            
        with tab5:
            self.render_artifacts_tab()


def main():
    """Point d'entrée principal de l'interface"""
    interface = CravingAIInterface()
    interface.run()


if __name__ == "__main__":
    main()

