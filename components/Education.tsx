
import React, { useState, useEffect } from 'react';
import { useStore } from '../store';
import { recommendCourse } from '../geminiService';
import { Course } from '../types';

const Education: React.FC = () => {
  const { courses, tradeHistory } = useStore();
  const [recCourse, setRecCourse] = useState<Course | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const getRec = async () => {
      setLoading(true);
      try {
        const recId = await recommendCourse(tradeHistory, courses);
        const match = courses.find(c => c.id === recId);
        if (match) setRecCourse(match);
      } catch (e) {
        console.error("AI Recommendation failed");
      } finally {
        setLoading(false);
      }
    };
    if (tradeHistory.length > 0) getRec();
  }, [tradeHistory]);

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-12 bg-[#0b0e11]">
      <div className="flex items-end justify-between">
        <div>
          <h2 className="text-4xl font-extrabold text-white mb-2">{t('academy.title')}</h2>
          <p className="text-gray-500">{t('academy.subtitle')}</p>
        </div>
        <div className="hidden lg:flex items-center gap-6">
          <div className="text-right">
            <p className="text-xs text-gray-500 font-bold uppercase tracking-widest mb-1">{t('academy.rank')}</p>
            <p className="text-lg font-bold text-yellow-500">Silver Scholar</p>
          </div>
          <div className="w-12 h-12 rounded-2xl bg-yellow-500/10 flex items-center justify-center border border-yellow-500/20">
            <i className="fas fa-award text-yellow-500 text-xl"></i>
          </div>
        </div>
      </div>

      {/* AI Recommendation Banner */}
      {tradeHistory.length > 0 && (
        <div className="relative group">
          <div className="absolute inset-0 bg-gradient-to-r from-purple-600/20 to-indigo-600/20 rounded-3xl blur-xl opacity-50"></div>
          <div className="relative bg-[#161a1e] border border-purple-500/30 rounded-3xl p-8 flex flex-col lg:flex-row items-center gap-8 shadow-2xl">
            <div className="p-6 bg-purple-500/10 rounded-3xl border border-purple-500/20">
              <i className="fas fa-brain text-purple-500 text-4xl"></i>
            </div>
            <div className="flex-1 text-center lg:text-left">
              <span className="px-3 py-1 rounded-full bg-purple-500/20 text-purple-500 text-[10px] font-bold uppercase tracking-widest mb-2 inline-block">{t('academy.aiRec')}</span>
              <h3 className="text-2xl font-bold text-white mb-2">
                {loading ? t('academy.analyzing') : `${t('academy.focusOn')} ${recCourse?.title || 'Advanced Risk'}`}
              </h3>
              <p className="text-gray-400 text-sm leading-relaxed max-w-2xl">
                {t('academy.aiReason')}
              </p>
            </div>
            <button className="px-8 py-4 bg-purple-600 text-white font-bold rounded-2xl hover:bg-purple-500 transition-all shadow-lg shadow-purple-600/20">
              {t('academy.resume')}
            </button>
          </div>
        </div>
      )}

      {/* Categories */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {['Technical', 'Psychology', 'Risk'].map(category => (
          <section key={category}>
            <div className="flex items-center gap-3 mb-6">
              <div className="w-1.5 h-6 bg-yellow-500 rounded-full"></div>
              <h3 className="text-lg font-bold text-white">{category} {t('academy.modules')}</h3>
            </div>
            <div className="space-y-4">
              {courses.filter(c => c.category === category).map(course => (
                <div key={course.id} className="group bg-[#161a1e] border border-[#1e2329] rounded-2xl p-5 hover:border-yellow-500/30 transition-all cursor-pointer">
                  <div className="flex justify-between items-start mb-4">
                    <div className="flex items-center gap-2">
                      <span className="text-[10px] font-bold text-yellow-500 uppercase tracking-widest">{course.level}</span>
                      {course.premium && <i className="fas fa-crown text-[10px] text-yellow-500"></i>}
                    </div>
                    <span className="text-[10px] text-gray-500 font-mono">{course.duration}</span>
                  </div>
                  <h4 className="font-bold text-white mb-4 group-hover:text-yellow-500 transition-colors">{course.title}</h4>

                  {course.progress !== undefined ? (
                    <div className="space-y-2">
                      <div className="flex justify-between text-[10px] text-gray-500">
                        <span>{t('academy.progress')}</span>
                        <span>{course.progress}%</span>
                      </div>
                      <div className="h-1.5 bg-[#0b0e11] rounded-full overflow-hidden">
                        <div className="h-full bg-yellow-500 transition-all duration-1000" style={{ width: `${course.progress}%` }}></div>
                      </div>
                    </div>
                  ) : (
                    <button className="text-[10px] font-bold text-gray-500 group-hover:text-white flex items-center gap-2 transition-colors">
                      {t('academy.start')} <i className="fas fa-arrow-right text-[8px]"></i>
                    </button>
                  )}
                </div>
              ))}
            </div>
          </section>
        ))}
      </div>
    </div>
  );
};

export default Education;
