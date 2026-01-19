import React from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  Zap,
  ArrowRight,
  Globe,
  Users,
  GraduationCap,
  Star,
  TrendingUp,
  Activity,
  CheckCircle2,
  LogIn,
  Trophy,
  Bot,
  Check
} from 'lucide-react';

interface LandingPageProps {
  onStartChallenge?: () => void;
  onLogin?: () => void;
}

const LandingPage: React.FC<LandingPageProps> = ({ onStartChallenge, onLogin }) => {
  const navigate = useNavigate();

  const handleStart = () => {
    if (onStartChallenge) onStartChallenge();
    else navigate('/register');
  };

  const handleLoginAction = () => {
    if (onLogin) onLogin();
    else navigate('/login');
  };

  const scrollToSection = (id: string) => {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <div className="min-h-screen bg-[#050505] text-white font-sans selection:bg-yellow-500/30 overflow-x-hidden">

      {/* Background Effects - Enhanced */}
      <div className="fixed inset-0 z-0 pointer-events-none">
        <div className="absolute top-[-20%] left-[-10%] w-[50vw] h-[50vw] bg-orange-600/15 rounded-full blur-[150px] mix-blend-screen animate-pulse" />
        <div className="absolute top-[40%] right-[-15%] w-[60vw] h-[60vw] bg-yellow-600/10 rounded-full blur-[180px] mix-blend-screen" />
        <div className="absolute bottom-[-20%] left-[30%] w-[40vw] h-[40vw] bg-orange-500/10 rounded-full blur-[140px] mix-blend-screen" />

        {/* Energy Lines Pattern */}
        <div className="absolute inset-0 opacity-10">
          <svg className="w-full h-full" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
                <path d="M 40 0 L 0 0 0 40" fill="none" stroke="rgba(234,179,8,0.3)" strokeWidth="0.5" />
              </pattern>
            </defs>
            <rect width="100%" height="100%" fill="url(#grid)" />
          </svg>
        </div>

        <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20"></div>
      </div>

      {/* Navbar */}
      <nav className="relative z-50 px-6 py-5 border-b border-white/5 backdrop-blur-md bg-black/20">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <div className="flex items-center gap-2">
            <div className="w-10 h-10 bg-gradient-to-br from-yellow-400 to-yellow-600 rounded-xl flex items-center justify-center shadow-lg shadow-yellow-500/20">
              <Zap className="w-6 h-6 text-black fill-current" />
            </div>
            <span className="text-xl font-black tracking-tighter">TradeSense</span>
          </div>

          <div className="hidden md:flex items-center gap-8">
            <button onClick={() => scrollToSection('features')} className="text-sm text-gray-400 hover:text-white transition-colors">
              Caractéristiques
            </button>
            <button onClick={() => scrollToSection('testimonials')} className="text-sm text-gray-400 hover:text-white transition-colors">
              Témoignages
            </button>
            <button onClick={() => scrollToSection('pricing')} className="text-sm text-gray-400 hover:text-white transition-colors">
              Tarifs
            </button>
            <button
              onClick={handleLoginAction}
              className="text-sm text-gray-400 hover:text-white transition-colors"
            >
              Se connecter
            </button>
            <button
              onClick={handleStart}
              className="px-6 py-2.5 bg-yellow-500 hover:bg-yellow-400 text-black font-bold rounded-lg transition-all text-sm"
            >
              S'inscrire
            </button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative z-10 pt-20 pb-32 px-6">
        <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">

          {/* Text Content */}
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
            className="text-left"
          >
            <h1 className="text-5xl md:text-6xl lg:text-7xl font-black leading-[1.1] mb-8 tracking-tight">
              Construisez la Première <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-yellow-200 via-yellow-400 to-yellow-600">
                Prop Firm Assistée par IA
              </span>
            </h1>

            <p className="text-lg text-gray-400 leading-relaxed mb-10 max-w-xl">
              Rejoignez la plateforme de prop trading de nouvelle génération
              qui combine <span className="text-white font-bold">signaux IA</span> en temps réel,
              <span className="text-white font-bold"> communauté active</span> et
              <span className="text-white font-bold"> formation MasterClass premium</span>.
            </p>

            <div className="flex flex-wrap gap-4 mb-12">
              <button
                onClick={() => scrollToSection('pricing')}
                className="px-8 py-4 bg-yellow-500 hover:bg-yellow-400 text-black font-black rounded-xl shadow-[0_0_30px_-10px_rgba(234,179,8,0.5)] transition-all transform hover:-translate-y-1 flex items-center gap-3"
              >
                DÉMARRER LE CHALLENGE
              </button>
              <button
                onClick={() => scrollToSection('features')}
                className="px-8 py-4 bg-white/5 hover:bg-white/10 text-white font-bold rounded-xl border border-white/10 backdrop-blur-md transition-all"
              >
                DÉCOUVRIR
              </button>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-3 gap-4">
              {[
                { count: '+10 000', label: 'Traders Rejoints' },
                { count: '+2,5M', label: 'Événements Suivis' },
                { count: '+1 500', label: 'Comptes Financés' },
              ].map((stat, i) => (
                <div key={i} className="text-center">
                  <div className="text-2xl md:text-3xl font-black text-yellow-500">{stat.count}</div>
                  <div className="text-xs text-gray-500 mt-1">{stat.label}</div>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Platform Screenshot */}
          <motion.div
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="relative"
          >
            {/* Glow behind */}
            <div className="absolute inset-0 bg-yellow-500/20 blur-[100px] rounded-full" />

            <div className="relative rounded-2xl overflow-hidden border border-white/10 shadow-2xl backdrop-blur-xl transform hover:scale-105 transition-all duration-500">
              <img
                src="/dashboard-preview.png"
                alt="TradeSense AI Platform Dashboard"
                className="w-full h-auto"
              />
            </div>
          </motion.div>
        </div>
      </section>

      {/* Features / Challenge Section */}
      <section id="features" className="relative z-10 py-24 bg-black/40 border-y border-white/5">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-black text-white mb-6 uppercase tracking-tighter">
              Passez le <span className="text-yellow-500">Challenge</span> et Devenez un Trader <span className="text-yellow-500">Financé</span>
            </h2>
            <p className="text-gray-400 max-w-3xl mx-auto text-lg">
              Testez votre potentiel en réalisant un objectif de profit en respectant les règles strictes du jeu. L'alliance la ferme du identity originale, communauté et formation MasterClass premium.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              {
                title: "Assistance IA en Trading",
                icon: Bot,
                items: [
                  "+1000 Signaux IA/Alertes/IA",
                  "Plans IA personnalisés",
                  "Alertes de détection de risque"
                ],
                button: "Choisir Starter",
                color: "green"
              },
              {
                title: "Actus & Marchés en Direct",
                icon: Globe,
                items: [
                  "Actualités réseau main direct",
                  "Evénements IA/Alertes/MArco",
                  "Marchés internationaux & Maroc"
                ],
                button: "Choisir",
                color: "yellow",
                highlighted: true
              },
              {
                title: "Communauté Active",
                icon: Users,
                items: [
                  "Créatifs, com arguments, nématique",
                  "Échanges avec/entre commentaires",
                  "Communauté plan/se dialogues"
                ],
                button: "Choisir Pro",
                color: "purple"
              },
              {
                title: "Cours MasterClass Pro",
                icon: GraduationCap,
                items: [
                  "Tous ind. Thèmes renforcés le règles",
                  "Webinaires Face intégrités",
                  "Radio de manuscle & règle"
                ],
                button: "Choisir Elite",
                color: "green"
              },
            ].map((feature, i) => (
              <motion.div
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.1 }}
                viewport={{ once: true }}
                key={i}
                className={`p-8 rounded-3xl border ${feature.highlighted
                  ? 'bg-gradient-to-br from-yellow-500/20 to-orange-500/10 border-yellow-500/30'
                  : 'bg-[#0d1117] border-white/5'
                  } hover:border-yellow-500/50 transition-all group flex flex-col relative overflow-hidden`}
              >
                {feature.highlighted && (
                  <div className="absolute inset-0 bg-gradient-to-br from-yellow-500/5 to-orange-500/5 animate-pulse" />
                )}

                <div className="relative z-10">
                  <div className={`w-14 h-14 rounded-2xl ${feature.color === 'green' ? 'bg-green-500/10' :
                    feature.color === 'yellow' ? 'bg-yellow-500/10' :
                      'bg-purple-500/10'
                    } flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300`}>
                    <feature.icon className={`w-7 h-7 ${feature.color === 'green' ? 'text-green-500' :
                      feature.color === 'yellow' ? 'text-yellow-500' :
                        'text-purple-500'
                      }`} />
                  </div>
                  <h3 className="text-xl font-black mb-4">{feature.title}</h3>
                  <ul className="space-y-2 mb-6 flex-1">
                    {feature.items.map((item, idx) => (
                      <li key={idx} className="flex items-start gap-2 text-sm text-gray-400">
                        <CheckCircle2 className={`w-4 h-4 mt-0.5 flex-shrink-0 ${feature.color === 'green' ? 'text-green-500' :
                          feature.color === 'yellow' ? 'text-yellow-500' :
                            'text-purple-500'
                          }`} />
                        <span>{item}</span>
                      </li>
                    ))}
                  </ul>
                  <button
                    onClick={handleStart}
                    className={`w-full py-3 rounded-xl text-sm font-black uppercase tracking-wider transition-all ${feature.highlighted
                      ? 'bg-yellow-500 text-black hover:bg-yellow-400'
                      : 'bg-white/5 hover:bg-white/10 border border-white/5'
                      }`}
                  >
                    {feature.button}
                  </button>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Partners Logos */}
      <div className="py-16 border-b border-white/5 overflow-hidden relative z-10">
        <div className="container mx-auto px-6 flex justify-center gap-16 md:gap-24 opacity-40 grayscale hover:grayscale-0 hover:opacity-60 transition-all duration-500 flex-wrap items-center">
          <div className="text-xl font-bold tracking-wider flex items-center gap-2">
            <svg className="w-6 h-6" viewBox="0 0 24 24" fill="currentColor">
              <path d="M4 4h16v16H4V4z" />
            </svg>
            TradingView
          </div>
          <div className="text-xl font-bold italic">2yfinance</div>
          <div className="text-xl font-black tracking-tight">BVC<span className="text-sm">SCRAP</span></div>
        </div>
      </div>

      {/* Why Choose Section */}
      <section className="py-24 relative z-10">
        <div className="container mx-auto px-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            <motion.div
              initial={{ opacity: 0, x: -30 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
            >
              <h2 className="text-4xl md:text-5xl font-black mb-8">
                Pourquoi les Traders Choisissent <br />
                <span className="text-yellow-500">TradeSense AI</span>
              </h2>

              <div className="space-y-4 mb-10">
                {[
                  "Liste plateforme unique pour le trading, l'apprentissage et la communauté",
                  "Rapideté, IA, et surtout de réussite vs l'aisance",
                  "Acteur / réseau / MasterClass dans une seule interface",
                  "Évitez les tarifs respatriés et les frais visites/contrisence"
                ].map((item, i) => (
                  <div key={i} className="flex items-start gap-3">
                    <Check className="w-6 h-6 text-yellow-500 flex-shrink-0 mt-0.5" />
                    <span className="text-gray-300">{item}</span>
                  </div>
                ))}
              </div>

              <button
                onClick={handleStart}
                className="px-8 py-4 bg-yellow-500 hover:bg-yellow-400 text-black font-black rounded-xl transition-all"
              >
                Rejoindre
              </button>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 30 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="relative"
            >
              <div className="absolute inset-0 bg-yellow-500/20 blur-[100px] rounded-full" />
              <div className="relative rounded-2xl overflow-hidden border border-white/10 shadow-2xl">
                <div className="w-full aspect-video bg-gradient-to-br from-gray-900 via-gray-800 to-black flex items-center justify-center">
                  <div className="text-center">
                    <Bot className="w-16 h-16 text-yellow-500 mx-auto mb-4" />
                    <div className="text-2xl font-black text-white">TradeSense AI</div>
                    <div className="text-sm text-gray-400">Trading Platform</div>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Testimonial + Community */}
      <section id="testimonials" className="py-24 relative z-10 bg-black/40 border-y border-white/5">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-6xl font-black mb-6 tracking-tight">
              Rejoignez la <span className="text-yellow-500">Communauté</span> TradeSense Ai
            </h2>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center max-w-6xl mx-auto">
            <motion.div
              initial={{ scale: 0.95, opacity: 0 }}
              whileInView={{ scale: 1, opacity: 1 }}
              viewport={{ once: true }}
              className="bg-gradient-to-br from-[#161a1e] to-[#0b0e11] p-10 rounded-3xl border border-white/10 relative overflow-hidden"
            >
              <div className="flex justify-start gap-1 mb-6">
                {[1, 2, 3, 4, 5].map(s => <Star key={s} className="w-5 h-5 text-yellow-500 fill-current" />)}
              </div>

              <p className="text-xl md:text-2xl font-bold text-gray-200 mb-8 leading-relaxed">
                TradeSense AI a complètement changé ma façon de trader. Grâce aux signaux
                IA précis et à la formation de pointe, j'ai pu devenir un trader financé en
                seulement quelques semaines!
              </p>

              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-full bg-gradient-to-br from-yellow-400 to-yellow-600 flex items-center justify-center text-black font-black">
                  OE
                </div>
                <div className="text-left">
                  <div className="font-black text-white">Othman El ESGG</div>
                  <div className="text-xs text-yellow-500 font-bold uppercase tracking-wider">
                    Trader Financé
                  </div>
                </div>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 30 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="relative"
            >
              <div className="absolute inset-0 bg-yellow-500/20 blur-[100px] rounded-full" />
              <div className="relative rounded-2xl overflow-hidden border border-white/10 shadow-2xl">
                <div className="w-full aspect-video bg-gradient-to-br from-purple-900/50 via-gray-900 to-black flex items-center justify-center">
                  <div className="text-center">
                    <Users className="w-16 h-16 text-purple-500 mx-auto mb-4" />
                    <div className="text-2xl font-black text-white">Community Hub</div>
                    <div className="text-sm text-gray-400">Connect with Traders</div>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>

          <div className="text-center mt-16">
            <button
              onClick={handleStart}
              className="px-10 py-5 bg-yellow-500 hover:bg-yellow-400 text-black font-black rounded-full transition-all shadow-2xl flex items-center gap-3 mx-auto"
            >
              <Users className="w-5 h-5" />
              Rejoindre
            </button>
          </div>
        </div>
      </section>

      {/* Pricing Section (hidden by default, visible on scroll) */}
      <section id="pricing" className="py-24 relative z-10">
        <div className="container mx-auto px-6 text-center">
          <h2 className="text-4xl font-black mb-4 uppercase">Choisissez Votre Challenge</h2>
          <p className="text-gray-400 mb-16 max-w-2xl mx-auto">
            Sélectionnez le plan qui correspond à vos objectifs de trading
          </p>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            {[
              { name: 'Starter', price: '200 DH', capital: '$5,000' },
              { name: 'Pro', price: '500 DH', capital: '$25,000', featured: true },
              { name: 'Elite', price: '1000 DH', capital: '$100,000' }
            ].map((plan, i) => (
              <div
                key={plan.name}
                className={`p-8 rounded-3xl border transition-all ${plan.featured
                  ? 'bg-gradient-to-br from-yellow-500 to-yellow-600 text-black border-yellow-400 scale-105 shadow-2xl'
                  : 'bg-[#161a1e] border-white/10 hover:border-white/20'
                  }`}
              >
                <h3 className={`text-xl font-bold uppercase mb-2 ${plan.featured ? 'text-black/70' : 'text-gray-400'}`}>
                  {plan.name}
                </h3>
                <div className={`text-4xl font-black mb-2 ${plan.featured ? 'text-black' : 'text-white'}`}>
                  {plan.price}
                </div>
                <div className={`text-sm mb-6 ${plan.featured ? 'text-black/60' : 'text-gray-500'}`}>
                  Capital: {plan.capital}
                </div>
                <button
                  onClick={handleStart}
                  className={`w-full py-4 rounded-xl font-black uppercase tracking-wider transition-all ${plan.featured
                    ? 'bg-black text-white hover:bg-black/80'
                    : 'bg-white/10 hover:bg-white/20 text-white'
                    }`}
                >
                  Choisir {plan.name}
                </button>
              </div>
            ))}
          </div>
        </div>
      </section>

    </div>
  );
};

export default LandingPage;
