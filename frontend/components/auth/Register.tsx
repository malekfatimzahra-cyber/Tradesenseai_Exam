import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useStore } from '../../store';
import { Mail, Lock, User, Eye, EyeOff, Loader2 } from 'lucide-react';
import { AuthLayout, AuthCard, AuthInput } from './AuthComponents';

const Register: React.FC = () => {
    const [fullName, setFullName] = useState('');
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const [localError, setLocalError] = useState<string | null>(null);
    const { register, isLoading, error } = useStore();
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLocalError(null);

        if (password.length < 8) {
            setLocalError("Le mot de passe doit contenir au moins 8 caractères.");
            return;
        }

        if (password !== confirmPassword) {
            setLocalError('Les mots de passe ne correspondent pas.');
            return;
        }

        const success = await register(fullName, username, email, password);
        if (success) {
            navigate('/terminal');
        }
    };

    return (
        <AuthLayout>
            <AuthCard
                title="Créer un compte"
                subtitle="Rejoignez la première Prop Firm assistée par IA."
            >
                <form className="space-y-2" onSubmit={handleSubmit}>
                    <div className="grid grid-cols-2 gap-4">
                        <AuthInput
                            label="Nom Complet"
                            icon={User}
                            type="text"
                            required
                            placeholder="John Doe"
                            value={fullName}
                            onChange={(e) => setFullName(e.target.value)}
                        />
                        <AuthInput
                            label="Pseudo"
                            icon={User}
                            type="text"
                            required
                            placeholder="TraderPro"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                        />
                    </div>

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
                            onChange={(e) => {
                                setPassword(e.target.value);
                                setLocalError(null);
                            }}
                        />
                        <button
                            type="button"
                            onClick={() => setShowPassword(!showPassword)}
                            className="absolute right-3 top-[38px] text-gray-500 hover:text-gray-300 transition-colors"
                        >
                            {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                        </button>
                    </div>

                    <AuthInput
                        label="Confirmer"
                        icon={Lock}
                        type="password"
                        required
                        placeholder="••••••••"
                        value={confirmPassword}
                        onChange={(e) => {
                            setConfirmPassword(e.target.value);
                            setLocalError(null);
                        }}
                        error={localError || undefined}
                    />

                    <div className="flex items-center gap-2 mb-6">
                        <input type="checkbox" required className="w-4 h-4 rounded border-gray-600 bg-[#15151A] text-yellow-500 focus:ring-yellow-500/50" />
                        <span className="text-xs text-gray-500">
                            J'accepte les <a href="#" className="text-gray-400 hover:text-white underline">Conditions Générales</a>
                        </span>
                    </div>

                    {(error) && (
                        <div className="rounded-lg bg-red-500/10 border border-red-500/20 p-3 mb-4">
                            <p className="text-xs text-red-500 text-center font-medium">{error}</p>
                        </div>
                    )}

                    <button
                        type="submit"
                        disabled={isLoading}
                        className="w-full flex justify-center py-3.5 px-4 border border-transparent rounded-xl shadow-[0_0_20px_-5px_rgba(234,179,8,0.3)] text-sm font-bold text-black bg-gradient-to-r from-yellow-500 to-yellow-600 hover:from-yellow-400 hover:to-yellow-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-yellow-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all transform hover:-translate-y-0.5"
                    >
                        {isLoading ? <Loader2 className="animate-spin" /> : "S'INSCRIRE"}
                    </button>
                </form>

                <div className="mt-8 text-center space-y-4">
                    <p className="text-sm text-gray-500">
                        Déjà un compte ?{' '}
                        <Link to="/login" className="font-bold text-yellow-500 hover:text-yellow-400 transition-colors">
                            Se connecter
                        </Link>
                    </p>
                </div>
            </AuthCard>
        </AuthLayout>
    );
};

export default Register;
