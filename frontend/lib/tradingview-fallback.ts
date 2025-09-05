// TradingView Fallback 處理工具
// 當TradingView服務不可用時提供本地替代方案

export interface TradingViewError {
  type: 'NETWORK_ERROR' | 'CORS_ERROR' | 'SCRIPT_LOAD_ERROR' | 'TIMEOUT_ERROR';
  message: string;
  timestamp: number;
}

export interface FallbackChartData {
  symbol: string;
  data: any[];
  lastUpdated: number;
}

// TradingView服務健康檢查
export const checkTradingViewHealth = async (): Promise<boolean> => {
  try {
    // 簡單的健康檢查 - 嘗試載入TradingView腳本
    const response = await fetch('https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js', {
      method: 'HEAD',
      mode: 'no-cors', // 避免CORS問題
    });
    
    return true; // 如果沒有拋出錯誤，表示可以訪問
  } catch (error) {
    console.warn('TradingView health check failed:', error);
    return false;
  }
};

// 創建錯誤報告
export const createTradingViewError = (type: TradingViewError['type'], message: string): TradingViewError => ({
  type,
  message,
  timestamp: Date.now(),
});

// 本地存儲錯誤日誌
export const logTradingViewError = (error: TradingViewError): void => {
  if (typeof window !== 'undefined') {
    try {
      const errors = JSON.parse(localStorage.getItem('tradingview_errors') || '[]');
      errors.push(error);
      
      // 只保留最近的10個錯誤
      if (errors.length > 10) {
        errors.splice(0, errors.length - 10);
      }
      
      localStorage.setItem('tradingview_errors', JSON.stringify(errors));
    } catch (e) {
      console.error('Failed to log TradingView error:', e);
    }
  }
};

// 獲取錯誤統計
export const getTradingViewErrorStats = (): { [key: string]: number } => {
  if (typeof window === 'undefined') return {};
  
  try {
    const errors: TradingViewError[] = JSON.parse(localStorage.getItem('tradingview_errors') || '[]');
    const stats: { [key: string]: number } = {};
    
    errors.forEach(error => {
      stats[error.type] = (stats[error.type] || 0) + 1;
    });
    
    return stats;
  } catch (e) {
    console.error('Failed to get TradingView error stats:', e);
    return {};
  }
};

// Fallback圖表生成器
export const generateFallbackChart = (symbol: string): string => {
  return `
    <div class="fallback-chart-container">
      <style>
        .fallback-chart-container {
          background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
          border-radius: 8px;
          padding: 24px;
          height: 500px;
          display: flex;
          flex-direction: column;
          justify-content: center;
          align-items: center;
          color: white;
          font-family: system-ui, -apple-system, sans-serif;
        }
        
        .chart-icon {
          font-size: 4rem;
          margin-bottom: 1rem;
          opacity: 0.7;
        }
        
        .chart-title {
          font-size: 1.5rem;
          font-weight: 600;
          margin-bottom: 0.5rem;
          color: #f1f5f9;
        }
        
        .chart-subtitle {
          font-size: 1rem;
          color: #94a3b8;
          margin-bottom: 2rem;
          text-align: center;
          max-width: 400px;
        }
        
        .chart-actions {
          display: flex;
          gap: 12px;
          margin-top: 1rem;
        }
        
        .chart-btn {
          padding: 8px 16px;
          border-radius: 6px;
          border: none;
          font-size: 0.875rem;
          cursor: pointer;
          transition: all 0.2s;
        }
        
        .chart-btn-primary {
          background: #3b82f6;
          color: white;
        }
        
        .chart-btn-primary:hover {
          background: #2563eb;
        }
        
        .chart-btn-secondary {
          background: #4b5563;
          color: white;
        }
        
        .chart-btn-secondary:hover {
          background: #374151;
        }
        
        .error-details {
          background: rgba(239, 68, 68, 0.1);
          border: 1px solid rgba(239, 68, 68, 0.3);
          border-radius: 6px;
          padding: 12px;
          margin-top: 1rem;
          font-size: 0.875rem;
          color: #fca5a5;
        }
      </style>
      
      <div class="chart-icon">📊</div>
      <h3 class="chart-title">Chart Temporarily Unavailable</h3>
      <p class="chart-subtitle">
        We're unable to load the TradingView chart for <strong>${symbol}</strong> at the moment. 
        This could be due to network connectivity issues or service maintenance.
      </p>
      
      <div class="chart-actions">
        <button class="chart-btn chart-btn-primary" onclick="window.location.reload()">
          🔄 Retry
        </button>
        <button class="chart-btn chart-btn-secondary" onclick="this.parentElement.parentElement.style.display='none'">
          ❌ Hide
        </button>
      </div>
      
      <div class="error-details">
        <strong>Troubleshooting:</strong><br>
        • Check your internet connection<br>
        • Try refreshing the page<br>
        • Contact support if the issue persists
      </div>
    </div>
  `;
};

// 智能重試機制
export class TradingViewRetryManager {
  private attempts: number = 0;
  private maxAttempts: number = 3;
  private baseDelay: number = 1000; // 1秒
  private symbol: string;

  constructor(symbol: string, maxAttempts: number = 3) {
    this.symbol = symbol;
    this.maxAttempts = maxAttempts;
  }

  async retry<T>(operation: () => Promise<T>): Promise<T> {
    while (this.attempts < this.maxAttempts) {
      try {
        const result = await operation();
        this.attempts = 0; // 重置計數器
        return result;
      } catch (error) {
        this.attempts++;
        
        if (this.attempts >= this.maxAttempts) {
          const tradingViewError = createTradingViewError(
            'NETWORK_ERROR',
            `Failed to load chart for ${this.symbol} after ${this.maxAttempts} attempts`
          );
          logTradingViewError(tradingViewError);
          throw error;
        }

        // 指數退避延遲
        const delay = this.baseDelay * Math.pow(2, this.attempts - 1);
        console.log(`TradingView retry attempt ${this.attempts} for ${this.symbol} in ${delay}ms`);
        
        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }
    
    throw new Error('Max retry attempts exceeded');
  }

  reset() {
    this.attempts = 0;
  }
}

// 性能監控
export const measureTradingViewPerformance = (symbol: string) => {
  const startTime = performance.now();
  
  return {
    end: () => {
      const endTime = performance.now();
      const duration = endTime - startTime;
      
      console.log(`TradingView chart load time for ${symbol}: ${duration.toFixed(2)}ms`);
      
      // 記錄性能數據
      if (typeof window !== 'undefined') {
        try {
          const perfData = JSON.parse(localStorage.getItem('tradingview_performance') || '{}');
          perfData[symbol] = {
            duration,
            timestamp: Date.now()
          };
          localStorage.setItem('tradingview_performance', JSON.stringify(perfData));
        } catch (e) {
          console.error('Failed to store performance data:', e);
        }
      }
      
      return duration;
    }
  };
};

// 清理工具
export const cleanupTradingViewData = () => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('tradingview_errors');
    localStorage.removeItem('tradingview_performance');
    console.log('TradingView data cleaned up');
  }
};