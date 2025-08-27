'use client';

import { useState, useEffect } from 'react';

export function StatusBar() {
  const [status, setStatus] = useState({
    apiConnected: true,
    realTimeData: true,
    aiAnalysisReady: true
  });

  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const statusItems = [
    {
      label: 'API Connected',
      status: status.apiConnected,
      icon: '🔌'
    },
    {
      label: 'Real-time Data',
      status: status.realTimeData,
      icon: '📡'
    },
    {
      label: 'AI Analysis Ready',
      status: status.aiAnalysisReady,
      icon: '🤖'
    }
  ];

  return (
    <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700 p-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-6">
          {statusItems.map((item, index) => (
            <div key={index} className="flex items-center space-x-2">
              <span className="text-lg">{item.icon}</span>
              <div className="flex items-center space-x-2">
                <div className={`w-2 h-2 rounded-full ${item.status ? 'bg-green-400' : 'bg-red-400'}`}></div>
                <span className={`text-sm ${item.status ? 'text-green-200' : 'text-red-200'}`}>
                  {item.label}
                </span>
              </div>
            </div>
          ))}
        </div>
        
        <div className="flex items-center space-x-4 text-sm text-slate-400">
          <span>System Time: {currentTime.toLocaleTimeString()}</span>
          <span>|</span>
          <span>Market: {currentTime.getHours() >= 9 && currentTime.getHours() < 16 ? 'Open' : 'Closed'}</span>
        </div>
      </div>
    </div>
  );
}