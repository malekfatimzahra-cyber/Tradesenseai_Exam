import React, { useState, useEffect } from 'react';
import { Settings, Save, CheckCircle, AlertCircle, Loader, ExternalLink } from 'lucide-react';
import toast from 'react-hot-toast';

const PayPalSettings: React.FC = () => {
    const [config, setConfig] = useState({
        client_id: '',
        client_secret: '',
        email: '',
        sandbox_mode: true
    });
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [testStatus, setTestStatus] = useState<'idle' | 'testing' | 'success' | 'error'>('idle');

    useEffect(() => {
        fetchConfig();
    }, []);

    const fetchConfig = async () => {
        try {
            const token = localStorage.getItem('auth_token');
            const response = await fetch('/api/paypal/config', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                const data = await response.json();
                setConfig(data);
            }
        } catch (error) {
            console.error('Failed to fetch PayPal config:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleSave = async () => {
        setSaving(true);
        try {
            const token = localStorage.getItem('auth_token');
            const response = await fetch('/api/paypal/config', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(config)
            });

            if (response.ok) {
                toast.success('✅ Configuration PayPal sauvegardée');
                setTestStatus('idle');
            } else {
                toast.error('Erreur lors de la sauvegarde');
            }
        } catch (error) {
            toast.error('Erreur réseau');
        } finally {
            setSaving(false);
        }
    };

    const testConnection = async () => {
        setTestStatus('testing');

        // Simulate test
        setTimeout(async () => {
            try {
                const response = await fetch('/api/paypal/status');
                const data = await response.json();

                if (data.enabled && data.email_configured) {
                    setTestStatus('success');
                    toast.success('✅ PayPal configuré correctement');
                } else {
                    setTestStatus('error');
                    toast.error('❌ Configuration incomplète');
                }
            } catch (error) {
                setTestStatus('error');
                toast.error('❌ Test échoué');
            }
        }, 1500);
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center p-12">
                <Loader className="animate-spin text-blue-500" size={32} />
            </div>
        );
    }

    return (
        <div className="bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 rounded-2xl p-8 border border-slate-700/50">
            {/* Header */}
            <div className="flex items-center gap-4 mb-8 pb-6 border-b border-slate-700/50">
                <div className="bg-blue-500/10 p-3 rounded-xl">
                    <svg className="w-8 h-8 text-blue-400" viewBox="0 0 24 24">
                        <path fill="currentColor" d="M20.905 9.5c.21-1.302.024-2.19-.59-2.811-.673-.68-1.902-1-3.445-1h-5.113c-.341 0-.632.248-.686.584l-2.024 12.845c-.04.254.156.482.413.482h3.007l.755-4.784-.024.15c.054-.335.343-.584.686-.584h1.429c2.808 0 5.005-1.14 5.647-4.437.02-.099.037-.195.053-.288.199-1.28.09-2.153-.587-2.777l-.521-.42z" />
                        <path fill="#0070E0" d="M9.078 9.5c.054-.336.345-.584.686-.584h5.113c.645 0 1.245.042 1.802.133.166.027.327.058.484.094.157.035.31.075.457.12.294.089.568.197.823.328.21-1.302.024-2.19-.59-2.811-.673-.68-1.902-1-3.445-1H9.295c-.341 0-.632.248-.686.584L6.585 18.209c-.04.254.156.482.413.482h3.007L9.078 9.5z" />
                    </svg>
                </div>
                <div>
                    <h2 className="text-2xl font-bold text-white">Configuration PayPal</h2>
                    <p className="text-slate-400 text-sm">Connectez votre compte PayPal Business/Sandbox</p>
                </div>
            </div>

            {/* Alert Info */}
            <div className="bg-blue-500/10 border border-blue-500/20 rounded-xl p-4 mb-6 flex gap-3">
                <AlertCircle className="text-blue-400 flex-shrink-0 mt-0.5" size={20} />
                <div className="text-sm text-blue-300">
                    <p className="font-semibold mb-1">Comment obtenir vos credentials PayPal ?</p>
                    <ol className="list-decimal list-inside space-y-1 text-blue-300/80">
                        <li>Créez un compte sur <a href="https://developer.paypal.com" target="_blank" rel="noopener" className="underline hover:text-blue-200">PayPal Developer</a></li>
                        <li>Créez une nouvelle application ("Create App")</li>
                        <li>Copiez le Client ID et Secret</li>
                        <li>Pour les tests, utilisez le mode Sandbox</li>
                    </ol>
                </div>
            </div>

            {/* Form */}
            <div className="space-y-6">
                {/* Sandbox Mode Toggle */}
                <div className="flex items-center justify-between bg-slate-800/50 p-4 rounded-xl border border-slate-700/30">
                    <div>
                        <label className="font-semibold text-white">Mode Sandbox (Test)</label>
                        <p className="text-sm text-slate-400">Utilisez les credentials de test PayPal</p>
                    </div>
                    <button
                        onClick={() => setConfig({ ...config, sandbox_mode: !config.sandbox_mode })}
                        className={`relative w-14 h-8 rounded-full transition-colors ${config.sandbox_mode ? 'bg-blue-500' : 'bg-slate-600'
                            }`}
                    >
                        <div
                            className={`absolute top-1 left-1 w-6 h-6 bg-white rounded-full transition-transform ${config.sandbox_mode ? 'translate-x-6' : ''
                                }`}
                        />
                    </button>
                </div>

                {/* Client ID */}
                <div>
                    <label className="block text-sm font-semibold text-slate-300 mb-2">
                        Client ID {config.sandbox_mode && '(Sandbox)'}
                    </label>
                    <input
                        type="text"
                        value={config.client_id}
                        onChange={(e) => setConfig({ ...config, client_id: e.target.value })}
                        placeholder="AXxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
                        className="w-full bg-slate-800/50 border border-slate-700/50 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-all font-mono text-sm"
                    />
                </div>

                {/* Client Secret */}
                <div>
                    <label className="block text-sm font-semibold text-slate-300 mb-2">
                        Client Secret {config.sandbox_mode && '(Sandbox)'}
                    </label>
                    <input
                        type="password"
                        value={config.client_secret}
                        onChange={(e) => setConfig({ ...config, client_secret: e.target.value })}
                        placeholder="ELxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
                        className="w-full bg-slate-800/50 border border-slate-700/50 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-all font-mono text-sm"
                    />
                </div>

                {/* PayPal Email */}
                <div>
                    <label className="block text-sm font-semibold text-slate-300 mb-2">
                        Email PayPal Business
                    </label>
                    <input
                        type="email"
                        value={config.email}
                        onChange={(e) => setConfig({ ...config, email: e.target.value })}
                        placeholder="business@example.com"
                        className="w-full bg-slate-800/50 border border-slate-700/50 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-all"
                    />
                </div>

                {/* Action Buttons */}
                <div className="flex gap-3 pt-4">
                    <button
                        onClick={handleSave}
                        disabled={saving || !config.client_id || !config.client_secret}
                        className="flex-1 bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-500 hover:to-blue-600 text-white py-3 px-6 rounded-xl font-semibold flex items-center justify-center gap-2 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        {saving ? (
                            <>
                                <Loader className="animate-spin" size={20} />
                                Sauvegarde...
                            </>
                        ) : (
                            <>
                                <Save size={20} />
                                Sauvegarder
                            </>
                        )}
                    </button>

                    <button
                        onClick={testConnection}
                        disabled={testStatus === 'testing' || !config.client_id}
                        className="bg-slate-700/50 hover:bg-slate-700 text-white py-3 px-6 rounded-xl font-semibold flex items-center justify-center gap-2 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        {testStatus === 'testing' ? (
                            <>
                                <Loader className="animate-spin" size={20} />
                                Test...
                            </>
                        ) : testStatus === 'success' ? (
                            <>
                                <CheckCircle className="text-green-400" size={20} />
                                Connecté
                            </>
                        ) : testStatus === 'error' ? (
                            <>
                                <AlertCircle className="text-red-400" size={20} />
                                Erreur
                            </>
                        ) : (
                            <>
                                <Settings size={20} />
                                Tester
                            </>
                        )}
                    </button>
                </div>
            </div>

            {/* Success Message */}
            {testStatus === 'success' && (
                <div className="mt-6 bg-green-500/10 border border-green-500/20 rounded-xl p-4 flex gap-3">
                    <CheckCircle className="text-green-400 flex-shrink-0" size={20} />
                    <div className="text-sm text-green-300">
                        <p className="font-semibold">PayPal configuré avec succès !</p>
                        <p className="text-green-300/80">Les utilisateurs peuvent maintenant payer via PayPal.</p>
                    </div>
                </div>
            )}
        </div>
    );
};

export default PayPalSettings;
