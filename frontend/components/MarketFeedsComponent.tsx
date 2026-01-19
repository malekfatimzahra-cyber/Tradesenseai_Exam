import React, { useState, useEffect, useCallback } from 'react';
import { useStore } from '../store';
import { fetchMarketPrices, getAssetCatalog, getAssetBySymbol } from './MarketFeedsData';
import { Market } from '../types';
import TradingViewChart from './TradingViewChart';
import { usePreferencesStore } from '../preferencesStore';

const MarketFeeds: React.FC = () => {
  const { prices, updatePrices, setCurrentAsset, setCurrentMarket, currentAsset } = useStore();
  const { theme } = usePreferencesStore();
  const [selectedMarket, setSelectedMarket] = useState<Market | 'All'>('All');
  const [timeFrame, setTimeFrame] = useState<'1H' | '1D' | '1W' | '1M'>('1D');
  const isDark = theme === 'dark' || (theme === 'system' && typeof window !== 'undefined' && window.matchMedia('(prefers-color-scheme: dark)').matches);

  // Function to map our symbols to TradingView symbols
  const getTradingViewSymbol = useCallback((symbol: string): string => {
    // Handle different symbol formats
    if (symbol.includes('(Maroc')) {
      // For Moroccan stocks, TradingView doesn't support Casablanca Stock Exchange directly
      // So we'll return an empty string to indicate we should use our fallback chart
      return '';
    } else if (symbol.includes('/') && !symbol.includes('USD')) {
      // For Forex pairs like EUR/USD, format for TradingView
      const pair = symbol.replace('/', '');
      return `FX_IDC:${pair}`;
    } else if (symbol.includes('/USD')) {
      // For crypto pairs, format for TradingView (Binance)
      return `BINANCE:${symbol.replace('/', '')}`;
    } else if (['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'NFLX', 'AMD', 'INTC', 'TSLA',
      'PYPL', 'UBER', 'ABNB', 'COIN', 'SQ', 'SHOP'].includes(symbol)) {
      // NASDAQ stocks
      return `NASDAQ:${symbol}`;
    } else {
      // For Casablanca Bourse and unsupported assets, use fallback
      return '';
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
    };

    poll();
    const interval = setInterval(poll, 10000);

    return () => {
      isActive = false;
      clearInterval(interval);
    };
  }, [updatePrices]);

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

  // Map timeframe to TradingView interval format
  const getInterval = (tf: string) => {
    switch (tf) {
      case '1H': return '60';
      case '1D': return 'D';
      case '1W': return 'W';
      case '1M': return 'M';
      default: return 'D';
    }
  };

  const tradingViewUrl = shouldUseTradingView
    ? `https://s.tradingview.com/widgetembed/?frameElementId=tradingview_97283&symbol=${getTradingViewSymbol(currentAsset)}&interval=${getInterval(timeFrame)}&hideideas=1&hidesidetoolbar=0&symboledit=1&saveimage=1&toolbarbg=${isDark ? '0b0e11' : 'f3f4f6'}&studies=RSI@tv-basicstudies|MACD@tv-basicstudies|BB@tv-basicstudies&theme=${isDark ? 'dark' : 'light'}&style=1&timezone=Etc%2FUTC&withdateranges=1&locale=en&utm_source=tradesenseai&utm_medium=widget&utm_campaign=chart&utm_term=${getTradingViewSymbol(currentAsset)}`
    : null;

  return (
    <div className="p-6 h-full bg-gray-100 text-gray-900 dark:bg-[#0b0e11] dark:text-white overflow-y-auto">
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">Market Feeds</h2>
        <p className="text-gray-600 dark:text-gray-500">Real-time data for NASDAQ, Forex, Crypto, and Casablanca Bourse markets</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Market Selection Panel */}
        <div className="lg:col-span-1 space-y-6">
          <div className="bg-white rounded-3xl border border-gray-200 p-6 dark:bg-[#161a1e] dark:border-[#1e2329]">
            <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4">Market Filters</h3>

            <div className="space-y-4">
              <div>
                <label className="text-[10px] font-black text-gray-500 uppercase tracking-widest block mb-2">Time Frame</label>
                <div className="grid grid-cols-4 gap-2">
                  {(['1H', '1D', '1W', '1M'] as const).map((frame) => (
                    <button
                      key={frame}
                      onClick={() => setTimeFrame(frame)}
                      className={`py-2 rounded-lg text-[10px] font-bold uppercase ${timeFrame === frame
                        ? 'bg-yellow-500 text-black'
                        : 'bg-gray-100 text-gray-600 hover:bg-gray-200 dark:bg-[#0b0e11] dark:text-gray-500 dark:hover:bg-[#1e2329]'
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
                  className="w-full bg-gray-50 border border-gray-200 rounded-lg py-2 px-3 text-gray-900 focus:outline-none focus:ring-1 focus:ring-yellow-500 dark:bg-[#0b0e11] dark:border-[#1e2329] dark:text-white"
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
          <div className="bg-white rounded-3xl border border-gray-200 p-6 dark:bg-[#161a1e] dark:border-[#1e2329]">
            <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4">Assets</h3>
            <div className="space-y-3 max-h-96 overflow-y-auto">
              {filteredAssets.map(([symbol, price]) => (
                <div
                  key={symbol}
                  className={`p-4 rounded-xl cursor-pointer transition-all ${currentAsset === symbol
                    ? 'bg-yellow-500/20 border border-yellow-500/30'
                    : 'bg-gray-50 hover:bg-gray-100 border border-transparent dark:bg-[#0b0e11] dark:hover:bg-[#1e2329]'
                    }`}
                  onClick={() => handleAssetSelect(symbol, price.market as Market)}
                >
                  <div className="flex justify-between items-center">
                    <div>
                      <div className="font-bold text-gray-900 dark:text-white">{symbol}</div>
                      <div className="text-[10px] text-gray-500 uppercase">{price.market}</div>
                    </div>
                    <div className="text-right">
                      <div className="font-bold text-gray-900 dark:text-white">
                        ${(price.price ?? 0).toLocaleString(undefined, {
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
          <div className="bg-white rounded-3xl border border-gray-200 p-8 dark:bg-[#161a1e] dark:border-[#1e2329]">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-8">
              <div>
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">{currentAsset}</h3>
                <div className="flex items-center gap-3">
                  <span className="text-[10px] font-black text-gray-500 uppercase tracking-widest">
                    {prices[currentAsset]?.market || 'Market'}
                  </span>
                  <span className={`text-[10px] font-black ${(prices[currentAsset]?.change || 0) >= 0 ? 'text-green-500' : 'text-red-500'
                    }`}>
                    {(prices[currentAsset]?.change || 0) >= 0 ? '▲' : '▼'} {Math.abs(prices[currentAsset]?.change || 0).toFixed(2)}%
                  </span>
                </div>
              </div>
              <div className="text-right">
                <p className="text-3xl font-mono font-black text-gray-900 dark:text-white tracking-tighter">
                  ${(prices[currentAsset]?.price ?? 0).toLocaleString(undefined, {
                    minimumFractionDigits: (prices[currentAsset]?.price || 0) < 1 ? 4 : 2,
                    maximumFractionDigits: (prices[currentAsset]?.price || 0) < 1 ? 6 : 2
                  })}
                </p>
                <p className="text-[10px] font-black text-gray-600 uppercase tracking-widest">Current Price</p>
              </div>
            </div>

            {/* TradingView Widget or Fallback Chart */}
            <div className="h-[500px]">
              {shouldUseTradingView ? (
                <iframe
                  src={tradingViewUrl || ''}
                  width="100%"
                  height="100%"
                  frameBorder="0"
                  allowTransparency={true}
                  style={{ background: isDark ? '#0b0e11' : '#ffffff' }}
                ></iframe>
              ) : (
                <TradingViewChart
                  symbol={getAssetBySymbol(currentAsset)?.apiSymbol || currentAsset}
                  marketType={getAssetBySymbol(currentAsset)?.apiMarket === 'MA' ? 'MA' : 'US'}
                  colors={{
                    backgroundColor: 'transparent',
                    lineColor: '#eab308',
                    textColor: isDark ? 'rgba(200, 200, 200, 1)' : 'rgba(55, 65, 81, 1)',
                    areaTopColor: isDark ? 'rgba(234, 179, 8, 0.4)' : 'rgba(234, 179, 8, 0.3)',
                    areaBottomColor: isDark ? 'rgba(234, 179, 8, 0.05)' : 'rgba(234, 179, 8, 0.02)',
                  }}
                />
              )}
            </div>
          </div>

          {/* Market Overview */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {Object.entries(assetsByMarket).map(([market, assets]) => (
              <div key={market} className="bg-white rounded-3xl border border-gray-200 p-6 dark:bg-[#161a1e] dark:border-[#1e2329]">
                <h4 className="text-lg font-bold text-gray-900 dark:text-white mb-4">{market} Market</h4>
                <div className="space-y-3">
                  {assets.slice(0, 5).map(([symbol, price]) => (
                    <div key={symbol} className="flex justify-between items-center pb-3 border-b border-gray-200 dark:border-[#1e2329] last:border-0 last:pb-0">
                      <div>
                        <div className="font-bold text-gray-900 dark:text-white text-sm">{symbol}</div>
                      </div>
                      <div className="text-right">
                        <div className="font-bold text-gray-900 dark:text-white text-sm">
                          ${(price.price ?? 0).toLocaleString(undefined, {
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
