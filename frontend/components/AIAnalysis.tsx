'use client';

import { useState, useEffect } from 'react';

interface AIAnalysisProps {
  symbol: string;
  analysisData: any;
  loading: boolean;
}

export function AIAnalysis({ symbol, analysisData, loading }: AIAnalysisProps) {
  const [aiInsights, setAiInsights] = useState<string[]>([]);

  useEffect(() => {
    if (analysisData?.ai_analysis) {
      // 解析AI分析結果
      const insights = analysisData.ai_analysis.split('\n')
        .filter((line: string) => line.trim().length > 0)
        .slice(0, 5); // 取前5條洞察
      setAiInsights(insights);
    }
  }, [analysisData]);

  if (loading) {
    return (
      <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700 p-6">
        <div className="flex items-center space-x-3 mb-4">
          <span className="text-xl">🤖</span>
          <h3 className="text-lg font-semibold text-white">AI Analysis</h3>
        </div>
        
        <div className="flex items-center justify-center py-8">
          <div className="text-center">
            <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
            <p className="text-slate-400">AI is analyzing {symbol}...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700 p-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-3">
          <span className="text-xl">🤖</span>
          <h3 className="text-lg font-semibold text-white">AI Analysis</h3>
        </div>
        <div className="px-2 py-1 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full">
          <span className="text-xs text-white font-medium">GPT-4 Powered</span>
        </div>
      </div>
      
      {!analysisData ? (
        <div className="text-center py-8">
          <div className="text-4xl mb-4">🎯</div>
          <p className="text-slate-400">Select a symbol for AI analysis</p>
        </div>
      ) : (
        <div className="space-y-4">
          {/* AI Recommendation */}
          <div className="bg-gradient-to-r from-blue-600/20 to-purple-600/20 rounded-lg p-4 border border-blue-500/30">
            <div className="flex items-center space-x-2 mb-2">
              <span className="text-sm font-medium text-blue-200">AI Recommendation</span>
              <div className="px-2 py-0.5 bg-blue-600 text-white text-xs rounded-full">
                {analysisData.ai_recommendation || 'Analyzing'}
              </div>
            </div>
            <p className="text-sm text-slate-300">
              {analysisData.ai_summary || 'Generating insights based on technical and fundamental analysis...'}
            </p>
          </div>

          {/* Key Insights */}
          {aiInsights.length > 0 && (
            <div>
              <h4 className="text-sm font-medium text-slate-300 mb-3">Key Insights</h4>
              <div className="space-y-2">
                {aiInsights.map((insight, index) => (
                  <div key={index} className="flex items-start space-x-2 text-sm">
                    <div className="w-1.5 h-1.5 bg-blue-400 rounded-full mt-2 flex-shrink-0"></div>
                    <span className="text-slate-300">{insight}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Technical Score */}
          {analysisData.technical_score && (
            <div className="border-t border-slate-600 pt-4">
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm text-slate-400">Technical Score</span>
                <span className="text-white font-semibold">
                  {(analysisData.technical_score * 100).toFixed(0)}/100
                </span>
              </div>
              <div className="w-full bg-slate-700 rounded-full h-2">
                <div 
                  className="bg-gradient-to-r from-red-500 via-yellow-500 to-green-500 h-2 rounded-full transition-all duration-500"
                  style={{ width: `${analysisData.technical_score * 100}%` }}
                ></div>
              </div>
            </div>
          )}

          <div className="text-xs text-slate-500 mt-4 text-center">
            ⚡ Real-time AI analysis powered by advanced algorithms
          </div>
        </div>
      )}
    </div>
  );
}