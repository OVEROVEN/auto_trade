// API 配置和工具函數

// 獲取API基礎URL
export const getApiUrl = (): string => {
  // 優先使用環境變數
  if (process.env.NEXT_PUBLIC_API_URL) {
    return process.env.NEXT_PUBLIC_API_URL;
  }
  
  // 開發環境默認
  if (process.env.NODE_ENV === 'development') {
    return 'http://localhost:8001';
  }
  
  // 生產環境 - 相對路徑（同域名）
  return '';
};

// 獲取WebSocket URL
export const getWebSocketUrl = (): string => {
  if (process.env.NEXT_PUBLIC_WS_URL) {
    return process.env.NEXT_PUBLIC_WS_URL;
  }
  
  const apiUrl = getApiUrl();
  if (apiUrl.startsWith('https://')) {
    return apiUrl.replace('https://', 'wss://');
  } else if (apiUrl.startsWith('http://')) {
    return apiUrl.replace('http://', 'ws://');
  }
  
  return 'ws://localhost:8001';
};

// API 請求包裝器
export const apiRequest = async (endpoint: string, options: RequestInit = {}) => {
  const apiUrl = getApiUrl();
  const url = apiUrl ? `${apiUrl}${endpoint}` : endpoint;
  
  // 獲取認證 token
  const token = typeof window !== 'undefined' ? localStorage.getItem('auth_token') : null;
  
  const defaultHeaders: Record<string, string> = {
    'Content-Type': 'application/json',
  };
  
  // 添加認證 header
  if (token) {
    defaultHeaders['Authorization'] = `Bearer ${token}`;
  }
  
  const config: RequestInit = {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers,
    },
  };
  
  try {
    const response = await fetch(url, config);
    
    if (!response.ok) {
      throw new Error(`API request failed: ${response.status} ${response.statusText}`);
    }
    
    // 檢查是否是 JSON 響應
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('application/json')) {
      return await response.json();
    }
    
    return await response.text();
  } catch (error) {
    console.error('API Request Error:', error);
    throw error;
  }
};

// 分析股票的 API 調用
export const analyzeStock = async (symbol: string, options: {
  period?: string;
  include_ai?: boolean;
  language?: string;
} = {}) => {
  const { period = '3mo', include_ai = true, language = 'zh' } = options;
  
  return apiRequest(`/analyze/${symbol}`, {
    method: 'POST',
    body: JSON.stringify({
      symbol,
      period,
      include_ai,
      language,
    }),
  });
};

// 獲取健康狀態
export const getHealthStatus = async () => {
  return apiRequest('/health');
};

// 獲取股票代碼列表
export const getSymbols = async () => {
  return apiRequest('/symbols');
};

// 兌換碼 API
export const redeemCode = async (code: string) => {
  return apiRequest('/api/redemption/redeem', {
    method: 'POST',
    body: JSON.stringify({ code }),
  });
};

// Google OAuth 登入
export const googleLogin = async (credential: string) => {
  return apiRequest('/auth/google', {
    method: 'POST',
    body: JSON.stringify({ credential }),
  });
};

// 獲取用戶資訊
export const getUserInfo = async () => {
  return apiRequest('/auth/me');
};

// WebSocket 連接包裝器
export class StockWebSocket {
  private ws: WebSocket | null = null;
  private symbol: string;
  private onMessage: (data: any) => void;
  private onError: (error: Event) => void;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;

  constructor(symbol: string, onMessage: (data: any) => void, onError: (error: Event) => void = () => {}) {
    this.symbol = symbol;
    this.onMessage = onMessage;
    this.onError = onError;
  }

  connect() {
    try {
      const wsUrl = getWebSocketUrl();
      this.ws = new WebSocket(`${wsUrl}/stream/${this.symbol}`);
      
      this.ws.onopen = () => {
        console.log(`WebSocket connected for ${this.symbol}`);
        this.reconnectAttempts = 0;
      };
      
      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          this.onMessage(data);
        } catch (error) {
          console.error('WebSocket message parsing error:', error);
        }
      };
      
      this.ws.onclose = () => {
        console.log(`WebSocket disconnected for ${this.symbol}`);
        this.attemptReconnect();
      };
      
      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        this.onError(error);
      };
      
    } catch (error) {
      console.error('WebSocket connection error:', error);
      this.onError(error as Event);
    }
  }

  private attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);
      
      console.log(`Attempting to reconnect WebSocket in ${delay}ms (attempt ${this.reconnectAttempts})`);
      
      setTimeout(() => {
        this.connect();
      }, delay);
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }
}