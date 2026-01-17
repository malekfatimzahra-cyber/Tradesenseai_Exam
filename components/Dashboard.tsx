
import React from 'react';
import { useStore } from '../store';
import { useTranslation } from 'react-i18next';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';

const Dashboard: React.FC = () => {
  const { t } = useTranslation();
  // Fixed: PropFirmState doesn't have a direct 'balance' property. Using activeAccount's current balance.
  const { activeAccount, tradeHistory, activeTrades } = useStore();
  const currentBalance = activeAccount?.currentBalance || 0;

  const data = [
    { name: 'Mon', pnl: 400 },
    { name: 'Tue', pnl: -200 },
    { name: 'Wed', pnl: 600 },
    { name: 'Thu', pnl: 800 },
    { name: 'Fri', pnl: -100 },
    { name: 'Sat', pnl: 1100 },
    { name: 'Sun', pnl: 400 },
  ];

  return (
    <div className="p-8 space-y-8 max-w-7xl mx-auto">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {[
          { label: t('dashboard.accountBalance'), value: `$${currentBalance.toLocaleString()}`, trend: '+12.4%', color: 'text-green-500', icon: 'fa-wallet' },
          { label: t('dashboard.totalPnl'), value: '+$4,210.00', trend: '+5.2%', color: 'text-green-500', icon: 'fa-chart-pie' },
          { label: t('dashboard.activeTrades'), value: activeTrades.length, trend: 'Neutral', color: 'text-yellow-500', icon: 'fa-exchange-alt' },
          { label: t('dashboard.winRate'), value: '68.4%', trend: '+2.1%', color: 'text-green-500', icon: 'fa-percentage' },
        ].map((stat, i) => (
          <div key={i} className="bg-[#161a1e] p-6 rounded-2xl border border-[#1e2329] shadow-lg">
            <div className="flex items-center justify-between mb-4">
              <div className="p-2 bg-yellow-500/10 rounded-xl">
                <i className={`fas ${stat.icon} text-yellow-500 text-lg`}></i>
              </div>
              <span className={`text-xs font-bold ${stat.color}`}>{stat.trend}</span>
            </div>
            <p className="text-xs text-gray-500 mb-1">{stat.label}</p>
            <p className="text-2xl font-bold text-white">{stat.value}</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Weekly Performance */}
        <div className="lg:col-span-2 bg-[#161a1e] p-6 rounded-2xl border border-[#1e2329] shadow-lg">
          <div className="flex items-center justify-between mb-8">
            <h3 className="text-lg font-bold text-white">{t('dashboard.weeklyPerformance')}</h3>
            <div className="flex gap-2">
              <button className="px-3 py-1 text-xs rounded-md bg-[#2b2f36] text-white">{t('dashboard.daily')}</button>
              <button className="px-3 py-1 text-xs rounded-md text-gray-500 hover:text-white transition-colors">{t('dashboard.weekly')}</button>
            </div>
          </div>
          <div className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data}>
                <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fill: '#474d57', fontSize: 12 }} />
                <Tooltip
                  cursor={{ fill: '#1e2329' }}
                  contentStyle={{ backgroundColor: '#161a1e', borderColor: '#2b3139', borderRadius: '8px' }}
                />
                <Bar dataKey="pnl" radius={[4, 4, 0, 0]}>
                  {data.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.pnl > 0 ? '#22c55e' : '#ef4444'} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* AI Portfolio Suggestions */}
        <div className="bg-[#161a1e] p-6 rounded-2xl border border-[#1e2329] shadow-lg">
          <h3 className="text-lg font-bold text-white mb-6">{t('dashboard.aiOptimization')}</h3>
          <div className="space-y-4">
            {[
              { type: 'Risk', msg: 'Exposure to Altcoins is high (15% above target). Diversify into Forex majors.', icon: 'fa-exclamation-triangle', color: 'text-orange-500' },
              { type: 'Profit', msg: 'Take profit reached on EUR/USD signal. Consider closing manually.', icon: 'fa-bullseye', color: 'text-green-500' },
              { type: 'Alert', msg: 'High volatility expected on Gold (XAU/USD) during NFP release.', icon: 'fa-bell', color: 'text-yellow-500' }
            ].map((rec, i) => (
              <div key={i} className="p-4 rounded-xl bg-[#0b0e11] border border-[#1e2329] flex gap-4">
                <div className={`mt-1 p-2 bg-gray-800 rounded-lg ${rec.color}`}>
                  <i className={`fas ${rec.icon} text-sm`}></i>
                </div>
                <div>
                  <p className="text-xs font-bold text-white mb-1 uppercase tracking-wider">{rec.type}</p>
                  <p className="text-xs text-gray-400 leading-relaxed">{rec.msg}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Trade History */}
      <div className="bg-[#161a1e] rounded-2xl border border-[#1e2329] overflow-hidden shadow-lg">
        <div className="p-6 border-b border-[#1e2329]">
          <h3 className="text-lg font-bold text-white">{t('dashboard.executionHistory')}</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead>
              <tr className="text-xs text-gray-500 border-b border-[#1e2329]">
                <th className="p-4">{t('dashboard.table.asset')}</th>
                <th className="p-4">{t('dashboard.table.type')}</th>
                <th className="p-4">{t('dashboard.table.entry')}</th>
                <th className="p-4">{t('dashboard.table.exit')}</th>
                <th className="p-4">{t('dashboard.table.pnl')}</th>
                <th className="p-4">{t('dashboard.table.status')}</th>
              </tr>
            </thead>
            <tbody className="text-sm">
              {tradeHistory.length === 0 ? (
                <tr>
                  <td colSpan={6} className="p-12 text-center text-gray-600">{t('dashboard.table.noTrades')}</td>
                </tr>
              ) : (
                tradeHistory.map(trade => (
                  <tr key={trade.id} className="border-b border-[#1e2329] hover:bg-[#1e2329]/50 transition-colors">
                    <td className="p-4 font-semibold text-white">{trade.asset}</td>
                    <td className={`p-4 font-bold ${trade.type === 'BUY' ? 'text-green-500' : 'text-red-500'}`}>{trade.type}</td>
                    <td className="p-4 text-gray-300 font-mono">${trade.entryPrice.toFixed(2)}</td>
                    <td className="p-4 text-gray-300 font-mono">${trade.exitPrice?.toFixed(2)}</td>
                    <td className={`p-4 font-mono font-bold ${(trade.pnl || 0) > 0 ? 'text-green-500' : 'text-red-500'}`}>
                      {(trade.pnl || 0) > 0 ? '+' : ''}${trade.pnl?.toFixed(2)}
                    </td>
                    <td className="p-4">
                      <span className="px-2 py-1 rounded-full bg-gray-800 text-gray-400 text-[10px] font-bold uppercase">{t('dashboard.table.closed')}</span>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
