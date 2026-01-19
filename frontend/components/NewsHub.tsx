import React, { useState, useEffect } from 'react';
import { Newspaper, Bot, Calendar, TrendingUp, TrendingDown, Minus, Sparkles, RefreshCw, AlertCircle } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { API_BASE } from '../store';

// Types
interface NewsItem {
  id: string;
  source: string;
  time: string;
  title: string;
  sentiment: 'bullish' | 'bearish' | 'neutral';
}

interface EconomicEvent {
  id: string;
  date: string;
  time: string;
  event: string;
  impact: 'high' | 'medium' | 'low';
  forecast?: string;
}

// Mock Data
const mockNews: NewsItem[] = [
  {
    id: '1',
    source: 'Bloomberg',
    time: '14:02',
    title: 'Bitcoin breaks $45,000 resistance, analysts predict continued upside',
    sentiment: 'bullish'
  },
  {
    id: '2',
    source: 'Reuters',
    time: '13:45',
    title: 'Fed keeps rates unchanged, signals cautious approach',
    sentiment: 'neutral'
  }
]; // Simplified mock data as it will be replaced by API or uses fallback

const mockEvents: EconomicEvent[] = [
  {
    id: '1',
    date: '15 Jan',
    time: '14:30',
    event: 'Non-Farm Payrolls (USA)',
    impact: 'high',
    forecast: '+180K'
  },
  {
    id: '2',
    date: '16 Jan',
    time: '10:00',
    event: 'CPI (EUR)',
    impact: 'high',
    forecast: '+2.8%'
  },
  {
    id: '3',
    date: '17 Jan',
    time: '16:00',
    event: 'Interest Rate Decision (Fed)',
    impact: 'high',
    forecast: '5.50%'
  },
  {
    id: '4',
    date: '18 Jan',
    time: '09:30',
    event: 'Retail Sales (UK)',
    impact: 'medium',
    forecast: '+0.4%'
  }
];

const NewsHub: React.FC = () => {
  const { t, i18n } = useTranslation();
  const [currentTime, setCurrentTime] = useState(new Date());

  // Default summary based on language could be handled better, but init state here
  const [aiSummary, setAiSummary] = useState(
    t('newsHub.subtitle') // Placeholder initial state, will be updated by generate
  );

  const [isGenerating, setIsGenerating] = useState(false);

  // News State
  const [newsItems, setNewsItems] = useState<NewsItem[]>(mockNews);
  const [isNewsLoading, setIsNewsLoading] = useState(false);
  const [newsError, setNewsError] = useState('');

  // Live clock
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  // Fetch News Function
  const fetchNews = async () => {
    setIsNewsLoading(true);
    setNewsError('');
    try {
      const response = await fetch(`${API_BASE}/news/live`);
      if (!response.ok) {
        throw new Error('Failed to fetch news');
      }
      const data = await response.json();
      if (data.error) {
        console.warn("API Error:", data.error);
        return;
      }
      setNewsItems(data);
    } catch (err) {
      console.error("Error fetching news:", err);
    } finally {
      setIsNewsLoading(false);
    }
  };

  // Fetch news on mount
  useEffect(() => {
    fetchNews();
  }, []);

  // Generate AI Summary
  const handleGenerateSummary = () => {
    setIsGenerating(true);
    setTimeout(() => {
      // In a real app, this would also fetch from backend based on language
      const summaries = [
        "Market Trend: Indices consolidating after recent volatility. Investor sentiment remains cautiously optimistic. Cryptos dominating discussions with Bitcoin showing relative strength. Recommendation: Watch key support levels.",
        "Market Analysis: Recent economic data suggests inflation stabilizing. Central banks maintaining wait-and-see stance. Institutional flows favoring defensive assets. Opportunities in tech and commodities.",
        "Market Overview: Increased volatility in major pairs. European equities underperforming US counterparts. Gold continuing bullish trajectory. Strategy: Diversification with prudent exposure to risk assets."
      ];
      setAiSummary(summaries[Math.floor(Math.random() * summaries.length)]);
      setIsGenerating(false);
    }, 2000);
  };

  const getSentimentIcon = (sentiment: string) => {
    switch (sentiment) {
      case 'bullish':
        return <TrendingUp className="w-4 h-4" />;
      case 'bearish':
        return <TrendingDown className="w-4 h-4" />;
      default:
        return <Minus className="w-4 h-4" />;
    }
  };

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case 'bullish':
        return 'bg-green-500/20 text-green-500 border-green-500/30';
      case 'bearish':
        return 'bg-red-500/20 text-red-500 border-red-500/30';
      default:
        return 'bg-gray-500/20 text-gray-500 border-gray-500/30';
    }
  };

  const getImpactBadge = (impact: string) => {
    switch (impact) {
      case 'high':
        return 'bg-red-500/20 text-red-500 border-red-500/30';
      case 'medium':
        return 'bg-yellow-500/20 text-yellow-500 border-yellow-500/30';
      default:
        return 'bg-gray-500/20 text-gray-500 border-gray-500/30';
    }
  };

  const getImpactLabel = (impact: string) => {
    return t(`newsHub.impact.${impact}`);
  };

  const getSentimentLabel = (sentiment: string) => {
    return t(`newsHub.sentiment.${sentiment}`);
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-[#0b0e11] p-4 md:p-8">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header Section */}
        <div className="bg-white dark:bg-black/40 backdrop-blur-xl border border-gray-200 dark:border-white/10 rounded-2xl p-6 shadow-lg">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div className="flex-1">
              <div className="flex items-center gap-3 mb-2">
                <div className="p-2 bg-gradient-to-br from-yellow-400 to-yellow-600 rounded-xl">
                  <Newspaper className="w-6 h-6 text-black" />
                </div>
                <h1 className="text-2xl md:text-3xl font-black text-gray-900 dark:text-white tracking-tight">
                  {t('newsHub.title')}
                </h1>
              </div>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                {t('newsHub.subtitle')}
              </p>
            </div>

            {/* Live Clock */}
            <div className="flex flex-col items-end bg-gray-100 dark:bg-white/5 px-4 py-3 rounded-xl border border-gray-200 dark:border-white/10">
              <div className="flex items-center gap-2 text-2xl font-mono font-black text-gray-900 dark:text-white">
                <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
                {currentTime.toLocaleTimeString(i18n.language === 'fr' ? 'fr-FR' : 'en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit' })}
              </div>
              <div className="text-xs font-bold text-gray-600 dark:text-gray-500 uppercase tracking-wider">
                {currentTime.toLocaleDateString(i18n.language === 'fr' ? 'fr-FR' : 'en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
              </div>
            </div>
          </div>

          {/* Key Features */}
          <div className="mt-6 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
            {[
              { icon: Newspaper, text: t('newsHub.features.realTime') },
              { icon: Bot, text: t('newsHub.features.aiSummary') },
              { icon: AlertCircle, text: t('newsHub.features.alerts') },
              { icon: TrendingUp, text: t('newsHub.features.ahead') }
            ].map((feature, idx) => (
              <div key={idx} className="flex items-center gap-2 text-xs font-medium text-gray-700 dark:text-gray-400">
                <feature.icon className="w-4 h-4 text-yellow-500 shrink-0" />
                <span>{feature.text}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Main Grid Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - News Feed */}
          <div className="lg:col-span-2 bg-white dark:bg-black/40 backdrop-blur-xl border border-gray-200 dark:border-white/10 rounded-2xl shadow-lg overflow-hidden">
            <div className="p-6 border-b border-gray-200 dark:border-white/10 bg-gray-50 dark:bg-white/5 flex items-center justify-between">
              <h2 className="text-lg font-black text-gray-900 dark:text-white uppercase tracking-wider flex items-center gap-2">
                <Newspaper className="w-5 h-5 text-yellow-500" />
                {t('newsHub.latestNews')}
              </h2>
              <button
                onClick={fetchNews}
                disabled={isNewsLoading}
                className="p-2 bg-gray-100 dark:bg-white/10 hover:bg-gray-200 dark:hover:bg-white/20 rounded-lg transition-colors text-gray-600 dark:text-gray-300"
                title="Actualiser les news"
              >
                <RefreshCw className={`w-4 h-4 ${isNewsLoading ? 'animate-spin' : ''}`} />
              </button>
            </div>

            <div className="p-4 space-y-3 max-h-[800px] overflow-y-auto custom-scrollbar">
              {newsItems.map((news) => (
                <div
                  key={news.id}
                  className="group p-4 bg-gray-50 dark:bg-white/5 hover:bg-gray-100 dark:hover:bg-white/10 border border-gray-200 dark:border-white/10 rounded-xl transition-all cursor-pointer"
                >
                  <div className="flex items-start justify-between gap-3 mb-2">
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-black text-gray-600 dark:text-gray-500 uppercase tracking-wider">
                        {news.source}
                      </span>
                      <span className="text-xs text-gray-500 dark:text-gray-600">•</span>
                      <span className="text-xs font-mono font-bold text-gray-500 dark:text-gray-600">
                        {news.time}
                      </span>
                    </div>
                    <span className={`flex items-center gap-1 px-2 py-1 rounded-lg border text-xs font-black uppercase tracking-wider ${getSentimentColor(news.sentiment)}`}>
                      {getSentimentIcon(news.sentiment)}
                      {getSentimentLabel(news.sentiment)}
                    </span>
                  </div>
                  <p className="text-sm font-medium text-gray-900 dark:text-white leading-relaxed group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                    {news.title}
                  </p>
                </div>
              ))}
            </div>
          </div>

          {/* Right Column - AI & Events */}
          <div className="space-y-6">
            {/* AI Market Summary */}
            <div className="bg-white dark:bg-black/40 backdrop-blur-xl border-2 border-purple-500/30 dark:border-purple-500/20 rounded-2xl shadow-lg overflow-hidden bg-gradient-to-br from-purple-500/5 to-blue-500/5">
              <div className="p-6 border-b border-purple-500/20 bg-gradient-to-r from-purple-500/10 to-blue-500/10">
                <h3 className="text-lg font-black text-gray-900 dark:text-white uppercase tracking-wider flex items-center gap-2">
                  <Bot className="w-5 h-5 text-purple-500" />
                  {t('newsHub.aiMarketSummary')}
                </h3>
              </div>

              <div className="p-6">
                <div className="mb-4 p-4 bg-white dark:bg-white/5 rounded-xl border border-purple-500/20">
                  <p className="text-sm text-gray-700 dark:text-gray-300 leading-relaxed font-medium">
                    {aiSummary}
                  </p>
                </div>

                <button
                  onClick={handleGenerateSummary}
                  disabled={isGenerating}
                  className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white font-black text-sm uppercase tracking-wider rounded-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-xl"
                >
                  {isGenerating ? (
                    <>
                      <RefreshCw className="w-4 h-4 animate-spin" />
                      {t('newsHub.generating')}
                    </>
                  ) : (
                    <>
                      <Sparkles className="w-4 h-4" />
                      {t('newsHub.generateNew')}
                    </>
                  )}
                </button>
              </div>
            </div>

            {/* Economic Calendar */}
            <div className="bg-white dark:bg-black/40 backdrop-blur-xl border border-gray-200 dark:border-white/10 rounded-2xl shadow-lg overflow-hidden">
              <div className="p-6 border-b border-gray-200 dark:border-white/10 bg-gray-50 dark:bg-white/5">
                <h3 className="text-lg font-black text-gray-900 dark:text-white uppercase tracking-wider flex items-center gap-2">
                  <Calendar className="w-5 h-5 text-yellow-500" />
                  {t('newsHub.economicCalendar')}
                </h3>
              </div>

              <div className="p-4 space-y-3">
                {mockEvents.map((event) => (
                  <div
                    key={event.id}
                    className="p-4 bg-gray-50 dark:bg-white/5 border border-gray-200 dark:border-white/10 rounded-xl hover:border-yellow-500/50 transition-all"
                  >
                    <div className="flex items-start justify-between gap-3 mb-2">
                      <div className="flex items-center gap-2">
                        <span className="text-xs font-black text-gray-600 dark:text-gray-500 uppercase">
                          {event.date}
                        </span>
                        <span className="text-xs text-gray-500 dark:text-gray-600">•</span>
                        <span className="text-xs font-mono font-bold text-gray-500 dark:text-gray-600">
                          {event.time}
                        </span>
                      </div>
                      <span className={`px-2 py-1 rounded-lg border text-[10px] font-black uppercase tracking-wider ${getImpactBadge(event.impact)}`}>
                        {getImpactLabel(event.impact)}
                      </span>
                    </div>
                    <p className="text-sm font-bold text-gray-900 dark:text-white mb-1">
                      {event.event}
                    </p>
                    {event.forecast && (
                      <p className="text-xs text-gray-600 dark:text-gray-500">
                        {t('newsHub.forecast')}: <span className="font-bold">{event.forecast}</span>
                      </p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NewsHub;
