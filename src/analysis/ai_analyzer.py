import openai
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import json
import logging
import base64
from io import BytesIO
from datetime import datetime
import asyncio
import aiohttp

try:
    from PIL import Image
    import matplotlib.pyplot as plt
    import mplfinance as mpf
    PLOTTING_AVAILABLE = True
except ImportError:
    PLOTTING_AVAILABLE = False
    logging.warning("Plotting libraries not available. Chart analysis will be limited.")

from config.settings import settings

logger = logging.getLogger(__name__)

@dataclass
class AIAnalysisResult:
    symbol: str
    analysis_type: str
    timestamp: datetime
    confidence: float
    recommendation: str  # 'BUY', 'SELL', 'HOLD'
    reasoning: str
    key_factors: List[str]
    price_target: Optional[float] = None
    stop_loss: Optional[float] = None
    risk_score: Optional[float] = None

class OpenAIAnalyzer:
    """
    AI-powered trading analysis using OpenAI's GPT models.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.openai_api_key
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        openai.api_key = self.api_key
        self.client = openai.OpenAI(api_key=self.api_key)
        
    async def analyze_technical_data(
        self, 
        symbol: str,
        data: pd.DataFrame,
        indicators: Dict[str, Any],
        patterns: Dict[str, List],
        context: Optional[str] = None
    ) -> AIAnalysisResult:
        """
        Analyze technical data using AI.
        
        Args:
            symbol: Stock symbol
            data: OHLCV DataFrame
            indicators: Technical indicators
            patterns: Detected patterns
            context: Additional context
            
        Returns:
            AI analysis result
        """
        try:
            # Prepare data summary for AI
            data_summary = self._prepare_technical_summary(symbol, data, indicators, patterns)
            
            # Create prompt
            prompt = self._create_technical_analysis_prompt(data_summary, context)
            
            # Get AI response
            response = await self._get_ai_response(prompt)
            
            # Parse response
            analysis = self._parse_ai_response(symbol, response, 'technical_analysis')
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error in AI technical analysis: {str(e)}")
            return self._create_fallback_analysis(symbol, 'technical_analysis')
    
    async def analyze_chart_image(
        self, 
        symbol: str,
        chart_image: bytes,
        timeframe: str = "1D",
        context: Optional[str] = None
    ) -> AIAnalysisResult:
        """
        Analyze a chart image using OpenAI's vision capabilities.
        
        Args:
            symbol: Stock symbol
            chart_image: Chart image bytes
            timeframe: Chart timeframe
            context: Additional context
            
        Returns:
            AI analysis result
        """
        try:
            # Encode image to base64
            image_base64 = base64.b64encode(chart_image).decode('utf-8')
            
            # Create vision prompt
            prompt = self._create_chart_analysis_prompt(symbol, timeframe, context)
            
            # Use GPT-4 Vision
            response = self.client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            # Parse response
            analysis = self._parse_ai_response(symbol, response.choices[0].message.content, 'chart_analysis')
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error in AI chart analysis: {str(e)}")
            return self._create_fallback_analysis(symbol, 'chart_analysis')
    
    async def analyze_market_sentiment(
        self,
        symbol: str,
        news_headlines: List[str],
        social_sentiment: Optional[Dict] = None,
        earnings_data: Optional[Dict] = None
    ) -> AIAnalysisResult:
        """
        Analyze market sentiment using AI.
        
        Args:
            symbol: Stock symbol
            news_headlines: List of recent news headlines
            social_sentiment: Social media sentiment data
            earnings_data: Recent earnings information
            
        Returns:
            AI sentiment analysis result
        """
        try:
            # Prepare sentiment data
            sentiment_summary = self._prepare_sentiment_summary(
                symbol, news_headlines, social_sentiment, earnings_data
            )
            
            # Create prompt
            prompt = self._create_sentiment_analysis_prompt(sentiment_summary)
            
            # Get AI response
            response = await self._get_ai_response(prompt)
            
            # Parse response
            analysis = self._parse_ai_response(symbol, response, 'sentiment_analysis')
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error in AI sentiment analysis: {str(e)}")
            return self._create_fallback_analysis(symbol, 'sentiment_analysis')
    
    async def generate_trading_strategy(
        self,
        symbol: str,
        technical_analysis: AIAnalysisResult,
        sentiment_analysis: AIAnalysisResult,
        risk_tolerance: str = "moderate",
        investment_horizon: str = "medium_term"
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive trading strategy using AI.
        
        Args:
            symbol: Stock symbol
            technical_analysis: Technical analysis result
            sentiment_analysis: Sentiment analysis result
            risk_tolerance: Risk tolerance level
            investment_horizon: Investment time horizon
            
        Returns:
            Comprehensive trading strategy
        """
        try:
            # Combine analyses
            combined_data = {
                'symbol': symbol,
                'technical': {
                    'recommendation': technical_analysis.recommendation,
                    'confidence': technical_analysis.confidence,
                    'reasoning': technical_analysis.reasoning,
                    'key_factors': technical_analysis.key_factors
                },
                'sentiment': {
                    'recommendation': sentiment_analysis.recommendation,
                    'confidence': sentiment_analysis.confidence,
                    'reasoning': sentiment_analysis.reasoning,
                    'key_factors': sentiment_analysis.key_factors
                },
                'risk_tolerance': risk_tolerance,
                'investment_horizon': investment_horizon
            }
            
            # Create strategy prompt
            prompt = self._create_strategy_prompt(combined_data)
            
            # Get AI response
            response = await self._get_ai_response(prompt)
            
            # Parse strategy response
            strategy = self._parse_strategy_response(response)
            
            return strategy
            
        except Exception as e:
            logger.error(f"Error generating trading strategy: {str(e)}")
            return self._create_fallback_strategy(symbol)
    
    def _prepare_technical_summary(
        self, 
        symbol: str, 
        data: pd.DataFrame, 
        indicators: Dict, 
        patterns: Dict
    ) -> Dict[str, Any]:
        """Prepare technical data summary for AI analysis."""
        if data.empty:
            return {}
        
        latest = data.iloc[-1]
        prev_week = data.tail(5)
        
        summary = {
            'symbol': symbol,
            'current_price': latest['close'],
            'price_change_1d': ((latest['close'] - data.iloc[-2]['close']) / data.iloc[-2]['close']) * 100 if len(data) > 1 else 0,
            'price_change_5d': ((latest['close'] - prev_week.iloc[0]['close']) / prev_week.iloc[0]['close']) * 100 if len(prev_week) >= 5 else 0,
            'volume_ratio': latest['volume'] / data['volume'].rolling(20).mean().iloc[-1] if len(data) >= 20 else 1,
            'indicators': {},
            'patterns': {}
        }
        
        # Add key indicators
        indicator_fields = ['rsi', 'macd', 'macd_signal', 'bb_upper', 'bb_lower', 'sma_20', 'sma_50']
        for field in indicator_fields:
            if field in data.columns and not pd.isna(latest.get(field)):
                summary['indicators'][field] = latest[field]
        
        # Add patterns summary
        for pattern_type, pattern_list in patterns.items():
            if pattern_list:
                summary['patterns'][pattern_type] = len(pattern_list)
        
        return summary
    
    def _prepare_sentiment_summary(
        self,
        symbol: str,
        news_headlines: List[str],
        social_sentiment: Optional[Dict],
        earnings_data: Optional[Dict]
    ) -> Dict[str, Any]:
        """Prepare sentiment data summary for AI analysis."""
        summary = {
            'symbol': symbol,
            'news_headlines': news_headlines[:10],  # Limit to recent 10
            'social_sentiment': social_sentiment or {},
            'earnings_data': earnings_data or {}
        }
        return summary
    
    def _create_technical_analysis_prompt(self, data_summary: Dict, context: Optional[str]) -> str:
        """Create prompt for technical analysis."""
        prompt = f"""
        As an expert technical analyst, analyze the following stock data and provide a trading recommendation.

        Stock: {data_summary.get('symbol', 'Unknown')}
        Current Price: ${data_summary.get('current_price', 0):.2f}
        1-Day Change: {data_summary.get('price_change_1d', 0):.2f}%
        5-Day Change: {data_summary.get('price_change_5d', 0):.2f}%
        Volume Ratio: {data_summary.get('volume_ratio', 1):.2f}x

        Technical Indicators:
        """
        
        for indicator, value in data_summary.get('indicators', {}).items():
            prompt += f"- {indicator.upper()}: {value:.2f}\n"
        
        prompt += "\nDetected Patterns:\n"
        for pattern_type, count in data_summary.get('patterns', {}).items():
            prompt += f"- {pattern_type.replace('_', ' ').title()}: {count} detected\n"
        
        if context:
            prompt += f"\nAdditional Context: {context}\n"
        
        prompt += """
        Please provide:
        1. Overall recommendation (BUY/SELL/HOLD)
        2. Confidence level (0-1)
        3. Key reasoning factors
        4. Price target (if applicable)
        5. Stop loss level (if applicable)
        6. Risk assessment (0-1, where 1 is highest risk)

        Format your response as JSON with keys: recommendation, confidence, reasoning, key_factors, price_target, stop_loss, risk_score
        """
        
        return prompt
    
    def _create_chart_analysis_prompt(self, symbol: str, timeframe: str, context: Optional[str]) -> str:
        """Create prompt for chart image analysis."""
        prompt = f"""
        As an expert chart analyst, analyze this {timeframe} chart for {symbol}.

        Look for:
        1. Trend direction and strength
        2. Support and resistance levels
        3. Chart patterns (triangles, flags, head & shoulders, etc.)
        4. Volume patterns
        5. Potential breakout or breakdown signals
        6. Entry and exit points

        {f"Additional context: {context}" if context else ""}

        Provide a trading recommendation with reasoning. Format your response as JSON with keys:
        recommendation, confidence, reasoning, key_factors, price_target, stop_loss, risk_score
        """
        
        return prompt
    
    def _create_sentiment_analysis_prompt(self, sentiment_summary: Dict) -> str:
        """Create prompt for sentiment analysis."""
        prompt = f"""
        As a market sentiment expert, analyze the following information for {sentiment_summary['symbol']}:

        Recent News Headlines:
        """
        
        for headline in sentiment_summary['news_headlines']:
            prompt += f"- {headline}\n"
        
        if sentiment_summary['social_sentiment']:
            prompt += f"\nSocial Sentiment Data: {sentiment_summary['social_sentiment']}\n"
        
        if sentiment_summary['earnings_data']:
            prompt += f"\nEarnings Information: {sentiment_summary['earnings_data']}\n"
        
        prompt += """
        Analyze the overall market sentiment and provide:
        1. Sentiment-based recommendation (BUY/SELL/HOLD)
        2. Confidence level (0-1)
        3. Key sentiment drivers
        4. Risk factors from sentiment perspective

        Format as JSON with keys: recommendation, confidence, reasoning, key_factors, risk_score
        """
        
        return prompt
    
    def _create_strategy_prompt(self, combined_data: Dict) -> str:
        """Create prompt for strategy generation."""
        prompt = f"""
        Create a comprehensive trading strategy for {combined_data['symbol']} based on:

        Technical Analysis:
        - Recommendation: {combined_data['technical']['recommendation']}
        - Confidence: {combined_data['technical']['confidence']:.2f}
        - Reasoning: {combined_data['technical']['reasoning']}

        Sentiment Analysis:
        - Recommendation: {combined_data['sentiment']['recommendation']}
        - Confidence: {combined_data['sentiment']['confidence']:.2f}
        - Reasoning: {combined_data['sentiment']['reasoning']}

        Risk Tolerance: {combined_data['risk_tolerance']}
        Investment Horizon: {combined_data['investment_horizon']}

        Provide a detailed strategy including:
        1. Overall recommendation and rationale
        2. Position sizing recommendation
        3. Entry strategy
        4. Exit strategy
        5. Risk management rules
        6. Timeline and milestones

        Format as JSON with keys: recommendation, position_size, entry_strategy, exit_strategy, risk_management, timeline
        """
        
        return prompt
    
    async def _get_ai_response(self, prompt: str) -> str:
        """Get response from OpenAI API."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert financial analyst and trader. Provide accurate, data-driven analysis."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error getting AI response: {str(e)}")
            raise
    
    def _parse_ai_response(self, symbol: str, response: str, analysis_type: str) -> AIAnalysisResult:
        """Parse AI response into structured result."""
        try:
            # Try to parse as JSON first
            if response.strip().startswith('{'):
                data = json.loads(response)
            else:
                # Extract JSON from text response
                json_start = response.find('{')
                json_end = response.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = response[json_start:json_end]
                    data = json.loads(json_str)
                else:
                    # Fallback: parse manually
                    data = self._manual_parse_response(response)
            
            return AIAnalysisResult(
                symbol=symbol,
                analysis_type=analysis_type,
                timestamp=datetime.now(),
                confidence=float(data.get('confidence', 0.5)),
                recommendation=data.get('recommendation', 'HOLD').upper(),
                reasoning=data.get('reasoning', 'AI analysis performed'),
                key_factors=data.get('key_factors', []),
                price_target=data.get('price_target'),
                stop_loss=data.get('stop_loss'),
                risk_score=data.get('risk_score')
            )
            
        except Exception as e:
            logger.error(f"Error parsing AI response: {str(e)}")
            return self._create_fallback_analysis(symbol, analysis_type)
    
    def _manual_parse_response(self, response: str) -> Dict:
        """Manually parse response if JSON parsing fails."""
        data = {
            'confidence': 0.5,
            'recommendation': 'HOLD',
            'reasoning': response[:200],  # First 200 chars
            'key_factors': [],
            'risk_score': 0.5
        }
        
        # Extract recommendation
        response_upper = response.upper()
        if 'BUY' in response_upper and 'SELL' not in response_upper:
            data['recommendation'] = 'BUY'
        elif 'SELL' in response_upper:
            data['recommendation'] = 'SELL'
        
        return data
    
    def _parse_strategy_response(self, response: str) -> Dict[str, Any]:
        """Parse strategy response."""
        try:
            if response.strip().startswith('{'):
                return json.loads(response)
            else:
                # Extract JSON from text
                json_start = response.find('{')
                json_end = response.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = response[json_start:json_end]
                    return json.loads(json_str)
        except Exception as e:
            logger.error(f"Error parsing strategy response: {str(e)}")
        
        # Fallback strategy
        return self._create_fallback_strategy("Unknown")
    
    def _create_fallback_analysis(self, symbol: str, analysis_type: str) -> AIAnalysisResult:
        """Create fallback analysis when AI fails."""
        return AIAnalysisResult(
            symbol=symbol,
            analysis_type=analysis_type,
            timestamp=datetime.now(),
            confidence=0.3,
            recommendation='HOLD',
            reasoning='Unable to complete AI analysis. Defaulting to HOLD recommendation.',
            key_factors=['AI analysis failed'],
            risk_score=0.5
        )
    
    def _create_fallback_strategy(self, symbol: str) -> Dict[str, Any]:
        """Create fallback strategy when AI fails."""
        return {
            'recommendation': 'HOLD',
            'position_size': 0.05,  # 5% of portfolio
            'entry_strategy': 'Wait for clearer signals',
            'exit_strategy': 'Review in 1 week',
            'risk_management': 'Use 2% stop loss',
            'timeline': '1-2 weeks for reassessment'
        }
    
    def create_chart_image(self, data: pd.DataFrame, symbol: str) -> Optional[bytes]:
        """
        Create a chart image for AI analysis.
        
        Args:
            data: OHLCV DataFrame
            symbol: Stock symbol
            
        Returns:
            Chart image as bytes or None if plotting not available
        """
        if not PLOTTING_AVAILABLE or data.empty:
            return None
        
        try:
            # Create candlestick chart
            fig, axes = mpf.plot(
                data.tail(50),  # Last 50 periods
                type='candle',
                style='charles',
                title=f'{symbol} - Stock Chart',
                ylabel='Price ($)',
                volume=True,
                returnfig=True,
                figsize=(12, 8)
            )
            
            # Save to bytes
            buffer = BytesIO()
            fig.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            
            chart_bytes = buffer.getvalue()
            buffer.close()
            
            return chart_bytes
            
        except Exception as e:
            logger.error(f"Error creating chart image: {str(e)}")
            return None

# Example usage
if __name__ == "__main__":
    import asyncio
    
    async def test_ai_analyzer():
        # Note: Requires valid OpenAI API key
        try:
            analyzer = OpenAIAnalyzer()
            
            # Create sample data
            dates = pd.date_range('2023-01-01', periods=50, freq='D')
            np.random.seed(42)
            
            close_prices = 100 + np.cumsum(np.random.randn(50) * 0.5)
            sample_data = pd.DataFrame({
                'open': close_prices + np.random.randn(50) * 0.3,
                'high': close_prices + np.random.rand(50) * 2,
                'low': close_prices - np.random.rand(50) * 2,
                'close': close_prices,
                'volume': np.random.randint(1000000, 5000000, 50)
            }, index=dates)
            
            # Mock indicators and patterns
            indicators = {'rsi': 65, 'macd': 0.5}
            patterns = {'breakouts': [], 'triangles': []}
            
            # Test technical analysis
            result = await analyzer.analyze_technical_data(
                'AAPL', sample_data, indicators, patterns
            )
            
            print(f"AI Analysis Result:")
            print(f"Recommendation: {result.recommendation}")
            print(f"Confidence: {result.confidence:.2f}")
            print(f"Reasoning: {result.reasoning}")
            
        except Exception as e:
            print(f"Test failed: {str(e)}")
    
    # Run test
    # asyncio.run(test_ai_analyzer())