import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useStore } from '../store';
import AdminDashboard from './AdminDashboard'; // Import Admin Dashboard
import { LeaderboardEntry } from '../types';

// --- Extended Type for UI ---
interface EliteTrader extends LeaderboardEntry {
  country: string;
  consistencyScore: number;
  riskScore: number;
  fundedCapital: number;
  badges: string[]; // 'Elite', 'Sniper', 'Shark', etc.
  sparkline: number[]; // Array of last 7 days PnL %
}

// --- Personal Performance Types ---
interface PersonalStats {
  winRate: number;
  dailyDrawdown: number;
  profitFactor: number;
  avgPayout: number;
  equityCurve: number[];
}

// --- Mock Data Removed (Using Real API) ---

const Leaderboard: React.FC = () => {
  const { currentUser, activeAccount } = useStore();
  const { t } = useTranslation();
  const [leaders, setLeaders] = useState<EliteTrader[]>([]);
  const [timeframe, setTimeframe] = useState<'THIS_MONTH' | 'ALL_TIME'>('ALL_TIME');
  const [selectedTrader, setSelectedTrader] = useState<EliteTrader | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchLeaders = async () => {
      setLoading(true);
      try {
        const res = await fetch(`https://faty2002.pythonanywhere.com/api/community/leaderboard?period=${timeframe}`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
          }
        });
        if (res.ok) {
          const data = await res.json();
          // Map backend fields to frontend interface if needed
          // The backend now returns { username, country, profit, roi, winRate, fundedCapital, badges, sparkline, ... }
          // This matches EliteTrader interface closely.

          const mappedData: EliteTrader[] = data.map((item: any) => ({
            ...item,
            // Ensure defaults if missing
            badges: item.badges || [],
            sparkline: item.sparkline || [],
            riskScore: item.riskScore || 0,
            consistencyScore: item.consistencyScore || 0,
            fundedCapital: item.fundedCapital || 0
          }));

          // ELITE HALL OF FAME: Only show TOP 10 traders
          setLeaders(mappedData.slice(0, 10));
        } else {
          setLeaders([]);
        }
      } catch (e) {
        console.error("Failed to fetch leaderboard", e);
        setLeaders([]);
      } finally {
        setLoading(false);
      }
    };
    fetchLeaders();
  }, [timeframe]);

  const isPremium = currentUser?.role === 'SUPERADMIN' || (currentUser?.balance || 0) > 10000;

  return (
    <div className="min-h-full bg-gray-100 dark:bg-[#0b0e11] p-6 lg:p-10 transition-colors duration-300">
      <div className="max-w-7xl mx-auto space-y-12">

        {/* SECTION 0: Admin Dashboard (Visible Only to Admins) */}
        {/* SECTION 0: Admin Dashboard (FORCED VISIBLE FOR DEMO) */}
        <div className="mb-12 border-b border-gray-200 dark:border-gray-800 pb-12">
          <div className="bg-gradient-to-r from-yellow-500/10 to-transparent p-4 rounded-xl border border-yellow-500/20 mb-6">
            <h2 className="text-xl font-bold text-yellow-500 flex items-center gap-2">
              <i className="fas fa-shield-alt"></i> {t('leaderboard.adminControl')}
            </h2>
          </div>
          <AdminDashboard />
        </div>



        {/* SECTION 2: Global Rankings */}
        <div className="space-y-6">
          <div className="flex flex-col md:flex-row items-center justify-between gap-8 text-center md:text-left">
            <div>
              <h2 className="text-4xl lg:text-5xl font-black text-gray-900 dark:text-white uppercase tracking-tighter mb-2">
                {t('leaderboard.title')}
              </h2>
              <p className="text-gray-500 font-medium">{t('leaderboard.subtitle')}</p>
            </div>

            {/* Timeframe Toggle */}
            <div className="bg-gray-200 dark:bg-[#161a1e] p-1 rounded-xl flex items-center">
              {(['THIS_MONTH', 'ALL_TIME'] as const).map((t) => (
                <button
                  key={t}
                  onClick={() => setTimeframe(t)}
                  className={`px-4 py-2 rounded-lg text-xs font-bold uppercase tracking-wider transition-all ${timeframe === t
                    ? 'bg-white dark:bg-[#2b3139] text-gray-900 dark:text-white shadow-md'
                    : 'text-gray-500 hover:text-gray-900 dark:hover:text-gray-300'
                    }`}
                >
                  {t.replace('_', ' ')}
                </button>
              ))}
            </div>
          </div>

          {/* Empty State / Loading State */}
          {loading ? (
            <div className="w-full py-20 text-center">
              <i className="fas fa-circle-notch fa-spin text-4xl text-blue-500 mb-4"></i>
              <p className="text-gray-500 font-bold">{t('leaderboard.fetching')}</p>
            </div>
          ) : leaders.length === 0 ? (
            <div className="w-full py-20 bg-white dark:bg-[#161a1e] rounded-[2.5rem] border border-gray-200 dark:border-[#1e2329] flex flex-col items-center justify-center text-center shadow-lg">
              <div className="w-20 h-20 bg-gray-100 dark:bg-[#0b0e11] rounded-full flex items-center justify-center mb-6 text-3xl">
                <i className="fas fa-trophy text-gray-300"></i>
              </div>
              <h3 className="text-2xl font-black text-gray-900 dark:text-white mb-2">{t('leaderboard.noTraders')}</h3>
              <p className="text-gray-500 font-medium max-w-sm">{t('leaderboard.beFirst')}</p>
            </div>
          ) : (
            <>
              {/* Top 3 Podium */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 items-end">
                {leaders[1] && <PodiumCard trader={leaders[1]} rank={2} onClick={() => setSelectedTrader(leaders[1])} />}
                {leaders[0] && <PodiumCard trader={leaders[0]} rank={1} onClick={() => setSelectedTrader(leaders[0])} />}
                {leaders[2] && <PodiumCard trader={leaders[2]} rank={3} onClick={() => setSelectedTrader(leaders[2])} />}
              </div>

              {/* List Table (Rank 4+) */}
              {leaders.length > 3 && (
                <div className="bg-white dark:bg-[#161a1e] rounded-3xl border border-gray-200 dark:border-[#1e2329] overflow-hidden shadow-xl">
                  <div className="overflow-x-auto">
                    <table className="w-full text-left">
                      <thead>
                        <tr className="text-[10px] font-black text-gray-400 uppercase tracking-widest bg-gray-50 dark:bg-[#1e2329]/50 border-b border-gray-200 dark:border-[#1e2329]">
                          <th className="p-6">{t('leaderboard.table.rank')}</th>
                          <th className="p-6">{t('leaderboard.table.trader')}</th>
                          <th className="p-6">{t('leaderboard.table.country')}</th>
                          <th className="p-6 text-right">{t('leaderboard.table.funded')}</th>
                          <th className="p-6 text-right">{t('leaderboard.table.profit')}</th>
                          <th className="p-6 text-right">{t('leaderboard.table.roi')}</th>
                          <th className="p-6 text-right">{t('leaderboard.table.winRate')}</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-gray-100 dark:divide-[#1e2329] text-sm font-medium text-gray-700 dark:text-gray-300">
                        {leaders.slice(3).map((l) => (
                          <tr
                            key={l.rank}
                            onClick={() => setSelectedTrader(l)}
                            className="hover:bg-gray-50 dark:hover:bg-[#1e2329] transition-colors cursor-pointer group"
                          >
                            <td className="p-6 font-black text-gray-400 group-hover:text-yellow-500">#{l.rank}</td>
                            <td className="p-6">
                              <div className="flex items-center gap-3">
                                <img src={l.avatar} className="w-8 h-8 rounded-lg" alt="" />
                                <span className="font-bold text-gray-900 dark:text-white group-hover:text-yellow-500 transition-colors">{l.username}</span>
                                {l.badges.includes('Elite') && <i className="fas fa-check-circle text-blue-500 text-xs" title="Verified Elite"></i>}
                              </div>
                            </td>
                            <td className="p-6">
                              <img src={`https://flagcdn.com/w20/${l.country.toLowerCase()}.png`} width="20" alt={l.country} className="opacity-80" />
                            </td>
                            <td className="p-6 text-right text-gray-500 font-mono">${(l.fundedCapital / 1000)}k</td>
                            <td className="p-6 text-right font-bold text-green-500">+${l.profit.toLocaleString()}</td>
                            <td className="p-6 text-right font-mono">{l.roi}%</td>
                            <td className="p-6 text-right">
                              <div className="flex items-center justify-end gap-2">
                                <div className="w-16 h-1.5 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                                  <div className="h-full bg-blue-500" style={{ width: `${l.winRate}%` }}></div>
                                </div>
                                <span className="text-xs">{l.winRate}%</span>
                              </div>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}
            </>
          )}

        </div>

        {/* Drawer */}
        {selectedTrader && (
          <TraderDrawer
            trader={selectedTrader}
            onClose={() => setSelectedTrader(null)}
            isPremium={isPremium}
          />
        )}
      </div>
    </div>
  );
};

// --- Sub Components ---

interface StatCardProps {
  title: string;
  value: string;
  subtitle?: string;
  icon: string;
  color: 'blue' | 'red' | 'green' | 'yellow' | 'purple';
  progress?: number;
  showProgress?: boolean;
  critical?: boolean;
}

const StatCard: React.FC<StatCardProps> = ({
  title,
  value,
  subtitle,
  icon,
  color,
  progress,
  showProgress = true,
  critical = false
}) => {
  const colorClasses = {
    blue: { bg: 'bg-blue-500/10', border: 'border-blue-500/30', text: 'text-blue-500', glow: 'shadow-blue-500/20' },
    red: { bg: 'bg-red-500/10', border: 'border-red-500/30', text: 'text-red-500', glow: 'shadow-red-500/20' },
    green: { bg: 'bg-green-500/10', border: 'border-green-500/30', text: 'text-green-500', glow: 'shadow-green-500/20' },
    yellow: { bg: 'bg-yellow-500/10', border: 'border-yellow-500/30', text: 'text-yellow-500', glow: 'shadow-yellow-500/20' },
    purple: { bg: 'bg-purple-500/10', border: 'border-purple-500/30', text: 'text-purple-500', glow: 'shadow-purple-500/20' }
  };

  const classes = colorClasses[color];

  return (
    <div className={`bg-white dark:bg-[#161a1e] rounded-2xl border ${critical ? 'border-red-500/50' : 'border-gray-200 dark:border-[#1e2329]'} p-6 shadow-xl ${critical ? 'shadow-red-500/20 animate-pulse' : classes.glow} transition-all hover:-translate-y-1`}>
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xs font-black text-gray-400 uppercase tracking-wider">{title}</h3>
        <div className={`w-10 h-10 ${classes.bg} rounded-xl flex items-center justify-center`}>
          <i className={`fas ${icon} ${classes.text} text-lg`}></i>
        </div>
      </div>

      <div className="mb-2">
        <div className={`text-3xl font-black ${critical ? 'text-red-500' : 'text-gray-900 dark:text-white'} mb-1`}>
          {value}
        </div>
        {subtitle && (
          <div className="text-xs text-gray-500 font-bold">
            {subtitle}
          </div>
        )}
      </div>

      {showProgress && progress !== undefined && (
        <div>
          <div className="h-2 bg-gray-100 dark:bg-[#0b0e11] rounded-full overflow-hidden">
            <div
              className={`h-full ${critical ? 'bg-red-500' : `bg-${color}-500`} rounded-full transition-all duration-1000`}
              style={{ width: `${Math.min(progress, 100)}%` }}
            ></div>
          </div>
          {critical && (
            <p className="text-xs text-red-500 font-bold mt-2 animate-pulse">
              ⚠️ Approaching limit!
            </p>
          )}
        </div>
      )}
    </div>
  );
};

const EquityCurve: React.FC<{ data: number[] }> = ({ data }) => {
  const max = Math.max(...data);
  const min = Math.min(...data);
  const range = max - min;

  return (
    <div className="relative h-48 flex items-end justify-between gap-1">
      {data.map((value, i) => {
        const height = range > 0 ? ((value - min) / range) * 100 : 50;
        const isGain = i > 0 && value > data[i - 1];

        return (
          <div
            key={i}
            className="relative flex-1 group cursor-pointer"
            style={{ height: '100%' }}
          >
            <div
              className={`absolute bottom-0 w-full rounded-t-lg transition-all duration-300 ${isGain ? 'bg-green-500/20 border-t-2 border-green-500' : 'bg-gray-500/20 border-t-2 border-gray-500'
                } group-hover:opacity-100 opacity-80`}
              style={{ height: `${height}%` }}
            ></div>

            {/* Tooltip */}
            <div className="absolute -top-10 left-1/2 -translate-x-1/2 bg-gray-900 text-white text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-10">
              ${value.toLocaleString()}
            </div>
          </div>
        );
      })}
    </div>
  );
};

const PodiumCard = ({ trader, rank, onClick }: { trader: EliteTrader; rank: number; onClick: () => void }) => {
  const isGold = rank === 1;
  const isSilver = rank === 2;
  const isBronze = rank === 3;

  const borderColor = isGold ? 'border-yellow-500' : isSilver ? 'border-gray-300' : 'border-orange-700';
  const glowColor = isGold ? 'shadow-yellow-500/20' : isSilver ? 'shadow-gray-400/20' : 'shadow-orange-700/20';
  const medalIcon = isGold ? 'fa-medal text-yellow-500' : isSilver ? 'fa-medal text-gray-300' : 'fa-medal text-orange-700';

  return (
    <div
      onClick={onClick}
      className={`relative bg-white dark:bg-[#161a1e] rounded-[2.5rem] p-8 flex flex-col items-center text-center cursor-pointer hover:-translate-y-2 transition-transform duration-300 border-2 ${borderColor} shadow-2xl ${glowColor} ${isGold ? 'z-10 scale-105 md:scale-110' : ''}`}
    >
      <div className="absolute -top-6 w-12 h-12 bg-white dark:bg-[#161a1e] rounded-full border-2 border-inherit flex items-center justify-center text-2xl shadow-lg">
        <i className={`fas ${rank === 1 ? 'fa-crown text-yellow-500' : medalIcon}`}></i>
      </div>

      <div className="mt-4 mb-4 relative">
        <div className={`w-24 h-24 rounded-3xl p-1 bg-gradient-to-br ${isGold ? 'from-yellow-400 to-yellow-600' : isSilver ? 'from-gray-300 to-gray-500' : 'from-orange-600 to-orange-800'}`}>
          <img src={trader.avatar} alt={trader.username} className="w-full h-full rounded-[1.3rem] object-cover bg-black" />
        </div>
        <div className="absolute -bottom-2 -right-2 bg-white dark:bg-[#2b3139] p-1.5 rounded-lg shadow-sm border border-gray-100 dark:border-black">
          <img src={`https://flagcdn.com/w20/${trader.country.toLowerCase()}.png`} width="20" alt={trader.country} />
        </div>
      </div>

      <h3 className="text-xl font-black text-gray-900 dark:text-white mb-1">{trader.username}</h3>
      <div className="flex gap-1 mb-6">
        {trader.badges.map(b => (
          <span key={b} className="px-1.5 py-0.5 bg-gray-100 dark:bg-[#2b3139] rounded text-[10px] font-bold text-gray-500 uppercase">{b}</span>
        ))}
      </div>

      <div className="w-full space-y-4">
        <div className="flex justify-between items-center text-sm border-b border-gray-100 dark:border-[#2b3139] pb-3">
          <span className="text-gray-400 font-bold uppercase text-xs">Total Profit</span>
          <span className="font-black text-green-500 text-lg">+${trader.profit.toLocaleString()}</span>
        </div>
        <div className="flex justify-between items-center text-sm text-gray-600 dark:text-gray-400">
          <span>ROI</span>
          <span className="font-bold">{trader.roi}%</span>
        </div>
        <div className="flex justify-between items-center text-sm text-gray-600 dark:text-gray-400">
          <span>Performance</span>
          <div className="h-4 w-16 bg-gray-50 dark:bg-[#0b0e11] rounded flex items-end justify-between px-0.5 overflow-hidden">
            {trader.sparkline.map((v, i) => (
              <div key={i} className={`w-1 rounded-t ${v > 5 ? 'bg-green-500' : 'bg-gray-400'}`} style={{ height: `${v * 10}%` }}></div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

const TraderDrawer = ({ trader, onClose, isPremium }: { trader: EliteTrader; onClose: () => void; isPremium: boolean }) => {
  return (
    <div className="fixed inset-0 z-50 flex justify-end">
      <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" onClick={onClose}></div>
      <div className="relative w-full max-w-md bg-white dark:bg-[#161a1e] h-full shadow-2xl border-l border-gray-200 dark:border-[#2b3139] animate-in slide-in-from-right duration-300 flex flex-col">

        {/* Header */}
        <div className="p-8 border-b border-gray-100 dark:border-[#1e2329] bg-gray-50 dark:bg-[#1e2329]/50 relative">
          <button onClick={onClose} className="absolute top-6 left-6 text-gray-400 hover:text-gray-900 dark:hover:text-white">
            <i className="fas fa-times text-xl"></i>
          </button>
          <div className="flex flex-col items-center mt-4">
            <img src={trader.avatar} className="w-20 h-20 rounded-2xl shadow-lg mb-4" alt="" />
            <h2 className="text-2xl font-black text-gray-900 dark:text-white">{trader.username}</h2>
            <div className="flex items-center gap-2 mt-2">
              <span className="px-2 py-1 bg-yellow-500/10 text-yellow-600 font-bold text-xs uppercase rounded-lg border border-yellow-500/20">Rank #{trader.rank}</span>
              <span className="px-2 py-1 bg-gray-100 dark:bg-[#2b3139] text-gray-500 font-bold text-xs uppercase rounded-lg">{trader.country}</span>
            </div>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="flex-1 overflow-y-auto p-8 space-y-8">

          <div className="grid grid-cols-2 gap-4">
            <div className="p-4 bg-gray-50 dark:bg-[#0b0e11] rounded-2xl border border-gray-100 dark:border-[#2b3139]">
              <div className="text-xs text-gray-400 font-bold uppercase mb-1">{t('leaderboard.drawer.totalPayouts')}</div>
              <div className="text-xl font-black text-green-500">${trader.profit.toLocaleString()}</div>
            </div>
            <div className="p-4 bg-gray-50 dark:bg-[#0b0e11] rounded-2xl border border-gray-100 dark:border-[#2b3139]">
              <div className="text-xs text-gray-400 font-bold uppercase mb-1">{t('leaderboard.drawer.fundedCap')}</div>
              <div className="text-xl font-black text-gray-900 dark:text-white">${trader.fundedCapital.toLocaleString()}</div>
            </div>
          </div>

          {/* Locked Section for Non-Premium */}
          {!isPremium ? (
            <div className="p-8 border border-yellow-500/30 bg-yellow-500/5 rounded-3xl text-center space-y-4">
              <div className="w-12 h-12 bg-yellow-500/20 rounded-full flex items-center justify-center mx-auto text-yellow-500 text-xl">
                <i className="fas fa-lock"></i>
              </div>
              <div>
                <h4 className="font-bold text-gray-900 dark:text-white">{t('leaderboard.drawer.locked')}</h4>
                <p className="text-xs text-gray-500 mt-1">{t('leaderboard.drawer.lockedDesc')}</p>
              </div>
              <button className="w-full py-3 bg-yellow-500 text-black font-bold uppercase text-xs rounded-xl hover:bg-yellow-400 transition-colors">
                {t('leaderboard.drawer.unlock')}
              </button>
            </div>
          ) : (
            <div className="space-y-6">
              {/* Advanced Stats */}
              <div>
                <h4 className="text-sm font-black text-gray-900 dark:text-white uppercase mb-4">{t('leaderboard.drawer.audit')}</h4>
                <div className="space-y-4">
                  <div>
                    <div className="flex justify-between text-xs mb-1">
                      <span className="text-gray-500 font-bold">{t('leaderboard.drawer.consistency')}</span>
                      <span className="text-gray-900 dark:text-white font-bold">{trader.consistencyScore}/100</span>
                    </div>
                    <div className="h-2 bg-gray-100 dark:bg-[#2b3139] rounded-full overflow-hidden">
                      <div className="h-full bg-purple-500 rounded-full" style={{ width: `${trader.consistencyScore}%` }}></div>
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between text-xs mb-1">
                      <span className="text-gray-500 font-bold">{t('leaderboard.drawer.riskMgmt')}</span>
                      <span className="text-gray-900 dark:text-white font-bold">{trader.riskScore}/10</span>
                    </div>
                    <div className="h-2 bg-gray-100 dark:bg-[#2b3139] rounded-full overflow-hidden">
                      <div className="h-full bg-blue-500 rounded-full" style={{ width: `${trader.riskScore * 10}%` }}></div>
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between text-xs mb-1">
                      <span className="text-gray-500 font-bold">{t('leaderboard.table.winRate')}</span>
                      <span className="text-gray-900 dark:text-white font-bold">{trader.winRate}%</span>
                    </div>
                    <div className="h-2 bg-gray-100 dark:bg-[#2b3139] rounded-full overflow-hidden">
                      <div className="h-full bg-green-500 rounded-full" style={{ width: `${trader.winRate}%` }}></div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Recent Activity Mock */}
              <div>
                <h4 className="text-sm font-black text-gray-900 dark:text-white uppercase mb-4">{t('leaderboard.drawer.latestTrades')}</h4>
                <div className="space-y-3">
                  {[1, 2, 3].map(i => (
                    <div key={i} className="flex items-center justify-between p-3 rounded-xl bg-gray-50 dark:bg-[#0b0e11] border border-gray-100 dark:border-[#2b3139]">
                      <div className="flex items-center gap-3">
                        <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded ${i === 2 ? 'bg-red-500/10 text-red-500' : 'bg-green-500/10 text-green-500'}`}>
                          {i === 2 ? 'SELL' : 'BUY'}
                        </span>
                        <span className="text-xs font-bold text-gray-700 dark:text-gray-300">XAUUSD</span>
                      </div>
                      <span className={`text-xs font-black ${i === 2 ? 'text-red-500' : 'text-green-500'}`}>
                        {i === 2 ? '-$450' : '+$1,250'}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Leaderboard;
