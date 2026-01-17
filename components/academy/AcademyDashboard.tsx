import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useStore } from '../../store';

// Types
interface Course {
    id: number | string;
    title: string;
    description?: string;
    category: string;
    level: string;
    thumbnail_url: string;
    duration: string;
    xp_reward: number;
    premium: boolean;
    progress: number;
    is_completed: boolean;
}

const normalizeCourse = (course: Partial<Course> & Pick<Course, 'id' | 'title'>): Course => {
    const category = (course.category || 'TECHNICAL').toUpperCase();
    const level = (course.level || 'BEGINNER').toUpperCase();
    const progress = typeof course.progress === 'number' ? course.progress : 0;

    return {
        id: course.id,
        title: course.title,
        description: course.description || '',
        category,
        level,
        thumbnail_url: course.thumbnail_url || '',
        duration: course.duration || '',
        xp_reward: course.xp_reward || 0,
        premium: Boolean(course.premium),
        progress,
        is_completed: Boolean(course.is_completed)
    };
};

const AcademyDashboard: React.FC = () => {
    const navigate = useNavigate();
    const { t, i18n } = useTranslation();
    const { courses: localCourses } = useStore();
    const [courses, setCourses] = useState<Course[]>([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [selectedLevel, setSelectedLevel] = useState('ALL');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const levels = ['ALL', 'BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'EXPERT'];

    useEffect(() => {
        const fetchCourses = async () => {
            setLoading(true);
            setError(null);

            try {
                const token = localStorage.getItem('auth_token');
                const apiBase = '';

                // Build query params
                const params = new URLSearchParams();
                if (selectedLevel !== 'ALL') params.append('level', selectedLevel);
                if (searchTerm) params.append('search', searchTerm);
                if (i18n.language) params.append('lang', i18n.language);
                // We'll leave it for now or user might have configured i18n globally to send headers. 
                // Wait, let's check if I can easily get i18n instance.


                const response = await fetch(`${apiBase}/api/academy/courses?${params.toString()}`, {
                    headers: { 'Authorization': `Bearer ${token}` }
                });

                if (response.ok) {
                    const data = await response.json();
                    setCourses(data.map(normalizeCourse));
                } else {
                    setError(`Server error: ${response.status}`);
                }
            } catch (err: any) {
                console.error("Error fetching courses", err);
                setError("Could not connect to the academy server.");
            } finally {
                setLoading(false);
            }
        };

        const debounceTimer = setTimeout(() => {
            fetchCourses();
        }, 300); // Debounce search

        return () => clearTimeout(debounceTimer);
    }, [selectedLevel, searchTerm]);

    const filteredCourses = courses;

    // Helper for icons
    const getCategoryIcon = (cat: string) => {
        switch (cat.toUpperCase()) {
            case 'TECHNICAL': return 'chart-line';
            case 'PSYCHOLOGY': return 'brain';
            case 'RISK': return 'shield-alt';
            case 'QUANT': return 'calculator';
            case 'PLATFORM': return 'laptop-code';
            default: return 'graduation-cap';
        }
    };

    // Helper for colors
    const getLevelColor = (level: string) => {
        switch (level.toUpperCase()) {
            case 'BEGINNER': return 'text-green-500';
            case 'INTERMEDIATE': return 'text-blue-500';
            case 'ADVANCED': return 'text-purple-500';
            case 'EXPERT': return 'text-red-500';
            default: return 'text-gray-500';
        }
    };

    return (
        <div className="p-6 max-w-[1600px] mx-auto space-y-6 bg-gray-50 text-gray-900 dark:bg-[#0b0e11] dark:text-white min-h-screen">
            <div className="flex flex-col md:flex-row justify-between items-end gap-6">
                <div>
                    <h1 className="text-3xl font-extrabold text-gray-900 dark:text-white mb-1">{t('academy.title')}</h1>
                    <p className="text-gray-600 dark:text-gray-400 text-sm">{t('academy.subtitle')}</p>
                </div>

                <div className="relative w-full md:w-80">
                    <input
                        type="text"
                        placeholder={t('academy.searchPlaceholder')}
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        className="w-full bg-white border border-gray-200 text-gray-900 pl-10 pr-4 py-2.5 rounded-xl text-sm focus:outline-none focus:border-yellow-500 transition-colors dark:bg-[#161a1e] dark:border-[#1e2329] dark:text-white"
                    />
                    <i className="fas fa-search absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 text-xs"></i>
                </div>
            </div>

            <div className="flex gap-4 overflow-x-auto pb-1 scrollbar-hide">
                <span className="flex-shrink-0 flex items-center text-[10px] font-bold text-gray-400 uppercase tracking-widest mr-2">{t('academy.experience')}</span>
                {levels.map(lvl => (
                    <button
                        key={lvl}
                        onClick={() => setSelectedLevel(lvl)}
                        className={`px-3 py-1 rounded-full text-[11px] font-bold tracking-wider transition-all whitespace-nowrap ${selectedLevel === lvl
                            ? 'bg-blue-500 text-white'
                            : 'bg-white text-gray-600 border border-gray-200 dark:bg-[#161a1e] dark:text-gray-400 dark:border-[#1e2329]'
                            }`}
                    >
                        {t(`academy.levels.${lvl.toLowerCase()}`)}
                    </button>
                ))}
            </div>

            {error && (
                <div className="bg-red-500/10 border border-red-500/30 p-4 rounded-xl text-center space-y-3">
                    <i className="fas fa-exclamation-triangle text-2xl text-red-500"></i>
                    <p className="text-red-600 dark:text-red-400 font-bold text-sm">{error}</p>
                    <button
                        onClick={() => window.location.reload()}
                        className="px-4 py-1.5 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-all font-bold text-xs dark:bg-white/10 dark:text-white dark:hover:bg-white/20"
                    >
                        {t('academy.refresh')}
                    </button>
                </div>
            )}

            {loading ? (
                <div className="text-gray-900 dark:text-white text-center py-20 flex flex-col items-center gap-4">
                    <div className="w-8 h-8 border-2 border-yellow-500 border-t-transparent rounded-full animate-spin"></div>
                    <p className="text-gray-600 dark:text-gray-400 text-sm">{t('academy.loading')}</p>
                </div>
            ) : filteredCourses.length > 0 ? (
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
                    {filteredCourses.map(course => (
                        <div
                            key={course.id}
                            onClick={() => navigate(`/academy/course/${course.id}`)}
                            className="group bg-white border border-gray-200 rounded-xl overflow-hidden hover:border-yellow-500/50 transition-all duration-300 hover:shadow-xl cursor-pointer flex flex-col h-full dark:bg-[#161a1e] dark:border-[#1e2329]"
                        >
                            <div className="h-32 relative overflow-hidden bg-gray-100 dark:bg-gray-800">
                                {course.thumbnail_url ? (
                                    <img
                                        src={course.thumbnail_url}
                                        alt={course.title}
                                        className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                                        onError={(e) => {
                                            (e.target as HTMLImageElement).src = 'https://images.unsplash.com/photo-1611974765270-ca12586343bb?w=800';
                                        }}
                                    />
                                ) : (
                                    <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-gray-100 to-gray-200 dark:from-gray-800 dark:to-black">
                                        <i className={`fas fa-${getCategoryIcon(course.category)} text-5xl text-gray-300 dark:text-white/5`}></i>
                                    </div>
                                )}

                                <div className="absolute inset-0 bg-black/20 group-hover:bg-black/0 transition-colors"></div>

                                {course.premium && (
                                    <div className="absolute top-2 right-2 bg-yellow-500 text-black px-1.5 py-0.5 rounded text-[10px] font-bold flex items-center gap-1 z-10 shadow-lg shadow-black/20">
                                        <i className="fas fa-lock text-[8px]"></i> PRO
                                    </div>
                                )}

                                <div className="absolute top-2 left-2 bg-black/60 backdrop-blur-md px-1.5 py-0.5 rounded text-[9px] text-white border border-white/10 font-bold uppercase tracking-wider">
                                    {course.category}
                                </div>

                                <div className="absolute bottom-2 left-2 bg-white/70 backdrop-blur-sm px-1.5 py-0.5 rounded text-[10px] text-gray-700 border border-gray-200 dark:bg-black/80 dark:text-white dark:border-white/10 font-medium">
                                    <i className="far fa-clock mr-1"></i> {course.duration}
                                </div>
                            </div>

                            <div className="p-4 flex-1 flex flex-col">
                                <div className="flex justify-between items-center mb-1.5">
                                    <span className={`text-[9px] font-bold uppercase tracking-widest ${getLevelColor(course.level)}`}>
                                        {t(`academy.levels.${course.level.toLowerCase()}`)}
                                    </span>
                                    {course.is_completed && <i className="fas fa-check-circle text-green-500 text-xs"></i>}
                                </div>

                                <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-1.5 group-hover:text-yellow-500 transition-colors line-clamp-2 leading-tight">{course.title}</h3>
                                <p className="text-gray-600 dark:text-gray-500 text-xs mb-4 line-clamp-2 flex-1">{course.description || "Master this skill to improve your trading edge."}</p>

                                <div className="mt-auto">
                                    <div className="flex justify-between text-[10px] text-gray-400 mb-1">
                                        <span>{t('academy.progress')}</span>
                                        <span>{course.progress}%</span>
                                    </div>
                                    <div className="h-1 bg-gray-100 dark:bg-[#0b0e11] rounded-full overflow-hidden">
                                        <div
                                            className="h-full bg-gradient-to-r from-yellow-600 to-yellow-400 transition-all duration-1000"
                                            style={{ width: `${course.progress}%` }}
                                        ></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            ) : (
                <div className="text-center py-20 bg-white rounded-2xl border border-dashed border-gray-200 dark:bg-[#161a1e] dark:border-[#1e2329]">
                    <i className="fas fa-graduation-cap text-5xl text-gray-300 dark:text-gray-700 mb-4"></i>
                    <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-1">{t('academy.noCourses')}</h3>
                    <p className="text-gray-500 text-sm max-w-md mx-auto">
                        {t('academy.noCoursesDesc')}
                    </p>
                    <button
                        onClick={() => window.location.reload()}
                        className="mt-6 px-5 py-2 bg-yellow-500 text-black font-bold text-sm rounded-lg hover:bg-yellow-400 transition-all"
                    >
                        {t('academy.refresh')}
                    </button>
                </div>
            )}
        </div>
    );
};

export default AcademyDashboard;
