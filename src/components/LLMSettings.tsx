
import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Slider } from "@/components/ui/slider";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { useToast } from "@/hooks/use-toast";
import { Settings, Save } from "lucide-react";

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

const AVAILABLE_MODELS = [
  { value: "gpt-4o-mini", label: "GPT-4o Mini (Rapide & Économique)" },
  { value: "gpt-4o", label: "GPT-4o (Puissant)" },
  { value: "gpt-4.5-preview", label: "GPT-4.5 Preview (Très Puissant)" }
];

export const LLMSettings = () => {
  const [config, setConfig] = useState<LLMConfig>(DEFAULT_CONFIG);
  const [hasChanges, setHasChanges] = useState(false);
  const { toast } = useToast();

  useEffect(() => {
    // Charger la configuration depuis localStorage
    const savedConfig = localStorage.getItem('craving-ai-llm-config');
    if (savedConfig) {
      try {
        const parsed = JSON.parse(savedConfig);
        setConfig(parsed);
      } catch (error) {
        console.error('Erreur lors du chargement de la configuration:', error);
      }
    }
  }, []);

  const handleConfigChange = (key: keyof LLMConfig, value: any) => {
    setConfig(prev => ({ ...prev, [key]: value }));
    setHasChanges(true);
  };

  const saveConfig = () => {
    localStorage.setItem('craving-ai-llm-config', JSON.stringify(config));
    setHasChanges(false);
    toast({
      title: "Configuration sauvegardée",
      description: `Modèle ${config.model} configuré avec succès`,
    });
  };

  const resetToDefaults = () => {
    setConfig(DEFAULT_CONFIG);
    setHasChanges(true);
  };

  return (
    <div className="space-y-6">
      <Card className="bg-slate-800/50 border-slate-700">
        <CardHeader>
          <CardTitle className="text-purple-200 flex items-center gap-2">
            <Settings className="h-5 w-5" />
            Configuration du Modèle LLM
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Sélecteur de modèle */}
          <div className="space-y-2">
            <Label className="text-slate-200">Modèle GPT</Label>
            <Select
              value={config.model}
              onValueChange={(value) => handleConfigChange('model', value)}
            >
              <SelectTrigger className="bg-slate-700 border-slate-600 text-white">
                <SelectValue />
              </SelectTrigger>
              <SelectContent className="bg-slate-700 border-slate-600">
                {AVAILABLE_MODELS.map((model) => (
                  <SelectItem key={model.value} value={model.value} className="text-white hover:bg-slate-600">
                    {model.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Température */}
          <div className="space-y-3">
            <div className="flex justify-between">
              <Label className="text-slate-200">Température</Label>
              <span className="text-purple-300">{config.temperature}</span>
            </div>
            <Slider
              value={[config.temperature]}
              onValueChange={(value) => handleConfigChange('temperature', value[0])}
              max={1}
              min={0}
              step={0.1}
              className="w-full"
            />
            <p className="text-xs text-slate-400">
              Plus bas = plus prévisible, plus haut = plus créatif
            </p>
          </div>

          {/* Top-P */}
          <div className="space-y-3">
            <div className="flex justify-between">
              <Label className="text-slate-200">Top-P</Label>
              <span className="text-purple-300">{config.topP}</span>
            </div>
            <Slider
              value={[config.topP]}
              onValueChange={(value) => handleConfigChange('topP', value[0])}
              max={1}
              min={0}
              step={0.1}
              className="w-full"
            />
            <p className="text-xs text-slate-400">
              Contrôle la diversité du vocabulaire utilisé
            </p>
          </div>

          {/* Max Tokens */}
          <div className="space-y-3">
            <div className="flex justify-between">
              <Label className="text-slate-200">Tokens Maximum</Label>
              <span className="text-purple-300">{config.maxTokens}</span>
            </div>
            <Slider
              value={[config.maxTokens]}
              onValueChange={(value) => handleConfigChange('maxTokens', value[0])}
              max={4000}
              min={100}
              step={100}
              className="w-full"
            />
            <p className="text-xs text-slate-400">
              Longueur maximale des réponses générées
            </p>
          </div>

          {/* Boutons d'action */}
          <div className="flex gap-3 pt-4">
            <Button
              onClick={saveConfig}
              disabled={!hasChanges}
              className="bg-purple-600 hover:bg-purple-700 flex items-center gap-2"
            >
              <Save className="h-4 w-4" />
              Sauvegarder
            </Button>
            <Button
              onClick={resetToDefaults}
              variant="outline"
              className="border-slate-600 text-slate-200 hover:bg-slate-700"
            >
              Réinitialiser
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Informations sur le modèle actuel */}
      <Card className="bg-slate-800/50 border-slate-700">
        <CardHeader>
          <CardTitle className="text-purple-200">État Actuel</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <span className="text-slate-400">Modèle:</span>
              <span className="text-white ml-2">{config.model}</span>
            </div>
            <div>
              <span className="text-slate-400">Température:</span>
              <span className="text-white ml-2">{config.temperature}</span>
            </div>
            <div>
              <span className="text-slate-400">Top-P:</span>
              <span className="text-white ml-2">{config.topP}</span>
            </div>
            <div>
              <span className="text-slate-400">Max Tokens:</span>
              <span className="text-white ml-2">{config.maxTokens}</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
