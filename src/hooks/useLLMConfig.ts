
import { useState, useEffect } from "react";

interface LLMConfig {
  model: string;
  temperature: number;
  topP: number;
  maxTokens: number;
}

const DEFAULT_CONFIG: LLMConfig = {
  model: "gpt-4o-mini",
  temperature: 0.7,
  topP: 0.9,
  maxTokens: 1000
};

export const useLLMConfig = () => {
  const [config, setConfig] = useState<LLMConfig>(DEFAULT_CONFIG);

  useEffect(() => {
    const savedConfig = localStorage.getItem('craving-ai-llm-config');
    if (savedConfig) {
      try {
        const parsed = JSON.parse(savedConfig);
        setConfig(parsed);
      } catch (error) {
        console.error('Erreur lors du chargement de la configuration LLM:', error);
      }
    }
  }, []);

  const updateConfig = (newConfig: Partial<LLMConfig>) => {
    const updatedConfig = { ...config, ...newConfig };
    setConfig(updatedConfig);
    localStorage.setItem('craving-ai-llm-config', JSON.stringify(updatedConfig));
  };

  return {
    config,
    updateConfig
  };
};
