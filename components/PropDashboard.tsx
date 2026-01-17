import React, { useState } from 'react';
import { useStore } from '../store';
import { useTranslation } from 'react-i18next';
import { evaluatePropTrader } from '../geminiService';
import { AIPropEvaluation } from '../types';

const PropDashboard: React.FC = () => {
  const { activeAccount, plans, violations, tradeHistory, startChallenge, resetAccount } = useStore();
  const { t } = useTranslation();
  const [evaluation, setEvaluation] = useState<AIPropEvaluation | null>(null);
  const [isEvaluating, setIsEvaluating] = useState(false);

  const plan = plans.find(p => p.id === activeAccount?.planId);

  const handleEvaluate = async () => {
    if (!activeAccount || tradeHistory.length === 0) return;
    setIsEvaluating(true);
    try {
      const result = await evaluatePropTrader(tradeHistory, activeAccount);
      setEvaluation(result);
    } finally {
      setIsEvaluating(false);
    }
  };

  if (!activeAccount) {
    return (
      <div className="p-12 max-w-6xl mx-auto space-y-12">
        <div className="text-center space-y-4">
          <h2 className="text-4xl font-extrabold text-gray-900 dark:text-white tracking-tight">{t('dashboard.title')}</h2>
          <p className="text-gray-500 text-lg max-w-2xl mx-auto">{t('dashboard.subtitle')}</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {plans.map(p => (
            <div key={p.id} className="bg-white dark:bg-[#161a1e] border border-gray-200 dark:border-[#1e2329] rounded-3xl p-8 flex flex-col hover:border-yellow-500/50 transition-all group shadow-xl dark:shadow-none">
              <div className="mb-6">
                <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">{p.name}</h3>
                <div className="text-3xl font-bold text-yellow-600 dark:text-yellow-500">${p.capital.toLocaleString()} <span className="text-sm font-normal text-gray-500">{t('dashboard.funded')}</span></div>
              </div>
              <ul className="space-y-4 mb-8 flex-1">
                <li className="flex justify-between text-sm"><span className="text-gray-500">{t('dashboard.profitTarget')}</span> <span className="text-green-600 dark:text-green-500 font-bold">${p.profitTarget.toLocaleString()}</span></li>
                <li className="flex justify-between text-sm"><span className="text-gray-500">{t('dashboard.dailyLoss')}</span> <span className="text-red-600 dark:text-red-500 font-bold">${p.dailyLossLimit.toLocaleString()}</span></li>
                <li className="flex justify-between text-sm"><span className="text-gray-500">{t('dashboard.maxDrawdown')}</span> <span className="text-red-600 dark:text-red-500 font-bold">${p.maxDrawdown.toLocaleString()}</span></li>
                <li className="flex justify-between text-sm"><span className="text-gray-500">{t('dashboard.leverage')}</span> <span className="text-gray-900 dark:text-white font-bold">1:100</span></li>
              </ul>
              <button
                onClick={() => startChallenge(p.id)}
                className="w-full py-4 bg-yellow-500 text-black font-extrabold rounded-2xl hover:bg-yellow-400 transition-all shadow-lg shadow-yellow-500/10"
              >
                {t('dashboard.buyChallenge')} (${p.price})
              </button>
            </div>
          ))}
        </div>
      </div>
    );
  }

  const profitProgress = Math.min(((activeAccount.currentBalance - activeAccount.initialBalance) / (plan?.profitTarget || 1)) * 100, 100);
  const drawdownUsed = Math.min(((activeAccount.initialBalance - activeAccount.equity) / (plan?.maxDrawdown || 1)) * 100, 100);

  return (
    <div className="p-8 space-y-8 bg-gray-100 dark:bg-[#0b0e11] min-h-full transition-colors duration-300">
      {/* Account Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 bg-white dark:bg-[#161a1e] p-8 rounded-3xl border border-gray-200 dark:border-[#1e2329] shadow-sm transition-all duration-300">
        <div className="space-y-2">
          <div className="flex items-center gap-3">
            <span className={`px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-widest ${activeAccount.status === 'FAILED' ? 'bg-red-500/20 text-red-600 dark:text-red-500' :
                activeAccount.status === 'FUNDED' ? 'bg-green-500/20 text-green-600 dark:text-green-500' : 'bg-yellow-500/20 text-yellow-600 dark:text-yellow-500'
              }`}>
              {activeAccount.status} {t('dashboard.phase')}
            </span>
            <span className="text-gray-500 text-xs font-mono">ID: {activeAccount.id}</span>
          </div>
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white transition-colors">${activeAccount.currentBalance.toLocaleString(undefined, { minimumFractionDigits: 2 })}</h2>
          <p className="text-gray-500 text-sm">{t('dashboard.accountBalance')} ({t('dashboard.institutionalSimulation')})</p>
        </div>
        <div className="flex gap-4">
          <button onClick={resetAccount} className="px-6 py-3 rounded-xl bg-gray-100 dark:bg-[#1e2329] text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-all border border-gray-200 dark:border-transparent">{t('dashboard.newChallenge')}</button>
          <button className="px-6 py-3 rounded-xl bg-yellow-500 text-black font-bold hover:bg-yellow-400 transition-all shadow-md">{t('dashboard.withdrawPayout')}</button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Risk Indicators */}
        <div className="lg:col-span-2 space-y-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white dark:bg-[#161a1e] p-6 rounded-3xl border border-gray-200 dark:border-[#1e2329] shadow-sm transition-all duration-300">
              <div className="flex justify-between items-center mb-4">
                <h4 className="text-sm font-bold text-gray-500 uppercase">{t('dashboard.profitTarget')}</h4>
                <span className="text-xs font-bold text-green-600 dark:text-green-500">${activeAccount.currentBalance - activeAccount.initialBalance} / ${plan?.profitTarget}</span>
              </div>
              <div className="h-4 bg-gray-100 dark:bg-[#0b0e11] rounded-full overflow-hidden border border-gray-200 dark:border-[#1e2329]">
                <div className="h-full bg-green-500 transition-all duration-1000" style={{ width: `${Math.max(0, profitProgress)}%` }}></div>
              </div>
            </div>
            <div className="bg-white dark:bg-[#161a1e] p-6 rounded-3xl border border-gray-200 dark:border-[#1e2329] shadow-sm transition-all duration-300">
              <div className="flex justify-between items-center mb-4">
                <h4 className="text-sm font-bold text-gray-500 uppercase">{t('dashboard.totalDrawdown')}</h4>
                <span className="text-xs font-bold text-red-600 dark:text-red-500">{drawdownUsed.toFixed(1)}% {t('dashboard.used')}</span>
              </div>
              <div className="h-4 bg-gray-100 dark:bg-[#0b0e11] rounded-full overflow-hidden border border-gray-200 dark:border-[#1e2329]">
                <div className="h-full bg-red-500 transition-all duration-1000" style={{ width: `${drawdownUsed}%` }}></div>
              </div>
            </div>
          </div>

          {/* Trade List */}
          <div className="bg-white dark:bg-[#161a1e] rounded-3xl border border-gray-200 dark:border-[#1e2329] overflow-hidden shadow-sm transition-all duration-300">
            <div className="p-6 border-b border-gray-200 dark:border-[#1e2329] flex justify-between items-center">
              <h3 className="font-bold text-gray-900 dark:text-white uppercase tracking-wider text-sm">{t('dashboard.evaluationHistory')}</h3>
              <button onClick={handleEvaluate} disabled={isEvaluating} className="text-xs font-bold text-yellow-600 dark:text-yellow-500 hover:underline">
                {isEvaluating ? t('dashboard.aiAnalyzing') : t('dashboard.generateReport')}
              </button>
            </div>
            <table className="w-full text-left">
              <thead>
                <tr className="text-[10px] text-gray-500 border-b border-gray-200 dark:border-[#1e2329]">
                  <th className="p-6">{t('dashboard.date')}</th>
                  <th className="p-6">{t('dashboard.asset')}</th>
                  <th className="p-6">{t('dashboard.type')}</th>
                  <th className="p-6 text-right">{t('dashboard.pnl')}</th>
                </tr>
              </thead>
              <tbody className="text-sm">
                {tradeHistory.map(t => (
                  <tr key={t.id} className="border-b border-gray-200 dark:border-[#1e2329] hover:bg-gray-50 dark:hover:bg-[#1e2329]/50 transition-colors">
                    <td className="p-6 text-gray-500">{new Date(t.timestamp).toLocaleDateString()}</td>
                    <td className="p-6 font-bold text-gray-900 dark:text-white">{t.asset}</td>
                    <td className={`p-6 font-bold ${t.type === 'BUY' ? 'text-green-600 dark:text-green-500' : 'text-red-600 dark:text-red-500'}`}>{t.type}</td>
                    <td className={`p-6 text-right font-mono font-bold ${t.pnl! > 0 ? 'text-green-600 dark:text-green-500' : 'text-red-600 dark:text-red-500'}`}>
                      {t.pnl! > 0 ? '+' : ''}${t.pnl?.toFixed(2)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Sidebar: AI Coach & Rule Breaches */}
        <div className="space-y-8">
          <div className="bg-white dark:bg-[#161a1e] p-6 rounded-3xl border border-gray-200 dark:border-[#1e2329] space-y-6 shadow-sm transition-all duration-300">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-yellow-500/10 rounded-xl">
                <i className="fas fa-user-shield text-yellow-600 dark:text-yellow-500"></i>
              </div>
              <h4 className="font-bold text-gray-900 dark:text-white">{t('dashboard.aiCoach')}</h4>
            </div>
            {evaluation ? (
              <div className="space-y-4 animate-in fade-in slide-in-from-bottom-2 duration-500">
                <div className="flex items-center justify-between">
                  <span className="text-xs text-gray-500 uppercase">{t('dashboard.grade')}</span>
                  <span className="text-2xl font-black text-yellow-600 dark:text-yellow-500">{evaluation.riskRating}</span>
                </div>
                <div className="p-4 rounded-2xl bg-gray-50 dark:bg-[#0b0e11] border border-gray-200 dark:border-[#1e2329] text-xs leading-relaxed text-gray-600 dark:text-gray-400">
                  {evaluation.feedback}
                </div>
                <div className="flex justify-between items-center text-[10px] font-bold text-gray-500">
                  <span>{t('dashboard.disciplineScore')}</span>
                  <span>{evaluation.disciplineScore}/100</span>
                </div>
                <div className="h-1.5 bg-gray-200 dark:bg-[#0b0e11] rounded-full overflow-hidden">
                  <div className="h-full bg-yellow-500" style={{ width: `${evaluation.disciplineScore}%` }}></div>
                </div>
              </div>
            ) : (
              <p className="text-xs text-gray-500 dark:text-gray-600 italic">{t('dashboard.noEvaluation')}</p>
            )}
          </div>

          <div className="bg-white dark:bg-[#161a1e] p-6 rounded-3xl border border-gray-200 dark:border-[#1e2329] shadow-sm transition-all duration-300">
            <h4 className="text-xs font-bold text-red-600 dark:text-red-500 uppercase mb-4 tracking-widest">{t('dashboard.riskViolations')}</h4>
            {violations.length === 0 ? (
              <div className="flex items-center gap-2 text-green-600 dark:text-green-500">
                <i className="fas fa-check-circle text-xs"></i>
                <span className="text-[10px] font-bold uppercase">{t('dashboard.allRulesRespected')}</span>
              </div>
            ) : (
              <div className="space-y-3">
                {violations.map((v, i) => (
                  <div key={i} className="p-3 rounded-xl bg-red-500/10 border border-red-500/20 text-[10px] text-red-600 dark:text-red-500 font-bold">
                    {v.message}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default PropDashboard;
