import React, { useEffect, useRef, useState, useMemo } from 'react';
import { createChart, ColorType, IChartApi, ISeriesApi } from 'lightweight-charts';

interface ChartProps {
    symbol: string;
    colors?: {
        backgroundColor?: string;
        lineColor?: string;
        textColor?: string;
        areaTopColor?: string;
        areaBottomColor?: string;
    };
    marketType: 'US' | 'MA';
}

// 1. TradingView Widget Component (No hooks dependent on props that change structure)
const TradingViewWidget: React.FC<{ symbol: string }> = ({ symbol }) => {
    // Advanced Real-Time Chart Widget
    const widgetUrl = `https://s.tradingview.com/widgetembed/?frameElementId=tradingview_widget&symbol=${symbol}&interval=D&symboledit=1&saveimage=1&toolbarbg=f1f3f6&studies=RSI%40tv-basicstudies%7CMASimple%40tv-basicstudies&theme=dark&style=1&timezone=Etc%2FUTC&lang=en&utm_source=www.tradingview.com&utm_medium=widget&utm_campaign=chart&utm_term=${symbol}`;

    return (
        <div className="w-full h-full bg-[#0b0e11] rounded-2xl overflow-hidden key={symbol}">
            <iframe
                src={widgetUrl}
                className="w-full h-full border-none"
                allowTransparency={true}
                scrolling="no"
            ></iframe>
        </div>
    );
};

// 2. Lightweight Chart Component (Encapsulates all the local chart logic)
const LightweightChart: React.FC<ChartProps> = ({ symbol, colors = {}, marketType }) => {
    const apiBase = import.meta.env.VITE_API_BASE || 'https://faty2002.pythonanywhere.com';
    const chartContainerRef = useRef<HTMLDivElement>(null);
    const chartRef = useRef<IChartApi | null>(null);
    const seriesRef = useRef<ISeriesApi<"Candlestick"> | null>(null);
    const [initError, setInitError] = useState<string | null>(null);
    const [chartTitle, setChartTitle] = useState<string>(symbol);

    // Merge defaults
    const finalColors = {
        backgroundColor: 'transparent',
        lineColor: '#2962FF',
        textColor: 'rgba(150, 150, 150, 1)',
        areaTopColor: '#2962FF',
        areaBottomColor: 'rgba(41, 98, 255, 0.28)',
        ...colors
    };

    // Map symbols to human-readable names
    const getSymbolName = (sym: string) => {
        const nameMap: Record<string, string> = {
            'IAM': 'Maroc Telecom',
            'ATW': 'Attijariwafa Bank',
            'BCP': 'Banque Centrale Populaire',
            'BOA': 'Bank of Africa',
            'CMA': 'CMA CGM',
            'BTC-USD': 'Bitcoin',
            'ETH-USD': 'Ethereum',
            'AAPL': 'Apple Inc.',
            'GOOGL': 'Google',
            'TSLA': 'Tesla',
            'MSFT': 'Microsoft'
        };
        return nameMap[sym] || sym;
    };

    // Fetch historical data
    const fetchHistoricalData = async () => {
        try {
            const response = await fetch(`/api/market/history/${encodeURIComponent(symbol)}`);
            const result = await response.json();

            if (result.data && seriesRef.current) {
                // Clear existing data
                seriesRef.current.setData([]);

                // Convert to lightweight-charts format
                const formattedData = result.data.map((candle: any) => ({
                    time: candle.time,
                    open: candle.open,
                    high: candle.high,
                    low: candle.low,
                    close: candle.close
                }));

                seriesRef.current.setData(formattedData);
                console.log(`Loaded ${formattedData.length} candles for ${symbol} (${result.type})`);
            }
        } catch (err) {
            console.error('Failed to fetch historical data:', err);
            // Fallback to mock data
            if (seriesRef.current) {
                const fallbackData = generateInitialData();
                seriesRef.current.setData(fallbackData);
            }
        }
    };

    useEffect(() => {
        if (!chartContainerRef.current) return;

        const container = chartContainerRef.current;
        const width = container.clientWidth || 800;
        const height = container.clientHeight || 400;

        const handleResize = () => {
            if (chartRef.current && chartContainerRef.current) {
                chartRef.current.applyOptions({ width: chartContainerRef.current.clientWidth });
            }
        };

        try {
            const chart = createChart(container, {
                layout: {
                    background: {
                        type: ColorType.Solid,
                        color: finalColors.backgroundColor === 'transparent' ? '#0b0e11' : (finalColors.backgroundColor || '#0b0e11')
                    },
                    textColor: finalColors.textColor || 'rgba(150, 150, 150, 1)',
                },
                width: width,
                height: height,
                grid: {
                    vertLines: { color: 'rgba(42, 46, 57, 0.05)' },
                    horzLines: { color: 'rgba(42, 46, 57, 0.05)' },
                },
                timeScale: {
                    borderColor: 'rgba(197, 203, 206, 0.1)',
                    timeVisible: true,
                    secondsVisible: false,
                },
            });

            const candlestickSeries = chart.addCandlestickSeries({
                upColor: '#26a69a',
                downColor: '#ef5350',
                borderVisible: false,
                wickUpColor: '#26a69a',
                wickDownColor: '#ef5350',
            });

            chartRef.current = chart;
            seriesRef.current = candlestickSeries;

            // Update title
            setChartTitle(getSymbolName(symbol));

            // Fetch real historical data
            fetchHistoricalData();

            window.addEventListener('resize', handleResize);

            return () => {
                window.removeEventListener('resize', handleResize);
                if (chartRef.current) {
                    chartRef.current.remove();
                    chartRef.current = null;
                }
            };
        } catch (err: any) {
            console.error("Chart Init Error:", err);
            setInitError(err.message || "Renderer Initialization Error");
        }
    }, [symbol]); // Re-run when symbol changes

    // Real-time updates
    useEffect(() => {
        if (initError || !seriesRef.current) return;

        const interval = setInterval(async () => {
            const endpoint = marketType === 'MA' ? '/api/market/ma' : '/api/market/us';
            try {
                const response = await fetch(`${apiBase}${endpoint}?symbol=${encodeURIComponent(symbol)}`);
                const data = await response.json();

                if (data.price && seriesRef.current) {
                    const time = Math.floor(Date.now() / 1000) as any;
                    seriesRef.current.update({
                        time,
                        open: data.open || data.price,
                        high: data.high || data.price * 1.001,
                        low: data.low || data.price * 0.999,
                        close: data.price
                    });
                }
            } catch (e) { }
        }, 5000);

        return () => clearInterval(interval);
    }, [symbol, marketType, initError, apiBase]);

    const generateInitialData = () => {
        const data = [];
        let price = 150.0;
        const now = Math.floor(Date.now() / 1000);
        for (let i = 0; i < 100; i++) {
            const time = now - (100 - i) * 60;
            const vol = (Math.random() - 0.5) * 0.4;
            price += vol;
            data.push({
                time: time as any,
                open: price - Math.random() * 0.1,
                high: price + Math.random() * 0.1,
                low: price - Math.random() * 0.1,
                close: price
            });
        }
        return data;
    };

    if (initError) {
        return (
            <div className="w-full h-full min-h-[400px] flex flex-col items-center justify-center bg-[#0b0e11] rounded-2xl border border-red-500/30 text-red-500 p-10">
                <i className="fas fa-exclamation-circle text-3xl mb-4"></i>
                <p className="font-bold uppercase tracking-widest text-xs mb-2">Graphics Engine Failure</p>
                <p className="text-[10px] opacity-60 font-mono text-center">{initError}</p>
                <button
                    onClick={() => window.location.reload()}
                    className="mt-6 px-4 py-2 bg-red-500/10 border border-red-500/20 rounded-lg text-[9px] font-black uppercase tracking-widest hover:bg-red-500 hover:text-white transition-all"
                >
                    Refresh Terminal
                </button>
            </div>
        );
    }

    return (
        <div className="relative w-full h-full min-h-[400px]">
            {/* Dynamic Chart Title */}
            <div className="absolute top-4 left-4 z-10 pointer-events-none">
                <h3 className="text-lg font-black text-gray-400 dark:text-gray-500 uppercase tracking-wider">
                    {chartTitle}
                </h3>
                <p className="text-xs text-gray-500 dark:text-gray-600 font-bold">{symbol}</p>
            </div>
            <div ref={chartContainerRef} className="w-full h-full" />
        </div>
    );
};

// 3. Main Container Component (Decides which chart to render)
const TradingViewChart: React.FC<ChartProps> = (props) => {
    const { symbol, marketType } = props;

    // Helper to determine TradingView symbol
    const tvSymbol = useMemo(() => {
        if (marketType === 'MA') return null; // Casablanca not supported by TV Widget

        // Handle Crypto (BTC-USD -> BINANCE:BTCUSDT)
        if (symbol.includes('-USD')) {
            const coin = symbol.split('-')[0];
            return `BINANCE:${coin}USDT`;
        }

        // Handle Crypto with Slash (BTC/USD -> BINANCE:BTCUSDT)
        if (symbol.includes('/')) {
            return `BINANCE:${symbol.replace('/', '')}T`; // e.g. BTC/USD -> BTCUSDT
        }

        // Handle Forex (EURUSD=X -> FX:EURUSD)
        if (symbol.includes('=X')) {
            return `FX:${symbol.replace('=X', '')}`;
        }

        // Handle plain Crypto Tickers if passed directly (BTC -> BTCUSDT)
        if (['BTC', 'ETH', 'SOL', 'XRP'].includes(symbol)) {
            return `BINANCE:${symbol}USDT`;
        }

        // Default to NASDAQ for Stocks
        return `NASDAQ:${symbol}`;
    }, [symbol, marketType]);

    // Force re-mount when switching modes to prevent hook collisions
    if (tvSymbol) {
        return <TradingViewWidget key="tv-widget" symbol={tvSymbol} />;
    }

    return <LightweightChart key="lw-chart" {...props} />;
};

export default TradingViewChart;
