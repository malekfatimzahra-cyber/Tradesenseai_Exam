import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useStore, API_BASE } from '../store';
import { useTranslation } from 'react-i18next';
import PaymentModal from './PaymentModal';

const Pricing: React.FC = () => {
  const { plans, startChallenge } = useStore();
  const { t } = useTranslation();
  const navigate = useNavigate();

  const [selectedPlan, setSelectedPlan] = useState<any>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [paypalEnabled, setPaypalEnabled] = useState(false);

  // Check PayPal Availability
  React.useEffect(() => {
    fetch(`${API_BASE}/payments/paypal-availability`)
      .then(res => res.json())
      .then(data => setPaypalEnabled(data.enabled))
      .catch(err => console.error("Failed to check PayPal status", err));
  }, []);

  const handleOpenPayment = (planId: string) => {
    const plan = plans.find(p => p.id === planId);
    if (plan) {
      setSelectedPlan(plan);
      setIsModalOpen(true);
    }
  };

  const handlePaymentSuccess = () => {
    if (selectedPlan) {
      startChallenge(selectedPlan.id);
      navigate('/terminal');
    }
  };

  return (
    <div className="py-16 px-8 max-w-7xl mx-auto space-y-16 h-full overflow-y-auto bg-gray-100 dark:bg-[#0b0e11] transition-colors duration-300">
      <div className="text-center space-y-4">
        <h2 className="text-5xl font-black text-gray-900 dark:text-white tracking-tighter uppercase transition-colors">{t('pricing.title')}</h2>
        <p className="text-gray-500 text-lg">{t('pricing.subtitle')}</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 pb-10">
        {plans.map((plan) => (
          <div key={plan.id} className="relative group overflow-hidden bg-white dark:bg-[#161a1e] border border-gray-200 dark:border-[#1e2329] rounded-[2.5rem] p-10 flex flex-col hover:border-yellow-500/50 transition-all duration-500 shadow-xl dark:shadow-2xl">
            {plan.id === 'pro' && (
              <div className="absolute top-0 right-0 p-6 opacity-5 group-hover:opacity-20 transition-opacity">
                <i className="fas fa-crown text-8xl text-yellow-500"></i>
              </div>
            )}

            <div className="mb-8">
              <h3 className="text-sm font-black text-yellow-600 dark:text-yellow-500 uppercase tracking-[0.3em] mb-4">{plan.name}</h3>
              <div className="text-5xl font-black text-gray-900 dark:text-white mb-2">{plan.capital.toLocaleString()} {plan.currency}</div>
              <p className="text-gray-500 text-xs uppercase font-bold tracking-widest">{t('pricing.initialFunding')}</p>
            </div>

            <ul className="space-y-6 mb-12 flex-1">
              {[
                { label: t('dashboard.profitTarget'), value: `${plan.profitTarget.toLocaleString()} MAD`, icon: 'fa-bullseye', color: 'text-green-600 dark:text-green-500' },
                { label: t('dashboard.dailyLoss'), value: `${plan.dailyLossLimit.toLocaleString()} MAD`, icon: 'fa-calendar-day', color: 'text-red-600 dark:text-red-500' },
                { label: t('dashboard.maxDrawdown'), value: `${plan.maxDrawdown.toLocaleString()} MAD`, icon: 'fa-chart-area', color: 'text-red-600 dark:text-red-500' },
                { label: t('dashboard.leverage'), value: '1:100 (Int) / 1:1 (BVC)', icon: 'fa-bolt', color: 'text-yellow-600 dark:text-yellow-500' },
              ].map((item, i) => (
                <li key={i} className="flex items-center justify-between text-sm">
                  <div className="flex items-center gap-3 text-gray-400">
                    <i className={`fas ${item.icon} text-xs w-4`}></i>
                    <span>{item.label}</span>
                  </div>
                  <span className={`font-black ${item.color}`}>{item.value}</span>
                </li>
              ))}
            </ul>

            <div className="space-y-3">
              <button
                onClick={() => handleOpenPayment(plan.id)}
                className="w-full py-5 bg-yellow-500 text-black font-black uppercase text-xs rounded-2xl hover:bg-yellow-400 transition-all shadow-xl shadow-yellow-500/10 flex items-center justify-center gap-3"
              >
                {t('pricing.pay')} {plan.price} MAD <i className="fas fa-arrow-right"></i>
              </button>

              <div className="flex gap-2">
                <button
                  onClick={() => paypalEnabled && handleOpenPayment(plan.id)}
                  disabled={!paypalEnabled}
                  className={`flex-1 py-3 bg-gray-100 dark:bg-[#1e2329] border border-gray-200 dark:border-[#2b3139] rounded-xl text-[10px] font-bold uppercase transition-colors ${paypalEnabled ? 'text-gray-500 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white' : 'text-gray-300 dark:text-gray-700 cursor-not-allowed opacity-50'}`}
                  title={paypalEnabled ? "Pay with PayPal" : "PayPal currently unavailable"}
                >
                  PayPal
                </button>
                <button
                  onClick={() => handleOpenPayment(plan.id)}
                  className="flex-1 py-3 bg-gray-100 dark:bg-[#1e2329] border border-gray-200 dark:border-[#2b3139] rounded-xl text-[10px] font-bold text-gray-500 dark:text-gray-400 uppercase hover:text-gray-900 dark:hover:text-white transition-colors"
                >
                  CMI / CB
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Payment Modal Integration */}
      {selectedPlan && (
        <PaymentModal
          isOpen={isModalOpen}
          onClose={() => setIsModalOpen(false)}
          onSuccess={handlePaymentSuccess}
          planId={selectedPlan.id}
          planName={selectedPlan.name}
          amount={selectedPlan.price}
          currency={selectedPlan.currency}
        />
      )}
    </div>
  );
};

export default Pricing;
