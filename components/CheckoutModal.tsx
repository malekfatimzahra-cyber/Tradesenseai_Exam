import React, { useState, useEffect } from 'react';
import { X, CheckCircle, Loader2, ShieldCheck, CreditCard, Lock } from 'lucide-react';
import { ChallengePlan } from '../../types';

interface CheckoutModalProps {
    isOpen: boolean;
    onClose: () => void;
    plan: ChallengePlan;
    provider: string; // 'PayPal' | 'CMI' | 'Mock' | 'Crypto'
    onConfirm: () => Promise<void>;
}

const CheckoutModal: React.FC<CheckoutModalProps> = ({ isOpen, onClose, plan, provider, onConfirm }) => {
    const [step, setStep] = useState<'summary' | 'processing' | 'success' | 'error'>('summary');
    const [errorMsg, setErrorMsg] = useState('');

    useEffect(() => {
        if (isOpen) setStep('summary');
    }, [isOpen]);

    if (!isOpen) return null;

    const handleConfirm = async () => {
        setStep('processing');
        try {
            // Simulate network delay for effect
            await new Promise(resolve => setTimeout(resolve, 2000));
            await onConfirm();
            setStep('success');
            // Auto close after success
            setTimeout(() => {
                onClose();
            }, 2000);
        } catch (err: any) {
            setStep('error');
            setErrorMsg(err.message || 'Transaction failed');
        }
    };

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-in fade-in duration-200">
            <div className="bg-[#161a1e] border border-[#2b3139] w-full max-w-md rounded-3xl overflow-hidden shadow-2xl relative">
                <button
                    onClick={onClose}
                    className="absolute top-4 right-4 text-gray-500 hover:text-white transition-colors"
                >
                    <X size={20} />
                </button>

                <div className="p-8">
                    {step === 'summary' && (
                        <div className="space-y-6">
                            <div className="text-center">
                                <h3 className="text-xl font-black text-white uppercase tracking-wider mb-2">Confirm Order</h3>
                                <p className="text-gray-500 text-sm">Secure Checkout via {provider}</p>
                            </div>

                            <div className="bg-[#0b0e11] rounded-2xl p-4 border border-white/5 space-y-3">
                                <div className="flex justify-between items-center">
                                    <span className="text-sm font-bold text-gray-400">Plan</span>
                                    <span className="text-sm font-black text-white">{plan.name}</span>
                                </div>
                                <div className="flex justify-between items-center">
                                    <span className="text-sm font-bold text-gray-400">Funding</span>
                                    <span className="text-sm font-black text-yellow-500">{plan.capital.toLocaleString()} {plan.currency}</span>
                                </div>
                                <div className="h-[1px] bg-white/5 my-2"></div>
                                <div className="flex justify-between items-center text-lg">
                                    <span className="font-bold text-gray-300">Total</span>
                                    <span className="font-black text-white">{plan.price} {plan.currency}</span>
                                </div>
                            </div>

                            <div className="flex items-center gap-3 text-[10px] text-gray-500 bg-blue-500/5 p-3 rounded-xl border border-blue-500/10">
                                <ShieldCheck size={14} className="text-blue-500 shrink-0" />
                                <p>256-bit SSL Encrypted. Your payment information is safe.</p>
                            </div>

                            <button
                                onClick={handleConfirm}
                                className="w-full py-4 bg-yellow-500 hover:bg-yellow-400 text-black font-black uppercase text-xs tracking-widest rounded-xl transition-all shadow-lg shadow-yellow-500/20 active:scale-95 flex items-center justify-center gap-2"
                            >
                                <Lock size={14} /> Pay Now
                            </button>
                        </div>
                    )}

                    {step === 'processing' && (
                        <div className="py-12 flex flex-col items-center justify-center text-center space-y-6">
                            <div className="relative">
                                <div className="w-16 h-16 border-4 border-yellow-500/20 border-t-yellow-500 rounded-full animate-spin"></div>
                                <div className="absolute inset-0 flex items-center justify-center">
                                    <CreditCard size={20} className="text-yellow-500 opacity-50" />
                                </div>
                            </div>
                            <div>
                                <h3 className="text-lg font-bold text-white mb-1">Processing Payment</h3>
                                <p className="text-sm text-gray-500">Please verify the transaction in your provider...</p>
                            </div>
                        </div>
                    )}

                    {step === 'success' && (
                        <div className="py-12 flex flex-col items-center justify-center text-center space-y-6 animate-in zoom-in duration-300">
                            <div className="w-20 h-20 bg-green-500/10 rounded-full flex items-center justify-center text-green-500 border border-green-500/20 shadow-[0_0_30px_-5px_rgba(34,197,94,0.4)]">
                                <CheckCircle size={40} />
                            </div>
                            <div>
                                <h3 className="text-xl font-black text-white mb-2">Payment Successful!</h3>
                                <p className="text-sm text-gray-500">Your challenge account has been created.</p>
                            </div>
                        </div>
                    )}

                    {step === 'error' && (
                        <div className="py-12 flex flex-col items-center justify-center text-center space-y-6">
                            <div className="w-20 h-20 bg-red-500/10 rounded-full flex items-center justify-center text-red-500 border border-red-500/20">
                                <X size={40} />
                            </div>
                            <div>
                                <h3 className="text-xl font-black text-white mb-2">Payment Failed</h3>
                                <p className="text-sm text-red-400 max-w-xs mx-auto">{errorMsg}</p>
                            </div>
                            <button
                                onClick={() => setStep('summary')}
                                className="px-6 py-2 bg-[#2b3139] hover:bg-[#363d47] text-white text-xs font-bold uppercase tracking-wider rounded-lg transition-colors"
                            >
                                Try Again
                            </button>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default CheckoutModal;
