import React from 'react';
import { TrendingUp, Shield, Target, Activity, CheckCircle, Clock, AlertTriangle } from 'lucide-react';
import { TradingAccount } from '../../types';

interface ActiveChallengeCardProps {
    account: TradingAccount;
    paypalConnected: boolean;
}

const ActiveChallengeCard: React.FC<ActiveChallengeCardProps> = ({ account, paypalConnected }) => {
    const profit = account.equity - account.initialBalance;
    const profitPercentage = (profit / account.initialBalance) * 100;

    // Profit limit is 10%
    const profitTarget = account.initialBalance * 0.1;
    const progress = Math.min(100, Math.max(0, (profit / profitTarget) * 100));

    // Daily drawdown calc
    const dailyDrawdown = ((account.equity - account.dailyStartingEquity) / account.dailyStartingEquity) * 100;
    // Limit is -5%
    const dailyLimitPerc = -5.00;

    // Total drawdown calc
    const totalDrawdown = ((account.equity - account.initialBalance) / account.initialBalance) * 100;
    const totalLimitPerc = -10.00;

    return (
        <div className="bg-[#15191e] border border-white/10 rounded-[1.5rem] p-8 relative overflow-hidden shadow-2xl">
            {/* Top Gradient Line */}
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-yellow-500/0 via-yellow-500 to-yellow-500/0 opacity-50"></div>

            <div className="flex flex-col md:flex-row gap-12">

                {/* LEFT PANEL: Live Stats */}
                <div className="flex-1 space-y-8">
                    {/* Header */}
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                        <div className="space-y-1">
                            <h3 className="text-sm font-black text-yellow-500 uppercase tracking-widest">{account.planId} CHALLENGE</h3>
                            <p className="text-xs text-gray-400 font-medium">Active since {new Date(account.startTime || Date.now()).toLocaleDateString()}</p>
                        </div>
                        <div className="flex items-center gap-3 bg-[#0b0e11] px-4 py-2 rounded-lg border border-white/5">
                            <span className="text-xl font-black text-white">{account.equity.toLocaleString()} MAD</span>
                            <span className={`text-xs font-black px-2 py-0.5 rounded ${profitPercentage >= 0 ? 'bg-green-500/20 text-green-500' : 'bg-red-500/20 text-red-500'}`}>
                                {profitPercentage >= 0 ? '+' : ''}{profitPercentage.toFixed(2)}%
                            </span>
                            {profitPercentage >= 0 ? <TrendingUp size={16} className="text-green-500" /> : <TrendingUp size={16} className="text-red-500 rotate-180" />}
                        </div>
                    </div>

                    {/* Metrics List */}
                    <div className="space-y-6">

                        {/* 1. Current Equity */}
                        <div className="flex items-center justify-between p-4 bg-[#0b0e11]/50 rounded-xl border border-white/5 group hover:border-white/10 transition-colors">
                            <div className="flex items-center gap-4">
                                <div className="w-10 h-10 rounded-full bg-[#1e2329] flex items-center justify-center text-gray-400 group-hover:text-white transition-colors">
                                    <Activity size={18} />
                                </div>
                                <div>
                                    <p className="text-xs font-bold text-gray-400 uppercase tracking-wider">Current Equity</p>
                                    <p className="text-[10px] text-gray-600">Real-time balance</p>
                                </div>
                            </div>
                            <span className="text-lg font-black text-white">{account.equity.toLocaleString('fr-MA', { minimumFractionDigits: 2 })}</span>
                        </div>

                        {/* 2. Daily Drawdown */}
                        <div className="flex items-center justify-between p-4 bg-[#0b0e11]/50 rounded-xl border border-white/5 group hover:border-white/10 transition-colors">
                            <div className="flex items-center gap-4">
                                <div className="w-10 h-10 rounded-full bg-[#1e2329] flex items-center justify-center text-gray-400 group-hover:text-white transition-colors">
                                    <Shield size={18} />
                                </div>
                                <div>
                                    <p className="text-xs font-bold text-gray-400 uppercase tracking-wider">Daily Drawdown</p>
                                    <p className="text-[10px] text-gray-600">Resets at midnight</p>
                                </div>
                            </div>
                            <div className="text-right">
                                <div className="flex items-center gap-2 justify-end">
                                    <span className={`text-lg font-black ${dailyDrawdown <= -4 ? 'text-red-500 animate-pulse' : 'text-white'}`}>
                                        {dailyDrawdown.toFixed(2)}%
                                    </span>
                                    <span className="text-xs font-bold text-red-500/60">/ -5.00%</span>
                                </div>
                                <div className="w-32 h-1 bg-gray-800 rounded-full mt-1 ml-auto overflow-hidden">
                                    <div className="h-full bg-red-500" style={{ width: `${Math.min(100, (Math.abs(dailyDrawdown) / 5) * 100)}%` }}></div>
                                </div>
                            </div>
                        </div>

                        {/* 3. Profit Target */}
                        <div className="space-y-3 p-4 bg-[#0b0e11]/50 rounded-xl border border-white/5">
                            <div className="flex items-center justify-between">
                                <div className="flex items-center gap-4">
                                    <div className="w-10 h-10 rounded-full bg-[#1e2329] flex items-center justify-center text-yellow-500">
                                        <Target size={18} />
                                    </div>
                                    <p className="text-xs font-bold text-gray-300 uppercase tracking-wider">Profit Target</p>
                                </div>
                                <span className="text-lg font-black text-yellow-500">{progress.toFixed(2)}%</span>
                            </div>

                            <div className="relative w-full h-3 bg-[#1e2329] rounded-full overflow-hidden">
                                <div
                                    className="absolute h-full bg-gradient-to-r from-yellow-600 to-yellow-400 rounded-full transition-all duration-1000 shadow-[0_0_15px_rgba(234,179,8,0.3)]"
                                    style={{ width: `${progress}%` }}
                                ></div>
                            </div>

                            <div className="flex justify-between items-center text-[10px] font-bold text-gray-500 uppercase tracking-wider">
                                <span>{profit > 0 ? profit.toLocaleString() : 0} MAD Gain</span>
                                <span>Target: {profitTarget.toLocaleString()} MAD</span>
                            </div>
                        </div>

                    </div>
                </div>

                {/* Divider (Vertical on desktop, horizontal on mobile) */}
                <div className="w-full h-[1px] md:w-[1px] md:h-auto bg-white/10"></div>

                {/* RIGHT PANEL: Kill Switch Report */}
                <div className="w-full md:w-[35%] flex flex-col justify-between space-y-8">
                    <div>
                        <h4 className="text-lg font-black text-white uppercase tracking-tight flex items-center gap-2 mb-6">
                            Kill <span className="text-yellow-500">Switch</span> Report
                        </h4>

                        <div className="space-y-6">
                            <div className="flex items-start gap-4 group">
                                <div className={`mt-1.5 w-2 h-2 rounded-full ring-2 ring-offset-2 ring-offset-[#15191e] transition-colors ${dailyDrawdown <= -5 ? 'bg-red-500 ring-red-500' : 'bg-gray-700 ring-gray-700 group-hover:bg-red-500/50 group-hover:ring-red-500/50'}`}></div>
                                <div>
                                    <p className="text-xs font-bold text-gray-300">Daily Drawdown Limit</p>
                                    <p className="text-[11px] text-gray-500 leading-relaxed mt-1">
                                        Account fails if equity drops <span className="text-red-400 font-bold">-5%</span> from daily starting balance.
                                    </p>
                                </div>
                            </div>

                            <div className="flex items-start gap-4 group">
                                <div className={`mt-1.5 w-2 h-2 rounded-full ring-2 ring-offset-2 ring-offset-[#15191e] transition-colors ${totalDrawdown <= -10 ? 'bg-red-500 ring-red-500' : 'bg-gray-700 ring-gray-700 group-hover:bg-red-500/50 group-hover:ring-red-500/50'}`}></div>
                                <div>
                                    <p className="text-xs font-bold text-gray-300">Total Drawdown Limit</p>
                                    <p className="text-[11px] text-gray-500 leading-relaxed mt-1">
                                        Account fails if total equity drops <span className="text-red-400 font-bold">-10%</span> from initial balance.
                                    </p>
                                </div>
                            </div>

                            <div className="flex items-start gap-4 group">
                                <div className={`mt-1.5 w-2 h-2 rounded-full ring-2 ring-offset-2 ring-offset-[#15191e] bg-green-500 ring-green-500 shadow-[0_0_10px_#22c55e]`}></div>
                                <div>
                                    <p className="text-xs font-bold text-white">Profit Target Goal</p>
                                    <p className="text-[11px] text-gray-500 leading-relaxed mt-1 flex items-center flex-wrap gap-2">
                                        Reach <span className="text-green-500 font-bold">+10%</span> to pass.
                                        <span className="text-[9px] bg-green-500 text-black px-2 py-0.5 rounded font-black uppercase">Account Passed</span>
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="space-y-4">
                        <div className="p-3 bg-yellow-500/5 rounded-lg border border-yellow-500/10 flex items-start gap-3">
                            <AlertTriangle size={14} className="text-yellow-500 mt-0.5 shrink-0" />
                            <p className="text-[10px] text-yellow-500/80 font-medium leading-relaxed">
                                Engine monitors all trades in real-time. Breaching strict rules results in immediate disqualification.
                            </p>
                        </div>

                        {/* Updated PayPal Button style match Reference Image 2 */}
                        <div className="w-full h-14 bg-[#1e2329] rounded-xl border border-white/5 flex items-center justify-center">
                            {paypalConnected ? (
                                <div className="flex items-center gap-2">
                                    <span className="text-sm font-bold text-white italic tracking-wide">PayPal</span>
                                    <span className="text-sm font-medium text-gray-400">Connected</span>
                                    <div className="w-5 h-5 rounded-full bg-green-500 flex items-center justify-center shadow-lg shadow-green-500/20">
                                        <CheckCircle size={12} className="text-black stroke-[3]" />
                                    </div>
                                </div>
                            ) : (
                                <div className="flex items-center gap-2 opacity-50">
                                    <span className="text-sm font-bold text-white italic tracking-wide">PayPal</span>
                                    <span className="text-sm font-medium text-gray-500">Not Configured</span>
                                    <CheckCircle size={16} className="text-gray-600" />
                                </div>
                            )}
                        </div>
                    </div>
                </div>

            </div>
        </div>
    );
};

export default ActiveChallengeCard;
