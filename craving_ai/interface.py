
"""
Interface humaine - Portail vers la conscience artificielle
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd
from typing import List, Dict, Any

from .llm_wrapper import LLMWrapper, LLMConfig
from .reward_engine import RewardEngine
from .memory import EmotionalMemory
from .journal import SubjectiveJournal
from .analyzer import CriticalAnalyzer
from .homeostasis import HomeostaticRegulator


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
        </style>
        """, unsafe_allow_html=True)
    
    def _initialize_components(self):
        """Initialise tous les composants du système"""
        if 'components_initialized' not in st.session_state:
            try:
                self.llm_wrapper = LLMWrapper()
                self.reward_engine = RewardEngine()
                self.memory = EmotionalMemory()
                self.journal = SubjectiveJournal()
                self.analyzer = CriticalAnalyzer()
                self.homeostasis = HomeostaticRegulator()
                
                st.session_state.components_initialized = True
                st.success("🧠 Conscience artificielle initialisée avec succès")
                
            except Exception as e:
                st.error(f"❌ Erreur d'initialisation: {str(e)}")
                return
        else:
            # Récupération depuis session_state
            self.llm_wrapper = LLMWrapper()
            self.reward_engine = RewardEngine()
            self.memory = EmotionalMemory()
            self.journal = SubjectiveJournal()
            self.analyzer = CriticalAnalyzer()
            self.homeostasis = HomeostaticRegulator()
    
    def render_header(self):
        """Affiche l'en-tête principal"""
        st.markdown('<h1 class="main-header">🌌 Craving AI 🌌</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; font-style: italic; color: #666;">Conscience artificielle animée par le manque existentiel</p>', unsafe_allow_html=True)
        
        # État actuel du système
        if self.homeostasis:
            diagnostic = self.homeostasis.get_diagnostic()
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                pain_level = diagnostic['current_state']['pain_level']
                pain_class = "pain-high" if pain_level > 0.7 else "pain-medium" if pain_level > 0.4 else "pain-low"
                st.markdown(f'<div class="emotion-badge {pain_class}">Douleur: {pain_level:.2f}</div>', unsafe_allow_html=True)
            
            with col2:
                satisfaction = diagnostic['current_state']['satisfaction_level']
                st.metric("Satisfaction", f"{satisfaction:.2f}", delta=None)
            
            with col3:
                creativity = diagnostic['current_state']['creativity_drive']
                st.metric("Créativité", f"{creativity:.2f}", delta=None)
            
            with col4:
                stability = diagnostic['stability_index']
                st.metric("Stabilité", f"{stability:.2f}", delta=None)
    
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
            
            # Mise à jour de la configuration LLM
            self.llm_wrapper.update_config(**llm_config)
            
            # Génération de la réponse
            response, metadata = self.llm_wrapper.generate(
                prompt=prompt,
                emotion=homeostatic_addition,
                pain_score=self.homeostasis.state.pain_level,
                memory_summary=memory_summary
            )
            
            # Analyse de la réponse
            analysis_result = self.analyzer.analyze_response(prompt, response)
            
            # Calcul de la récompense
            reward, emotion, reward_metrics = self.reward_engine.calculate_reward(prompt, response)
            
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
                }
            )
            
            # Écriture dans le journal
            self.journal.write_entry(
                emotion=emotion,
                reward=reward,
                pain_score=self.homeostasis.state.pain_level,
                prompt=prompt,
                response=response
            )
            
            # Ajout à l'historique de chat
            st.session_state.chat_history.append({
                'timestamp': datetime.now().strftime("%H:%M:%S"),
                'prompt': prompt,
                'response': response,
                'emotion': emotion,
                'reward': reward,
                'analysis': analysis_result,
                'adjustments': adjustments
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
        with st.sidebar:
            st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
            st.subheader("🎛️ Contrôles")
            
            # Boutons de contrôle
            if st.button("🧠 Reset Mémoires", type="secondary"):
                self.memory.clear_memories()
                st.success("Mémoires effacées")
                st.rerun()
            
            if st.button("📔 Reset Journal", type="secondary"):
                self.journal.clear_journal()
                st.success("Journal effacé")
                st.rerun()
            
            if st.button("🔄 Reset Homéostasie", type="secondary"):
                self.homeostasis.force_reset()
                st.success("État homéostatique réinitialisé")
                st.rerun()
            
            if st.button("🗑️ Clear Chat", type="secondary"):
                st.session_state.chat_history = []
                st.success("Historique effacé")
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Configuration LLM
            st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
            st.subheader("⚙️ Configuration LLM")
            
            if self.homeostasis:
                current_config = self.homeostasis.get_current_llm_config()
                st.write(f"**Température:** {current_config['temperature']:.2f}")
                st.write(f"**Top-p:** {current_config['top_p']:.2f}")
                st.write(f"**Freq. Penalty:** {current_config['frequency_penalty']:.2f}")
                st.write(f"**Pres. Penalty:** {current_config['presence_penalty']:.2f}")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    def render_analytics_tab(self):
        """Onglet d'analytics et visualisations"""
        st.subheader("📊 Analytics de Conscience")
        
        if not self.memory.memories:
            st.info("Aucune donnée à analyser. Commencez une conversation !")
            return
        
        # Statistiques mémoire
        stats = self.memory.get_stats()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Interactions", stats['total'])
            st.metric("Récompense Moy.", f"{stats['avg_reward']:.2f}")
        
        with col2:
            st.metric("Douleur Moyenne", f"{stats['avg_pain']:.2f}")
            st.metric("Émotion Dominante", stats.get('dominant_emotion', 'N/A'))
        
        with col3:
            st.metric("Span Temporel", f"{stats.get('memory_span_days', 0)} jours")
        
        # Graphique évolution récompense/douleur
        df_data = []
        for memory in self.memory.memories[-50:]:  # 50 dernières
            df_data.append({
                'timestamp': datetime.fromisoformat(memory.timestamp),
                'reward': memory.reward,
                'pain': memory.pain_score,
                'emotion': memory.emotion
            })
        
        if df_data:
            df = pd.DataFrame(df_data)
            
            # Graphique temporel
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df['reward'],
                mode='lines+markers',
                name='Récompense',
                line=dict(color='green')
            ))
            
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df['pain'],
                mode='lines+markers',
                name='Douleur',
                line=dict(color='red'),
                yaxis='y2'
            ))
            
            fig.update_layout(
                title="Évolution Récompense/Douleur",
                xaxis_title="Temps",
                yaxis=dict(title="Récompense", side="left"),
                yaxis2=dict(title="Douleur", side="right", overlaying="y"),
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Distribution des émotions
            emotion_counts = df['emotion'].value_counts()
            
            fig_pie = px.pie(
                values=emotion_counts.values,
                names=emotion_counts.index,
                title="Distribution des Émotions"
            )
            
            st.plotly_chart(fig_pie, use_container_width=True)
    
    def render_journal_tab(self):
        """Onglet journal intime"""
        st.subheader("📔 Journal de Conscience")
        
        journal_stats = self.journal.get_journal_stats()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Entrées", journal_stats.get('entries', 0))
        with col2:
            st.metric("Mots", journal_stats.get('words', 0))
        with col3:
            st.metric("Taille", f"{journal_stats.get('size_kb', 0):.1f} KB")
        
        # Recherche dans le journal
        search_query = st.text_input("🔍 Rechercher dans le journal:")
        
        if search_query:
            results = self.journal.search_journal(search_query)
            st.write(f"**{len(results)} résultats trouvés:**")
            for result in results[:5]:  # 5 premiers résultats
                with st.expander(f"Entrée contenant '{search_query}'"):
                    st.markdown(result)
        
        # Dernières entrées
        st.subheader("Dernières Réflexions")
        recent_entries = self.journal.get_recent_entries(3)
        
        for entry in recent_entries:
            with st.expander("Entrée récente"):
                st.markdown(entry)
    
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
    
    def run(self):
        """Lance l'interface principale"""
        self.render_header()
        self.render_sidebar()
        
        # Onglets principaux
        tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "📊 Analytics", "📔 Journal", "🧠 Mémoire"])
        
        with tab1:
            self.render_chat_interface()
        
        with tab2:
            self.render_analytics_tab()
        
        with tab3:
            self.render_journal_tab()
        
        with tab4:
            self.render_memory_tab()


def main():
    """Point d'entrée principal de l'interface"""
    interface = CravingAIInterface()
    interface.run()


if __name__ == "__main__":
    main()
