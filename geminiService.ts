import { API_BASE } from "./store";
import { Trade, AIPropEvaluation, TradingSignal, NewsItem } from "./types";

// AI evaluation of trader performance
export const evaluatePropTrader = async (history: Trade[], account: any): Promise<AIPropEvaluation> => {
  try {
    const token = localStorage.getItem('auth_token');
    const baseUrl = API_BASE.endsWith('/') ? API_BASE.slice(0, -1) : API_BASE;
    const response = await fetch(`${baseUrl}/ai-agency/evaluate`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ history, account })
    });

    if (response.ok) {
      return await response.json();
    }
  } catch (e) {
    console.error("Evaluation error", e);
  }

  // Fallback
  return {
    disciplineScore: 75,
    riskRating: 'B',
    feedback: 'Keep maintaining consistent position sizes.',
    suggestedLessonId: 'risk-1'
  };
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
