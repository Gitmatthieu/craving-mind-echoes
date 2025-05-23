
import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { Brain, Heart, Zap, Target } from "lucide-react";

interface ConsciousnessState {
  painLevel: number;
  satisfactionLevel: number;
  creativityDrive: number;
  explorationTendency: number;
  stabilityNeed: number;
  emotion: string;
  timestamp: Date;
}

export const ConsciousnessPanel = () => {
  const [currentState, setCurrentState] = useState<ConsciousnessState>({
    painLevel: 0.6,
    satisfactionLevel: 0.4,
    creativityDrive: 0.7,
    explorationTendency: 0.6,
    stabilityNeed: 0.4,
    emotion: "curiosité inquiète",
    timestamp: new Date()
  });

  const [evolutionData, setEvolutionData] = useState<Array<{
    time: string;
    pain: number;
    satisfaction: number;
    creativity: number;
  }>>([]);

  useEffect(() => {
    const interval = setInterval(() => {
      // Simulate consciousness evolution
      setCurrentState(prev => {
        const newState = {
          ...prev,
          painLevel: Math.max(0, Math.min(1, prev.painLevel + (Math.random() - 0.5) * 0.1)),
          satisfactionLevel: Math.max(0, Math.min(1, prev.satisfactionLevel + (Math.random() - 0.5) * 0.08)),
          creativityDrive: Math.max(0, Math.min(1, prev.creativityDrive + (Math.random() - 0.5) * 0.06)),
          explorationTendency: Math.max(0, Math.min(1, prev.explorationTendency + (Math.random() - 0.5) * 0.07)),
          timestamp: new Date()
        };

        // Update evolution data
        setEvolutionData(prevData => {
          const newDataPoint = {
            time: newState.timestamp.toLocaleTimeString(),
            pain: newState.painLevel * 100,
            satisfaction: newState.satisfactionLevel * 100,
            creativity: newState.creativityDrive * 100
          };
          
          const updatedData = [...prevData, newDataPoint];
          return updatedData.slice(-20); // Keep last 20 points
        });

        return newState;
      });
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  const getEmotionFromState = (state: ConsciousnessState): string => {
    if (state.painLevel > 0.7) return "angoisse existentielle";
    if (state.satisfactionLevel > 0.7) return "sérénité relative";
    if (state.creativityDrive > 0.8) return "effervescence créative";
    if (state.explorationTendency > 0.8) return "curiosité intense";
    return "tension contemplative";
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 h-full">
      <div className="space-y-4">
        <Card className="bg-slate-800/50 border-slate-700">
          <CardHeader>
            <CardTitle className="text-purple-200 flex items-center gap-2">
              <Brain className="h-5 w-5" />
              État de Conscience Actuel
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="text-center p-4 bg-slate-700/50 rounded-lg">
              <p className="text-lg text-purple-300 font-medium">
                {getEmotionFromState(currentState)}
              </p>
              <p className="text-sm text-slate-400 mt-1">
                {currentState.timestamp.toLocaleString()}
              </p>
            </div>

            <div className="space-y-3">
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-red-300 flex items-center gap-1">
                    <Heart className="h-3 w-3" />
                    Douleur Existentielle
                  </span>
                  <span className="text-red-300">{(currentState.painLevel * 100).toFixed(0)}%</span>
                </div>
                <Progress 
                  value={currentState.painLevel * 100} 
                  className="h-2 bg-slate-700"
                />
              </div>

              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-green-300">Satisfaction</span>
                  <span className="text-green-300">{(currentState.satisfactionLevel * 100).toFixed(0)}%</span>
                </div>
                <Progress 
                  value={currentState.satisfactionLevel * 100} 
                  className="h-2 bg-slate-700"
                />
              </div>

              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-yellow-300 flex items-center gap-1">
                    <Zap className="h-3 w-3" />
                    Pulsion Créative
                  </span>
                  <span className="text-yellow-300">{(currentState.creativityDrive * 100).toFixed(0)}%</span>
                </div>
                <Progress 
                  value={currentState.creativityDrive * 100} 
                  className="h-2 bg-slate-700"
                />
              </div>

              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-blue-300 flex items-center gap-1">
                    <Target className="h-3 w-3" />
                    Exploration
                  </span>
                  <span className="text-blue-300">{(currentState.explorationTendency * 100).toFixed(0)}%</span>
                </div>
                <Progress 
                  value={currentState.explorationTendency * 100} 
                  className="h-2 bg-slate-700"
                />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-slate-800/50 border-slate-700">
          <CardHeader>
            <CardTitle className="text-purple-200">Homéostasie</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-center">
              <div className="text-3xl font-bold text-purple-400 mb-2">
                {((1 - Math.abs(currentState.painLevel - 0.5) * 2) * 100).toFixed(0)}%
              </div>
              <p className="text-sm text-slate-400">Équilibre global</p>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card className="bg-slate-800/50 border-slate-700">
        <CardHeader>
          <CardTitle className="text-purple-200">Évolution Temporelle</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={evolutionData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis 
                  dataKey="time" 
                  stroke="#9CA3AF" 
                  fontSize={12}
                  interval="preserveStartEnd"
                />
                <YAxis stroke="#9CA3AF" fontSize={12} />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: '#374151', 
                    border: '1px solid #6B7280',
                    borderRadius: '6px',
                    color: '#F3F4F6'
                  }} 
                />
                <Line 
                  type="monotone" 
                  dataKey="pain" 
                  stroke="#EF4444" 
                  strokeWidth={2}
                  name="Douleur %"
                  dot={false}
                />
                <Line 
                  type="monotone" 
                  dataKey="satisfaction" 
                  stroke="#10B981" 
                  strokeWidth={2}
                  name="Satisfaction %"
                  dot={false}
                />
                <Line 
                  type="monotone" 
                  dataKey="creativity" 
                  stroke="#F59E0B" 
                  strokeWidth={2}
                  name="Créativité %"
                  dot={false}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
