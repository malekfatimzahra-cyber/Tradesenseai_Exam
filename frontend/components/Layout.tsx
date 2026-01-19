import React from 'react';
import { useStore } from '../store';
import { Location, NavigateFunction } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { usePreferencesStore, Language } from '../preferencesStore';
import { Globe, ChevronDown, Check } from 'lucide-react';
import { Menu, Transition } from '@headlessui/react';

interface LayoutProps {
  children: React.ReactNode;
  location?: Location;
  navigate?: NavigateFunction;
}

const Layout: React.FC<LayoutProps> = ({ children, location, navigate }) => {
  const { activeAccount, currentUser } = useStore();
  const { t, i18n } = useTranslation();
  const { language, setLanguage } = usePreferencesStore();
  const currentBalance = activeAccount?.equity || 0;

  // Map current path to active tab
  const pathToTab: Record<string, string> = {
    '/challenges': 'challenges',
    '/terminal': 'terminal',
    '/leaderboard': 'leaderboard',
    '/news': 'news',
    '/community': 'community',
    '/education': 'education',
    '/settings': 'settings',
    '/marketfeeds': 'marketfeeds',
    '/admin': 'admin',
  };

  const activeTab = location ? pathToTab[location.pathname] || 'challenges' : 'challenges';

  const setActiveTab = (tab: string) => {
    if (navigate) {
      const tabToPath: Record<string, string> = {
        'challenges': '/challenges',
        'terminal': '/terminal',
        'leaderboard': '/leaderboard',
        'news': '/news',
        'community': '/community',
        'education': '/education',
        'settings': '/settings',
        'marketfeeds': '/marketfeeds',
        'admin': '/admin',
      };
      navigate(tabToPath[tab] || '/challenges');
    }
  };

  // Navigate back to Home (Landing Page)
  const goHome = () => {
    if (navigate) navigate('/');
  };

  const menuItems = [
    { id: 'challenges', icon: 'fa-tags', label: t('sidebar.challenges') },
    { id: 'terminal', icon: 'fa-chart-line', label: t('sidebar.terminal') },
    { id: 'leaderboard', icon: 'fa-trophy', label: t('sidebar.leaderboard') },
    { id: 'news', icon: 'fa-newspaper', label: t('sidebar.newsHub') },
    { id: 'community', icon: 'fa-users', label: t('sidebar.community') },
    { id: 'education', icon: 'fa-graduation-cap', label: t('sidebar.academy') },
    { id: 'marketfeeds', icon: 'fa-chart-simple', label: t('sidebar.marketFeeds') },
    { id: 'settings', icon: 'fa-cog', label: t('sidebar.settings') },
  ];



  return (
    <div className="flex h-screen h-dvh w-full overflow-hidden bg-gray-50 dark:bg-[#050505] text-gray-900 dark:text-gray-100 font-sans selection:bg-blue-500 selection:text-white">
      {/* GLASSMORPHIC LEFT SIDEBAR */}
      <aside className="w-20 lg:w-64 flex-shrink-0 flex flex-col border-r border-gray-200 dark:border-white/5 bg-white dark:bg-black/40 backdrop-blur-md relative z-50 shadow-lg dark:shadow-none">
        <div className="p-8 flex items-center justify-center lg:justify-start gap-3 cursor-pointer" onClick={goHome}>
          <div className="w-10 h-10 bg-gradient-to-br from-yellow-400 to-yellow-600 rounded-xl flex items-center justify-center shadow-[0_0_20px_rgba(234,179,8,0.2)]">
            <i className="fas fa-bolt text-black text-xl"></i>
          </div>
          <h1 className="hidden lg:block text-lg font-black tracking-tighter uppercase text-gray-900 dark:text-white">
            TradeSense <span className="text-yellow-500">AI</span>
          </h1>
        </div>

        <nav className="flex-1 mt-4 px-4 space-y-2 overflow-y-auto no-scrollbar">
          {menuItems.map((item) => (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center justify-center lg:justify-start gap-4 p-4 rounded-xl transition-all duration-300 group relative overflow-hidden ${activeTab === item.id
                ? 'bg-yellow-50 dark:bg-white/5 text-yellow-600 dark:text-yellow-500 shadow-md dark:shadow-[0_0_15px_-5px_rgba(234,179,8,0.3)] border border-yellow-200 dark:border-yellow-500/20'
                : 'text-gray-500 dark:text-gray-500 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-white/5'
                }`}
            >
              <i className={`fas ${item.icon} text-lg w-6 transition-transform group-hover:scale-110`}></i>
              <span className="hidden lg:block font-bold text-xs uppercase tracking-widest">{item.label}</span>
              {activeTab === item.id && <div className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-6 bg-yellow-500 rounded-r-full shadow-[0_0_10px_#eab308]"></div>}
            </button>
          ))}
        </nav>

        <div className="p-4 mt-auto">
          <div className="flex items-center gap-3 px-4 py-3 bg-[#161a1e] border border-white/5 rounded-2xl shadow-inner">
            <div className="relative flex h-2 w-2">
              <div className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></div>
              <div className="relative inline-flex rounded-full h-2 w-2 bg-green-500 shadow-[0_0_10px_#22c55e]"></div>
            </div>
            <p className="text-sm font-black text-white tracking-tight">
              {currentBalance.toLocaleString('fr-MA', { minimumFractionDigits: 2 })} <span className="text-[10px] text-gray-500 ml-1">MAD</span>
            </p>
          </div>
        </div>
      </aside>

      <main className="flex-1 flex flex-col min-w-0 h-full overflow-hidden relative bg-gray-50 dark:bg-[url('https://grainy-gradients.vercel.app/noise.svg')] dark:bg-opacity-20">
        <header className="flex-shrink-0 h-20 border-b border-gray-200 dark:border-white/5 flex items-center justify-between px-6 lg:px-10 bg-white dark:bg-black/20 backdrop-blur-xl sticky top-0 z-40 shadow-sm dark:shadow-none">
          <div className="flex items-center gap-6">
            {/* Back Arrow */}
            <button
              onClick={goHome}
              className="w-10 h-10 flex items-center justify-center rounded-xl bg-gray-100 dark:bg-white/5 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white hover:bg-gray-200 dark:hover:bg-white/10 transition-all border border-gray-200 dark:border-white/5"
              title="Back to Home"
            >
              <i className="fas fa-arrow-left"></i>
            </button>

            <div className="flex items-center gap-3">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500 shadow-[0_0_10px_#22c55e]"></span>
              </span>
              <span className="text-[10px] font-black text-gray-500 dark:text-gray-400 uppercase tracking-[0.2em] group-hover:text-green-500 transition-colors">
                {t('sidebar.feedsStatus')} <span className="text-green-500 glow-text">{t('common.live')}</span>
              </span>
            </div>
          </div>
          <div className="flex items-center gap-6">
            {/* Language Picker */}
            <Menu as="div" className="relative">
              <Menu.Button className="flex items-center gap-2 px-3 py-1.5 rounded-xl hover:bg-gray-100 dark:hover:bg-white/5 transition-all border border-transparent hover:border-gray-200 dark:hover:border-white/10 group">
                <Globe className="w-4 h-4 text-gray-500 group-hover:text-yellow-500 transition-colors" />
                <span className="text-[10px] font-black uppercase tracking-widest text-gray-600 dark:text-gray-400">
                  {language === 'en' ? 'EN' : language === 'fr' ? 'FR' : 'AR'}
                </span>
                <ChevronDown className="w-3 h-3 text-gray-400" />
              </Menu.Button>
              <Transition
                as={React.Fragment}
                enter="transition ease-out duration-100"
                enterFrom="transform opacity-0 scale-95"
                enterTo="transform opacity-100 scale-100"
                leave="transition ease-in duration-75"
                leaveFrom="transform opacity-100 scale-100"
                leaveTo="transform opacity-0 scale-95"
              >
                <Menu.Items className="absolute right-0 mt-2 w-40 origin-top-right rounded-2xl bg-white dark:bg-[#161a1e] border border-gray-200 dark:border-[#1e2329] shadow-2xl focus:outline-none z-50 overflow-hidden">
                  <div className="p-1">
                    {[
                      { code: 'en', label: 'English', flag: '🇬🇧' },
                      { code: 'fr', label: 'Français', flag: '🇫🇷' },
                      { code: 'ar', label: 'العربية', flag: '🇲🇦' }
                    ].map((l) => (
                      <Menu.Item key={l.code}>
                        {({ active }) => (
                          <button
                            onClick={() => {
                              setLanguage(l.code as Language);
                              i18n.changeLanguage(l.code);
                            }}
                            className={`${active ? 'bg-gray-50 dark:bg-white/5' : ''} ${language === l.code ? 'text-yellow-600 dark:text-yellow-500' : 'text-gray-700 dark:text-gray-300'} group flex w-full items-center justify-between rounded-xl px-3 py-2 text-xs font-bold transition-colors`}
                          >
                            <span className="flex items-center gap-2">
                              <span>{l.flag}</span>
                              {l.label}
                            </span>
                            {language === l.code && <Check className="w-3 h-3 animate-in zoom-in" />}
                          </button>
                        )}
                      </Menu.Item>
                    ))}
                  </div>
                </Menu.Items>
              </Transition>
            </Menu>

            <button className="hidden md:flex items-center gap-2 px-4 py-2 bg-yellow-500/10 text-yellow-600 dark:text-yellow-500 rounded-full border border-yellow-500/20 font-black text-[10px] uppercase tracking-wider hover:bg-yellow-500/20 transition-all shadow-[0_0_15px_-5px_rgba(234,179,8,0.3)]">
              <i className="fas fa-gem"></i> {t('sidebar.premiumExpert')}
            </button>
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-gray-300 to-gray-500 dark:from-gray-700 dark:to-gray-900 border border-gray-300 dark:border-white/10 ring-2 ring-gray-100 dark:ring-black"></div>
          </div>
        </header>
        {/* Scrollable Content Area */}
        <div className="flex-1 overflow-y-auto min-h-0 scroll-smooth custom-scrollbar">
          {children}
        </div>
      </main>
    </div>
  );
};

export default Layout;