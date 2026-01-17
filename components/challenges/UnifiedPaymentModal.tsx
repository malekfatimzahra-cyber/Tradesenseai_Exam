import React, { useState } from 'react';
import { ChallengePlan } from '../../types';
import { X, CreditCard, Loader2, CheckCircle2 } from 'lucide-react';

interface UnifiedPaymentModalProps {
    plan: ChallengePlan | null;
    provider: string | null;
    onClose: () => void;
    onSuccess: () => void;
}

/**
 * MODAL DE PAIEMENT UNIFIÉ
 * 
 * Gère TOUS les providers (PayPal, CMI, Crypto) via UN SEUL endpoint backend
 * GARANTIT la persistance totale en MySQL
 */
const UnifiedPaymentModal: React.FC<UnifiedPaymentModalProps> = ({ plan, provider, onClose, onSuccess }) => {
    const [processing, setProcessing] = useState(false);
    const [success, setSuccess] = useState(false);
    const [error, setError] = useState<string | null>(null);

    if (!plan || !provider) return null;

    const handlePayment = async () => {
        setProcessing(true);
        setError(null);

        try {
            const token = localStorage.getItem('auth_token');
            if (!token) {
                throw new Error('Non authentifié. Veuillez vous reconnecter.');
            }

            // ========================================
            // UNIFIED PAYMENT ENDPOINT
            // ========================================
            const response = await fetch('http://127.0.0.1:5000/api/unified-payment/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    plan: plan.name,
                    amount: plan.price,
                    payment_method: provider.toUpperCase(),
                    transaction_id: `${provider.toUpperCase()}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
                })
            });

            const data = await response.json();

            if (response.ok && data.success) {
                setSuccess(true);

                // Attendre 1.5s pour afficher le succès
                setTimeout(() => {
                    onSuccess();
                    // Rediriger vers le terminal
                    window.location.href = '/terminal';
                }, 1500);
            } else {
                throw new Error(data.message || 'Échec du paiement');
            }
        } catch (err: any) {
            console.error('Payment error:', err);
            setError(err.message || 'Erreur réseau. Vérifiez que le backend est actif.');
            setProcessing(false);
        }
    };

    const getProviderIcon = () => {
        switch (provider.toUpperCase()) {
            case 'PAYPAL':
                return (
                    <svg className="w-12 h-12" viewBox="0 0 24 24">
                        <path fill="#00457C" d="M20.905 9.5c.21-1.302.024-2.19-.59-2.811-.673-.68-1.902-1-3.445-1h-5.113c-.341 0-.632.248-.686.584l-2.024 12.845c-.04.254.156.482.413.482h3.007l.755-4.784-.024.15c.054-.335.343-.584.686-.584h1.429c2.808 0 5.005-1.14 5.647-4.437.02-.099.037-.195.053-.288.199-1.28.09-2.153-.587-2.777l-.521-.42z" />
                    </svg>
                );
            case 'CMI':
                return <CreditCard className="w-12 h-12 text-emerald-500" />;
            case 'CRYPTO':
                return (
                    <svg className="w-12 h-12 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                );
            default:
                return <CreditCard className="w-12 h-12 text-gray-500" />;
        }
    };

    return (
        <div className="fixed inset-0 bg-black/80 z-[9999] flex items-center justify-center p-4 backdrop-blur-sm">
            <div className="bg-[#161a1e] border border-white/10 rounded-2xl max-w-md w-full p-8 relative shadow-2xl">
                {!success && (
                    <button
                        onClick={onClose}
                        disabled={processing}
                        className="absolute top-4 right-4 text-gray-400 hover:text-white transition-colors disabled:opacity-50"
                    >
                        <X size={24} />
                    </button>
                )}

                {success ? (
                    <div className="text-center py-8">
                        <CheckCircle2 className="w-20 h-20 text-green-500 mx-auto mb-6 animate-pulse" />
                        <h2 className="text-2xl font-black text-white mb-3">Paiement Réussi!</h2>
                        <p className="text-gray-400 text-sm mb-6">
                            Votre challenge <span className="text-yellow-500 font-bold">{plan.name}</span> est maintenant actif.
                        </p>
                        <div className="flex items-center justify-center gap-2 text-green-500 text-sm">
                            <Loader2 className="w-4 h-4 animate-spin" />
                            <span>Redirection vers le Terminal...</span>
                        </div>
                    </div>
                ) : (
                    <>
                        <div className="text-center mb-8">
                            <div className="mb-6 flex justify-center">
                                {getProviderIcon()}
                            </div>
                            <h2 className="text-2xl font-black text-white mb-2">
                                Confirmer le Paiement
                            </h2>
                            <p className="text-gray-400 text-sm">
                                Méthode: <span className="text-yellow-500 font-bold">{provider.toUpperCase()}</span>
                            </p>
                        </div>

                        <div className="bg-[#0b0e11] rounded-xl p-6 mb-6 border border-white/5">
                            <div className="flex justify-between mb-3">
                                <span className="text-gray-400 text-sm">Challenge</span>
                                <span className="text-white font-bold">{plan.name}</span>
                            </div>
                            <div className="flex justify-between mb-3">
                                <span className="text-gray-400 text-sm">Capital Initial</span>
                                <span className="text-white font-bold">{plan.capital.toLocaleString()} MAD</span>
                            </div>
                            <div className="border-t border-white/5 pt-3 mt-3">
                                <div className="flex justify-between">
                                    <span className="text-lg font-black text-white">Total à Payer</span>
                                    <span className="text-2xl font-black text-yellow-500">{plan.price} MAD</span>
                                </div>
                            </div>
                        </div>

                        {error && (
                            <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-4 mb-6">
                                <p className="text-red-500 text-sm font-bold">{error}</p>
                            </div>
                        )}

                        <button
                            onClick={handlePayment}
                            disabled={processing}
                            className="w-full bg-yellow-500 hover:bg-yellow-400 text-black font-black text-sm py-4 rounded-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                        >
                            {processing ? (
                                <>
                                    <Loader2 className="w-5 h-5 animate-spin" />
                                    <span>Traitement en cours...</span>
                                </>
                            ) : (
                                <>
                                    <span>CONFIRMER LE PAIEMENT</span>
                                </>
                            )}
                        </button>

                        <p className="text-center text-gray-500 text-xs mt-4">
                            En confirmant, vous acceptez les{' '}
                            <a href="#" className="text-yellow-500 hover:text-yellow-400">Conditions Générales</a>
                        </p>
                    </>
                )}
            </div>
        </div>
    );
};

export default UnifiedPaymentModal;
