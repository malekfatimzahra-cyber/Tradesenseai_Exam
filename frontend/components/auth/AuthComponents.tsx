import React from 'react';
import { motion } from 'framer-motion';
import { ArrowLeft, Check } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

// --- LAYOUT PRINCIPAL ---
export const AuthLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const navigate = useNavigate();

    return (
        <div className="min-h-screen w-full bg-[#050505] text-white font-sans selection:bg-yellow-500/30 overflow-hidden relative flex items-center justify-center p-4">
            {/* Background Ambience */}
            <div className="fixed inset-0 pointer-events-none">
                {/* Grain Texture */}
                <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-[0.03]"></div>

                {/* Subtle Glows - Très atténués selon demande */}
                <div className="absolute top-[-10%] left-[-10%] w-[40vw] h-[40vw] bg-yellow-900/10 rounded-full blur-[120px]" />
                <div className="absolute bottom-[-10%] right-[-10%] w-[40vw] h-[40vw] bg-orange-900/10 rounded-full blur-[120px]" />
            </div>

            {/* Button Retour Accueil */}
            <div className="absolute top-6 left-6 z-20">
                <button
                    onClick={() => navigate('/')}
                    className="flex items-center gap-2 text-gray-400 hover:text-white transition-colors group text-sm font-medium px-4 py-2 rounded-full hover:bg-white/5"
                >
                    <ArrowLeft className="w-4 h-4 group-hover:-translate-x-1 transition-transform" />
                    Retour à l'accueil
                </button>
            </div>

            {/* Main Content Container */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, ease: "easeOut" }}
                className="w-full max-w-md relative z-10"
            >
                {children}
            </motion.div>
        </div>
    );
};

// --- AUTH CARD ---
export const AuthCard: React.FC<{ children: React.ReactNode; title: string; subtitle?: string }> = ({ children, title, subtitle }) => {
    return (
        <div className="relative group">
            {/* Thin glowing border effect */}
            <div className="absolute -inset-0.5 bg-gradient-to-b from-yellow-600/20 to-orange-900/20 rounded-2xl blur-[1px] opacity-75 group-hover:opacity-100 transition duration-1000"></div>

            <div className="relative bg-[#0B0B0F]/90 backdrop-blur-xl border border-white/10 rounded-2xl p-8 shadow-2xl">
                {/* Logo Header */}
                <div className="flex flex-col items-center mb-8">
                    <div className="w-12 h-12 bg-gradient-to-br from-yellow-500/80 to-yellow-700/80 rounded-xl flex items-center justify-center shadow-[0_0_15px_rgba(234,179,8,0.3)] mb-6">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-black">
                            <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>
                        </svg>
                    </div>
                    <h1 className="text-2xl md:text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-br from-white to-gray-400">
                        {title}
                    </h1>
                    {subtitle && (
                        <p className="mt-2 text-sm text-gray-500 text-center max-w-xs">{subtitle}</p>
                    )}
                </div>

                {children}
            </div>
        </div>
    );
};

// --- AUTH INPUT ---
interface AuthInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
    label: string;
    icon?: React.ElementType;
    error?: string;
}

export const AuthInput: React.FC<AuthInputProps> = ({ label, icon: Icon, error, className, ...props }) => {
    return (
        <div className="mb-5">
            <label className="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-2 ml-1">
                {label}
            </label>
            <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    {Icon && <Icon className="h-5 w-5 text-gray-500" />}
                </div>
                <input
                    className={`
            block w-full pl-10 pr-3 py-3.5 
            bg-[#15151A] border border-white/5 rounded-xl
            text-gray-200 placeholder-gray-600 sm:text-sm
            focus:ring-1 focus:ring-yellow-500/50 focus:border-yellow-500/50 focus:bg-[#1A1A20]
            transition-all duration-200
            ${error ? 'border-red-500/50 focus:border-red-500 focus:ring-red-500/20' : ''}
            ${className}
          `}
                    {...props}
                />
                {/* Error icon or status could go right */}
            </div>
            {error && (
                <p className="mt-2 text-xs text-red-400 ml-1">{error}</p>
            )}
        </div>
    );
};
