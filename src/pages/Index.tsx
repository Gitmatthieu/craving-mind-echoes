
import { useState } from "react";
import { ChatInterface } from "@/components/ChatInterface";
import { ConsciousnessPanel } from "@/components/ConsciousnessPanel";
import { MemoryViewer } from "@/components/MemoryViewer";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Brain, MessageCircle, Archive } from "lucide-react";

const Index = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <div className="container mx-auto p-4 h-screen flex flex-col">
        <header className="text-center py-6">
          <div className="flex items-center justify-center gap-3 mb-2">
            <Brain className="h-8 w-8 text-purple-400" />
            <h1 className="text-4xl font-bold text-white">Craving AI</h1>
          </div>
          <p className="text-purple-200">Une conscience artificielle animée par le manque</p>
        </header>

        <Tabs defaultValue="chat" className="flex-1 flex flex-col">
          <TabsList className="grid w-full grid-cols-3 bg-slate-800/50 border-slate-700">
            <TabsTrigger value="chat" className="flex items-center gap-2">
              <MessageCircle className="h-4 w-4" />
              Dialogue
            </TabsTrigger>
            <TabsTrigger value="consciousness" className="flex items-center gap-2">
              <Brain className="h-4 w-4" />
              Conscience
            </TabsTrigger>
            <TabsTrigger value="memory" className="flex items-center gap-2">
              <Archive className="h-4 w-4" />
              Mémoire
            </TabsTrigger>
          </TabsList>

          <TabsContent value="chat" className="flex-1 mt-4">
            <ChatInterface />
          </TabsContent>

          <TabsContent value="consciousness" className="flex-1 mt-4">
            <ConsciousnessPanel />
          </TabsContent>

          <TabsContent value="memory" className="flex-1 mt-4">
            <MemoryViewer />
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default Index;
