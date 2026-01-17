import React, { useEffect, useState } from 'react';

type AIAnalysis = {
    symbol: string;
    signal: 'BUY' | 'SELL' | 'HOLD';
    confidence: number;
    entry_price: number;
    stop_loss: number;
    take_profit: number;
    risk_level: 'Low' | 'Medium' | 'High';
    ai_comment: string;
    timestamp: string;
};

type Props = {
    /** Symbol the chart is currently showing (e.g. "BTCUSD") */
    symbol: string;
};

export default function AITradingAssistant({ symbol }: Props) {
    const [analysis, setAnalysis] = useState<AIAnalysis | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    // Fetch AI analysis from backend
    const fetchAnalysis = async () => {
        setLoading(true);
        setError(null);

        try {
            // Remove slashes from symbol (Flask doesn't handle encoded slashes well in routes)
            const cleanSymbol = symbol.replace(/\//g, '');
            // console.log('Fetching AI analysis for symbol:', symbol, 'cleaned:', cleanSymbol);

            const response = await fetch(`/api/ai-analysis/${cleanSymbol}`);

            // console.log('AI Analysis response status:', response.status);

            if (!response.ok) {
                const errorText = await response.text();
                console.error('AI Analysis error response:', errorText);
                throw new Error(`API Error: ${response.status}`);
            }

            const data: AIAnalysis = await response.json();
            // console.log('AI Analysis data received:', data);
            setAnalysis(data);
        } catch (err) {
            console.error('Failed to fetch AI analysis:', err);
            setError('AI analysis unavailable. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    // Auto-fetch on mount and when symbol changes
    useEffect(() => {
        fetchAnalysis();
    }, [symbol]);

    // Signal color mapping
    const getSignalColor = (signal: string) => {
        switch (signal) {
            case 'BUY':
                return {
                    bg: 'bg-green-500/20',
                    border: 'border-green-500/40',
                    text: 'text-green-400',
                    glow: 'shadow-[0_0_30px_-5px_rgba(34,197,94,0.4)]',
                    icon: 'fa-arrow-trend-up'
                };
            case 'SELL':
                return {
                    bg: 'bg-red-500/20',
                    border: 'border-red-500/40',
                    text: 'text-red-400',
                    glow: 'shadow-[0_0_30px_-5px_rgba(239,68,68,0.4)]',
                    icon: 'fa-arrow-trend-down'
                };
            default:
                return {
                    bg: 'bg-gray-500/20',
                    border: 'border-gray-500/40',
                    text: 'text-gray-400',
                    glow: 'shadow-[0_0_20px_-5px_rgba(156,163,175,0.3)]',
                    icon: 'fa-shield-halved'
                };
        }
    };

    // Risk level color and width
    const getRiskData = (level: string) => {
        switch (level) {
            case 'Low':
                return { color: 'bg-green-500', width: '33%', glow: 'shadow-[0_0_15px_rgba(34,197,94,0.5)]' };
            case 'Medium':
                return { color: 'bg-yellow-500', width: '66%', glow: 'shadow-[0_0_15px_rgba(234,179,8,0.5)]' };
            case 'High':
                return { color: 'bg-red-500', width: '100%', glow: 'shadow-[0_0_15px_rgba(239,68,68,0.5)]' };
            default:
                return { color: 'bg-gray-500', width: '50%', glow: '' };
        }
    };

    return (
        <div className="w-full h-full bg-gradient-to-br from-gray-900/95 via-black/95 to-gray-900/95 backdrop-blur-xl border-l border-white/10 flex flex-col">
            {/* Header */}
            <div className="px-6 py-4 border-b border-white/10 bg-gradient-to-r from-blue-500/10 to-purple-500/10">
                <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center shadow-[0_0_20px_-5px_rgba(59,130,246,0.6)]">
                            <i className="fas fa-robot text-white text-lg"></i>
                        </div>
                        <div>
                            <h2 className="text-sm font-black text-white uppercase tracking-wider">AI Trading Assistant</h2>
                            <p className="text-[10px] text-gray-400 font-bold">Real-Time Analysis Engine</p>
                        </div>
                    </div>
                    <button
                        onClick={fetchAnalysis}
                        disabled={loading}
                        className="p-2 rounded-lg bg-white/5 border border-white/10 hover:bg-white/10 hover:border-blue-500/30 transition-all disabled:opacity-50 disabled:cursor-not-allowed group"
                        title="Refresh Analysis"
                    >
                        <i className={`fas fa-sync-alt text-gray-400 group-hover:text-blue-400 transition-all ${loading ? 'fa-spin' : ''}`}></i>
                    </button>
                </div>
            </div>

            {/* Content */}
            <div className="flex-1 overflow-y-auto p-6 space-y-6 custom-scrollbar">
                {/* Loading State */}
                {loading && !analysis && (
                    <div className="flex flex-col items-center justify-center h-64 space-y-4">
                        <i className="fas fa-circle-notch fa-spin text-4xl text-blue-500"></i>
                        <p className="text-sm font-bold text-gray-400 uppercase tracking-widest">AI is analyzing {symbol}...</p>
                    </div>
                )}

                {/* Error State */}
                {error && (
                    <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/30 flex items-start gap-3">
                        <i className="fas fa-exclamation-triangle text-red-500 mt-1"></i>
                        <div>
                            <p className="text-sm font-bold text-red-400">Analysis Error</p>
                            <p className="text-xs text-gray-400 mt-1">{error}</p>
                        </div>
                    </div>
                )}

                {/* Analysis Display */}
                {analysis && !loading && (
                    <>
                        {/* Signal Badge */}
                        <div className={`p-6 rounded-2xl border ${getSignalColor(analysis.signal).bg} ${getSignalColor(analysis.signal).border} ${getSignalColor(analysis.signal).glow} backdrop-blur-md`}>
                            <div className="flex items-center justify-between mb-4">
                                <span className="text-[10px] font-black text-gray-500 uppercase tracking-widest">Signal</span>
                                <div className="flex items-center gap-2">
                                    <div className={`w-2 h-2 rounded-full ${analysis.signal === 'BUY' ? 'bg-green-500' : analysis.signal === 'SELL' ? 'bg-red-500' : 'bg-gray-500'} animate-pulse`}></div>
                                    <span className="text-[10px] font-bold text-gray-400">LIVE</span>
                                </div>
                            </div>

                            <div className="flex items-center justify-between">
                                <div className="flex items-center gap-4">
                                    <i className={`fas ${getSignalColor(analysis.signal).icon} text-4xl ${getSignalColor(analysis.signal).text}`}></i>
                                    <div>
                                        <h3 className={`text-4xl font-black ${getSignalColor(analysis.signal).text} uppercase tracking-tight`}>
                                            {analysis.signal}
                                        </h3>
                                        <p className="text-xs text-gray-400 font-bold mt-1">
                                            {analysis.confidence}% Confidence
                                        </p>
                                    </div>
                                </div>
                            </div>

                            {/* Confidence Bar */}
                            <div className="mt-4">
                                <div className="h-2 bg-black/40 rounded-full overflow-hidden">
                                    <div
                                        className={`h-full ${getSignalColor(analysis.signal).bg} ${getSignalColor(analysis.signal).glow} transition-all duration-1000 rounded-full`}
                                        style={{ width: `${analysis.confidence}%` }}
                                    ></div>
                                </div>
                            </div>
                        </div>

                        {/* AI Comment */}
                        <div className="p-4 rounded-xl bg-blue-500/5 border border-blue-500/20 backdrop-blur-sm">
                            <div className="flex items-start gap-3">
                                <div className="w-8 h-8 rounded-lg bg-blue-500/20 flex items-center justify-center flex-shrink-0">
                                    <i className="fas fa-microchip text-blue-400"></i>
                                </div>
                                <div>
                                    <p className="text-[10px] font-black text-blue-400 uppercase tracking-widest mb-1">AI Analysis</p>
                                    <p className="text-sm text-gray-300 leading-relaxed">{analysis.ai_comment}</p>
                                </div>
                            </div>
                        </div>

                        {/* Risk Radar */}
                        <div className="p-5 rounded-xl bg-white/5 border border-white/10 backdrop-blur-sm">
                            <div className="flex items-center gap-2 mb-4">
                                <i className="fas fa-radiation text-yellow-500"></i>
                                <h3 className="text-[10px] font-black text-gray-500 uppercase tracking-widest">Risk Radar</h3>
                            </div>

                            <div className="space-y-3">
                                <div className="flex justify-between items-baseline">
                                    <span className="text-xs font-bold text-gray-400">Risk Level</span>
                                    <span className={`text-lg font-black uppercase tracking-wide ${analysis.risk_level === 'Low' ? 'text-green-400' :
                                        analysis.risk_level === 'Medium' ? 'text-yellow-400' :
                                            'text-red-400'
                                        }`}>
                                        {analysis.risk_level}
                                    </span>
                                </div>

                                <div className="relative h-3 bg-black/40 rounded-full overflow-hidden">
                                    <div
                                        className={`h-full ${getRiskData(analysis.risk_level).color} ${getRiskData(analysis.risk_level).glow} transition-all duration-1000 rounded-full`}
                                        style={{ width: getRiskData(analysis.risk_level).width }}
                                    ></div>
                                </div>
                            </div>
                        </div>

                        {/* Trade Plan */}
                        <div className="p-5 rounded-xl bg-gradient-to-br from-purple-500/10 to-blue-500/10 border border-purple-500/20 backdrop-blur-sm">
                            <div className="flex items-center gap-2 mb-4">
                                <i className="fas fa-crosshairs text-purple-400"></i>
                                <h3 className="text-[10px] font-black text-purple-400 uppercase tracking-widest">Trade Plan</h3>
                            </div>

                            <div className="space-y-3">
                                {/* Entry Price */}
                                <div className="flex items-center justify-between p-3 bg-white/5 rounded-lg border border-white/10">
                                    <span className="text-[10px] font-bold text-gray-500 uppercase tracking-wide">Entry Price</span>
                                    <span className="text-lg font-mono font-black text-white">${analysis.entry_price.toFixed(2)}</span>
                                </div>

                                {/* Stop Loss */}
                                <div className="flex items-center justify-between p-3 bg-red-500/10 rounded-lg border border-red-500/20">
                                    <span className="text-[10px] font-bold text-red-500/80 uppercase tracking-wide">Stop Loss</span>
                                    <span className="text-lg font-mono font-black text-red-400">${analysis.stop_loss.toFixed(2)}</span>
                                </div>

                                {/* Take Profit */}
                                <div className="flex items-center justify-between p-3 bg-green-500/10 rounded-lg border border-green-500/20">
                                    <span className="text-[10px] font-bold text-green-500/80 uppercase tracking-wide">Take Profit</span>
                                    <span className="text-lg font-mono font-black text-green-400">${analysis.take_profit.toFixed(2)}</span>
                                </div>
                            </div>
                        </div>

                        {/* Risk/Reward Ratio */}
                        <div className="p-4 rounded-xl bg-white/5 border border-white/10 backdrop-blur-sm">
                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <p className="text-[9px] font-black text-gray-500 uppercase tracking-widest mb-1">Risk</p>
                                    <p className="text-sm font-mono font-bold text-red-400">
                                        {Math.abs(analysis.entry_price - analysis.stop_loss).toFixed(2)}
                                    </p>
                                </div>
                                <div>
                                    <p className="text-[9px] font-black text-gray-500 uppercase tracking-widest mb-1">Reward</p>
                                    <p className="text-sm font-mono font-bold text-green-400">
                                        {Math.abs(analysis.take_profit - analysis.entry_price).toFixed(2)}
                                    </p>
                                </div>
                            </div>
                            <div className="mt-3 pt-3 border-t border-white/10">
                                <div className="flex items-baseline justify-between">
                                    <span className="text-[9px] font-black text-gray-500 uppercase tracking-widest">R:R Ratio</span>
                                    <span className="text-lg font-black text-blue-400">
                                        1:{(Math.abs(analysis.take_profit - analysis.entry_price) / Math.abs(analysis.entry_price - analysis.stop_loss)).toFixed(2)}
                                    </span>
                                </div>
                            </div>
                        </div>

                        {/* Disclaimer */}
                        <div className="p-3 rounded-lg bg-yellow-500/5 border border-yellow-500/20">
                            <p className="text-[9px] text-yellow-500/80 text-center leading-relaxed">
                                ⚠️ This is a simulated AI analysis for educational purposes. Always perform your own research before trading.
                            </p>
                        </div>
                    </>
                )}
            </div>
        </div>
    );
}
