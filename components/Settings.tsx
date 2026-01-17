import React, { useState, useEffect, Fragment } from 'react';
import { useTranslation } from 'react-i18next';
import { usePreferencesStore, Theme, Language } from '../preferencesStore';
import { useStore } from '../store';
import { Dialog, Transition } from '@headlessui/react';
import {
  User, Shield, Sliders, Palette, Bell,
  Activity, Lock, LogOut, Trash2, Globe, moon,
  AlertTriangle, Save, CheckCircle
} from 'lucide-react';

// --- Reusable Components ---

interface SettingToggleProps {
  label: string;
  description?: string;
  checked: boolean;
  onChange: (checked: boolean) => void;
  disabled?: boolean;
}

const SettingToggle: React.FC<SettingToggleProps> = ({ label, description, checked, onChange, disabled }) => (
  <div className={`flex items-center justify-between p-4 rounded-2xl border transition-all ${checked
    ? 'bg-yellow-500/5 border-yellow-500/20'
    : 'bg-gray-50 dark:bg-black/20 border-transparent hover:border-gray-200 dark:hover:border-gray-800'
    } ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}>
    <div>
      <h3 className="font-bold text-gray-900 dark:text-white text-sm">{label}</h3>
      {description && <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">{description}</p>}
    </div>
    <button
      onClick={() => !disabled && onChange(!checked)}
      className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:ring-offset-2 dark:focus:ring-offset-black ${checked ? 'bg-yellow-500' : 'bg-gray-200 dark:bg-gray-700'
        }`}
    >
      <span
        className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${checked ? 'translate-x-6' : 'translate-x-1'
          }`}
      />
    </button>
  </div>
);

interface SettingSelectProps {
  label: string;
  description?: string;
  value: string;
  options: { value: string; label: string }[];
  onChange: (value: string) => void;
}

const SettingSelect: React.FC<SettingSelectProps> = ({ label, description, value, options, onChange }) => (
  <div className="flex flex-col sm:flex-row sm:items-center justify-between p-4 rounded-2xl bg-gray-50 dark:bg-black/20 border border-transparent hover:border-gray-200 dark:hover:border-gray-800 transition-all gap-4">
    <div>
      <h3 className="font-bold text-gray-900 dark:text-white text-sm">{label}</h3>
      {description && <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">{description}</p>}
    </div>
    <select
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="bg-white dark:bg-[#0b0e11] border border-gray-200 dark:border-[#1e2329] rounded-lg py-2 pl-3 pr-8 text-sm font-medium text-gray-900 dark:text-white focus:outline-none focus:ring-1 focus:ring-yellow-500 transition-all cursor-pointer min-w-[150px]"
    >
      {options.map((opt) => (
        <option key={opt.value} value={opt.value}>{opt.label}</option>
      ))}
    </select>
  </div>
);

// --- Main Component ---

const Settings: React.FC = () => {
  const { t, i18n } = useTranslation();
  const { theme, language, setTheme, setLanguage } = usePreferencesStore();
  const { currentUser, activeAccount } = useStore();

  // Navigation State
  const [activeSection, setActiveSection] = useState<'profile' | 'security' | 'preferences' | 'appearance' | 'notifications' | 'trading' | 'privacy' | 'session' | 'danger'>('profile');

  // Modals
  const [isLogoutModalOpen, setIsLogoutModalOpen] = useState(false);
  const [isResetDataModalOpen, setIsResetDataModalOpen] = useState(false);
  const [isClearProgressModalOpen, setIsClearProgressModalOpen] = useState(false);

  // --- Local State for Settings ---

  // Profile
  const [profile, setProfile] = useState({
    name: '',
    username: '',
    email: '',
    accountType: 'Standard',
    accountNumber: '',
    joinDate: ''
  });

  // Security
  const [security, setSecurity] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  });

  // Notifications
  const [notifications, setNotifications] = useState({
    priceAlerts: true,
    riskAlerts: true,
    newsAlerts: true,
    weeklyProgress: false
  });

  // Trading Preferences
  const [tradingPrefs, setTradingPrefs] = useState({
    defaultMarket: 'Crypto',
    defaultPositionSize: '1000',
    confirmTrades: true,
    oneClickTrade: false
  });

  // Privacy
  const [privacy, setPrivacy] = useState({
    showOnLeaderboard: true,
    shareAnalytics: true
  });

  // Initial Load & Effect Sync
  useEffect(() => {
    // 1. Load Profile from Store/User
    if (currentUser) {
      setProfile({
        name: currentUser.name || '',
        username: currentUser.username || currentUser.email?.split('@')[0] || '',
        email: currentUser.email || '',
        accountType: activeAccount?.planId ?
          (activeAccount.planId === 'starter' ? 'Starter Challenge' :
            activeAccount.planId === 'pro' ? 'Professional Pro' :
              activeAccount.planId === 'elite' ? 'Elite Institutional' : 'Standard') : 'Standard',
        accountNumber: activeAccount?.id || 'N/A',
        joinDate: currentUser.joinedAt || new Date().toISOString()
      });


    }

    // 2. Load Persisted Settings
    const savedNotifs = localStorage.getItem('settings_notifications');
    if (savedNotifs) setNotifications(JSON.parse(savedNotifs));

    const savedTrading = localStorage.getItem('settings_trading');
    if (savedTrading) setTradingPrefs(JSON.parse(savedTrading));

    const savedPrivacy = localStorage.getItem('settings_privacy');
    if (savedPrivacy) setPrivacy(JSON.parse(savedPrivacy));

  }, [currentUser, activeAccount]);

  // Persistence Effects
  useEffect(() => localStorage.setItem('settings_notifications', JSON.stringify(notifications)), [notifications]);
  useEffect(() => localStorage.setItem('settings_trading', JSON.stringify(tradingPrefs)), [tradingPrefs]);
  useEffect(() => localStorage.setItem('settings_privacy', JSON.stringify(privacy)), [privacy]);


  // --- Handlers ---

  const handleLogout = async () => {
    try {
      // 1. Call Backend (best effort)
      const token = localStorage.getItem('auth_token');
      if (token) {
        await fetch('http://127.0.0.1:5000/api/auth/logout', {
          method: 'POST',
          headers: { 'Authorization': `Bearer ${token}` }
        }).catch(() => { }); // Ignore errors if backend endpoint missing
      }
    } finally {
      // 2. Clear Local Data
      localStorage.removeItem('auth_token');
      localStorage.removeItem('user');
      localStorage.removeItem('tradesense-storage'); // store.ts persist
      sessionStorage.clear();

      // 3. Hard Redirect
      window.location.href = '/';
    }
  };

  const handleResetLocalData = () => {
    localStorage.removeItem('settings_notifications');
    localStorage.removeItem('settings_trading');
    localStorage.removeItem('settings_privacy');
    localStorage.removeItem('preferences');
    // Reload to apply
    window.location.reload();
  };

  const handleClearCourseProgress = () => {
    localStorage.removeItem('course_progress'); // Assuming key name
    alert("Course progress has been reset.");
    setIsClearProgressModalOpen(false);
  };

  const menuItems = [
    { id: 'profile', label: t('settings.nav.profile'), icon: User, group: 'management' },
    { id: 'security', label: t('settings.nav.security'), icon: Shield, group: 'management' },
    { id: 'preferences', label: t('settings.nav.preferences'), icon: Sliders, group: 'management' },
    { id: 'appearance', label: t('settings.nav.appearance'), icon: Palette, group: 'management' },

    { id: 'notifications', label: t('settings.notifications.title'), icon: Bell, group: 'appSettings' },
    { id: 'trading', label: t('settings.trading.title'), icon: Activity, group: 'appSettings' },
    { id: 'privacy', label: t('settings.privacy.title'), icon: Lock, group: 'appSettings' },

    { id: 'session', label: t('settings.session.title'), icon: LogOut, group: 'system' },
    { id: 'danger', label: t('settings.danger.title'), icon: AlertTriangle, group: 'system', danger: true },
  ];

  return (
    <div className="p-6 h-full bg-gray-100 dark:bg-[#0b0e11] overflow-y-auto transition-colors duration-300">
      <div className="max-w-5xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-extrabold text-gray-900 dark:text-white mb-2 tracking-tight">Settings</h1>
          <p className="text-gray-500 dark:text-gray-400">Manage your account, preferences, and workspace configuration.</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">

          {/* Navigation Sidebar */}
          <div className="lg:col-span-1">
            <div className="bg-white dark:bg-[#161a1e] rounded-3xl border border-gray-200 dark:border-[#1e2329] p-4 shadow-sm sticky top-6">
              <nav className="space-y-6">
                {['management', 'appSettings', 'system'].map((group) => (
                  <div key={group}>
                    <h3 className="text-[10px] font-black text-gray-400 uppercase tracking-widest px-4 mb-2">{t(`settings.groups.${group}`)}</h3>
                    <div className="space-y-1">
                      {menuItems.filter(item => item.group === group).map((item) => (
                        <button
                          key={item.id}
                          onClick={() => setActiveSection(item.id as any)}
                          className={`w-full flex items-center gap-3 px-4 py-2.5 rounded-xl font-bold text-sm transition-all ${activeSection === item.id
                            ? item.danger
                              ? 'bg-red-500/10 text-red-500 border border-red-500/20'
                              : 'bg-yellow-500/10 text-yellow-500 border border-yellow-500/20'
                            : 'text-gray-500 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-[#1e2329] hover:text-gray-900 dark:hover:text-white'
                            }`}
                        >
                          <item.icon className="w-4 h-4" />
                          {item.label}
                        </button>
                      ))}
                    </div>
                  </div>
                ))}
              </nav>
            </div>
          </div>

          {/* Setting Content Area */}
          <div className="lg:col-span-3 space-y-6">

            {/* PROFILE SECTION */}
            {activeSection === 'profile' && (
              <div className="bg-white dark:bg-[#161a1e] rounded-3xl border border-gray-200 dark:border-[#1e2329] p-8 shadow-sm animate-in fade-in duration-300">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">{t('settings.profile.title')}</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">{t('settings.profile.fullName')}</label>
                    <input type="text" value={profile.name} onChange={e => setProfile({ ...profile, name: e.target.value })} className="w-full bg-gray-50 dark:bg-[#0b0e11] border border-gray-200 dark:border-[#1e2329] rounded-xl py-3 px-4 font-medium text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-yellow-500/50" />
                  </div>
                  <div>
                    <label className="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">{t('settings.profile.username')}</label>
                    <div className="w-full bg-gray-50 dark:bg-[#0b0e11] border border-transparent rounded-xl py-3 px-4 font-medium text-gray-500">{profile.username}</div>
                  </div>
                  <div className="md:col-span-2">
                    <label className="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">{t('settings.profile.email')}</label>
                    <input type="email" value={profile.email} onChange={e => setProfile({ ...profile, email: e.target.value })} className="w-full bg-gray-50 dark:bg-[#0b0e11] border border-gray-200 dark:border-[#1e2329] rounded-xl py-3 px-4 font-medium text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-yellow-500/50" />
                  </div>
                  <div>
                    <label className="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">{t('settings.profile.accountType')}</label>
                    <div className="w-full bg-yellow-500/10 border border-yellow-500/20 rounded-xl py-3 px-4 font-bold text-yellow-600 dark:text-yellow-500">{profile.accountType}</div>
                  </div>
                  <div>
                    <label className="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">{t('settings.profile.joinDate')}</label>
                    <div className="w-full bg-gray-50 dark:bg-[#0b0e11] border border-transparent rounded-xl py-3 px-4 font-medium text-gray-500">{new Date(profile.joinDate).toLocaleDateString()}</div>
                  </div>
                </div>
                <div className="mt-8 pt-6 border-t border-gray-100 dark:border-[#1e2329] flex justify-end">
                  <button className="px-6 py-3 bg-gray-900 dark:bg-white text-white dark:text-black font-bold rounded-xl hover:opacity-90 transition-opacity flex items-center gap-2">
                    <Save className="w-4 h-4" /> {t('settings.profile.updateBtn')}
                  </button>
                </div>
              </div>
            )}

            {/* SECURITY SECTION */}
            {activeSection === 'security' && (
              <div className="bg-white dark:bg-[#161a1e] rounded-3xl border border-gray-200 dark:border-[#1e2329] p-8 shadow-sm animate-in fade-in duration-300">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">{t('settings.security.title')}</h2>
                <div className="space-y-6 max-w-lg">
                  <div>
                    <label className="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">{t('settings.security.currentPwd')}</label>
                    <input type="password" value={security.currentPassword} onChange={e => setSecurity({ ...security, currentPassword: e.target.value })} className="w-full bg-gray-50 dark:bg-[#0b0e11] border border-gray-200 dark:border-[#1e2329] rounded-xl py-3 px-4 font-medium focus:outline-none focus:ring-2 focus:ring-yellow-500/50" />
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">{t('settings.security.newPwd')}</label>
                      <input type="password" value={security.newPassword} onChange={e => setSecurity({ ...security, newPassword: e.target.value })} className="w-full bg-gray-50 dark:bg-[#0b0e11] border border-gray-200 dark:border-[#1e2329] rounded-xl py-3 px-4 font-medium focus:outline-none focus:ring-2 focus:ring-yellow-500/50" />
                    </div>
                    <div>
                      <label className="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">{t('settings.security.confirmPwd')}</label>
                      <input type="password" value={security.confirmPassword} onChange={e => setSecurity({ ...security, confirmPassword: e.target.value })} className="w-full bg-gray-50 dark:bg-[#0b0e11] border border-gray-200 dark:border-[#1e2329] rounded-xl py-3 px-4 font-medium focus:outline-none focus:ring-2 focus:ring-yellow-500/50" />
                    </div>
                  </div>
                  <button className="px-6 py-3 bg-gray-900 dark:bg-white text-white dark:text-black font-bold rounded-xl hover:opacity-90 transition-opacity">
                    {t('settings.security.updateBtn')}
                  </button>
                </div>
              </div>
            )}

            {/* NOTIFICATIONS SECTION */}
            {activeSection === 'notifications' && (
              <div className="bg-white dark:bg-[#161a1e] rounded-3xl border border-gray-200 dark:border-[#1e2329] p-8 shadow-sm animate-in fade-in duration-300">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">{t('settings.notifications.title')}</h2>
                <div className="space-y-4">
                  <SettingToggle
                    label={t('settings.notifications.priceAlerts')}
                    description={t('settings.notifications.priceDesc')}
                    checked={notifications.priceAlerts}
                    onChange={v => setNotifications({ ...notifications, priceAlerts: v })}
                  />
                  <SettingToggle
                    label={t('settings.notifications.riskAlerts')}
                    description={t('settings.notifications.riskDesc')}
                    checked={notifications.riskAlerts}
                    onChange={v => setNotifications({ ...notifications, riskAlerts: v })}
                  />
                  <SettingToggle
                    label={t('settings.notifications.newsAlerts')}
                    description={t('settings.notifications.newsDesc')}
                    checked={notifications.newsAlerts}
                    onChange={v => setNotifications({ ...notifications, newsAlerts: v })}
                  />
                  <SettingToggle
                    label={t('settings.notifications.weekly')}
                    description={t('settings.notifications.weeklyDesc')}
                    checked={notifications.weeklyProgress}
                    onChange={v => setNotifications({ ...notifications, weeklyProgress: v })}
                  />
                </div>
              </div>
            )}

            {/* TRADING PREFERENCES SECTION */}
            {activeSection === 'trading' && (
              <div className="bg-white dark:bg-[#161a1e] rounded-3xl border border-gray-200 dark:border-[#1e2329] p-8 shadow-sm animate-in fade-in duration-300">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">{t('settings.trading.title')}</h2>
                <div className="space-y-6">
                  <SettingSelect
                    label={t('settings.trading.defaultMarket')}
                    description={t('settings.trading.defaultMarketDesc')}
                    value={tradingPrefs.defaultMarket}
                    onChange={v => setTradingPrefs({ ...tradingPrefs, defaultMarket: v })}
                    options={[
                      { value: 'Crypto', label: 'Cryptocurrency (Crypto)' },
                      { value: 'US Stocks', label: 'US Stocks (NASDAQ)' },
                      { value: 'Forex', label: 'Foreign Exchange (Forex)' },
                      { value: 'Casablanca', label: 'Casablanca Bourse (BVC)' }
                    ]}
                  />

                  <div>
                    <label className="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">{t('settings.trading.positionSize')}</label>
                    <input
                      type="number"
                      value={tradingPrefs.defaultPositionSize}
                      onChange={e => setTradingPrefs({ ...tradingPrefs, defaultPositionSize: e.target.value })}
                      className="w-full bg-gray-50 dark:bg-[#0b0e11] border border-gray-200 dark:border-[#1e2329] rounded-xl py-3 px-4 font-bold text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-yellow-500/50"
                    />
                    <p className="text-xs text-gray-400 mt-2">{t('settings.trading.positionDesc')}</p>
                  </div>

                  <div className="border-t border-gray-100 dark:border-[#1e2329] pt-6 space-y-4">
                    <SettingToggle
                      label={t('settings.trading.confirm')}
                      description={t('settings.trading.confirmDesc')}
                      checked={tradingPrefs.confirmTrades}
                      onChange={v => {
                        setTradingPrefs({
                          ...tradingPrefs,
                          confirmTrades: v,
                          oneClickTrade: v ? tradingPrefs.oneClickTrade : false
                        });
                      }}
                    />
                    <SettingToggle
                      label={t('settings.trading.oneClick')}
                      description={t('settings.trading.oneClickDesc')}
                      checked={tradingPrefs.oneClickTrade}
                      onChange={v => setTradingPrefs({ ...tradingPrefs, oneClickTrade: v })}
                      disabled={tradingPrefs.confirmTrades}
                    />
                  </div>
                </div>
              </div>
            )}

            {/* PRIVACY SECTION */}
            {activeSection === 'privacy' && (
              <div className="bg-white dark:bg-[#161a1e] rounded-3xl border border-gray-200 dark:border-[#1e2329] p-8 shadow-sm animate-in fade-in duration-300">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">{t('settings.privacy.title')}</h2>
                <div className="space-y-4">
                  <SettingToggle
                    label={t('settings.privacy.public')}
                    description={t('settings.privacy.publicDesc')}
                    checked={privacy.showOnLeaderboard}
                    onChange={v => setPrivacy({ ...privacy, showOnLeaderboard: v })}
                  />
                  <SettingToggle
                    label={t('settings.privacy.analytics')}
                    description={t('settings.privacy.analyticsDesc')}
                    checked={privacy.shareAnalytics}
                    onChange={v => setPrivacy({ ...privacy, shareAnalytics: v })}
                  />
                </div>
              </div>
            )}

            {/* APPEARANCE SECTION */}
            {activeSection === 'appearance' && (
              <div className="bg-white dark:bg-[#161a1e] rounded-3xl border border-gray-200 dark:border-[#1e2329] p-8 shadow-sm animate-in fade-in duration-300">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">Appearance</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

                  {/* Theme */}
                  <div className="space-y-3">
                    <h3 className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">{t('settings.appearance.title')}</h3>
                    {(['dark', 'light', 'system'] as const).map((mode) => (
                      <button
                        key={mode}
                        onClick={() => setTheme(mode)}
                        className={`w-full flex items-center justify-between p-4 rounded-xl border transition-all ${theme === mode ? 'bg-yellow-500/10 border-yellow-500 text-yellow-600 dark:text-yellow-500 font-bold' : 'bg-gray-50 dark:bg-black/20 border-transparent hover:border-gray-200 dark:hover:border-white/10'
                          }`}
                      >
                        <span className="capitalize">{t(`settings.appearance.${mode === 'system' ? 'system' : mode === 'dark' ? 'darkMode' : 'lightMode'}`)}</span>
                        {theme === mode && <CheckCircle className="w-5 h-5 text-yellow-500" />}
                      </button>
                    ))}
                  </div>

                  {/* Language */}
                  <div className="space-y-3">
                    <h3 className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">{t('settings.language.title')}</h3>
                    {[
                      { code: 'en', label: 'English', flag: '🇬🇧' },
                      { code: 'fr', label: 'Français', flag: '🇫🇷' },
                      { code: 'ar', label: 'العربية', flag: '🇲🇦' }
                    ].map((l) => (
                      <button
                        key={l.code}
                        onClick={() => { setLanguage(l.code as Language); i18n.changeLanguage(l.code); }}
                        className={`w-full flex items-center justify-between p-4 rounded-xl border transition-all ${language === l.code ? 'bg-blue-500/10 border-blue-500 text-blue-600 dark:text-blue-500 font-bold' : 'bg-gray-50 dark:bg-black/20 border-transparent hover:border-gray-200 dark:hover:border-white/10'
                          }`}
                      >
                        <span className="flex items-center gap-2 text-sm">{l.flag} {l.label}</span>
                        {language === l.code && <CheckCircle className="w-5 h-5 text-blue-500" />}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* SESSION SECTION */}
            {activeSection === 'session' && (
              <div className="bg-white dark:bg-[#161a1e] rounded-3xl border border-gray-200 dark:border-[#1e2329] p-8 shadow-sm animate-in fade-in duration-300">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">{t('settings.session.title')}</h2>
                <div className="p-6 bg-red-50 dark:bg-red-900/10 rounded-2xl border border-red-100 dark:border-red-900/30 flex items-center justify-between">
                  <div>
                    <h3 className="font-bold text-red-700 dark:text-red-400">{t('settings.session.signOut')}</h3>
                    <p className="text-sm text-red-600/80 dark:text-red-400/70 mt-1">{t('settings.session.signOutDesc')}</p>
                  </div>
                  <button onClick={() => setIsLogoutModalOpen(true)} className="px-6 py-2 bg-red-600 hover:bg-red-700 text-white font-bold rounded-xl transition-colors shadow-lg shadow-red-500/20">
                    {t('settings.session.btn')}
                  </button>
                </div>
              </div>
            )}

            {/* DANGER ZONE */}
            {activeSection === 'danger' && (
              <div className="bg-white dark:bg-[#161a1e] rounded-3xl border border-red-200 dark:border-red-900/30 p-8 shadow-sm animate-in fade-in duration-300 relative overflow-hidden">
                <div className="absolute top-0 right-0 p-4 opacity-5">
                  <AlertTriangle className="w-32 h-32 text-red-500" />
                </div>
                <h2 className="text-2xl font-bold text-red-600 dark:text-red-500 mb-6">{t('settings.danger.title')}</h2>

                <div className="space-y-6">
                  <div className="flex items-center justify-between p-4 border-b border-gray-100 dark:border-[#1e2329]">
                    <div>
                      <h3 className="font-bold text-gray-900 dark:text-white">{t('settings.danger.reset')}</h3>
                      <p className="text-xs text-gray-500">{t('settings.danger.resetDesc')}</p>
                    </div>
                    <button onClick={() => setIsResetDataModalOpen(true)} className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-xs font-bold hover:bg-gray-100 dark:hover:bg-white/5 transition-colors">
                      {t('settings.danger.btnReset')}
                    </button>
                  </div>

                  <div className="flex items-center justify-between p-4">
                    <div>
                      <h3 className="font-bold text-gray-900 dark:text-white">{t('settings.danger.clear')}</h3>
                      <p className="text-xs text-gray-500">{t('settings.danger.clearDesc')}</p>
                    </div>
                    <button onClick={() => setIsClearProgressModalOpen(true)} className="px-4 py-2 border border-red-200 dark:border-red-900/50 text-red-600 dark:text-red-500 rounded-lg text-xs font-bold hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors">
                      {t('settings.danger.btnClear')}
                    </button>
                  </div>
                </div>
              </div>
            )}

          </div>
        </div>
      </div>

      {/* --- MODALS --- */}

      {/* Logout Modal */}
      <ConfirmModal
        isOpen={isLogoutModalOpen}
        onClose={() => setIsLogoutModalOpen(false)}
        onConfirm={handleLogout}
        title={t('settings.session.modalTitle')}
        description={t('settings.session.modalDesc')}
        confirmText={t('settings.session.btn')}
        confirmColor="red"
      />

      {/* Reset Data Modal */}
      <ConfirmModal
        isOpen={isResetDataModalOpen}
        onClose={() => setIsResetDataModalOpen(false)}
        onConfirm={() => { handleResetLocalData(); setIsResetDataModalOpen(false); }}
        title={t('settings.danger.reset')}
        description={t('settings.danger.resetDesc')}
        confirmText={t('settings.danger.btnReset')}
        confirmColor="red"
      />

      {/* Clear Progress Modal */}
      <ConfirmModal
        isOpen={isClearProgressModalOpen}
        onClose={() => setIsClearProgressModalOpen(false)}
        onConfirm={handleClearCourseProgress}
        title={t('settings.danger.clear')}
        description={t('settings.danger.clearDesc')}
        confirmText={t('settings.danger.btnClear')}
        confirmColor="red"
      />

    </div>
  );
};

// --- Helper Modal Component ---

const ConfirmModal: React.FC<{
  isOpen: boolean;
  onClose: () => void;
  onConfirm: () => void;
  title: string;
  description: string;
  confirmText: string;
  confirmColor?: 'red' | 'blue' | 'yellow';
}> = ({ isOpen, onClose, onConfirm, title, description, confirmText, confirmColor = 'blue' }) => {
  const { t } = useTranslation();
  if (!isOpen) return null;

  const colorClasses = {
    red: 'bg-red-600 hover:bg-red-700 focus:ring-red-500',
    blue: 'bg-blue-600 hover:bg-blue-700 focus:ring-blue-500',
    yellow: 'bg-yellow-500 hover:bg-yellow-600 focus:ring-yellow-500 text-black'
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="bg-white dark:bg-[#161a1e] rounded-2xl shadow-2xl max-w-sm w-full p-6 border border-gray-200 dark:border-[#1e2329] transform scale-100 animate-in zoom-in-95 duration-200">
        <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">{title}</h3>
        <p className="text-sm text-gray-500 dark:text-gray-400 mb-6 leading-relaxed">
          {description}
        </p>
        <div className="flex gap-3 justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 text-sm font-bold text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-white/5 rounded-lg transition-colors"
          >
            {t('common.cancel')}
          </button>
          <button
            onClick={onConfirm}
            className={`px-4 py-2 text-sm font-bold text-white rounded-lg transition-colors shadow-lg ${colorClasses[confirmColor]}`}
          >
            {confirmText}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Settings;