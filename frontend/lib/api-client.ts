/**
 * 微服務API客戶端
 * 整合核心API和圖表服務
 */

const CORE_API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const CHART_SERVICE_URL = process.env.NEXT_PUBLIC_CHART_SERVICE_URL || 'http://localhost:8001';

interface ApiResponse<T> {
  data?: T;
  error?: string;
  status: number;
}

class ApiClient {
  private coreBaseUrl: string;
  private chartBaseUrl: string;

  constructor() {
    this.coreBaseUrl = CORE_API_URL;
    this.chartBaseUrl = CHART_SERVICE_URL;
  }

  private async request<T>(
    url: string, 
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    try {
      const token = localStorage.getItem('access_token');
      
      const response = await fetch(url, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...(token && { 'Authorization': `Bearer ${token}` }),
          ...options.headers,
        },
      });

      const data = await response.json();

      return {
        data: response.ok ? data : undefined,
        error: response.ok ? undefined : data.detail || 'Request failed',
        status: response.status,
      };
    } catch (error) {
      return {
        error: error instanceof Error ? error.message : 'Network error',
        status: 0,
      };
    }
  }

  // 核心API方法
  async analyzeStock(symbol: string, period: string = '3mo', includeAI: boolean = true) {
    return this.request(`${this.coreBaseUrl}/analyze/${symbol}`, {
      method: 'POST',
      body: JSON.stringify({
        symbol,
        period,
        include_ai: includeAI,
        include_patterns: true,
      }),
    });
  }

  async getStockChart(symbol: string, chartType: string = 'professional', theme: string = 'dark') {
    return this.request(`${this.coreBaseUrl}/chart/${symbol}`, {
      method: 'GET',
    });
  }

  async getStrategyAdvice(symbol: string, marketData: any, preferences: any = {}) {
    return this.request(`${this.coreBaseUrl}/ai/strategy-advice`, {
      method: 'POST',
      body: JSON.stringify({
        symbol,
        market_data: marketData,
        preferences,
      }),
    });
  }

  async getSymbols() {
    return this.request(`${this.coreBaseUrl}/symbols`);
  }

  // 圖表服務方法
  async generateChart(chartRequest: {
    symbol: string;
    period?: string;
    chart_type?: string;
    theme?: string;
    indicators?: any;
    patterns?: any[];
    data?: any;
  }) {
    return this.request(`${this.chartBaseUrl}/generate-chart`, {
      method: 'POST',
      body: JSON.stringify(chartRequest),
    });
  }

  async getChartTypes() {
    return this.request(`${this.chartBaseUrl}/chart-types`);
  }

  // 健康檢查
  async healthCheck(service: 'core' | 'chart' = 'core') {
    const baseUrl = service === 'core' ? this.coreBaseUrl : this.chartBaseUrl;
    return this.request(`${baseUrl}/health`);
  }

  // WebSocket連接 (核心服務)
  createWebSocket(symbol: string): WebSocket {
    const token = localStorage.getItem('access_token');
    const wsUrl = this.coreBaseUrl.replace('http', 'ws');
    return new WebSocket(`${wsUrl}/ws/${symbol}?token=${token}`);
  }
}

// 單例模式
export const apiClient = new ApiClient();

// React Hook
import { useState, useEffect } from 'react';

export function useApiHealth() {
  const [status, setStatus] = useState({
    core: 'checking',
    chart: 'checking',
  });

  useEffect(() => {
    const checkHealth = async () => {
      const [coreHealth, chartHealth] = await Promise.all([
        apiClient.healthCheck('core'),
        apiClient.healthCheck('chart'),
      ]);

      setStatus({
        core: coreHealth.status === 200 ? 'healthy' : 'unhealthy',
        chart: chartHealth.status === 200 ? 'healthy' : 'unhealthy',
      });
    };

    checkHealth();
    const interval = setInterval(checkHealth, 30000); // 30秒檢查一次

    return () => clearInterval(interval);
  }, []);

  return status;
}

export default apiClient;