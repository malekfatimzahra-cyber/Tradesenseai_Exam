import React, { useState, useEffect, useMemo } from 'react';
import { useStore } from '../store';
import { useTranslation } from 'react-i18next';
import { usePreferencesStore } from '../preferencesStore';
import TradingViewChart from './TradingViewChart';
import AITradingAssistant from './AITradingAssistant';
import { fetchMarketPrices, getAssetCatalog, getAssetBySymbol } from './MarketFeedsData';

// --- Sub-Components ---

const StatWidget = ({ label, value, color = "text-gray-900 dark:text-white", subValue, icon }: any) => (
  <div className="flex items-center gap-3 px-4 py-2 bg-gray-100 border border-gray-200 rounded-xl backdrop-blur-sm dark:bg-white/5 dark:border-white/10">
    <div className={`p-2 rounded-lg bg-white/5 text-gray-400 ${icon ? '' : 'hidden'}`}>
      <i className={`fas ${icon}`}></i>
    </div>
    <div>
      <p className="text-[9px] font-black text-gray-500 uppercase tracking-widest leading-none mb-1">{label}</p>
      <div className="flex items-baseline gap-2">
        <p className={`text-sm font-mono font-black ${color}`}>{value}</p>
        {subValue && <p className="text-[9px] text-gray-500 font-bold">{subValue}</p>}
      </div>
    </div>
  </div>
);

// Circular Risk Gauge Component
const CircularRiskGauge = ({ level, score }: { level: string, score: number }) => {
  const radius = 45;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (score / 100) * circumference;

  const colorMap = {
    SAFE: '#22c55e',
    WARNING: '#f59e0b',
    DANGER: '#ef4444'
  };

  const color = colorMap[level as keyof typeof colorMap] || colorMap.SAFE;

  return (
    <div className="relative w-32 h-32 mx-auto">
      <svg className="transform -rotate-90 w-32 h-32">
        <circle
          cx="64"
          cy="64"
          r={radius}
          stroke="rgba(255,255,255,0.05)"
          strokeWidth="8"
          fill="none"
        />
        <circle
          cx="64"
          cy="64"
          r={radius}
          stroke={color}
          strokeWidth="8"
          fill="none"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          className="transition-all duration-1000"
          style={{ filter: `drop-shadow(0 0 8px ${color})` }}
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="text-2xl font-black text-gray-900 dark:text-white">{score}%</span>
        <span className={`text-[9px] font-black uppercase tracking-widest`} style={{ color }}>{level}</span>
      </div>
    </div>
  );
};

const Terminal: React.FC = () => {
  const { currentAsset, currentMarket, setCurrentAsset, setCurrentMarket, openTrade, activeTrades, closeTrade, activeAccount, prices, updatePrices, aiSignals, riskAlerts, riskLevel, equityShield, fetchAiSignals, fetchRiskCheck, tradeHistory, validateTrade } = useStore();
  const { theme } = usePreferencesStore();
  const isDark = theme === 'dark' || (theme === 'system' && typeof window !== 'undefined' && window.matchMedia('(prefers-color-scheme: dark)').matches);
  const { t } = useTranslation();

  // Mode & Tabs
  const [expertMode, setExpertMode] = useState(true);
  const [activeTab, setActiveTab] = useState<'positions' | 'journal' | 'analytics'>('positions');
  const [leverage, setLeverage] = useState(1);

  // Order State
  const [orderAmount, setOrderAmount] = useState(1000);
  const [stopLoss, setStopLoss] = useState<number | ''>('');
  const [takeProfit, setTakeProfit] = useState<number | ''>('');
  const [loadingOrder, setLoadingOrder] = useState<string | null>(null);

  // Journal State
  const [journalNote, setJournalNote] = useState('');
  const [journalEntries, setJournalEntries] = useState<{ id: string, date: string, text: string, sentiment: string }[]>([]);

  // AI State
  const [aiContext, setAiContext] = useState<string | null>(null);
  const [loadingAi, setLoadingAi] = useState(false);

  // Derived Values
  const assetCatalog = getAssetCatalog();
  const assetInfo = getAssetBySymbol(currentAsset);
  const currentPrice = prices[currentAsset]?.price || 0;
  const currentChange = prices[currentAsset]?.change || 0;

  // Mock Equity with default
  const mockEquity = activeAccount?.equity || 0;

  // Real-time PnL
  const activePnL = useMemo(() => {
    return activeTrades.reduce((acc, t) => {
      const price = prices[t.asset]?.price || t.entryPrice;
      const pnl = t.type === 'BUY'
        ? (price - t.entryPrice) * (t.amount / t.entryPrice)
        : (t.entryPrice - price) * (t.amount / t.entryPrice);
      return acc + pnl;
    }, 0);
  }, [activeTrades, prices]);

  // Discipline Score Mock
  const disciplineScore = useMemo(() => {
    let score = 0;
    if (activePnL < -500) score -= 5;
    if (activeTrades.length > 3) score -= 10;
    return Math.max(0, score);
  }, [activePnL, activeTrades]);

  // Effects
  useEffect(() => {
    const fetchData = async () => {
      const newPrices = await fetchMarketPrices();
      updatePrices(newPrices);
      fetchRiskCheck();
    };
    const interval = setInterval(fetchData, 5000);
    fetchData();
    fetchAiSignals(currentAsset);
    return () => clearInterval(interval);
  }, [currentAsset]);

  // Handlers
  const handleSmartSize = () => {
    if (!activeAccount || !stopLoss || typeof stopLoss !== 'number') return alert("Enter a Stop Loss first for Smart Sizing.");

    const riskAmount = activeAccount.equity * 0.01;
    const distance = Math.abs(currentPrice - stopLoss);

    if (distance === 0) return alert("Stop Loss cannot be same as Entry.");

    const optimalAmount = (riskAmount / distance) * currentPrice;
    setOrderAmount(Math.floor(optimalAmount));
  };

  const handleExplainMove = async () => {
    setLoadingAi(true);
    const explanation = await useStore.getState().explainPriceAction(currentAsset, currentPrice, currentChange);
    setAiContext(explanation);
    setLoadingAi(false);
  };

  const handleTrade = async (type: 'BUY' | 'SELL') => {
    if (!activeAccount) return;
    setLoadingOrder(type);

    const validation = await validateTrade({
      asset: currentAsset,
      type,
      amount: orderAmount * leverage,
      entry: currentPrice
    });

    if (validation.status === 'BLOCKED') {
      alert(`Request Denied by Risk Desk: ${validation.message}`);
      setLoadingOrder(null);
      return;
    }

    if (validation.status === 'WARNING') {
      const proceed = window.confirm(`Risk Warning: ${validation.message}\n\nProceed anyway? (This will be logged)`);
      if (!proceed) {
        setLoadingOrder(null);
        return;
      }
    }

    await new Promise(r => setTimeout(r, 600));

    openTrade({
      id: `TRD-${Date.now()}`,
      asset: currentAsset,
      type,
      entryPrice: currentPrice,
      amount: orderAmount * leverage,
      sl: stopLoss === '' ? undefined : stopLoss,
      tp: takeProfit === '' ? undefined : takeProfit,
      status: 'OPEN',
      timestamp: new Date().toISOString(),
      market: currentMarket
    });
    setLoadingOrder(null);
  };

  const handleJournalAdd = () => {
    if (!journalNote.trim()) return;
    setJournalEntries([{
      id: Date.now().toString(),
      date: new Date().toLocaleTimeString(),
      text: journalNote,
      sentiment: activePnL > 0 ? 'Confident' : 'Anxious'
    }, ...journalEntries]);
    setJournalNote('');
  };

  return (
    <div className="flex flex-col h-full bg-gray-50 dark:bg-[#050505] font-sans selection:bg-blue-500 selection:text-white overflow-hidden">

      {/* Elite Header */}
      <header className="h-16 px-6 border-b border-gray-200 dark:border-white/5 bg-white dark:bg-black/40 backdrop-blur-xl flex items-center justify-between shrink-0 z-20 shadow-sm dark:shadow-none">
        <div className="flex items-center gap-6">
          <div className="relative group">
            <select
              value={currentAsset}
              onChange={e => setCurrentAsset(e.target.value)}
              className="appearance-none bg-white dark:bg-white/5 text-gray-900 dark:text-white font-black text-2xl px-4 py-2 pr-10 rounded-xl border border-gray-200 dark:border-white/10 focus:outline-none focus:ring-2 focus:ring-blue-500 cursor-pointer hover:border-blue-500/50 transition-all uppercase tracking-wider backdrop-blur-sm"
            >
              {assetCatalog.map(a => <option key={a.symbol} value={a.symbol} className="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">{a.symbol}</option>)}
            </select>
            <i className="fas fa-chevron-down absolute right-4 top-1/2 -translate-y-1/2 text-gray-500 pointer-events-none"></i>
          </div>

          <div className="flex flex-col">
            <span className={`text-3xl font-mono font-black tracking-tighter ${currentChange >= 0 ? 'text-green-500' : 'text-red-500'}`} style={{ textShadow: currentChange >= 0 ? '0 0 20px rgba(34,197,94,0.3)' : '0 0 20px rgba(239,68,68,0.3)' }}>
              ${currentPrice.toLocaleString(undefined, { minimumFractionDigits: 2 })}
            </span>
            <span className="text-[10px] font-bold text-gray-500 uppercase tracking-widest">{activeTrades.length} Active Positions</span>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <div className="hidden lg:flex gap-3">
            <StatWidget label={t('terminal.dayPnL')} value={`${activePnL >= 0 ? '+' : ''}${activePnL.toFixed(2)} MAD`} color={activePnL >= 0 ? 'text-green-500' : 'text-red-500'} icon="fa-chart-pie" />
            <StatWidget label={t('terminal.accountEquity')} value={`${mockEquity.toLocaleString('fr-MA', { minimumFractionDigits: 2 })} MAD`} icon="fa-wallet" />
            <StatWidget label={t('terminal.discipline')} value={`${disciplineScore}/100`} color={disciplineScore > 90 ? 'text-blue-400' : 'text-yellow-500'} icon="fa-brain" />
          </div>

          <div className="h-8 w-[1px] bg-gray-200 dark:bg-white/10"></div>

          <button
            onClick={() => setExpertMode(!expertMode)}
            className={`flex items-center gap-2 px-3 py-1.5 rounded-lg border text-[10px] font-black uppercase tracking-widest transition-all ${expertMode ? 'bg-purple-500/10 border-purple-500/30 text-purple-400 shadow-[0_0_15px_-5px_rgba(168,85,247,0.4)]' : 'bg-gray-100 border-gray-200 text-gray-600 dark:bg-white/5 dark:border-white/10 dark:text-gray-500'}`}
          >
            <i className={`fas ${expertMode ? 'fa-toggle-on' : 'fa-toggle-off'}`}></i>
            {expertMode ? t('terminal.proMode') : t('terminal.liteMode')}
          </button>
        </div>
      </header>

      {/* Main Grid Layout */}
      <div className="flex-1 flex overflow-hidden">

        {/* LEFT: Chart & Blotter */}
        <div className="flex-1 flex flex-col min-w-0">
          {/* Chart */}
          <div className="flex-1 bg-white dark:bg-[#0a0a0a] relative border-r border-gray-200 dark:border-white/5">
            <TradingViewChart
              symbol={assetInfo?.apiSymbol || currentAsset}
              marketType={assetInfo?.apiMarket === 'MA' ? 'MA' : 'US'}
              colors={{ backgroundColor: isDark ? '#0a0a0a' : '#ffffff', lineColor: '#3b82f6', textColor: isDark ? '#6b7280' : '#4b5563', areaTopColor: isDark ? 'rgba(59, 130, 246, 0.2)' : 'rgba(59, 130, 246, 0.15)', areaBottomColor: isDark ? 'rgba(59, 130, 246, 0.0)' : 'rgba(59, 130, 246, 0.0)' }}
            />

            {/* In-Chart AI Overlay */}
            <div className="absolute top-4 left-4 flex flex-col gap-2 z-10 pointer-events-none">
              {aiSignals[0] && (
                <div className="bg-white/80 text-gray-900 backdrop-blur-md border border-blue-500/30 p-3 rounded-xl animate-in slide-in-from-left duration-500 shadow-[0_0_20px_-5px_rgba(59,130,246,0.3)] dark:bg-black/60 dark:text-white">
                  <div className="flex items-center gap-2 mb-1">
                    <div className={`w-2 h-2 rounded-full ${aiSignals[0].type === 'BUY' ? 'bg-green-500' : 'bg-red-500'} animate-pulse`}></div>
                    <span className="text-[10px] font-black text-gray-900 uppercase tracking-widest dark:text-white">{t('terminal.aiBias')}: {aiSignals[0].type}</span>
                  </div>
                  <div className="text-[9px] text-gray-400 max-w-[200px] leading-tight opacity-80">{aiSignals[0].reasoning}</div>
                </div>
              )}
              {riskLevel !== 'SAFE' && (
                <div className="bg-red-500/10 backdrop-blur-md border border-red-500/30 p-3 rounded-xl animate-pulse">
                  <div className="flex items-center gap-2">
                    <i className="fas fa-exclamation-triangle text-red-500 text-xs"></i>
                    <span className="text-[10px] font-black text-red-500 uppercase tracking-widest">{t('terminal.volatilityWarning')}</span>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Bottom Blotter Panel */}
          <div className="h-72 bg-white dark:bg-black/40 backdrop-blur-md border-t border-gray-200 dark:border-white/5 flex flex-col shrink-0">
            {/* Tabs */}
            <div className="flex border-b border-gray-200 bg-gray-100 dark:border-white/5 dark:bg-black/20">
              {[
                { id: 'positions', icon: 'fa-list-ul', label: `Positions (${activeTrades.length})` },
                { id: 'journal', icon: 'fa-book-medical', label: 'Trading Journal' },
                { id: 'analytics', icon: 'fa-chart-area', label: 'Post-Trade Analysis' }
              ].map(tab => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={`px-6 py-3 flex items-center gap-2 text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === tab.id ? 'bg-white text-blue-600 border-t-2 border-t-blue-500 shadow-[0_-5px_20px_-5px_rgba(59,130,246,0.3)] dark:bg-black/40 dark:text-blue-500' : 'text-gray-600 hover:text-gray-900 dark:text-gray-500 dark:hover:text-white'}`}
                >
                  <i className={`fas ${tab.icon}`}></i> {t(`terminal.tabs.${tab.id}`)}
                </button>
              ))}
            </div>

            {/* Tab Content */}
            <div className="flex-1 overflow-y-auto p-4 custom-scrollbar">
              {activeTab === 'positions' && (
                <table className="w-full text-left border-collapse">
                  <thead className="text-[10px] font-black text-gray-600 uppercase tracking-widest sticky top-0 bg-gray-100 backdrop-blur-sm dark:bg-black/40">
                    <tr>
                      <th className="pb-4">{t('terminal.table.ticker')}</th>
                      <th className="pb-4">{t('terminal.table.type')}</th>
                      <th className="pb-4">{t('terminal.table.size')}</th>
                      <th className="pb-4">{t('terminal.table.entry')}</th>
                      <th className="pb-4">{t('terminal.table.current')}</th>
                      <th className="pb-4">{t('terminal.table.pnl')}</th>
                      <th className="pb-4 text-right">{t('terminal.table.actions')}</th>
                    </tr>
                  </thead>
                  <tbody className="text-xs font-mono font-medium text-gray-700 dark:text-gray-300">
                    {activeTrades.map(t => {
                      const pnl = (prices[t.asset]?.price || t.entryPrice) - t.entryPrice;
                      const totalPnl = t.type === 'BUY' ? pnl * (t.amount / t.entryPrice) : -pnl * (t.amount / t.entryPrice);
                      return (
                        <tr key={t.id} className="border-b border-gray-200 hover:bg-gray-100 group transition-colors dark:border-white/5 dark:hover:bg-white/5">
                          <td className="py-3 font-bold text-gray-900 dark:text-white">{t.asset}</td>
                          <td className={`py-3 font-black ${t.type === 'BUY' ? 'text-green-500' : 'text-red-500'}`}>{t.type}</td>
                          <td className="py-3 ">{t.amount.toLocaleString()} MAD</td>
                          <td className="py-3 ">{t.entryPrice.toFixed(2)}</td>
                          <td className="py-3 ">{prices[t.asset]?.price?.toFixed(2)}</td>
                          <td className={`py-3 font-bold ${totalPnl >= 0 ? 'text-green-500' : 'text-red-500'}`}>{totalPnl >= 0 ? '+' : ''}{totalPnl.toFixed(2)}</td>
                          <td className="py-3 text-right">
                            <button onClick={() => closeTrade(t.id, prices[t.asset]?.price)} className="px-3 py-1 bg-red-500/10 text-red-500 rounded hover:bg-red-500 hover:text-white transition-all text-[9px] font-black uppercase border border-red-500/20">Close</button>
                          </td>
                        </tr>
                      )
                    })}
                  </tbody>
                </table>
              )}
              {activeTab === 'journal' && (
                <div className="flex h-full gap-4">
                  <div className="w-1/3 flex flex-col gap-2">
                    <textarea
                      value={journalNote}
                      onChange={(e) => setJournalNote(e.target.value)}
                      placeholder="Log your thoughts, emotions, and thesis..."
                      className="flex-1 bg-gray-50 border border-gray-200 rounded-xl p-4 text-xs text-gray-900 focus:outline-none focus:border-blue-500 resize-none placeholder:text-gray-500 backdrop-blur-sm dark:bg-white/5 dark:border-white/10 dark:text-white dark:placeholder:text-gray-600"
                    ></textarea>
                    <button
                      onClick={handleJournalAdd}
                      className="px-4 py-2 bg-blue-600 text-white rounded-lg text-[10px] font-black uppercase tracking-widest hover:bg-blue-500 transition-colors shadow-[0_0_15px_-5px_rgba(59,130,246,0.5)]"
                    >
                      {t('terminal.journal.save')}
                    </button>
                  </div>
                  <div className="flex-1 flex flex-col gap-2 overflow-y-auto">
                    {journalEntries.length === 0 && <p className="text-gray-600 text-center italic text-xs mt-10">No entries yet. Discipline starts here.</p>}
                    {journalEntries.map(e => (
                      <div key={e.id} className="p-3 bg-white rounded-xl border border-gray-200 backdrop-blur-sm dark:bg-white/5 dark:border-white/10">
                        <div className="flex justify-between mb-1">
                          <span className="text-[10px] font-bold text-gray-500">{e.date}</span>
                          <span className="text-[10px] font-black text-blue-400 uppercase">{e.sentiment}</span>
                        </div>
                        <p className="text-xs text-gray-700 dark:text-gray-300">{e.text}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
              {activeTab === 'analytics' && (
                <div className="flex items-center justify-center h-full text-center">
                  <div className="space-y-2">
                    <i className="fas fa-chart-line text-4xl text-gray-700"></i>
                    <h3 className="text-gray-500 font-bold uppercase tracking-widest text-xs">Analytics Module Active</h3>
                    <p className="text-gray-600 text-[10px]">Processing trade history for behavioral patterns...</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* CENTER: Trading Execution Panel */}
        <aside className="w-[380px] shrink-0 border-l border-gray-200 dark:border-white/5 bg-white dark:bg-black/40 backdrop-blur-xl flex flex-col z-20 shadow-lg dark:shadow-2xl">

          {/* Order Ticket */}
          <div className="flex-1 p-6 flex flex-col gap-5 overflow-y-auto custom-scrollbar">
            <div>
              <h2 className="text-[10px] font-black text-gray-500 uppercase tracking-widest mb-4 flex justify-between items-center">
                Execution
                <button
                  onClick={handleSmartSize}
                  className="text-[9px] text-indigo-600 hover:text-indigo-700 transition-colors flex items-center gap-1 bg-indigo-500/10 px-2 py-1 rounded border border-indigo-500/20 dark:text-indigo-400 dark:hover:text-white" title="Calculate optimal size based on 1% Risk & SL"
                >
                  <i className="fas fa-wand-magic-sparkles"></i> {t('terminal.smartSize')}
                </button>
              </h2>

              <div className="space-y-4">
                {/* Amount with Neon Focus */}
                <div className="relative group">
                  <label className="text-[9px] font-bold text-gray-600 uppercase absolute -top-2 left-2 bg-white/90 dark:bg-black/80 px-1 z-10">Amount (MAD)</label>
                  <input
                    type="number"
                    value={orderAmount}
                    onChange={e => setOrderAmount(Number(e.target.value))}
                    className="w-full bg-gray-50 border border-gray-200 rounded-xl py-4 px-4 text-gray-900 font-mono font-bold focus:outline-none focus:border-blue-500 focus:shadow-[0_0_20px_-5px_rgba(59,130,246,0.5)] transition-all backdrop-blur-sm dark:bg-white/5 dark:border-white/10 dark:text-white"
                  />
                </div>

                {/* Leverage Slider */}
                {expertMode && (
                  <div className="relative">
                    <label className="text-[9px] font-bold text-gray-600 uppercase mb-2 block">Leverage: {leverage}x</label>
                    <input
                      type="range"
                      min="1"
                      max="10"
                      value={leverage}
                      onChange={e => setLeverage(Number(e.target.value))}
                      className="w-full h-2 bg-gradient-to-r from-green-500 via-yellow-500 to-red-500 rounded-full appearance-none cursor-pointer slider-thumb"
                      style={{
                        background: `linear-gradient(to right, #22c55e 0%, #eab308 50%, #ef4444 100%)`
                      }}
                    />
                    <div className="flex justify-between text-[8px] text-gray-600 mt-1">
                      <span>1x</span>
                      <span>5x</span>
                      <span>10x</span>
                    </div>
                  </div>
                )}

                {/* Smart Stops with Neon Borders */}
                {expertMode && (
                  <div className="grid grid-cols-2 gap-3">
                    <div className="relative group">
                      <label className="text-[9px] font-bold text-red-500/80 uppercase absolute -top-2 left-2 bg-white/90 dark:bg-black/80 px-1 z-10">SL</label>
                      <input
                        type="number" step="0.01" value={stopLoss} onChange={e => setStopLoss(e.target.value === '' ? '' : Number(e.target.value))}
                        className="w-full bg-gray-50 border border-red-200 rounded-xl py-3 px-3 text-red-600 font-mono text-sm font-bold focus:outline-none focus:border-red-500 focus:shadow-[0_0_20px_-5px_rgba(239,68,68,0.5)] transition-all backdrop-blur-sm dark:bg-white/5 dark:border-red-500/20 dark:text-red-500"
                      />
                      {aiSignals[0] && <button onClick={() => setStopLoss(aiSignals[0].sl)} className="absolute right-2 top-2 text-[8px] bg-gray-100 px-1.5 py-0.5 rounded text-gray-600 hover:text-gray-900 hover:bg-gray-200 transition-all uppercase font-black tracking-wider border border-gray-200 dark:bg-white/10 dark:text-gray-500 dark:hover:text-white dark:hover:bg-gray-700 dark:border-white/10">AI Set</button>}
                    </div>
                    <div className="relative group">
                      <label className="text-[9px] font-bold text-green-500/80 uppercase absolute -top-2 left-2 bg-white/90 dark:bg-black/80 px-1 z-10">TP</label>
                      <input
                        type="number" step="0.01" value={takeProfit} onChange={e => setTakeProfit(e.target.value === '' ? '' : Number(e.target.value))}
                        className="w-full bg-gray-50 border border-green-200 rounded-xl py-3 px-3 text-green-600 font-mono text-sm font-bold focus:outline-none focus:border-green-500 focus:shadow-[0_0_20px_-5px_rgba(34,197,94,0.5)] transition-all backdrop-blur-sm dark:bg-white/5 dark:border-green-500/20 dark:text-green-500"
                      />
                      {aiSignals[0] && <button onClick={() => setTakeProfit(aiSignals[0].tp)} className="absolute right-2 top-2 text-[8px] bg-gray-100 px-1.5 py-0.5 rounded text-gray-600 hover:text-gray-900 hover:bg-gray-200 transition-all uppercase font-black tracking-wider border border-gray-200 dark:bg-white/10 dark:text-gray-500 dark:hover:text-white dark:hover:bg-gray-700 dark:border-white/10">AI Set</button>}
                    </div>
                  </div>
                )}

                {/* Full-Width Glow Buttons */}
                <div className="grid grid-cols-2 gap-3 mt-4">
                  <button
                    onClick={() => handleTrade('BUY')}
                    disabled={!!loadingOrder}
                    className="relative group overflow-hidden py-5 rounded-xl bg-gradient-to-br from-green-600 to-green-500 text-white font-black text-sm uppercase tracking-widest shadow-[0_0_30px_-5px_rgba(34,197,94,0.5)] hover:shadow-[0_0_40px_-5px_rgba(34,197,94,0.8)] hover:scale-[1.02] active:scale-[0.98] transition-all disabled:opacity-50 border border-green-400/20"
                  >
                    {loadingOrder === 'BUY' ? <i className="fas fa-spinner animate-spin"></i> : t('terminal.long')}
                    <div className="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300"></div>
                  </button>
                  <button
                    onClick={() => handleTrade('SELL')}
                    disabled={!!loadingOrder}
                    className="relative group overflow-hidden py-5 rounded-xl bg-gradient-to-br from-red-600 to-red-500 text-white font-black text-sm uppercase tracking-widest shadow-[0_0_30px_-5px_rgba(239,68,68,0.5)] hover:shadow-[0_0_40px_-5px_rgba(239,68,68,0.8)] hover:scale-[1.02] active:scale-[0.98] transition-all disabled:opacity-50 border border-red-400/20"
                  >
                    {loadingOrder === 'SELL' ? <i className="fas fa-spinner animate-spin"></i> : t('terminal.short')}
                    <div className="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300"></div>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </aside>

        {/* RIGHT: AI Trading Assistant Panel */}
        <aside className="w-[380px] shrink-0">
          <AITradingAssistant symbol={currentAsset} />
        </aside>

      </div>
    </div>
  );
};

export default Terminal;
