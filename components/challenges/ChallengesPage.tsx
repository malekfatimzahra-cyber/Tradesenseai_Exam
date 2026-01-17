import React, { useState, useEffect } from 'react';
import { useStore } from '../../store';
import ActiveChallengeCard from './ActiveChallengeCard';
import PricingCard from './PricingCard';
import UnifiedPaymentModal from './UnifiedPaymentModal';  // NOUVEAU
import { ShieldCheck, Trophy, Target, CreditCard, ChevronLeft, Zap, Wallet } from 'lucide-react';
import toast from 'react-hot-toast';
import { useNavigate } from 'react-router-dom';
import { ChallengePlan } from '../../types';

const ChallengesPage: React.FC = () => {
    const { plans, activeAccount, fetchActiveAccount, isLoading } = useStore();
    const [paypalConfigured, setPaypalConfigured] = useState(false);
    const [checkingPaypal, setCheckingPaypal] = useState(true);
    const navigate = useNavigate();

    // Modal State
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [selectedPlan, setSelectedPlan] = useState<ChallengePlan | null>(null);
    const [selectedProvider, setSelectedProvider] = useState<string>('');

    useEffect(() => {
        // Ensure data is loaded
        useStore.getState().fetchPlans();
        fetchActiveAccount();

        // Check PayPal configuration via backend
        fetch('/api/paypal/status')
            .then(res => res.json())
            .then(data => {
                setPaypalConfigured(data.enabled && data.email_configured);
                setCheckingPaypal(false);
            })
            .catch(() => {
                console.error("Failed to check PayPal status");
                setPaypalConfigured(false);
                setCheckingPaypal(false);
            });
    }, []);

    const handleSelectPlan = (plan: ChallengePlan, provider: string) => {
        if (activeAccount) {
            toast.error("You already have an active challenge.");
            return;
        }

        setSelectedPlan(plan);
        setSelectedProvider(provider);
        setIsModalOpen(true);
    };

    const handlePaymentSuccess = () => {
        toast.success('Challenge activé avec succès!');
        setIsModalOpen(false);
        fetchActiveAccount();
        // Le modal redirige automatiquement vers /terminal
    };

    return (
        <div className="min-h-full bg-[#0b0e11] text-white flex flex-col items-center pb-20 overflow-y-auto relative no-scrollbar">

            {/* Background Noise/Gradient Filter */}
            <div className="fixed inset-0 pointer-events-none bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20 contrast-150 brightness-50"></div>

            {/* UNIFIED Payment Modal - Garantit la persistance SQL */}
            <UnifiedPaymentModal
                plan={selectedPlan}
                provider={selectedProvider}
                onClose={() => {
                    setIsModalOpen(false);
                    setSelectedPlan(null);
                    setSelectedProvider('');
                }}
                onSuccess={handlePaymentSuccess}
            />

            <div className="w-full max-w-7xl px-8 py-12 relative z-10 space-y-16">

                {/* TOP HEADER SECTION */}
                <div className="flex flex-col items-center text-center space-y-4 relative">
                    <button
                        onClick={() => navigate(-1)}
                        className="absolute left-0 top-0 w-10 h-10 rounded-full bg-[#1e2329] border border-white/5 flex items-center justify-center text-gray-400 hover:text-white hover:bg-[#252b32] transition-all"
                    >
                        <ChevronLeft size={20} />
                    </button>

                    <h1 className="text-5xl font-black tracking-widest uppercase leading-none text-transparent bg-clip-text bg-gradient-to-b from-white to-gray-500">
                        PICK <span className="text-yellow-500">YOUR</span> CHALLENGE
                    </h1>
                    <p className="text-gray-500 text-sm max-w-xl font-medium">
                        Pass the trading evaluation by following our strict rules, achieve targets, and unlock up to 1M MAD in funding.
                    </p>
                </div>

                {/* SECTION 1 — PERFORMANCE-BASED (ACTIVE OR EMPTY) */}
                <div className="space-y-6">
                    <div className="space-y-1">
                        <h2 className="text-xl font-black text-white uppercase tracking-tight flex items-center gap-3">
                            <Zap size={20} className="text-yellow-500" />
                            Performance-Based Challenges
                        </h2>
                        <p className="text-xs text-gray-500 font-medium ml-8">Pass the trading evaluation by following our strict rules and become a funded trader!</p>
                    </div>

                    {activeAccount ? (
                        <ActiveChallengeCard account={activeAccount} paypalConnected={paypalConfigured} />
                    ) : (
                        <div className="p-12 bg-[#15191e]/40 border border-white/5 rounded-[2rem] flex flex-col items-center justify-center text-center space-y-4 group hover:border-yellow-500/10 transition-all">
                            <div className="relative">
                                <div className="w-16 h-16 bg-white/5 rounded-full flex items-center justify-center text-gray-600 group-hover:text-yellow-500 group-hover:scale-110 transition-all duration-500 z-10 relative">
                                    <Wallet size={32} />
                                </div>
                                <div className="absolute inset-0 bg-yellow-500/20 blur-xl rounded-full opacity-0 group-hover:opacity-100 transition-opacity"></div>
                            </div>
                            <div className="space-y-1">
                                <h3 className="text-lg font-bold text-gray-400 group-hover:text-gray-300 transition-colors uppercase tracking-widest">No Active Challenge</h3>
                                <p className="text-gray-600 text-xs font-medium">Select a professional funding plan below to begin your career.</p>
                            </div>
                        </div>
                    )}
                </div>

                {/* SECTION 2 — PICK YOUR CHALLENGE (PRICING) */}
                <div className="space-y-6">
                    <div className="space-y-1">
                        <h2 className="text-xl font-black text-white uppercase tracking-tight flex items-center gap-3">
                            <Trophy size={20} className="text-yellow-500" />
                            Pick Your Challenge
                        </h2>
                        <p className="text-xs text-gray-500 font-medium ml-8">Choose your starting capital. Refundable registration fee.</p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                        {plans.map((plan) => (
                            <PricingCard
                                key={plan.id}
                                plan={plan}
                                onSelect={handleSelectPlan}
                                disabled={!!activeAccount} // Disable if active challenge exists
                                paypalEnabled={paypalConfigured}
                            />
                        ))}
                    </div>

                    {activeAccount && (
                        <div className="text-center p-4 bg-yellow-500/5 border border-yellow-500/20 rounded-xl">
                            <p className="text-yellow-500/80 text-xs font-black uppercase tracking-widest">
                                You have an active challenge. Complete it to unlock new funding options.
                            </p>
                        </div>
                    )}
                </div>

                {/* TRUST SIGNALS */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 py-8 border-t border-white/5 opacity-40 hover:opacity-100 transition-opacity duration-500">
                    {[
                        { label: 'Strict Rules', sub: 'Discipline First', icon: ShieldCheck, color: 'text-gray-400' },
                        { label: 'Instant Access', sub: 'Auto-Processing', icon: CreditCard, color: 'text-gray-400' },
                        { label: 'Secure Payments', sub: '256-bit SSL', icon: LockIcon, color: 'text-gray-400' }, // Correcting icon usage below
                        { label: '24/7 Support', sub: 'Always Online', icon: Zap, color: 'text-gray-400' }
                    ].map((item, i) => (
                        <div key={i} className="flex flex-col items-center text-center gap-2">
                            <item.icon size={20} className={item.color} />
                            <div>
                                <p className="text-[10px] font-black uppercase tracking-widest text-gray-500">{item.label}</p>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

// Helper for the Lock Icon which wasn't imported
const LockIcon = ({ size, className }: { size: number, className?: string }) => (
    <svg
        xmlns="http://www.w3.org/2000/svg"
        width={size}
        height={size}
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        className={className}
    >
        <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
        <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
    </svg>
);

export default ChallengesPage;
