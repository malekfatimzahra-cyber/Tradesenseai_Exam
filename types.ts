
export type Market = 'Forex' | 'Crypto' | 'Stocks' | 'BVC';
export type SignalType = 'BUY' | 'SELL';
// Added 'FUNDED' to ChallengeStatus
export type ChallengeStatus = 'ACTIVE' | 'PASSED' | 'FAILED' | 'PENDING' | 'FUNDED';

export type UserRole = 'USER' | 'ADMIN' | 'SUPERADMIN';

export interface User {
  id: string;
  name: string;
  username?: string;
  email: string;
  role: UserRole;
  balance: number;
  status: ChallengeStatus;
  avatar?: string;
  joinedAt: string;
}

export interface ChallengePlan {
  id: string;
  name: string;
  capital: number;
  profitTarget: number;
  maxDrawdown: number;
  dailyLossLimit: number;
  price: number;
  currency: 'USD' | 'MAD';
}

export interface TradingAccount {
  id: string;
  planId: string;
  initialBalance: number;
  currentBalance: number;
  equity: number;
  status: ChallengeStatus;
  startTime: string;
  dailyStartingEquity: number;
  payoutPending: number;
  reason?: string;
}

export interface Trade {
  id: string;
  asset: string;
  type: SignalType;
  entryPrice: number;
  exitPrice?: number;
  sl?: number;
  tp?: number;
  amount: number;
  status: 'OPEN' | 'CLOSED';
  pnl?: number;
  commission?: number;
  timestamp: string;
  market: Market;
}

export interface RuleViolation {
  type: 'DAILY_LOSS' | 'MAX_DRAWDOWN' | 'UNAUTHORIZED_TRADING';
  message: string;
  timestamp: string;
}

export interface LeaderboardEntry {
  rank: number;
  username: string;
  profit: number;
  winRate: number;
  roi: number;
  avatar: string;
}

export interface AssetPrice {
  symbol: string;
  price: number;
  change: number;
  market: Market;
}

// Added AI evaluation of trader performance type
export interface AIPropEvaluation {
  disciplineScore: number;
  riskRating: string;
  feedback: string;
  suggestedLessonId?: string;
}

// Added trading signal type
export interface TradingSignal {
  asset: string;
  type: SignalType;
  entry: number;
}

// Added news item type
export interface NewsItem {
  id: string;
  title: string;
  content: string;
  category: Market;
  impact: 'High' | 'Medium' | 'Low';
  volatilityScore: string;
  assetAffected: string;
}

// Added educational course type
export interface Course {
  id: string;
  title: string;
  category: 'Technical' | 'Psychology' | 'Risk';
  level: 'Beginner' | 'Intermediate' | 'Advanced';
  duration: string;
  premium?: boolean;
  progress?: number;
}

// Added community chat message type
// Update Community types
export interface TradingFloor {
  id: number;
  name: string;
  type: 'GLOBAL' | 'SCALPING' | 'SWING' | 'CRYPTO' | 'FOREX' | 'INDICES';
  description: string;
  icon: string;
  required_level: string;
}

export interface FloorMessage {
  id: number;
  floor_id: number;
  user_id: number;
  user_name: string;
  user_role: string;
  type: 'TEXT' | 'TRADE_IDEA' | 'ALERT' | 'REVIEW';
  content: string;
  metadata?: string; // JSON string
  likes: number;
  timestamp: string;
}

export interface MarketSignal {
  id: string;
  asset: string;
  type: 'BUY' | 'SELL';
  confidence: number;
  entry: number;
  sl: number;
  tp: number;
  reasoning: string;
  quality: 'HIGH' | 'MEDIUM' | 'LOW';
  timestamp: string;
}

export interface RiskAlert {
  id: string;
  type: 'VOLATILITY' | 'NEWS' | 'DRAWDOWN' | 'VIOLATION';
  severity: 'INFO' | 'WARNING' | 'DANGER';
  message: string;
  timestamp: string;
}

