/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    // 如果設置了API URL環境變數，使用它；否則使用默認本地地址
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';
    
    return [
      {
        source: '/api/:path*',
        destination: `${apiUrl}/:path*`,
      },
    ]
  },
  
  // 修復TradingView CORS問題的headers配置
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'SAMEORIGIN',
          },
          {
            key: 'Content-Security-Policy',
            value: [
              "default-src 'self'",
              "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://s3.tradingview.com https://*.tradingview.com",
              "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
              "img-src 'self' data: https: blob:",
              "font-src 'self' https://fonts.gstatic.com",
              "connect-src 'self' https://*.tradingview.com https://telemetry.tradingview.com wss://*.tradingview.com ws://localhost:* http://localhost:*",
              "frame-src 'self' https://*.tradingview.com",
              "worker-src 'self' blob:",
              "child-src 'self' https://*.tradingview.com",
              "object-src 'none'",
              "media-src 'self'",
              "manifest-src 'self'"
            ].join('; ')
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
        ],
      },
    ]
  },
  
  // 優化生產構建
  output: 'standalone',
  
  // 環境變數配置
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001',
  },
  
  // 圖片域名配置
  images: {
    domains: [
      'localhost',
      'your-api-domain.com',
      's3.tradingview.com',
      'static.tradingview.com'
    ],
  },
  
  // 實驗性功能 - 改善TradingView Widget載入
  experimental: {
    // 允許外部腳本
    externalDir: true,
  },
}

module.exports = nextConfig