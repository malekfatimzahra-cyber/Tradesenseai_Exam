import React, { useState, useEffect } from 'react';
import { X, CreditCard, CheckCircle, Loader, Wallet } from 'lucide-react';
import { PayPalScriptProvider, PayPalButtons } from '@paypal/react-paypal-js';

interface PaymentModalProps {
    isOpen: boolean;
    onClose: () => void;
    challenge: {
        id: number;
        name: string;
        price: number;
        type: string;
    };
    onSuccess: () => void;
}

type PaymentMethod = 'cmi' | 'crypto' | 'paypal' | null;
type PaymentStep = 'select' | 'processing' | 'success';

const PaymentModal: React.FC<PaymentModalProps> = ({ isOpen, onClose, challenge, onSuccess }) => {
    const [selectedMethod, setSelectedMethod] = useState<PaymentMethod>(null);
    const [step, setStep] = useState<PaymentStep>('select');
    const [isProcessing, setIsProcessing] = useState(false);
    const [paypalConfig, setPaypalConfig] = useState<{ clientId: string | null; enabled: boolean }>({ clientId: null, enabled: false });

    // Fetch PayPal Config on Open
    useEffect(() => {
        if (isOpen) {
            fetch('/api/paypal/status')
                .then(res => res.json())
                .then(data => {
                    if (data.enabled && data.client_id) {
                        setPaypalConfig({ clientId: data.client_id, enabled: true });
                    }
                })
                .catch(err => console.error('Failed to fetch PayPal config', err));
        }
    }, [isOpen]);

    if (!isOpen) return null;

    const handleBack = () => {
        setSelectedMethod(null);
        setStep('select');
    };

    const handleClose = () => {
        handleBack();
        onClose();
    };

    // Real PayPal Success Handler
    const handlePayPalSuccess = async (details: any) => {
        setIsProcessing(true);
        try {
            const token = localStorage.getItem('auth_token');
            const response = await fetch('/api/payment/success', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    challenge_type: challenge.type,
                    payment_method: 'PAYPAL',
                    transaction_id: details.id,
                    amount: challenge.price
                })
            });

            if (response.ok) {
                setStep('success');
                setTimeout(() => {
                    onSuccess();
                    handleClose();
                }, 2000);
            } else {
                throw new Error('Transaction recording failed');
            }
        } catch (error) {
            console.error('PayPal activation failed:', error);
            alert('Erreur lors de l\'activation avec PayPal.');
        } finally {
            setIsProcessing(false);
        }
    };

    // Generic Mock Payment Handler (Works for CMI/Crypto)
    const handleMockPayment = async () => {
        setIsProcessing(true);

        // 1. Simulate network/bank processing (Spinner)
        await new Promise(resolve => setTimeout(resolve, 3000));

        try {
            const token = localStorage.getItem('auth_token');

            // 2. Call Mock Backend
            const response = await fetch('/api/mock-payment', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    plan: challenge.name,
                    amount: challenge.price,
                    payment_method: selectedMethod?.toUpperCase()
                })
            });

            if (response.ok) {
                setStep('success');
                setTimeout(() => {
                    onSuccess();
                    handleClose();
                }, 2000);
            } else {
                if (response.status === 401) {
                    alert("Votre session a expiré. Veuillez vous reconnecter.");
                    window.location.href = '/login';
                    return;
                }
                throw new Error('Simulation failed');
            }
        } catch (error) {
            console.error('Payment failed:', error);
            alert('Erreur: Veuillez vérifier votre connexion ou vous reconnecter.');
        } finally {
            setIsProcessing(false);
        }
    };

    return (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-md flex items-center justify-center z-50 p-4">
            <div className="bg-slate-900 rounded-2xl max-w-md w-full shadow-2xl border border-slate-700/50 overflow-hidden">
                {/* Header */}
                <div className="bg-slate-800 p-6 flex justify-between items-center border-b border-slate-700">
                    <div>
                        <h2 className="text-xl font-bold text-white">
                            {step === 'success' ? 'Paiement Réussi' : 'Choisissez le paiement'}
                        </h2>
                        <p className="text-slate-400 text-sm">
                            {challenge.name} - {challenge.price} MAD
                        </p>
                    </div>
                    <button onClick={handleClose} className="text-slate-400 hover:text-white">
                        <X size={24} />
                    </button>
                </div>

                {/* Content */}
                <div className="p-6">

                    {/* Step 1: Selection */}
                    {step === 'select' && !selectedMethod && (
                        <div className="space-y-3">


                            {/* PayPal Button */}
                            <button
                                onClick={() => setSelectedMethod('paypal')}
                                className="w-full bg-[#003087]/20 hover:bg-[#003087]/30 p-4 rounded-xl border border-[#003087]/50 flex items-center justify-between group transition-all"
                            >
                                <div className="flex items-center gap-4">
                                    <div className="bg-[#003087] p-3 rounded-lg text-white">
                                        {/* Simple PayPal Icon */}
                                        <svg className="w-6 h-6 fill-current" viewBox="0 0 24 24">
                                            <path d="M7.076 21.337H2.47a.641.641 0 0 1-.633-.74L4.944.901C5.026.382 5.474 0 5.998 0h7.46c2.57 0 4.578.543 5.69 1.81 1.01 1.15 1.304 2.42 1.012 4.287-.023.143-.047.288-.074.432-.46 2.513-2.16 4.38-4.832 5.37a.673.673 0 0 0-.317.38c-.286 1.458-.895 3.52-1.32 5.71a.64.64 0 0 1-.633.518h-4.23a.64.64 0 0 1-.628-.765l.59-3.21a.208.208 0 0 0-.205-.245H7.72a.641.641 0 0 1-.632-.76l.163-.78c-1.353 3.653-1.63 6.944-1.175 8.39z" />
                                        </svg>
                                    </div>
                                    <div className="text-left">
                                        <div className="font-bold text-white">PayPal</div>
                                        <div className="text-xs text-slate-400">Paiement sécurisé</div>
                                    </div>
                                </div>
                                <div className="text-slate-500 group-hover:text-white">→</div>
                            </button>

                            {/* CMI Button */}
                            <button
                                onClick={() => setSelectedMethod('cmi')}
                                className="w-full bg-slate-800 hover:bg-slate-700 p-4 rounded-xl border border-slate-700 flex items-center justify-between group transition-all"
                            >
                                <div className="flex items-center gap-4">
                                    <div className="bg-green-500/20 p-3 rounded-lg text-green-500 group-hover:bg-green-500 group-hover:text-white transition-colors">
                                        <CreditCard size={24} />
                                    </div>
                                    <div className="text-left">
                                        <div className="font-bold text-white">Payer avec CMI</div>
                                        <div className="text-xs text-slate-400">Simulation Carte Bancaire</div>
                                    </div>
                                </div>
                                <div className="text-slate-500 group-hover:text-white">→</div>
                            </button>

                            {/* Crypto Button */}
                            <button
                                onClick={() => setSelectedMethod('crypto')}
                                className="w-full bg-slate-800 hover:bg-slate-700 p-4 rounded-xl border border-slate-700 flex items-center justify-between group transition-all"
                            >
                                <div className="flex items-center gap-4">
                                    <div className="bg-orange-500/20 p-3 rounded-lg text-orange-500 group-hover:bg-orange-500 group-hover:text-white transition-colors">
                                        <Wallet size={24} />
                                    </div>
                                    <div className="text-left">
                                        <div className="font-bold text-white">Payer avec Crypto</div>
                                        <div className="text-xs text-slate-400">Simulation USDT</div>
                                    </div>
                                </div>
                                <div className="text-slate-500 group-hover:text-white">→</div>
                            </button>
                        </div>
                    )}

                    {/* Step 2: Confirmation / Action */}
                    {step === 'select' && selectedMethod && (
                        <div className="text-center space-y-6">

                            {/* Common Header */}
                            <div className="bg-slate-800 p-6 rounded-xl border border-slate-700">
                                <div className="text-sm text-slate-400 mb-1">Montant à payer</div>
                                <div className="text-3xl font-bold text-white tracking-tight">
                                    {challenge.price} MAD
                                </div>
                                <div className="text-xs text-slate-500 mt-2">
                                    Méthode: <span className="uppercase text-blue-400">{selectedMethod}</span>
                                </div>
                            </div>

                            {/* Logic for PayPal vs Mock */}
                            {selectedMethod === 'paypal' ? (
                                <div className="mt-4">
                                    {paypalConfig.clientId && (
                                        <PayPalScriptProvider options={{
                                            clientId: paypalConfig.clientId,
                                            currency: "USD"
                                        }}>
                                            <PayPalButtons
                                                style={{ layout: "vertical", shape: "rect" }}
                                                createOrder={(data, actions) => {
                                                    return actions.order.create({
                                                        intent: "CAPTURE",
                                                        purchase_units: [{
                                                            amount: {
                                                                currency_code: "USD",
                                                                value: (challenge.price / 10).toFixed(2) // Approx conversion
                                                            }
                                                        }]
                                                    });
                                                }}
                                                onApprove={async (data, actions) => {
                                                    if (actions.order) {
                                                        const details = await actions.order.capture();
                                                        handlePayPalSuccess(details);
                                                    }
                                                }}
                                                onError={(err) => {
                                                    console.error('PayPal Error:', err);
                                                    alert('Erreur PayPal. Vérifiez la configuration.');
                                                }}
                                            />
                                        </PayPalScriptProvider>
                                    )}
                                    <button onClick={handleBack} className="mt-4 text-slate-400 text-sm hover:text-white">
                                        Annuler
                                    </button>
                                </div>
                            ) : (
                                /* Mock Flow (CMI/Crypto) */
                                <>
                                    <div className="bg-yellow-500/10 p-4 rounded-lg text-yellow-500 text-sm border border-yellow-500/20">
                                        ⓘ Ceci est une simulation. En cliquant ci-dessous, le paiement sera validé instantanément.
                                    </div>

                                    <div className="flex gap-3">
                                        <button
                                            onClick={handleBack}
                                            className="flex-1 px-4 py-3 rounded-lg border border-slate-600 text-slate-300 hover:bg-slate-800 font-medium"
                                        >
                                            Retour
                                        </button>
                                        <button
                                            onClick={handleMockPayment}
                                            disabled={isProcessing}
                                            className="flex-[2] bg-blue-600 hover:bg-blue-500 text-white px-4 py-3 rounded-lg font-bold flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                                        >
                                            {isProcessing ? (
                                                <>
                                                    <Loader className="animate-spin" size={20} />
                                                    Traitement...
                                                </>
                                            ) : (
                                                'Simuler le Paiement'
                                            )}
                                        </button>
                                    </div>
                                </>
                            )}
                        </div>
                    )}

                    {/* Step 3: Success */}
                    {step === 'success' && (
                        <div className="text-center py-8">
                            <div className="mb-6 flex justify-center">
                                <div className="bg-green-500/20 p-6 rounded-full animate-bounce">
                                    <CheckCircle className="w-16 h-16 text-green-400" />
                                </div>
                            </div>
                            <h3 className="text-2xl font-bold text-white mb-2">
                                Succès !
                            </h3>
                            <p className="text-slate-300">
                                Challenge activé avec succès.
                            </p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default PaymentModal;
