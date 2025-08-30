'use client';

import React from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import { Language } from '../lib/i18n';

const languages = [
  { code: 'en' as Language, name: 'EN', flag: '🇺🇸' },
  { code: 'zh-TW' as Language, name: 'TW', flag: '🇹🇼' },
  { code: 'zh-CN' as Language, name: 'CN', flag: '🇨🇳' }
];

export function LanguageSwitcher() {
  const { language, setLanguage } = useLanguage();

  return (
    <div className="flex space-x-1">
      {languages.map((lang) => (
        <button
          key={lang.code}
          onClick={() => setLanguage(lang.code)}
          className={`
            px-2 py-1 text-sm rounded transition-colors
            ${language === lang.code 
              ? 'bg-blue-600 text-white' 
              : 'text-slate-300 hover:text-white hover:bg-slate-700'
            }
          `}
          title={lang.name}
        >
          {lang.flag}
        </button>
      ))}
    </div>
  );
}