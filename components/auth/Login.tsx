import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useStore } from '../../store';
import { Mail, Lock, Eye, EyeOff, Loader2 } from 'lucide-react';
import { AuthLayout, AuthCard, AuthInput } from './AuthComponents';

const Login: React.FC = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const { login, isLoading, error } = useStore();
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        const success = await login(email, password);
        if (success) {
            navigate('/terminal');
        }
    };

    return (
        <AuthLayout>
            <AuthCard
                title="Connexion"
                subtitle="Entrez vos identifiants pour accéder à votre espace de trading."
            >
                <form className="space-y-2" onSubmit={handleSubmit}>
                    <AuthInput
                        label="Adresse Email"
                        icon={Mail}
                        type="email"
                        required
                        placeholder="exemple@email.com"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />

                    <div className="relative">
                        <AuthInput
                            label="Mot de Passe"
                            icon={Lock}
                            type={showPassword ? "text" : "password"}
                            required
                            placeholder="••••••••"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                        <button
                            type="button"
                            onClick={() => setShowPassword(!showPassword)}
                            className="absolute right-3 top-[38px] text-gray-500 hover:text-gray-300 transition-colors"
                        >
                            {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                        </button>
                    </div>

                    <div className="flex items-center justify-end pb-4">
                        <div className="text-xs">
                            <a href="#" className="font-medium text-yellow-600 hover:text-yellow-500 transition-colors">
                                Mot de passe oublié ?
                            </a>
                        </div>
                    </div>

                    {error && (
                        <div className="rounded-lg bg-red-500/10 border border-red-500/20 p-3 mb-4">
                            <p className="text-xs text-red-500 text-center font-medium">{error}</p>
                        </div>
                    )}

                    <button
                        type="submit"
                        disabled={isLoading}
                        className="w-full flex justify-center py-3.5 px-4 border border-transparent rounded-xl shadow-[0_0_20px_-5px_rgba(234,179,8,0.3)] text-sm font-bold text-black bg-gradient-to-r from-yellow-500 to-yellow-600 hover:from-yellow-400 hover:to-yellow-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-yellow-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all transform hover:-translate-y-0.5"
                    >
                        {isLoading ? <Loader2 className="animate-spin" /> : 'SE CONNECTER'}
                    </button>
                </form>

                <div className="mt-8 text-center space-y-4">
                    <p className="text-sm text-gray-500">
                        Pas encore de compte ?{' '}
                        <Link to="/register" className="font-bold text-yellow-500 hover:text-yellow-400 transition-colors">
                            S'inscrire
                        </Link>
                    </p>
                </div>
            </AuthCard>
        </AuthLayout>
    );
};

export default Login;
