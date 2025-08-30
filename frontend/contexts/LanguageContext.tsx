'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';
import { Language, Translations, getTranslations } from '../lib/i18n';

interface LanguageContextType {
  language: Language;
  setLanguage: (lang: Language) => void;
  t: Translations;
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

export function LanguageProvider({ children }: { children: React.ReactNode }) {
  const [language, setLanguage] = useState<Language>('en');
  const [t, setT] = useState<Translations>(getTranslations('en'));

  useEffect(() => {
    // Load saved language from localStorage
    const savedLanguage = localStorage.getItem('language') as Language;
    if (savedLanguage && ['en', 'zh-TW', 'zh-CN'].includes(savedLanguage)) {
      setLanguage(savedLanguage);
      setT(getTranslations(savedLanguage));
    } else {
      // Detect browser language
      const browserLang = navigator.language;
      let detectedLang: Language = 'en';
      
      if (browserLang.startsWith('zh')) {
        if (browserLang.includes('CN') || browserLang.includes('Hans')) {
          detectedLang = 'zh-CN';
        } else if (browserLang.includes('TW') || browserLang.includes('Hant')) {
          detectedLang = 'zh-TW';
        }
      }
      
      setLanguage(detectedLang);
      setT(getTranslations(detectedLang));
    }
  }, []);

  const handleSetLanguage = (lang: Language) => {
    setLanguage(lang);
    setT(getTranslations(lang));
    localStorage.setItem('language', lang);
  };

  return (
    <LanguageContext.Provider value={{ 
      language, 
      setLanguage: handleSetLanguage, 
      t 
    }}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage() {
  const context = useContext(LanguageContext);
  if (context === undefined) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
}