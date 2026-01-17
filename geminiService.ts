
import { GoogleGenAI, Type } from "@google/genai";
import { Trade, AIPropEvaluation, TradingAccount, TradingSignal, NewsItem, Course } from "./types";

const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });

// AI evaluation of trader performance
export const evaluatePropTrader = async (history: Trade[], account: TradingAccount): Promise<AIPropEvaluation> => {
  const winRate = history.length > 0 ? (history.filter(t => (t.pnl || 0) > 0).length / history.length) * 100 : 0;
  const avgPnl = history.length > 0 ? history.reduce((acc, t) => acc + (t.pnl || 0), 0) / history.length : 0;
  
  const prompt = `Act as a Prop Firm Risk Manager. Evaluate this trader's performance:
    - Total Trades: ${history.length}
    - Win Rate: ${winRate.toFixed(1)}%
    - Average PnL: $${avgPnl.toFixed(2)}
    - Current Account Status: ${account.status}
    - Initial Balance: $${account.initialBalance}
    - Current Balance: $${account.currentBalance}
    
    Analyze their risk management, consistency, and discipline. Provide a score (0-100) and a grade (A-F).`;

  const response = await ai.models.generateContent({
    model: 'gemini-3-flash-preview',
    contents: prompt,
    config: {
      responseMimeType: "application/json",
      responseSchema: {
        type: Type.OBJECT,
        properties: {
          disciplineScore: { type: Type.NUMBER },
          riskRating: { type: Type.STRING },
          feedback: { type: Type.STRING },
          suggestedLessonId: { type: Type.STRING }
        },
        required: ["disciplineScore", "riskRating", "feedback"]
      }
    }
  });

  return JSON.parse(response.text);
};

// Added missing generateAISignal function
export const generateAISignal = async (asset: string, market: string): Promise<TradingSignal> => {
  const prompt = `Generate a high-probability trading signal for ${asset} in the ${market} market. 
  Include the signal type (BUY/SELL) and a realistic entry price based on recent market trends.`;

  const response = await ai.models.generateContent({
    model: 'gemini-3-flash-preview',
    contents: prompt,
    config: {
      responseMimeType: "application/json",
      responseSchema: {
        type: Type.OBJECT,
        properties: {
          asset: { type: Type.STRING },
          type: { type: Type.STRING, enum: ["BUY", "SELL"] },
          entry: { type: Type.NUMBER },
        },
        required: ["asset", "type", "entry"]
      }
    }
  });

  return JSON.parse(response.text);
};

// Added missing getNewsAISummary function
export const getNewsAISummary = async (news: NewsItem): Promise<{ summary: string, strategy: string }> => {
  const prompt = `Analyze this financial news: "${news.title}: ${news.content}".
  Provide an executive summary and a suggested trading strategy for ${news.assetAffected}.`;

  const response = await ai.models.generateContent({
    model: 'gemini-3-flash-preview',
    contents: prompt,
    config: {
      responseMimeType: "application/json",
      responseSchema: {
        type: Type.OBJECT,
        properties: {
          summary: { type: Type.STRING },
          strategy: { type: Type.STRING },
        },
        required: ["summary", "strategy"]
      }
    }
  });

  return JSON.parse(response.text);
};

// Added missing recommendCourse function
export const recommendCourse = async (history: Trade[], courses: Course[]): Promise<string> => {
  const prompt = `Based on these past trades: ${JSON.stringify(history)}, 
  recommend the most suitable course ID from this list: ${JSON.stringify(courses)}.
  Identify the trader's main weakness (e.g., risk management, technical analysis, or psychology).`;

  const response = await ai.models.generateContent({
    model: 'gemini-3-flash-preview',
    contents: prompt,
    config: {
      responseMimeType: "application/json",
      responseSchema: {
        type: Type.OBJECT,
        properties: {
          recommendedCourseId: { type: Type.STRING },
          reasoning: { type: Type.STRING },
        },
        required: ["recommendedCourseId"]
      }
    }
  });

  const data = JSON.parse(response.text);
  return data.recommendedCourseId;
};
