import React, { useState, useEffect, useCallback } from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { useStore } from '../store';
import { fetchMarketPrices, getAssetCatalog } from './MarketFeedsData';
import { Market } from '../types';

const MarketFeeds: React.FC = () => {
  const { prices, updatePrices, setCurrentAsset, setCurrentMarket, currentAsset } = useStore();
  const [chartData, setChartData] = useState<any[]>([]);
  const [selectedMarket, setSelectedMarket] = useState<Market | 'All'>('All');
  const [timeFrame, setTimeFrame] = useState<'1H' | '1D' | '1W' | '1M'>('1D');
  
  // Function to map our symbols to TradingView symbols
  const getTradingViewSymbol = useCallback((symbol: string): string => {
    // Handle different symbol formats
    if (symbol.includes('(Maroc')) {
      // For Moroccan stocks, TradingView doesn't support Casablanca Stock Exchange directly
      // So we'll return an empty string to indicate we should use our fallback chart
      return '';
    } else if (symbol.includes('/')) {
      // For crypto pairs, format for TradingView
      return `BINANCE:${symbol.replace('/', '')}`;
    } else if (['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'NFLX', 'AMD', 'INTC', 'TSLA'].includes(symbol)) {
      // NASDAQ stocks
      return `NASDAQ:${symbol}`;
    } else {
      // For other stocks, try to use as is
      return symbol;
    }
  }, []);

  const assetCatalog = getAssetCatalog();

  // Real-time Data Feed Polling
  useEffect(() => {
    let isActive = true;

    const poll = async () => {
      const newPrices = await fetchMarketPrices();
      if (!isActive) return;
      updatePrices(newPrices);
      
      const currentPrice = newPrices[currentAsset]?.price || 0;
      setChartData(prev => [...prev.slice(-39), { 
        time: new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}), 
        price: currentPrice,
        [currentAsset]: currentPrice
      }]);
    };

    poll();
    const interval = setInterval(poll, 10000);
    
    return () => {
      isActive = false;
      clearInterval(interval);
    };
  }, [currentAsset, updatePrices]);
  
  const assetsWithPrices = assetCatalog.map((asset) => {
    const price = prices[asset.symbol] ?? {
      symbol: asset.symbol,
      price: 0,
      change: 0,
      market: asset.market
    };
    return [asset.symbol, price] as const;
  });
  
  // Filter assets by market
  const filteredAssets = selectedMarket === 'All' 
    ? assetsWithPrices
    : assetsWithPrices.filter(([_, price]) => price.market === selectedMarket);
  
  // Group assets by market for display
  const assetsByMarket: Record<string, [string, any][]> = {};
  assetsWithPrices.forEach(([symbol, price]) => {
    if (!assetsByMarket[price.market]) {
      assetsByMarket[price.market] = [];
    }
    assetsByMarket[price.market].push([symbol, price]);
  });
  
  const handleAssetSelect = (symbol: string, market: Market) => {
    setCurrentAsset(symbol);
    setCurrentMarket(market);
  };
  
  // Check if we should use TradingView or our fallback chart
  const shouldUseTradingView = getTradingViewSymbol(currentAsset) !== '';
  const tradingViewUrl = shouldUseTradingView 
    ? `https://s.tradingview.com/widgetembed/?frameElementId=tradingview_97283&symbol=${getTradingViewSymbol(currentAsset)}&interval=D&symboledit=1&saveimage=1&toolbarbg=f1f3f6&studies=RSI%40tv-basicstudies%7CMASimple%40tv-basicstudies&theme=dark&style=1&timezone=Etc%2FUTC&lang=en&utm_source=www.tradingview.com&utm_medium=widget&utm_campaign=chart&utm_term=${getTradingViewSymbol(currentAsset)}`
    : null;
  
  return (
    <div className="p-6 h-full bg-[#0b0e11] overflow-y-auto">
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-white mb-2">Market Feeds</h2>
        <p className="text-gray-500">Real-time data for NASDAQ, Casablanca Bourse, and Crypto markets</p>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Market Selection Panel */}
        <div className="lg:col-span-1 space-y-6">
          <div className="bg-[#161a1e] rounded-3xl border border-[#1e2329] p-6">
            <h3 className="text-lg font-bold text-white mb-4">Market Filters</h3>
            
            <div className="space-y-4">
              <div>
                <label className="text-[10px] font-black text-gray-500 uppercase tracking-widest block mb-2">Time Frame</label>
                <div className="grid grid-cols-4 gap-2">
                  {(['1H', '1D', '1W', '1M'] as const).map((frame) => (
                    <button
                      key={frame}
                      onClick={() => setTimeFrame(frame)}
                      className={`py-2 rounded-lg text-[10px] font-bold uppercase ${
                        timeFrame === frame 
                          ? 'bg-yellow-500 text-black' 
                          : 'bg-[#0b0e11] text-gray-500 hover:bg-[#1e2329]'
                      }`}
                    >
                      {frame}
                    </button>
                  ))}
                </div>
              </div>
              
              <div>
                <label className="text-[10px] font-black text-gray-500 uppercase tracking-widest block mb-2">Market Type</label>
                <select 
                  className="w-full bg-[#0b0e11] border border-[#1e2329] rounded-lg py-2 px-3 text-white focus:outline-none focus:ring-1 focus:ring-yellow-500"
                  value={selectedMarket}
                  onChange={(e) => setSelectedMarket(e.target.value as Market | 'All')}
                >
                  <option value="All">All Markets</option>
                  <option value="Stocks">NASDAQ Stocks</option>
                  <option value="BVC">Casablanca Bourse</option>
                  <option value="Crypto">Cryptocurrency</option>
                  <option value="Forex">Forex</option>
                </select>
              </div>
            </div>
          </div>
          
          {/* Asset List */}
          <div className="bg-[#161a1e] rounded-3xl border border-[#1e2329] p-6">
            <h3 className="text-lg font-bold text-white mb-4">Assets</h3>
            <div className="space-y-3 max-h-96 overflow-y-auto">
              {filteredAssets.map(([symbol, price]) => (
                <div 
                  key={symbol}
                  className={`p-4 rounded-xl cursor-pointer transition-all ${
                    currentAsset === symbol 
                      ? 'bg-yellow-500/20 border border-yellow-500/30' 
                      : 'bg-[#0b0e11] hover:bg-[#1e2329] border border-transparent'
                  }`}
                  onClick={() => handleAssetSelect(symbol, price.market as Market)}
                >
                  <div className="flex justify-between items-center">
                    <div>
                      <div className="font-bold text-white">{symbol}</div>
                      <div className="text-[10px] text-gray-500 uppercase">{price.market}</div>
                    </div>
                    <div className="text-right">
                      <div className="font-bold text-white">
                        ${price.price.toLocaleString(undefined, { 
                          minimumFractionDigits: price.price < 1 ? 4 : 2,
                          maximumFractionDigits: price.price < 1 ? 6 : 2
                        })}
                      </div>
                      <div className={`text-[10px] font-bold ${price.change >= 0 ? 'text-green-500' : 'text-red-500'}`}>
                        {price.change >= 0 ? '▲' : '▼'} {Math.abs(price.change).toFixed(2)}%
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
        
        {/* Chart and Details Panel */}
        <div className="lg:col-span-3 space-y-6">
          {/* Current Asset Details */}
          <div className="bg-[#161a1e] rounded-3xl border border-[#1e2329] p-8">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-8">
              <div>
                <h3 className="text-2xl font-bold text-white mb-2">{currentAsset}</h3>
                <div className="flex items-center gap-3">
                  <span className="text-[10px] font-black text-gray-500 uppercase tracking-widest">
                    {prices[currentAsset]?.market}
                  </span>
                  <span className={`text-[10px] font-black ${
                    prices[currentAsset]?.change >= 0 ? 'text-green-500' : 'text-red-500'
                  }`}>
                    {prices[currentAsset]?.change >= 0 ? '▲' : '▼'} {Math.abs(prices[currentAsset]?.change || 0).toFixed(2)}%
                  </span>
                </div>
              </div>
              <div className="text-right">
                <p className="text-3xl font-mono font-black text-white tracking-tighter">
                  ${prices[currentAsset]?.price.toLocaleString(undefined, { 
                    minimumFractionDigits: prices[currentAsset]?.price < 1 ? 4 : 2,
                    maximumFractionDigits: prices[currentAsset]?.price < 1 ? 6 : 2
                  })}
                </p>
                <p className="text-[10px] font-black text-gray-600 uppercase tracking-widest">Current Price</p>
              </div>
            </div>
            
            {/* TradingView Widget or Fallback Chart - Using iframe for supported assets, Recharts for unsupported */}
            <div className="h-[500px]">
              {shouldUseTradingView ? (
                <iframe
                  src={tradingViewUrl || ''}
                  width="100%"
                  height="100%"
                  frameBorder="0"
                  allowTransparency={true}
                  style={{ background: '#0b0e11' }}
                ></iframe>
              ) : (
                // Fallback chart for assets not supported by TradingView (like Casablanca Bourse)
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={chartData}>
                    <defs>
                      <linearGradient id="chartColor" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#eab308" stopOpacity={0.1}/>
                        <stop offset="95%" stopColor="#eab308" stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1e2329" vertical={false} />
                    <XAxis 
                      dataKey="time" 
                      axisLine={false} 
                      tickLine={false} 
                      tick={{ fill: '#6b7280', fontSize: 12 }} 
                    />
                    <YAxis 
                      domain={['auto', 'auto']} 
                      axisLine={false} 
                      tickLine={false} 
                      tick={{ fill: '#6b7280', fontSize: 12 }} 
                      tickFormatter={(value) => `$${value.toLocaleString()}`}
                    />
                    <Tooltip 
                      contentStyle={{ 
                        backgroundColor: '#161a1e', 
                        border: '1px solid #2b3139', 
                        borderRadius: '12px',
                        color: '#fff'
                      }} 
                      formatter={(value) => [`$${Number(value).toLocaleString(undefined, { minimumFractionDigits: 2 })}`, 'Price']}
                      labelFormatter={(label) => `Time: ${label}`}
                    />
                    <Area 
                      type="monotone" 
                      dataKey="price" 
                      stroke="#eab308" 
                      strokeWidth={3} 
                      fill="url(#chartColor)" 
                      animationDuration={300} 
                    />
                  </AreaChart>
                </ResponsiveContainer>
              )}
            </div>
          </div>
          
          {/* Market Overview */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {Object.entries(assetsByMarket).map(([market, assets]) => (
              <div key={market} className="bg-[#161a1e] rounded-3xl border border-[#1e2329] p-6">
                <h4 className="text-lg font-bold text-white mb-4">{market} Market</h4>
                <div className="space-y-3">
                  {assets.slice(0, 5).map(([symbol, price]) => (
                    <div key={symbol} className="flex justify-between items-center pb-3 border-b border-[#1e2329] last:border-0 last:pb-0">
                      <div>
                        <div className="font-bold text-white text-sm">{symbol}</div>
                      </div>
                      <div className="text-right">
                        <div className="font-bold text-white text-sm">
                          ${price.price.toLocaleString(undefined, { 
                            minimumFractionDigits: price.price < 1 ? 4 : 2,
                            maximumFractionDigits: price.price < 1 ? 6 : 2
                          })}
                        </div>
                        <div className={`text-[10px] font-bold ${price.change >= 0 ? 'text-green-500' : 'text-red-500'}`}>
                          {price.change >= 0 ? '+' : ''}{price.change.toFixed(2)}%
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default MarketFeeds;
