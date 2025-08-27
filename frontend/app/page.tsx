'use client';

import { useState, useEffect } from 'react';
import { StockSearch } from '../components/StockSearch';
import { TradingChart } from '../components/TradingChart';
import { MarketData } from '../components/MarketData';
import { AIAnalysis } from '../components/AIAnalysis';
import { PerformancePanel } from '../components/PerformancePanel';
import { FeatureCards } from '../components/FeatureCards';
import { StatusBar } from '../components/StatusBar';

export default function TradingDashboard() {
  const [selectedSymbol, setSelectedSymbol] = useState('AAPL');
  const [analysisData, setAnalysisData] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSymbolChange = (symbol: string) => {
    setSelectedSymbol(symbol);
    // 這會觸發所有組件的更新
  };

  const analyzeStock = async (symbol: string) => {
    setLoading(true);
    try {
      const response = await fetch(`http://localhost:8000/analyze/${symbol}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          symbol,
          period: '3mo',
          include_ai: true
        })
      });
      const data = await response.json();
      setAnalysisData(data);
    } catch (error) {
      console.error('Analysis failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-800">
      {/* Header */}
      <header className="bg-slate-800/80 backdrop-blur-sm border-b border-slate-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-3">
              <div className="text-2xl">🚀</div>
              <div>
                <h1 className="text-xl font-bold text-white">AI Trading Dashboard</h1>
                <p className="text-sm text-slate-300">Advanced Stock Analysis & AI-Powered Trading Insights</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2 px-3 py-1 bg-blue-600/20 rounded-lg border border-blue-500/30">
                <span className="w-2 h-2 bg-blue-400 rounded-full animate-pulse"></span>
                <span className="text-sm text-blue-200">Real-time Analysis</span>
              </div>
              
              <div className="flex items-center space-x-2 px-3 py-1 bg-green-600/20 rounded-lg border border-green-500/30">
                <span className="w-2 h-2 bg-green-400 rounded-full"></span>
                <span className="text-sm text-green-200">AI Recommendations</span>
              </div>
              
              <div className="flex items-center space-x-2 px-3 py-1 bg-purple-600/20 rounded-lg border border-purple-500/30">
                <span className="w-2 h-2 bg-purple-400 rounded-full"></span>
                <span className="text-sm text-purple-200">TradingView Charts</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {/* Stock Search Section */}
        <div className="mb-6">
          <StockSearch 
            selectedSymbol={selectedSymbol}
            onSymbolChange={handleSymbolChange}
            onAnalyze={analyzeStock}
            loading={loading}
          />
        </div>

        {/* Main Chart Section */}
        <div className="mb-6">
          <TradingChart 
            symbol={selectedSymbol}
            className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700"
          />
        </div>

        {/* Data Panels Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
          <MarketData 
            symbol={selectedSymbol}
            analysisData={analysisData}
          />
          <AIAnalysis 
            symbol={selectedSymbol}
            analysisData={analysisData}
            loading={loading}
          />
          <PerformancePanel 
            symbol={selectedSymbol}
            analysisData={analysisData}
          />
        </div>

        {/* Feature Cards */}
        <FeatureCards />

        {/* Status Bar */}
        <StatusBar />
      </div>
    </div>
  );
}