import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export type Theme = 'light' | 'dark' | 'system';
export type Language = 'en' | 'fr' | 'ar';

interface PreferencesState {
    theme: Theme;
    language: Language;
    setTheme: (theme: Theme) => void;
    setLanguage: (language: Language) => void;
}

export const usePreferencesStore = create<PreferencesState>()(
    persist(
        (set) => ({
            theme: 'dark', // Default to dark as it's a trading app
            language: 'en',
            setTheme: (theme) => set({ theme }),
            setLanguage: (language) => set({ language }),
        }),
        {
            name: 'tradesense-preferences', // unique name for localStorage key
        }
    )
);
