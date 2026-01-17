import React, { useState } from 'react';
import { Target, Shield, Zap, Check, ArrowRight, Loader2 } from 'lucide-react';
import { ChallengePlan } from '../../types';

interface PricingCardProps {
    plan: ChallengePlan;
    onSelect: (plan: ChallengePlan, provider: string) => void;
    disabled?: boolean;
    paypalEnabled?: boolean;
}

const PricingCard: React.FC<PricingCardProps> = ({ plan, onSelect, disabled, paypalEnabled }) => {
    const [showPaymentOptions, setShowPaymentOptions] = useState(false);

    const getStats = () => {
        if (plan.id === 'starter') {
            return [
                { label: 'Profit Target', value: `${(plan.capital * 0.05).toLocaleString()} MAD`, icon: Target, color: 'text-green-500' },
                { label: 'Daily Loss Limit', value: `${(plan.capital * 0.05).toLocaleString()} MAD`, icon: Shield, color: 'text-red-500' },
            ];
        }
        if (plan.id === 'pro') {
            return [
                { label: 'Daily Loss Limit', value: `${(plan.capital * 0.1).toLocaleString()} MAD`, icon: Shield, color: 'text-red-500' },
                { label: 'Daily Drawdown', value: `${(plan.capital * 0.05).toLocaleString()} MAD`, icon: Zap, color: 'text-red-500' },
            ];
        }
        return [
            { label: 'Daily Loss Limit', value: `${(plan.capital * 0.05).toLocaleString()} MAD`, icon: Shield, color: 'text-green-500' },
            { label: 'Max Drawdown', value: `${(plan.capital * 0.1).toLocaleString()} MAD`, icon: Zap, color: 'text-red-500' },
        ];
    };

    const handleMainPayClick = () => {
        if (disabled) return;
        setShowPaymentOptions(!showPaymentOptions);
    };

    return (
        <div className={`bg-[#15191e]/60 border border-white/5 rounded-[1.5rem] p-6 flex flex-col relative transition-all duration-300 hover:border-yellow-500/30 hover:bg-[#15191e] h-full ${disabled ? 'opacity-50 grayscale' : 'hover:-translate-y-1'}`}>

            {/* Crown Background Icon based on tier */}
            <div className="absolute top-4 right-4 opacity-[0.03] pointer-events-none">
                <Zap size={100} className="text-yellow-500" />
            </div>

            <div className="mb-6">
                <h3 className="text-[10px] font-black text-yellow-500 uppercase tracking-[0.2em] mb-3">{plan.name}</h3>
                <div className="flex items-baseline gap-2">
                    <span className="text-3xl font-black text-white">{plan.capital.toLocaleString()} <span className="text-sm font-bold text-yellow-500">MAD</span></span>
                </div>
                <p className="text-[9px] text-gray-500 font-bold uppercase tracking-wider mt-1">Initial Funding Potential</p>
            </div>

            <div className="space-y-4 mb-8 flex-1">
                {getStats().map((stat, i) => (
                    <div key={i} className="flex items-center justify-between border-b border-white/5 pb-2 last:border-0 last:pb-0">
                        <div className="flex items-center gap-2 text-gray-400">
                            <stat.icon size={12} className="opacity-50" />
                            <span className="text-[11px] font-bold uppercase tracking-wide">{stat.label}</span>
                        </div>
                        <span className={`text-xs font-black ${stat.color}`}>{stat.value}</span>
                    </div>
                ))}
            </div>

            <div className="space-y-3">
                {!showPaymentOptions ? (
                    <button
                        onClick={handleMainPayClick}
                        disabled={disabled}
                        className="w-full bg-yellow-500 hover:bg-yellow-400 text-black py-4 rounded-xl flex items-center justify-center gap-2 transition-all active:scale-[0.98] shadow-lg shadow-yellow-500/10 disabled:opacity-50 disabled:cursor-not-allowed group"
                    >
                        <span className="text-[11px] font-black uppercase tracking-widest flex items-center gap-2">
                            Pay {plan.price} MAD <ArrowRight size={14} className="group-hover:translate-x-1 transition-transform" />
                        </span>
                    </button>
                ) : (
                    <div className="space-y-3">
                        <button
                            onClick={() => setShowPaymentOptions(false)}
                            className="w-full text-gray-500 hover:text-gray-300 text-xs py-2 transition-colors"
                        >
                            ← Retour
                        </button>

                        <div className="grid grid-cols-2 gap-3">
                            <button
                                onClick={() => onSelect(plan, 'PayPal')}
                                disabled={disabled}
                                title="Pay via PayPal"
                                className={`col-span-1 bg-gradient-to-br from-blue-600 to-blue-500 py-4 rounded-xl text-xs font-black uppercase tracking-widest text-white transition-all flex flex-col items-center justify-center gap-1 ${disabled ? 'opacity-50 cursor-not-allowed' : 'hover:from-blue-500 hover:to-blue-600 hover:scale-105 shadow-lg shadow-blue-500/20'}`}
                            >
                                <svg className="w-6 h-6" viewBox="0 0 24 24">
                                    <path fill="currentColor" d="M20.905 9.5c.21-1.302.024-2.19-.59-2.811-.673-.68-1.902-1-3.445-1h-5.113c-.341 0-.632.248-.686.584l-2.024 12.845c-.04.254.156.482.413.482h3.007l.755-4.784-.024.15c.054-.335.343-.584.686-.584h1.429c2.808 0 5.005-1.14 5.647-4.437.02-.099.037-.195.053-.288.199-1.28.09-2.153-.587-2.777l-.521-.42z" />
                                </svg>
                                <span>PayPal</span>
                            </button>

                            <button
                                onClick={() => onSelect(plan, 'CMI')}
                                disabled={disabled}
                                className="col-span-1 bg-gradient-to-br from-emerald-600 to-emerald-500 py-4 rounded-xl text-xs font-black uppercase tracking-widest text-white hover:from-emerald-500 hover:to-emerald-600 hover:scale-105 transition-all flex flex-col items-center justify-center gap-1 shadow-lg shadow-emerald-500/20 disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <rect x="2" y="5" width="20" height="14" rx="2" strokeWidth="2" />
                                    <path d="M2 10h20" strokeWidth="2" />
                                </svg>
                                <span>CMI / CB</span>
                            </button>

                            <button
                                onClick={() => onSelect(plan, 'Crypto')}
                                disabled={disabled}
                                className="col-span-2 bg-gradient-to-br from-orange-600 to-orange-500 py-3 rounded-xl text-xs font-black uppercase tracking-widest text-white hover:from-orange-500 hover:to-orange-600 hover:scale-105 transition-all flex items-center justify-center gap-2 shadow-lg shadow-orange-500/20 disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                                </svg>
                                <span>Payer avec Crypto</span>
                            </button>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default PricingCard;
