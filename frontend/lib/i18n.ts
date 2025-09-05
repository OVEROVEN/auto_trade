// Internationalization configuration
export type Language = 'en' | 'zh-TW' | 'zh-CN';

export interface Translations {
  // Header
  appTitle: string;
  subtitle: string;
  
  // Navigation buttons
  realTimeAnalysis: string;
  aiRecommendations: string;
  tradingViewCharts: string;
  
  // Stock search
  searchPlaceholder: string;
  analyzeButton: string;
  popular: string;
  
  // Chart section
  chartAnalysis: string;
  chartDescription: string;
  saveButton: string;
  fullscreenButton: string;
  
  // Market data panel
  marketData: string;
  symbol: string;
  status: string;
  period: string;
  currentPrice: string;
  keyMetrics: string;
  volume: string;
  marketCap: string;
  lastUpdated: string;
  liveData: string;
  months: string;
  
  // AI Analysis panel
  aiAnalysis: string;
  aiRecommendation: string;
  analyzing: string;
  generatingAnalysis: string;
  keyInsights: string;
  aiPoweredDescription: string;
  aiConfidence: string;
  riskLevel: string;
  technicalScore: string;
  low: string;
  high: string;
  
  // Performance panel
  performance: string;
  accuracy: string;
  winRate: string;
  riskScore: string;
  stable: string;
  medium: string;
  recentPerformance: string;
  performanceTrend: string;
  
  // Feature cards
  technicalAnalysis: string;
  technicalAnalysisDesc: string;
  patternRecognition: string;
  patternRecognitionDesc: string;
  aiInsights: string;
  aiInsightsDesc: string;
  multiMarket: string;
  multiMarketDesc: string;
  active: string;
  
  // Status bar
  apiConnected: string;
  realTimeData: string;
  aiAnalysisReady: string;
  systemTime: string;
  market: string;
  marketClosed: string;
  marketOpen: string;
  
  // Recommendations
  buy: string;
  sell: string;
  hold: string;
  
  // Time periods
  oneMonth: string;
  threeMonths: string;
  sixMonths: string;
  oneYear: string;
  
  // Common words
  loading: string;
  error: string;
  noData: string;
  
  // Demo mode
  demoMode: string;
  setRealApiKey: string;
  
  // Authentication
  user: string;
  login: string;
  register: string;
  logout: string;
  email: string;
  password: string;
  fullName: string;
  premiumUser: string;
  freeUser: string;
  freeTier: string; // Added to fix build error
  loginError: string;
  registerError: string;
  networkError: string;
  processing: string;
  loggingIn: string; // Added to fix build error
  registering: string; // Added to fix build error
  loginButton: string;
  registerButton: string;
  noAccount: string;
  haveAccount: string;
  registerNow: string;
  loginNow: string;
  enterEmail: string; // Added to fix build error
  enterPassword: string; // Added to fix build error
  enterFullName: string;
  freeTrialInfo: string;
  
  // Payment
  upgradeNow: string;
  monthlyPlan: string;
  paymentMethods: string;
  creditCard: string;
  ecpay: string;
  newebpay: string;
  
  // Trading price levels
  tradingPriceLevels: string;
  entryPrice: string;
  targetPrice: string;
  stopLoss: string;
  potentialReturn: string;
  
  // Redemption codes
  redemptionCode: string;
  redeemCode: string;
  enterRedemptionCode: string;
  redeemNow: string;
  redemptionSuccess: string;
  redemptionError: string;
  invalidCode: string;
  codeAlreadyUsed: string;
  codeExpired: string;
  creditsAdded: string;
  totalCredits: string;
  redemptionHistory: string;
  noRedemptionHistory: string;
  yourCredits: string;
  bonusCredits: string;
  freeCredits: string;
  dailyCredits: string;
}

export const translations: Record<Language, Translations> = {
  'en': {
    // Header
    appTitle: 'AI Trading Dashboard',
    subtitle: 'Advanced Stock Analysis & AI-Powered Trading Insights',
    
    // Navigation buttons
    realTimeAnalysis: 'Real-time Analysis',
    aiRecommendations: 'AI Recommendations', 
    tradingViewCharts: 'TradingView Charts',
    
    // Stock search
    searchPlaceholder: 'Enter stock symbol (e.g., AAPL, 2330.TW)',
    analyzeButton: 'Analyze',
    popular: 'Popular:',
    
    // Chart section
    chartAnalysis: 'Chart Analysis',
    chartDescription: 'Real-time price data with technical indicators',
    saveButton: 'Save',
    fullscreenButton: 'Fullscreen',
    
    // Market data panel
    marketData: 'Market Data',
    symbol: 'Symbol',
    status: 'Status',
    period: 'Period',
    currentPrice: 'Current Price',
    keyMetrics: 'Key Metrics',
    volume: 'Volume',
    marketCap: 'Market Cap',
    lastUpdated: 'Last updated',
    liveData: 'Live Data',
    months: 'Months',
    
    // AI Analysis panel
    aiAnalysis: 'AI Analysis',
    aiRecommendation: 'AI Recommendation',
    analyzing: 'Analyzing',
    generatingAnalysis: 'Generating analysis based on technical and fundamental analysis...',
    keyInsights: 'Key Insights',
    aiPoweredDescription: 'Real-time AI analysis powered by advanced algorithms',
    aiConfidence: 'AI Confidence',
    riskLevel: 'Risk Level',
    technicalScore: 'Technical Score',
    low: 'Low',
    high: 'High',
    
    // Performance panel
    performance: 'Performance',
    accuracy: 'Accuracy',
    winRate: 'Win Rate',
    riskScore: 'Risk Score',
    stable: 'Stable',
    medium: 'Medium',
    recentPerformance: 'Recent Performance',
    performanceTrend: '10-day performance trend',
    
    // Feature cards
    technicalAnalysis: 'Technical Analysis',
    technicalAnalysisDesc: '15+ indicators including RSI, MACD, Bollinger Bands',
    patternRecognition: 'Pattern Recognition',
    patternRecognitionDesc: 'Advanced chart patterns and trend analysis',
    aiInsights: 'AI Insights',
    aiInsightsDesc: 'OpenAI powered trading recommendations',
    multiMarket: 'Multi-Market',
    multiMarketDesc: 'US stocks and Taiwan market support',
    active: 'Active',
    
    // Status bar
    apiConnected: 'API Connected',
    realTimeData: 'Real-time Data',
    aiAnalysisReady: 'AI Analysis Ready',
    systemTime: 'System Time',
    market: 'Market',
    marketClosed: 'Closed',
    marketOpen: 'Open',
    
    // Recommendations
    buy: 'BUY',
    sell: 'SELL',
    hold: 'HOLD',
    
    // Time periods
    oneMonth: '1 Month',
    threeMonths: '3 Months',
    sixMonths: '6 Months',
    oneYear: '1 Year',
    
    // Common words
    loading: 'Loading...',
    error: 'Error',
    noData: 'No data available',
    
    // Demo mode
    demoMode: 'DEMO MODE',
    setRealApiKey: 'Set real OpenAI API Key for live AI analysis',
    
    // Authentication
    user: 'User',
    login: 'Login',
    register: 'Register',
    logout: 'Logout',
    email: 'Email',
    password: 'Password',
    fullName: 'Full Name',
    premiumUser: 'Premium User',
    freeUser: 'Free User',
    freeTier: 'Free Tier',
    loginError: 'Login failed. Please check your credentials.',
    registerError: 'Registration failed. Please try again.',
    networkError: 'Network error. Please try again.',
    processing: 'Processing...',
    loggingIn: 'Logging in...',
    registering: 'Registering...',
    loginButton: 'Sign In',
    registerButton: 'Create Account',
    noAccount: 'Don\'t have an account?',
    haveAccount: 'Already have an account?',
    registerNow: 'Register now',
    loginNow: 'Login now',
    enterEmail: 'Enter your email',
    enterPassword: 'Enter your password',
    enterFullName: 'Enter your full name',
    freeTrialInfo: 'Free trial: 3 AI analyses + 1 daily analysis',
    
    // Payment
    upgradeNow: 'Upgrade Now',
    monthlyPlan: '$5/month - Unlimited AI Analysis',
    paymentMethods: 'Payment Methods:',
    creditCard: 'Credit Card',
    ecpay: 'ECPay (綠界科技)',
    newebpay: 'NewebPay (藍新金流)',
    
    // Trading price levels
    tradingPriceLevels: 'Trading Price Levels',
    entryPrice: 'Entry Price',
    targetPrice: 'Target Price',
    stopLoss: 'Stop Loss',
    potentialReturn: 'Potential Return',
    
    // Redemption codes
    redemptionCode: 'Redemption Code',
    redeemCode: 'Redeem Code',
    enterRedemptionCode: 'Enter redemption code (e.g., ABCD-1234-EFGH)',
    redeemNow: 'Redeem Now',
    redemptionSuccess: 'Code redeemed successfully!',
    redemptionError: 'Failed to redeem code',
    invalidCode: 'Invalid or inactive redemption code',
    codeAlreadyUsed: 'Code has already been used',
    codeExpired: 'Code has expired',
    creditsAdded: 'Credits Added',
    totalCredits: 'Total Credits',
    redemptionHistory: 'Redemption History',
    noRedemptionHistory: 'No redemption history yet',
    yourCredits: 'Your Credits',
    bonusCredits: 'Bonus Credits',
    freeCredits: 'Free Credits',
    dailyCredits: 'Daily Credits'
  },
  
  'zh-TW': {
    // Header
    appTitle: 'AI 交易儀表板',
    subtitle: '先進股票分析與 AI 智能交易洞察',
    
    // Navigation buttons
    realTimeAnalysis: '即時分析',
    aiRecommendations: 'AI 建議',
    tradingViewCharts: 'TradingView 圖表',
    
    // Stock search
    searchPlaceholder: '輸入股票代號 (例如：AAPL, 2330.TW)',
    analyzeButton: '分析',
    popular: '熱門：',
    
    // Chart section
    chartAnalysis: '圖表分析',
    chartDescription: '即時價格數據與技術指標',
    saveButton: '儲存',
    fullscreenButton: '全螢幕',
    
    // Market data panel
    marketData: '市場資料',
    symbol: '股票代號',
    status: '狀態',
    period: '週期',
    currentPrice: '當前價格',
    keyMetrics: '關鍵指標',
    volume: '成交量',
    marketCap: '市值',
    lastUpdated: '最後更新',
    liveData: '即時資料',
    months: '個月',
    
    // AI Analysis panel
    aiAnalysis: 'AI 分析',
    aiRecommendation: 'AI 建議',
    analyzing: '分析中',
    generatingAnalysis: '基於技術面和基本面分析生成建議中...',
    keyInsights: '關鍵洞察',
    aiPoweredDescription: '由先進演算法驅動的即時AI分析',
    aiConfidence: 'AI 信心度',
    riskLevel: '風險等級',
    technicalScore: '技術評分',
    low: '低',
    high: '高',
    
    // Performance panel
    performance: '績效表現',
    accuracy: '準確度',
    winRate: '勝率',
    riskScore: '風險評分',
    stable: '穩定',
    medium: '中等',
    recentPerformance: '近期表現',
    performanceTrend: '10日績效趨勢',
    
    // Feature cards
    technicalAnalysis: '技術分析',
    technicalAnalysisDesc: '15+ 指標包含 RSI、MACD、布林通道',
    patternRecognition: '形態辨識',
    patternRecognitionDesc: '進階圖表形態與趨勢分析',
    aiInsights: 'AI 洞察',
    aiInsightsDesc: 'OpenAI 驅動的交易建議',
    multiMarket: '多市場',
    multiMarketDesc: '美股與台股市場支援',
    active: '啟用中',
    
    // Status bar
    apiConnected: 'API 已連接',
    realTimeData: '即時資料',
    aiAnalysisReady: 'AI 分析就緒',
    systemTime: '系統時間',
    market: '市場',
    marketClosed: '已收盤',
    marketOpen: '開盤中',
    
    // Recommendations
    buy: '買入',
    sell: '賣出',
    hold: '持有',
    
    // Time periods
    oneMonth: '1個月',
    threeMonths: '3個月',
    sixMonths: '6個月',
    oneYear: '1年',
    
    // Common words
    loading: '載入中...',
    error: '錯誤',
    noData: '無可用資料',
    
    // Demo mode
    demoMode: '示範模式',
    setRealApiKey: '設定真實 OpenAI API 金鑰以取得即時 AI 分析',
    
    // Authentication
    user: '用戶',
    login: '登入',
    register: '註冊',
    logout: '登出',
    email: '電子郵件',
    password: '密碼',
    fullName: '全名',
    premiumUser: '付費用戶',
    freeUser: '免費用戶',
    freeTier: '免費方案',
    loginError: '登入失敗，請檢查您的憑證。',
    registerError: '註冊失敗，請重試。',
    networkError: '網路錯誤，請重試。',
    processing: '處理中...',
    loggingIn: '登入中...',
    registering: '註冊中...',
    loginButton: '登入',
    registerButton: '建立帳戶',
    noAccount: '沒有帳戶？',
    haveAccount: '已經有帳戶？',
    registerNow: '立即註冊',
    loginNow: '立即登入',
    enterEmail: '輸入您的電子郵件',
    enterPassword: '輸入您的密碼',
    enterFullName: '輸入您的全名',
    freeTrialInfo: '免費試用：3次AI分析 + 每天1次分析',
    
    // Payment
    upgradeNow: '立即升級',
    monthlyPlan: '每月$5美金 - 無限AI分析',
    paymentMethods: '付款方式：',
    creditCard: '信用卡',
    ecpay: '綠界科技',
    newebpay: '藍新金流',
    
    // Trading price levels
    tradingPriceLevels: '交易價位建議',
    entryPrice: '建議進場價',
    targetPrice: '目標價位',
    stopLoss: '停損價位',
    potentialReturn: '潛在報酬',
    
    // Redemption codes
    redemptionCode: '兌換碼',
    redeemCode: '兌換代碼',
    enterRedemptionCode: '輸入兌換碼 (例如：ABCD-1234-EFGH)',
    redeemNow: '立即兌換',
    redemptionSuccess: '兌換碼兌換成功！',
    redemptionError: '兌換失敗',
    invalidCode: '無效或已停用的兌換碼',
    codeAlreadyUsed: '兌換碼已被使用',
    codeExpired: '兌換碼已過期',
    creditsAdded: '增加點數',
    totalCredits: '總點數',
    redemptionHistory: '兌換歷史',
    noRedemptionHistory: '尚無兌換紀錄',
    yourCredits: '您的點數',
    bonusCredits: '額外點數',
    freeCredits: '免費點數',
    dailyCredits: '每日點數'
  },
  
  'zh-CN': {
    // Header
    appTitle: 'AI 交易仪表板',
    subtitle: '先进股票分析与 AI 智能交易洞察',
    
    // Navigation buttons
    realTimeAnalysis: '实时分析',
    aiRecommendations: 'AI 建议',
    tradingViewCharts: 'TradingView 图表',
    
    // Stock search
    searchPlaceholder: '输入股票代码 (例如：AAPL, 2330.TW)',
    analyzeButton: '分析',
    popular: '热门：',
    
    // Chart section
    chartAnalysis: '图表分析',
    chartDescription: '实时价格数据与技术指标',
    saveButton: '保存',
    fullscreenButton: '全屏',
    
    // Market data panel
    marketData: '市场数据',
    symbol: '股票代码',
    status: '状态',
    period: '周期',
    currentPrice: '当前价格',
    keyMetrics: '关键指标',
    volume: '成交量',
    marketCap: '市值',
    lastUpdated: '最后更新',
    liveData: '实时数据',
    months: '个月',
    
    // AI Analysis panel
    aiAnalysis: 'AI 分析',
    aiRecommendation: 'AI 建议',
    analyzing: '分析中',
    generatingAnalysis: '基于技术面和基本面分析生成建议中...',
    keyInsights: '关键洞察',
    aiPoweredDescription: '由先进算法驱动的实时AI分析',
    aiConfidence: 'AI 信心度',
    riskLevel: '风险等级',
    technicalScore: '技术评分',
    low: '低',
    high: '高',
    
    // Performance panel
    performance: '绩效表现',
    accuracy: '准确度',
    winRate: '胜率',
    riskScore: '风险评分',
    stable: '稳定',
    medium: '中等',
    recentPerformance: '近期表现',
    performanceTrend: '10日绩效趋势',
    
    // Feature cards
    technicalAnalysis: '技术分析',
    technicalAnalysisDesc: '15+ 指标包含 RSI、MACD、布林带',
    patternRecognition: '形态识别',
    patternRecognitionDesc: '进阶图表形态与趋势分析',
    aiInsights: 'AI 洞察',
    aiInsightsDesc: 'OpenAI 驱动的交易建议',
    multiMarket: '多市场',
    multiMarketDesc: '美股与台股市场支持',
    active: '启用中',
    
    // Status bar
    apiConnected: 'API 已连接',
    realTimeData: '实时数据',
    aiAnalysisReady: 'AI 分析就绪',
    systemTime: '系统时间',
    market: '市场',
    marketClosed: '已收盘',
    marketOpen: '开盘中',
    
    // Recommendations
    buy: '买入',
    sell: '卖出',
    hold: '持有',
    
    // Time periods
    oneMonth: '1个月',
    threeMonths: '3个月',
    sixMonths: '6个月',
    oneYear: '1年',
    
    // Common words
    loading: '加载中...',
    error: '错误',
    noData: '无可用数据',
    
    // Demo mode
    demoMode: '演示模式',
    setRealApiKey: '设置真实 OpenAI API 密钥以获取实时 AI 分析',
    
    // Authentication
    user: '用户',
    login: '登录',
    register: '注册',
    logout: '登出',
    email: '电子邮件',
    password: '密码',
    fullName: '全名',
    premiumUser: '付费用户',
    freeUser: '免费用户',
    freeTier: '免费方案',
    loginError: '登录失败，请检查您的凭证。',
    registerError: '注册失败，请重试。',
    networkError: '网络错误，请重试。',
    processing: '处理中...',
    loggingIn: '登录中...',
    registering: '注册中...',
    loginButton: '登录',
    registerButton: '创建账户',
    noAccount: '没有账户？',
    haveAccount: '已经有账户？',
    registerNow: '立即注册',
    loginNow: '立即登录',
    enterEmail: '输入您的电子邮件',
    enterPassword: '输入您的密码',
    enterFullName: '输入您的全名',
    freeTrialInfo: '免费试用：3次AI分析 + 每天1次分析',
    
    // Payment
    upgradeNow: '立即升级',
    monthlyPlan: '每月$5美金 - 无限AI分析',
    paymentMethods: '付款方式：',
    creditCard: '信用卡',
    ecpay: '绿界科技',
    newebpay: '蓝新金流',
    
    // Trading price levels
    tradingPriceLevels: '交易价位建议',
    entryPrice: '建议进场价',
    targetPrice: '目标价位',
    stopLoss: '止损价位',
    potentialReturn: '潜在回报',
    
    // Redemption codes
    redemptionCode: '兑换码',
    redeemCode: '兑换代码',
    enterRedemptionCode: '输入兑换码 (例如：ABCD-1234-EFGH)',
    redeemNow: '立即兑换',
    redemptionSuccess: '兑换码兑换成功！',
    redemptionError: '兑换失败',
    invalidCode: '无效或已停用的兑换码',
    codeAlreadyUsed: '兑换码已被使用',
    codeExpired: '兑换码已过期',
    creditsAdded: '增加积分',
    totalCredits: '总积分',
    redemptionHistory: '兑换历史',
    noRedemptionHistory: '暂无兑换记录',
    yourCredits: '您的积分',
    bonusCredits: '额外积分',
    freeCredits: '免费积分',
    dailyCredits: '每日积分'
  }
};

export const getTranslations = (lang: Language): Translations => {
  return translations[lang] || translations['en'];
};