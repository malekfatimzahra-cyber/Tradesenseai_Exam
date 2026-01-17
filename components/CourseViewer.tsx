import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ChevronRight, ChevronDown, CheckCircle, PlayCircle, Trophy, Loader2 } from 'lucide-react';
import { motion } from 'framer-motion';
import Quiz from './academy/Quiz';

interface Lesson {
    id: number;
    module_id: number;
    title: string;
    type: string;
    content: string;
    content_type: string;
    is_completed: boolean;
}

interface Module {
    id: number;
    title: string;
    lessons: Lesson[];
    module_quiz?: any[];
    quiz_id?: number;
    is_quiz_completed?: boolean;
}

interface CourseData {
    id: number;
    title: string;
    description?: string;
    modules: Module[];
    progress: number;
}

const CourseViewer: React.FC = () => {
    const { courseId } = useParams<{ courseId: string }>();
    const navigate = useNavigate();

    const [course, setCourse] = useState<CourseData | null>(null);
    const [selectedLessonId, setSelectedLessonId] = useState<number | null>(null);
    const [activeLesson, setActiveLesson] = useState<Lesson | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    // View State
    const [viewMode, setViewMode] = useState<'LESSON' | 'MODULE_QUIZ'>('LESSON');
    const [activeQuizQuestions, setActiveQuizQuestions] = useState<any[]>([]);
    const [activeQuizTitle, setActiveQuizTitle] = useState("");
    const [activeQuizId, setActiveQuizId] = useState<number | null>(null);
    const [activeModuleId, setActiveModuleId] = useState<number | null>(null);

    // Expanded/Collapsed modules
    const [expandedModules, setExpandedModules] = useState<Record<number, boolean>>({});

    useEffect(() => {
        if (courseId) {
            fetchCourseStructure();
        }
    }, [courseId]);

    const fetchCourseStructure = async () => {
        setLoading(true);
        try {
            const token = localStorage.getItem('auth_token');
            const res = await fetch(`http://127.0.0.1:5000/api/academy/courses/${courseId}`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });

            if (res.ok) {
                const data = await res.json();
                setCourse(data);

                // Expand first module by default
                if (data.modules && data.modules.length > 0) {
                    setExpandedModules(prev => ({ ...prev, [data.modules[0].id]: true }));
                    // Auto-select first lesson
                    if (data.modules[0].lessons.length > 0) {
                        handleSelectLesson(data.modules[0].lessons[0].id);
                    }
                }
            } else {
                setError("Cours introuvable.");
            }
        } catch (err) {
            console.error(err);
            setError("Erreur de connexion au serveur.");
        } finally {
            setLoading(false);
        }
    };

    const handleSelectLesson = async (lessonId: number) => {
        setViewMode('LESSON');
        setSelectedLessonId(lessonId);

        // Find lesson in current course structure or fetch from API
        let foundLesson = null;
        if (course) {
            for (const mod of course.modules) {
                const l = mod.lessons.find(lex => lex.id === lessonId);
                if (l) {
                    foundLesson = l;
                    break;
                }
            }
        }

        if (foundLesson) {
            setActiveLesson(foundLesson);
        } else {
            // Fetch if not found (fallback)
            try {
                const token = localStorage.getItem('auth_token');
                const res = await fetch(`http://127.0.0.1:5000/api/academy/lesson/${lessonId}`, {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                if (res.ok) {
                    const data = await res.json();
                    setActiveLesson(data);
                }
            } catch (err) {
                console.error(err);
            }
        }
    };

    const markLessonComplete = async () => {
        if (!selectedLessonId) return;

        try {
            const token = localStorage.getItem('auth_token');
            const res = await fetch(`http://127.0.0.1:5000/api/academy/lessons/${selectedLessonId}/complete`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${token}` }
            });

            if (res.ok) {
                const data = await res.json();
                // Update local state
                if (course) {
                    setCourse({
                        ...course,
                        progress: data.course_progress,
                        modules: course.modules.map(mod => ({
                            ...mod,
                            lessons: mod.lessons.map(l => l.id === selectedLessonId ? { ...l, is_completed: true } : l)
                        }))
                    });
                }

                // Advance to next lesson if possible
                advanceNext();
            }
        } catch (err) {
            console.error(err);
        }
    };

    const advanceNext = () => {
        if (!course || !selectedLessonId) return;

        let found = false;
        let nextLesson = null;
        let currentModId = activeLesson?.module_id;

        for (const mod of course.modules) {
            for (const les of mod.lessons) {
                if (found) {
                    nextLesson = les;
                    break;
                }
                if (les.id === selectedLessonId) found = true;
            }
            if (nextLesson) break;

            // If we found the current lesson and reached the end of its module, maybe go to module quiz
            if (found && currentModId === mod.id) {
                const quiz = mod.quiz_id;
                if (quiz && !mod.is_quiz_completed) {
                    handleStartModuleQuiz(mod.id);
                    return;
                }
            }
        }

        if (nextLesson) {
            handleSelectLesson(nextLesson.id);
            setExpandedModules(prev => ({ ...prev, [nextLesson!.module_id]: true }));
        }
    };

    const handleStartModuleQuiz = (moduleId: number) => {
        const mod = course?.modules.find(m => m.id === moduleId);
        if (mod && mod.module_quiz) {
            setActiveQuizTitle(mod.title);
            setActiveQuizQuestions(mod.module_quiz);
            setActiveQuizId(mod.quiz_id || null);
            setActiveModuleId(moduleId);
            setViewMode('MODULE_QUIZ');
            setSelectedLessonId(null);
            setActiveLesson(null);
        }
    };

    const handleQuizSubmit = async (score: number, passed: boolean, answers: any) => {
        if (!activeQuizId) return;

        try {
            const token = localStorage.getItem('auth_token');
            // We need to pass the answers to the backend for persistence as requested
            const res = await fetch(`http://127.0.0.1:5000/api/academy/quizzes/${activeQuizId}/submit`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ answers })
            });

            if (res.ok) {
                // Refresh course structure to get updated progress
                fetchCourseStructure();
            }
        } catch (err) {
            console.error(err);
        }
    };

    const toggleModule = (modId: number) => {
        setExpandedModules(prev => ({ ...prev, [modId]: !prev[modId] }));
    };

    if (loading) {
        return (
            <div className="flex flex-col items-center justify-center h-screen bg-[#0f1115] text-white">
                <Loader2 className="animate-spin text-yellow-500 w-12 h-12 mb-4" />
                <p className="text-gray-400">Chargement de l'Academy...</p>
            </div>
        );
    }

    if (error || !course) {
        return (
            <div className="flex flex-col items-center justify-center h-screen bg-[#0f1115] text-white p-6">
                <h1 className="text-2xl font-bold text-red-500 mb-4">Erreur</h1>
                <p className="text-gray-400 mb-8">{error || "Cours inaccessible."}</p>
                <button onClick={() => navigate('/academy')} className="px-6 py-2 bg-yellow-500 text-black font-bold rounded-lg hover:bg-yellow-400">
                    Retour Dashboard
                </button>
            </div>
        );
    }

    return (
        <div className="flex h-screen bg-[#0b0e11] text-white overflow-hidden font-sans">
            {/* SIDEBAR */}
            <div className="w-80 bg-[#161a1e] border-r border-[#1e2329] flex flex-col flex-shrink-0">
                <div className="p-6 border-b border-[#1e2329]">
                    <button onClick={() => navigate('/academy')} className="group flex items-center text-sm text-gray-400 hover:text-white mb-6 transition-colors">
                        <ChevronRight className="rotate-180 mr-2 group-hover:-translate-x-1 transition-transform" size={16} />
                        Back to Academy
                    </button>
                    <h2 className="font-bold text-xl leading-tight text-white mb-2">{course.title}</h2>
                    <div className="mt-4">
                        <div className="flex justify-between text-xs text-gray-400 mb-2">
                            <span>Progress</span>
                            <span>{course.progress}%</span>
                        </div>
                        <div className="w-full bg-[#0b0e11] h-1.5 rounded-full overflow-hidden">
                            <div className="bg-yellow-500 h-full transition-all duration-1000" style={{ width: `${course.progress}%` }}></div>
                        </div>
                    </div>
                </div>

                <div className="flex-1 overflow-y-auto p-3 space-y-2 scrollbar-hide">
                    {course.modules.map((mod, idx) => (
                        <div key={mod.id} className="space-y-1">
                            <button
                                onClick={() => toggleModule(mod.id)}
                                className={`flex items-center w-full p-3 rounded-xl text-left transition-all ${expandedModules[mod.id] ? 'bg-[#1e2329]' : 'hover:bg-[#1e2329]/50'}`}
                            >
                                <span className={`mr-3 text-gray-500 transition-transform ${expandedModules[mod.id] ? 'rotate-90' : ''}`}>
                                    <ChevronRight size={18} />
                                </span>
                                <span className="font-bold text-sm text-gray-200 uppercase tracking-tight">Module {idx + 1}: {mod.title}</span>
                            </button>

                            {expandedModules[mod.id] && (
                                <div className="ml-6 space-y-1 py-1">
                                    {mod.lessons.map(les => (
                                        <button
                                            key={les.id}
                                            onClick={() => handleSelectLesson(les.id)}
                                            className={`flex items-center w-full p-2.5 text-sm rounded-lg transition-all 
                                                ${selectedLessonId === les.id
                                                    ? 'bg-yellow-500/10 text-yellow-500 font-bold'
                                                    : 'text-gray-400 hover:text-white hover:bg-[#1e2329]'}`}
                                        >
                                            {les.is_completed ?
                                                <CheckCircle size={16} className="mr-3 text-green-500 flex-shrink-0" /> :
                                                <PlayCircle size={16} className="mr-3 flex-shrink-0" />
                                            }
                                            <span className="truncate">{les.title}</span>
                                        </button>
                                    ))}

                                    {mod.module_quiz && (
                                        <button
                                            onClick={() => handleStartModuleQuiz(mod.id)}
                                            className={`flex items-center w-full p-2.5 text-xs font-bold rounded-lg mt-2 transition-all
                                                ${viewMode === 'MODULE_QUIZ' && activeModuleId === mod.id
                                                    ? 'bg-orange-500/20 text-orange-500 shadow-inner'
                                                    : mod.is_quiz_completed
                                                        ? 'text-green-500 hover:bg-green-500/10'
                                                        : 'text-yellow-600 hover:text-yellow-500 hover:bg-yellow-500/5'
                                                }`}
                                        >
                                            <Trophy size={14} className="mr-3" />
                                            QUIZ DU MODULE
                                            {mod.is_quiz_completed && <CheckCircle size={12} className="ml-auto" />}
                                        </button>
                                    )}
                                </div>
                            )}
                        </div>
                    ))}

                    <div className="mt-8 pt-6 border-t border-[#1e2329]">
                        <button className="w-full flex items-center justify-center p-4 rounded-2xl font-bold border-2 border-dashed border-[#1e2329] text-gray-500 hover:border-yellow-500/50 hover:text-yellow-500 transition-all group">
                            <Trophy size={20} className="mr-2 group-hover:scale-110 transition-transform" />
                            FINAL EXAM
                        </button>
                    </div>
                </div>
            </div>

            {/* MAIN CONTENT AREA */}
            <div className="flex-1 overflow-y-auto bg-[#0b0e11] flex flex-col items-center">
                <main className="w-full max-w-5xl py-12 px-8 flex-1">
                    {viewMode === 'LESSON' && activeLesson ? (
                        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} key={activeLesson.id}>
                            <div className="mb-10 text-center">
                                <h1 className="text-4xl font-extrabold text-white mb-4">{activeLesson.title}</h1>
                                <div className="h-1 w-24 bg-yellow-500 mx-auto rounded-full"></div>
                            </div>

                            <div className="bg-[#161a1e] border border-[#1e2329] rounded-3xl p-10 shadow-2xl overflow-hidden">
                                <div
                                    className="prose prose-invert max-w-none 
                                    text-gray-300 leading-relaxed text-lg
                                    prose-h2:text-white prose-h2:text-3xl prose-h2:font-bold prose-h2:mb-6 prose-h2:mt-10
                                    prose-h3:text-yellow-500 prose-h3:text-xl prose-h3:font-bold prose-h3:mb-4 prose-h3:mt-8
                                    prose-p:mb-6 prose-ul:mb-6 prose-li:mb-2 prose-strong:text-white"
                                    dangerouslySetInnerHTML={{ __html: activeLesson.content }}
                                />

                                <div className="mt-16 pt-8 border-t border-[#1e2329] flex justify-center">
                                    <button
                                        onClick={markLessonComplete}
                                        disabled={activeLesson.is_completed}
                                        className={`px-12 py-4 rounded-2xl font-bold text-lg flex items-center shadow-xl transition-all active:scale-95
                                            ${activeLesson.is_completed
                                                ? 'bg-green-500/20 text-green-500 cursor-default border border-green-500/30'
                                                : 'bg-yellow-500 text-black hover:bg-yellow-400 hover:shadow-yellow-500/20'}`}
                                    >
                                        {activeLesson.is_completed ? (
                                            <><CheckCircle size={24} className="mr-3" /> Terminé</>
                                        ) : (
                                            <><CheckCircle size={24} className="mr-3" /> Mark Complete</>
                                        )}
                                    </button>
                                </div>
                            </div>
                        </motion.div>
                    ) : viewMode === 'MODULE_QUIZ' ? (
                        <div className="w-full max-w-3xl mx-auto">
                            <Quiz
                                title={activeQuizTitle}
                                questions={activeQuizQuestions}
                                passingScore={70}
                                onComplete={(score, passed, answers) => {
                                    handleQuizSubmit(score, passed, answers);
                                }}
                                onContinue={() => {
                                    setViewMode('LESSON');
                                    fetchCourseStructure(); // Refresh to show completed quiz
                                }}
                            />
                        </div>
                    ) : (
                        <div className="flex flex-col items-center justify-center h-full text-gray-500">
                            <i className="fas fa-book-open text-6xl mb-6 opacity-20"></i>
                            <p className="text-xl">Sélectionnez une leçon pour commencer</p>
                        </div>
                    )}
                </main>
            </div>
        </div>
    );
};

export default CourseViewer;
