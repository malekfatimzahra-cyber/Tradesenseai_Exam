
import { AssetPrice, Market } from '../types';

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:5000';

type ApiMarket = 'US' | 'MA';

export interface AssetCatalogItem {
  symbol: string;
  market: Market;
  apiSymbol: string;
  apiMarket: ApiMarket;
}

const ASSET_CATALOG: AssetCatalogItem[] = [
  { symbol: 'AAPL', market: 'Stocks', apiSymbol: 'AAPL', apiMarket: 'US' },
  { symbol: 'TSLA', market: 'Stocks', apiSymbol: 'TSLA', apiMarket: 'US' },
  { symbol: 'MSFT', market: 'Stocks', apiSymbol: 'MSFT', apiMarket: 'US' },
  { symbol: 'GOOGL', market: 'Stocks', apiSymbol: 'GOOGL', apiMarket: 'US' },
  { symbol: 'BTC/USD', market: 'Crypto', apiSymbol: 'BTC-USD', apiMarket: 'US' },
  { symbol: 'ETH/USD', market: 'Crypto', apiSymbol: 'ETH-USD', apiMarket: 'US' },
  { symbol: 'EUR/USD', market: 'Forex', apiSymbol: 'EURUSD=X', apiMarket: 'US' },
  { symbol: 'USD/JPY', market: 'Forex', apiSymbol: 'USDJPY=X', apiMarket: 'US' },
  { symbol: 'IAM (Maroc Telecom)', market: 'BVC', apiSymbol: 'IAM', apiMarket: 'MA' },
  { symbol: 'ATW (Attijariwafa)', market: 'BVC', apiSymbol: 'ATW', apiMarket: 'MA' }
];

const lastPrices: Record<string, number> = {};

export const getAssetCatalog = (): AssetCatalogItem[] => ASSET_CATALOG;

export const getAssetBySymbol = (symbol: string): AssetCatalogItem | undefined =>
  ASSET_CATALOG.find((asset) => asset.symbol === symbol);

const buildPrice = (asset: AssetCatalogItem, price: number, change?: number): AssetPrice => {
  const previous = lastPrices[asset.symbol];
  const safePrice = Number(price);
  const computedChange = typeof change === 'number'
    ? change
    : previous
      ? ((safePrice - previous) / previous) * 100
      : 0;

  lastPrices[asset.symbol] = safePrice;

  return {
    symbol: asset.symbol,
    price: safePrice,
    change: computedChange,
    market: asset.market
  };
};

export const fetchMarketPrices = async (symbols?: string[]): Promise<Record<string, AssetPrice>> => {
  const assets = symbols && symbols.length > 0
    ? ASSET_CATALOG.filter((asset) => symbols.includes(asset.symbol))
    : ASSET_CATALOG;

  const updates: Record<string, AssetPrice> = {};

  const responses = await Promise.all(assets.map(async (asset) => {
    const endpoint = asset.apiMarket === 'MA' ? '/api/market/ma' : '/api/market/us';
    const url = `${API_BASE}${endpoint}?symbol=${encodeURIComponent(asset.apiSymbol)}`;

    try {
      const res = await fetch(url);
      if (!res.ok) {
        throw new Error(`Market fetch failed: ${res.status}`);
      }
      const data = await res.json();
      if (typeof data.price !== 'number') {
        throw new Error('Invalid price payload');
      }
      return [asset.symbol, buildPrice(asset, data.price, data.change)] as const;
    } catch (error) {
      const fallback = lastPrices[asset.symbol];
      if (typeof fallback === 'number') {
        return [asset.symbol, buildPrice(asset, fallback, 0)] as const;
      }
      return null;
    }
  }));

  responses.forEach((entry) => {
    if (!entry) return;
    updates[entry[0]] = entry[1];
  });

  return updates;
};
