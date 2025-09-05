'use client';

import { useEffect, useRef, useState } from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import API_URL from '../lib/api';
import { 
  checkTradingViewHealth, 
  createTradingViewError, 
  logTradingViewError, 
  generateFallbackChart,
  TradingViewRetryManager,
  measureTradingViewPerformance 
} from '../lib/tradingview-fallback';

interface TradingChartProps {
  symbol: string;
  className?: string;
}

export function TradingChart({ symbol, className = '' }: TradingChartProps) {
  const { language, t } = useLanguage();
  const containerRef = useRef<HTMLDivElement>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [fallbackMode, setFallbackMode] = useState(false);

  useEffect(() => {
    if (!containerRef.current) return;
    
    setIsLoading(true);
    setError(null);
    
    // 清空容器
    containerRef.current.innerHTML = '';

    // 檢查是否使用fallback模式
    const checkTradingViewAvailability = () => {
      const testScript = document.createElement('script');
      testScript.onerror = () => {
        console.warn('TradingView script failed to load, switching to fallback mode');
        setFallbackMode(true);
        setIsLoading(false);
        loadFallbackChart();
      };
      
      testScript.onload = () => {
        console.log('TradingView script loaded successfully');
        loadTradingViewChart();
      };
      
      testScript.src = 'https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js';
      testScript.async = true;
      
      // 設置超時
      setTimeout(() => {
        if (isLoading) {
          console.warn('TradingView loading timeout, switching to fallback');
          setFallbackMode(true);
          setIsLoading(false);
          loadFallbackChart();
        }
      }, 10000);
      
      document.head.appendChild(testScript);
    };

    const loadTradingViewChart = () => {
      if (!containerRef.current) return;

      // 創建圖表容器
      const chartContainer = document.createElement('div');
      chartContainer.id = `tradingview_${symbol}_${Date.now()}`;
      chartContainer.style.height = '500px';
      chartContainer.style.position = 'relative';
      chartContainer.style.zIndex = '1'; // 確保不會阻擋其他UI元素
      containerRef.current.appendChild(chartContainer);

      // 創建TradingView腳本
      const script = document.createElement('script');
      script.type = 'text/javascript';
      script.async = true;
      
      // 修正的配置，禁用遙測和支持門戶
      const config = {
        autosize: true,
        symbol: symbol.includes('.TW') ? `TWSE:${symbol.replace('.TW', '')}` : `NASDAQ:${symbol}`,
        interval: '1D',
        timezone: 'Asia/Taipei',
        theme: 'dark',
        style: '1',
        locale: language === 'zh-TW' ? 'zh_TW' : language === 'zh-CN' ? 'zh_CN' : 'en',
        toolbar_bg: '#1e293b',
        enable_publishing: false,
        hide_top_toolbar: false,
        hide_legend: false,
        save_image: false, // 禁用保存圖像功能
        container_id: chartContainer.id,
        // 禁用遙測和支持功能
        disabled_features: [
          'header_symbol_search',
          'symbol_search_hot_key',
          'header_resolutions',
          'header_chart_type',
          'header_settings',
          'header_indicators',
          'header_compare',
          'header_undo_redo',
          'header_screenshot',
          'header_fullscreen_button'
        ],
        // 添加錯誤處理
        custom_css_url: undefined,
        studies: [
          'RSI@tv-basicstudies',
          'MACD@tv-basicstudies',
          'Volume@tv-basicstudies'
        ],
        overrides: {
          'paneProperties.background': '#1e293b',
          'paneProperties.vertGridProperties.color': '#334155',
          'paneProperties.horzGridProperties.color': '#334155',
          'symbolWatermarkProperties.transparency': 90,
          'scalesProperties.textColor': '#cbd5e1'
        }
      };

      script.innerHTML = JSON.stringify(config);
      chartContainer.appendChild(script);
      
      // 設置載入完成
      setTimeout(() => {
        setIsLoading(false);
      }, 3000);
    };

    const loadFallbackChart = async () => {
      if (!containerRef.current) return;
      
      try {
        // 創建fallback圖表容器
        const fallbackContainer = document.createElement('div');
        fallbackContainer.className = 'fallback-chart bg-slate-800 rounded-lg p-6';
        fallbackContainer.style.height = '500px';
        fallbackContainer.style.display = 'flex';
        fallbackContainer.style.flexDirection = 'column';
        fallbackContainer.style.justifyContent = 'center';
        fallbackContainer.style.alignItems = 'center';
        
        // 使用本地API獲取圖表
        const response = await fetch(`${API_URL}/chart/custom/${symbol}`);
        if (response.ok) {
          const htmlContent = await response.text();
          fallbackContainer.innerHTML = htmlContent;
        } else {
          fallbackContainer.innerHTML = `
            <div class="text-center">
              <div class="text-4xl mb-4">📊</div>
              <h3 class="text-xl font-semibold text-white mb-2">Chart Unavailable</h3>
              <p class="text-slate-400 mb-4">Unable to load TradingView chart for ${symbol}</p>
              <p class="text-sm text-slate-500">Please check your internet connection or try again later.</p>
              <div class="mt-4 p-4 bg-slate-700 rounded-lg">
                <p class="text-sm text-slate-300">
                  <strong>Symbol:</strong> ${symbol}<br>
                  <strong>Status:</strong> Chart service temporarily unavailable
                </p>
              </div>
            </div>
          `;
        }
        
        containerRef.current.appendChild(fallbackContainer);
        setIsLoading(false);
      } catch (error) {
        console.error('Fallback chart loading failed:', error);
        setError('Failed to load chart data');
        setIsLoading(false);
      }
    };

    checkTradingViewAvailability();

    return () => {
      if (containerRef.current) {
        containerRef.current.innerHTML = '';
      }
    };
  }, [symbol, language]);

  return (
    <div className={`relative ${className}`}>
      {/* Chart Header */}
      <div className="flex items-center justify-between p-4 border-b border-slate-700">
        <div className="flex items-center space-x-3">
          <span className="text-lg">📊</span>
          <div>
            <h2 className="text-lg font-semibold text-white">{t.chartAnalysis} - {symbol}</h2>
            <p className="text-sm text-slate-400">
              {fallbackMode ? 'Local Chart Mode' : 'TradingView Chart'}
            </p>
          </div>
        </div>
        
        <div className="flex items-center space-x-2">
          {fallbackMode && (
            <span className="px-2 py-1 bg-orange-600 text-white text-xs rounded">
              Fallback Mode
            </span>
          )}
          <button 
            className="px-3 py-1 bg-blue-600 text-white text-sm rounded hover:bg-blue-700 transition-colors disabled:bg-blue-800 disabled:cursor-not-allowed"
            disabled={isLoading}
          >
            {t.saveButton || 'Save'}
          </button>
          <button 
            className="px-3 py-1 bg-slate-600 text-white text-sm rounded hover:bg-slate-700 transition-colors disabled:bg-slate-800 disabled:cursor-not-allowed"
            disabled={isLoading}
          >
            {t.fullscreenButton || 'Fullscreen'}
          </button>
        </div>
      </div>
      
      {/* Chart Container */}
      <div ref={containerRef} className="relative bg-slate-800 min-h-[500px]">
        {isLoading && (
          <div className="absolute inset-0 flex items-center justify-center z-10">
            <div className="text-center">
              <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
              <p className="text-slate-400">Loading chart for {symbol}...</p>
              <p className="text-xs text-slate-500 mt-2">
                {fallbackMode ? 'Loading local chart' : 'Connecting to TradingView'}
              </p>
            </div>
          </div>
        )}
        
        {error && (
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="text-center">
              <div className="text-4xl mb-4">⚠️</div>
              <h3 className="text-xl font-semibold text-red-400 mb-2">Chart Error</h3>
              <p className="text-slate-400 mb-4">{error}</p>
              <button 
                onClick={() => window.location.reload()}
                className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
              >
                Reload Page
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}