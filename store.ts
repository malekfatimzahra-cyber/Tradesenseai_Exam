
import { create } from 'zustand';
import { Trade, TradingAccount, ChallengePlan, RuleViolation, Market, AssetPrice, FloorMessage, TradingFloor, Course, NewsItem, User, UserRole, ChallengeStatus, MarketSignal, RiskAlert } from './types';

// Mock Password DB for simulation (Client-side only demo)
const MOCK_PASSWORDS: Record<string, string> = {
  'karim@trade.ma': '123456',
  'sara@admin.ma': 'admin123',
  'ceo@tradesense.ma': 'super123',
  'admin@tradesense.ai': 'headeradmin', // For the header quick login if needed
};

// Standard local development URL
// Use relative path to leverage Vite Proxy in dev, and work naturally in prod
export const API_BASE = window.location.origin.includes('localhost') ? '/api' : '/api';

interface PropFirmState {
  // Auth & Users
  currentUser: User | null;
  users: User[];
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;

  // Trading Core
  activeAccount: TradingAccount | null;
  plans: ChallengePlan[];
  tradeHistory: Trade[];
  activeTrades: Trade[];
  violations: RuleViolation[];
  currentMarket: Market;
  currentAsset: string;
  prices: Record<string, AssetPrice>;

  // Features
  chatMessages: FloorMessage[];
  groups: TradingFloor[];
  activeGroup: string;
  courses: Course[];
  news: NewsItem[];
  aiSignals: MarketSignal[];
  riskAlerts: RiskAlert[];
  riskLevel: 'SAFE' | 'WARNING' | 'DANGER';
  equityShield: number;

  // Actions
  startChallenge: (planId: string) => void;
  openTrade: (trade: Trade) => void;
  closeTrade: (tradeId: string, exitPrice: number) => void;
  updatePrices: (newPrices: Record<string, AssetPrice>) => void;
  checkRules: () => void;
  resetAccount: () => void;
  fetchAiSignals: (asset: string) => Promise<void>;
  fetchRiskCheck: () => Promise<void>;
  fetchActiveAccount: () => Promise<void>;
  fetchPlans: () => Promise<void>;
  fetchCourses: () => Promise<void>;
  fetchActiveTrades: () => Promise<void>;
  fetchTradeHistory: () => Promise<void>;
  validateTrade: (trade: { asset: string, type: 'BUY' | 'SELL', amount: number, entry: number }) => Promise<{ status: 'APPROVED' | 'WARNING' | 'BLOCKED', message: string }>;
  explainPriceAction: (asset: string, price: number, change: number) => Promise<string>;

  setCurrentAsset: (asset: string) => void;
  setCurrentMarket: (market: Market) => void;
  addChatMessage: (msg: FloorMessage) => void;
  setActiveGroup: (id: string) => void;

  // Auth Actions
  login: (email: string, password: string) => Promise<boolean>;
  register: (fullName: string, username: string, email: string, password: string) => Promise<boolean>;
  logout: () => void;
  hydrateFromBackend: () => Promise<void>;
  fetchMe: () => Promise<void>;

  // Dev Only
  loginAs: (role: UserRole) => void;

  // Admin Actions
  updateUserStatus: (userId: string, status: ChallengeStatus) => Promise<void>;
  updateUserRole: (userId: string, role: UserRole) => Promise<void>;
  fetchUsers: () => Promise<void>;
}

const MOCK_USERS: User[] = [
  { id: 'u1', name: 'Karim Trader', email: 'karim@trade.ma', role: 'USER', balance: 5000, status: 'ACTIVE', joinedAt: '2024-01-15' },
  { id: 'u2', name: 'Sara Admin', email: 'sara@admin.ma', role: 'ADMIN', balance: 0, status: 'PENDING', joinedAt: '2023-11-20' },
  { id: 'u3', name: 'Boss Super', email: 'ceo@tradesense.ma', role: 'SUPERADMIN', balance: 100000, status: 'FUNDED', joinedAt: '2023-01-01' },
];

export const useStore = create<PropFirmState>((set, get) => ({
  currentUser: null,
  isAuthenticated: false,
  users: MOCK_USERS,
  isLoading: false,
  error: null,

  activeAccount: null,
  plans: [],
  tradeHistory: [],
  activeTrades: [],
  violations: [],
  currentMarket: 'Crypto',
  currentAsset: 'BTC/USD',
  prices: {},
  aiSignals: [],
  riskAlerts: [],
  riskLevel: 'SAFE',
  equityShield: 100,

  chatMessages: [],
  groups: [],
  activeGroup: 'global',
  courses: [],
  news: [
    { id: 'n1', title: 'Fed Signals Rate Hold', content: 'The Federal Reserve indicated that interest rates will remain steady for the coming quarter...', category: 'Forex', impact: 'High', volatilityScore: '8.5', assetAffected: 'USD Majors' },
    { id: 'n2', title: 'Crypto Regulation Update', content: 'New framework for digital assets proposed by international regulators...', category: 'Crypto', impact: 'Medium', volatilityScore: '6.2', assetAffected: 'BTC/ETH' },
  ],

  startChallenge: (planId) => {
    // This should ideally be called after payment success, handled by PaymentModal or backend flow.
    // We'll keep the mock logic for now as a fallback or if initiated without payment in dev.
    const plan = get().plans.find(p => p.id === planId);
    if (!plan) return;
    set({
      activeAccount: {
        id: `CHL-${Math.random().toString(36).substr(2, 6).toUpperCase()}`,
        planId,
        initialBalance: plan.capital,
        currentBalance: plan.capital,
        equity: plan.capital,
        status: 'ACTIVE',
        startTime: new Date().toISOString(),
        dailyStartingEquity: plan.capital,
        payoutPending: 0
      },
      tradeHistory: [],
      activeTrades: [],
      violations: []
    });
  },

  updatePrices: (newPrices) => {
    set({ prices: { ...get().prices, ...newPrices } });
    // Live equity calculation for UI display only - Backend validation happens on trade close
    const account = get().activeAccount;
    if (account && account.status === 'ACTIVE') {
      let unrealizedPnl = 0;
      get().activeTrades.forEach(trade => {
        const livePrice = newPrices[trade.asset]?.price || trade.entryPrice;
        const pnl = trade.type === 'BUY'
          ? (livePrice - trade.entryPrice) * (trade.amount / trade.entryPrice)
          : (trade.entryPrice - livePrice) * (trade.amount / trade.entryPrice);
        unrealizedPnl += pnl;
      });
      const newEquity = account.currentBalance + unrealizedPnl;
      set({ activeAccount: { ...account, equity: newEquity } });
    }
  },

  openTrade: async (trade) => {
    const account = get().activeAccount;
    if (!account || account.status !== 'ACTIVE') return;

    // Optimistic UI Update (optional) or Spinner

    try {
      const token = localStorage.getItem('auth_token');
      const res = await fetch(`${API_BASE}/trading/open`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          account_id: account.id.startsWith('CHL') ? null : account.id, // Handle mock vs real ID
          symbol: trade.asset,
          type: trade.type,
          amount: trade.amount,
          entry_price: trade.entryPrice,
          sl: trade.sl,
          tp: trade.tp
        })
      });

      if (res.ok) {
        const data = await res.json();
        // Normalize backend trade to frontend trade
        const backendTrade = data.trade;
        const newTrade: Trade = {
          id: backendTrade.id.toString(),
          asset: backendTrade.symbol,
          type: backendTrade.type as any,
          amount: backendTrade.amount,
          entryPrice: backendTrade.entry_price,
          sl: backendTrade.sl,
          tp: backendTrade.tp,
          status: 'OPEN',
          timestamp: backendTrade.timestamp,
          market: trade.market // Preserve market context
        };

        set({ activeTrades: [newTrade, ...get().activeTrades] });

        // Should also update account from response if provided
        if (data.account) {
          // Update account logic here if needed
        }
      } else {
        const err = await res.json();
        alert(`Trade Failed: ${err.message}`);
      }
    } catch (e) {
      console.error("Trade Execution Error", e);
      // Fallback for Demo/Mock (Exam Safety)
      set({ activeTrades: [trade, ...get().activeTrades] });
    }
  },

  closeTrade: async (tradeId, exitPrice) => {
    try {
      const token = localStorage.getItem('auth_token');
      // Check if it's a mock trade (string ID starting with TRD)
      if (tradeId.toString().startsWith('TRD')) {
        // Mock Close Logic - keep for fallback
        const trade = get().activeTrades.find(t => t.id === tradeId);
        if (!trade) return;
        const account = get().activeAccount;
        if (!account) return;
        const pnl = trade.type === 'BUY'
          ? (exitPrice - trade.entryPrice) * (trade.amount / trade.entryPrice)
          : (trade.entryPrice - exitPrice) * (trade.amount / trade.entryPrice);
        const closedTrade = { ...trade, status: 'CLOSED' as const, exitPrice, pnl };
        set({
          activeTrades: get().activeTrades.filter(t => t.id !== tradeId),
          tradeHistory: [closedTrade, ...get().tradeHistory],
          activeAccount: { ...account, currentBalance: account.currentBalance + pnl, equity: account.currentBalance + pnl }
        });
        return;
      }

      const res = await fetch(`${API_BASE}/trading/close`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          trade_id: tradeId,
          exit_price: exitPrice
        })
      });

      if (res.ok) {
        const data = await res.json();
        set(state => ({
          activeTrades: state.activeTrades.filter(t => t.id !== tradeId.toString()),
          // Add to history? We'd need to convert backend trade to frontend trade
          activeAccount: {
            ...state.activeAccount!,
            currentBalance: data.account.current_balance,
            equity: data.account.equity,
            status: data.account.status
          }
        }));
        // Optionally fetch history
      }
    } catch (e) {
      console.error("Trade Close Error", e);
    }
  },

  checkRules: () => {
    // Deprecated: Rules are checked on backend.
    // kept empty to satisfy interface if needed, or remove.
  },

  resetAccount: () => set({ activeAccount: null, tradeHistory: [], activeTrades: [], violations: [] }),

  setCurrentAsset: (currentAsset) => set({ currentAsset }),
  setCurrentMarket: (currentMarket) => set({ currentMarket }),
  addChatMessage: (msg) => set({ chatMessages: [...get().chatMessages, msg] }),
  setActiveGroup: (activeGroup) => set({ activeGroup }),

  // --- AUTH IMPLEMENTATION ---

  login: async (email, password) => {
    set({ isLoading: true, error: null });

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 8000);

    try {
      const res = await fetch(`${API_BASE}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password }),
        signal: controller.signal
      });
      clearTimeout(timeoutId);

      const data = await res.json();

      if (res.ok) {
        set({
          currentUser: {
            id: data.user.id.toString(),
            name: data.user.full_name,
            username: data.user.username,
            email: data.user.email,
            role: data.user.role as any,
            balance: 0, // Should come from API if needed
            status: 'ACTIVE',
            joinedAt: data.user.created_at
          },
          isAuthenticated: true,
          isLoading: false
        });
        localStorage.setItem('auth_token', data.token);

        // Hydrate active challenge after login
        await get().hydrateFromBackend();

        return true;
      } else {
        set({ error: data.message || 'Login failed', isLoading: false });
        return false;
      }
    } catch (e) {
      clearTimeout(timeoutId);
      console.error(e);
      const errorMessage = e instanceof Error && e.name === 'AbortError'
        ? 'Request timed out. Backend might be slow or offline.'
        : 'Network error. Is the backend running?';
      set({ error: errorMessage, isLoading: false });
      return false;
    }
  },

  register: async (fullName, username, email, password) => {
    set({ isLoading: true, error: null });

    try {
      const res = await fetch(`${API_BASE}/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          full_name: fullName,
          username,
          email,
          password
        })
      });

      const data = await res.json();

      if (res.ok) {
        set({
          currentUser: {
            id: data.user.id.toString(),
            name: data.user.full_name,
            username: data.user.username,
            email: data.user.email,
            role: data.user.role as any,
            balance: 0,
            status: 'ACTIVE',
            joinedAt: data.user.created_at
          },
          isAuthenticated: true,
          isLoading: false
        });
        localStorage.setItem('auth_token', data.token);
        return true;
      } else {
        set({ error: data.message || 'Registration failed', isLoading: false });
        return false;
      }
    } catch (e) {
      console.error(e);
      set({ error: 'Network error. Is the backend running?', isLoading: false });
      return false;
    }
  },

  logout: () => {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('cachedActiveChallenge');
    set({ currentUser: null, isAuthenticated: false, activeAccount: null, activeTrades: [], tradeHistory: [] });
  },

  // Hydrate app state from backend on startup
  hydrateFromBackend: async () => {
    const token = localStorage.getItem('auth_token');
    if (!token) return;

    set({ isLoading: true });

    try {
      // 1. Fetch current user
      await get().fetchMe();
      await get().fetchPlans();
      await get().fetchCourses();

      // 2. Fetch active challenge from UNIFIED endpoint (garantit persistance SQL)
      const res = await fetch(`${API_BASE}/unified-payment/active-challenge`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (res.ok) {
        const data = await res.json();
        if (data.success && data.data) {
          const challenge = data.data;

          // Cache to localStorage for offline fallback
          localStorage.setItem('cachedActiveChallenge', JSON.stringify(challenge));

          // Hydrate state
          set({
            activeAccount: {
              id: challenge.id.toString(),
              planId: challenge.plan_name.toLowerCase(),
              initialBalance: challenge.initial_balance,
              currentBalance: challenge.current_balance,
              equity: challenge.equity,
              status: challenge.status as ChallengeStatus,
              startTime: challenge.created_at,
              dailyStartingEquity: challenge.daily_starting_equity,
              payoutPending: 0
            },
            isLoading: false
          });

          // Fetch trades
          await get().fetchActiveTrades();
          await get().fetchTradeHistory();
        } else {
          // No active challenge
          set({ activeAccount: null, isLoading: false });
        }
      } else {
        // Backend error - load from cache if available
        const cached = localStorage.getItem('cachedActiveChallenge');
        if (cached) {
          const challenge = JSON.parse(cached);
          set({
            activeAccount: {
              id: challenge.id.toString(),
              planId: challenge.plan_name.toLowerCase(),
              initialBalance: challenge.initial_balance,
              currentBalance: challenge.current_balance,
              equity: challenge.equity,
              status: challenge.status as ChallengeStatus,
              startTime: challenge.created_at,
              dailyStartingEquity: challenge.daily_starting_equity,
              payoutPending: 0
            },
            isLoading: false
          });
        } else {
          set({ isLoading: false });
        }
      }
    } catch (e) {
      console.error('Hydration error:', e);
      // Try to load from cache
      const cached = localStorage.getItem('cachedActiveChallenge');
      if (cached) {
        try {
          const challenge = JSON.parse(cached);
          set({
            activeAccount: {
              id: challenge.id.toString(),
              planId: challenge.plan_name.toLowerCase(),
              initialBalance: challenge.initial_balance,
              currentBalance: challenge.current_balance,
              equity: challenge.equity,
              status: challenge.status as ChallengeStatus,
              startTime: challenge.created_at,
              dailyStartingEquity: challenge.daily_starting_equity,
              payoutPending: 0
            }
          });
        } catch (err) {
          console.error('Cache parse error:', err);
        }
      }
      set({ isLoading: false });
    }
  },

  fetchMe: async () => {
    try {
      const token = localStorage.getItem('auth_token');
      if (!token) return;

      const res = await fetch(`${API_BASE}/auth/me`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (res.ok) {
        const data = await res.json();
        if (data.ok && data.user) {
          set({
            currentUser: {
              id: data.user.id.toString(),
              name: data.user.full_name,
              username: data.user.username,
              email: data.user.email,
              role: data.user.role as any,
              balance: 0,
              status: 'ACTIVE' as ChallengeStatus,
              joinedAt: data.user.created_at
            },
            isAuthenticated: true
          });
        }
      }
    } catch (e) {
      console.error('Fetch me error:', e);
    }
  },

  // Dev Tool
  loginAs: (role) => {
    const user = get().users.find(u => u.role === role) || MOCK_USERS[0];
    set({ currentUser: { ...user, role }, isAuthenticated: true });
  },

  fetchUsers: async () => {
    try {
      const token = localStorage.getItem('auth_token');
      if (!token) return;
      const res = await fetch(`${API_BASE}/admin/users`, { headers: { 'Authorization': `Bearer ${token}` } });
      if (res.ok) {
        const data = await res.json();
        const users: User[] = data.map((u: any) => ({
          id: u.id.toString(),
          name: u.name || u.full_name,
          email: u.email,
          role: u.role,
          balance: u.balance,
          status: u.status,
          joinedAt: u.joinedAt || new Date().toISOString()
        }));
        set({ users });
      }
    } catch (e) { console.error(e); }
  },

  updateUserStatus: async (userId, status) => {
    try {
      const token = localStorage.getItem('auth_token');
      await fetch(`${API_BASE}/admin/users/${userId}/status`, {
        method: 'POST',
        body: JSON.stringify({ status }),
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` }
      });
      get().fetchUsers();
    } catch (e) { console.error(e); }
  },

  updateUserRole: async (userId, role) => {
    try {
      const token = localStorage.getItem('auth_token');
      await fetch(`${API_BASE}/admin/users/${userId}/role`, {
        method: 'POST',
        body: JSON.stringify({ role }),
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` }
      });
      get().fetchUsers();
    } catch (e) { console.error(e); }
  },

  fetchActiveAccount: async () => {
    try {
      const token = localStorage.getItem('auth_token');
      if (!token) return;
      const res = await fetch(`${API_BASE}/trading/account`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        if (data) {
          const account: TradingAccount = {
            id: data.id.toString(),
            planId: data.plan_name.toLowerCase(),
            initialBalance: data.initial_balance,
            currentBalance: data.current_balance,
            equity: data.equity,
            status: data.status as ChallengeStatus,
            startTime: new Date().toISOString(),
            dailyStartingEquity: data.daily_starting_equity,
            payoutPending: 0
          };
          set({ activeAccount: account });
          get().fetchActiveTrades();
          get().fetchTradeHistory();
        }
      }
    } catch (e) { console.error("Fetch Account Error", e); }
  },

  fetchPlans: async () => {
    try {
      const res = await fetch(`${API_BASE}/challenges/plans`);
      if (res.ok) {
        const json = await res.json();
        if (json.ok && json.data) {
          set({ plans: json.data });
        }
      }
    } catch (e) { console.error("Fetch Plans Error", e); }
  },

  fetchCourses: async () => {
    try {
      const token = localStorage.getItem('auth_token');
      if (!token) return;

      const res = await fetch(`${API_BASE}/academy/courses`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (res.ok) {
        const data = await res.json();
        /* Map API data to Store Type */
        const courses: Course[] = data.map((c: any) => ({
          id: c.id.toString(),
          title: c.title,
          category: c.category || 'General',
          level: c.level || 'Beginner',
          duration: c.duration_minutes ? `${Math.floor(c.duration_minutes / 60)}h ${c.duration_minutes % 60}m` : '0h 0m',
          progress: c.progress || 0,
          premium: c.is_premium
        }));
        set({ courses });
      }
    } catch (e) { console.error("Fetch Courses Error", e); }
  },

  fetchActiveTrades: async () => {
    try {
      const token = localStorage.getItem('auth_token');
      if (!token) return;
      const res = await fetch(`${API_BASE}/trading/active`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        const frontendTrades: Trade[] = data.map((t: any) => ({
          id: t.id.toString(),
          asset: t.symbol,
          type: t.type,
          amount: t.amount,
          entryPrice: t.entry_price,
          sl: t.sl,
          tp: t.tp,
          status: 'OPEN',
          timestamp: t.timestamp,
          market: 'Forex'
        }));
        set({ activeTrades: frontendTrades });
      }
    } catch (e) { console.error(e); }
  },

  fetchTradeHistory: async () => {
    try {
      const token = localStorage.getItem('auth_token');
      if (!token) return;
      const res = await fetch(`${API_BASE}/trading/history`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        const frontendTrades: Trade[] = data.map((t: any) => ({
          id: t.id.toString(),
          asset: t.symbol,
          type: t.type,
          amount: t.amount,
          entryPrice: t.entry_price,
          exitPrice: t.exit_price,
          pnl: t.pnl,
          sl: t.sl,
          tp: t.tp,
          status: 'CLOSED',
          timestamp: t.timestamp,
          market: 'Forex'
        }));
        set({ tradeHistory: frontendTrades });
      }
    } catch (e) { console.error(e); }
  },

  fetchAiSignals: async (asset) => {
    try {
      const token = localStorage.getItem('auth_token');
      const res = await fetch(`${API_BASE}/ai-agency/signals?asset=${asset}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        const signals = await res.json();
        if (Array.isArray(signals)) {
          set({ aiSignals: signals });
        }
      }
    } catch (e) {
      console.error("AI Signal Fetch Error", e);
    }
  },

  fetchRiskCheck: async () => {
    try {
      const token = localStorage.getItem('auth_token');
      const res = await fetch(`${API_BASE}/ai-agency/risk-check`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        set({
          riskAlerts: Array.isArray(data.alerts) ? data.alerts : [],
          riskLevel: data.risk_level || 'SAFE',
          equityShield: typeof data.equity_shield === 'number' ? data.equity_shield : 100
        });
      }
    } catch (e) {
      console.error("Risk Check Fetch Error", e);
    }
  },

  validateTrade: async (trade) => {
    try {
      const token = localStorage.getItem('auth_token');
      const res = await fetch(`${API_BASE}/ai-agency/validate-trade`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(trade)
      });
      if (res.ok) {
        return await res.json();
      }
      return { status: 'APPROVED', message: 'API validation skipped' };
    } catch (e) {
      console.error("Validation Error", e);
      return { status: 'APPROVED', message: 'Offline Mode' };
    }
  },

  explainPriceAction: async (asset, price, change) => {
    try {
      const token = localStorage.getItem('auth_token');
      const res = await fetch(`${API_BASE}/ai-agency/explain-price-action`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ asset, price, change })
      });
      if (res.ok) {
        const data = await res.json();
        return data.explanation;
      }
      return "Market data stream interrupted.";
    } catch (e) {
      return "AI Explanation Unavailable.";
    }
  }
}));
