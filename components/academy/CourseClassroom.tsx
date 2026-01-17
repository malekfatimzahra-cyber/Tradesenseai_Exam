import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';

// =====================================
// TYPES
// =====================================

interface Option {
    id: number;
    text: string;
}

interface Question {
    id: number;
    text: string;
    options: Option[];
    explanation?: string;
}

interface Quiz {
    id: number;
    title: string;
    questions: Question[];
    min_pass_score: number;
}

interface QuizResult {
    question_id: number;
    is_correct: boolean;
    correct_option_id: number;
    explanation: string;
}

interface Lesson {
    id: number;
    title: string;
    type: 'TEXT';
    content?: string;
    is_completed: boolean;
    quiz_passed: boolean;
    has_quiz: boolean;
    is_locked: boolean;
    status: 'completed' | 'locked' | 'current';
}

interface Module {
    id: number;
    title: string;
    lessons: Lesson[];
    is_completed: boolean;
}

interface CourseDetails {
    id: number;
    title: string;
    description: string;
    modules: Module[];
    progress: number;
    is_completed: boolean;
}

// =====================================
// LESSON STATUS ICONS
// =====================================

const StatusIcon: React.FC<{ status: 'completed' | 'locked' | 'current'; small?: boolean }> = ({ status, small }) => {
    const size = small ? 'w-5 h-5 text-[10px]' : 'w-6 h-6 text-xs';

    switch (status) {
        case 'completed':
            return (
                <div className={`${size} rounded-full bg-green-500 flex items-center justify-center text-black`}>
                    <i className="fas fa-check"></i>
                </div>
            );
        case 'locked':
            return (
                <div className={`${size} rounded-full bg-gray-700 flex items-center justify-center text-gray-400`}>
                    <i className="fas fa-lock text-[8px]"></i>
                </div>
            );
        case 'current':
            return (
                <div className={`${size} rounded-full bg-yellow-500 flex items-center justify-center text-black animate-pulse`}>
                    <i className="fas fa-play text-[8px]"></i>
                </div>
            );
    }
};

// =====================================
// MAIN COMPONENT
// =====================================

const CourseClassroom: React.FC = () => {
    const { courseId } = useParams<{ courseId: string }>();
    const navigate = useNavigate();
    const { t } = useTranslation();

    // Course & Lesson State
    const [course, setCourse] = useState<CourseDetails | null>(null);
    const [currentLesson, setCurrentLesson] = useState<Lesson | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    // Quiz State
    const [showQuiz, setShowQuiz] = useState(false);
    const [quizData, setQuizData] = useState<Quiz | null>(null);
    const [quizLoading, setQuizLoading] = useState(false);
    const [quizResults, setQuizResults] = useState<{
        passed: boolean;
        score_percent: number;
        min_pass_score: number;
        results: QuizResult[];
        xp_earned: number;
        course_progress: number;
        message: string;
    } | null>(null);
    const [selectedAnswers, setSelectedAnswers] = useState<Record<number, number>>({});

    // =====================================
    // API CALLS
    // =====================================

    const fetchCourse = useCallback(async () => {
        setLoading(true);
        setError(null);
        try {
            const token = localStorage.getItem('auth_token');
            const apiBase = 'https://faty2002.pythonanywhere.com';
            const response = await fetch(`${apiBase}/api/academy/courses/${courseId}`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });

            if (response.ok) {
                const data = await response.json();
                setCourse(data);

                // Select first unlocked lesson if none selected
                if (!currentLesson) {
                    const firstUnlocked = findFirstUnlockedLesson(data);
                    if (firstUnlocked) setCurrentLesson(firstUnlocked);
                } else {
                    // Refresh current lesson data
                    const updatedLesson = data.modules
                        .flatMap((m: Module) => m.lessons)
                        .find((l: Lesson) => l.id === currentLesson.id);
                    if (updatedLesson) setCurrentLesson(updatedLesson);
                }

                setError(null);
            } else {
                setError(t('common.error'));
            }
        } catch (err) {
            console.error("Error fetching course", err);
            setError(t('common.networkError'));
        } finally {
            setLoading(false);
        }
    }, [courseId, currentLesson, t]);

    const findFirstUnlockedLesson = (courseData: CourseDetails): Lesson | null => {
        for (const module of courseData.modules) {
            for (const lesson of module.lessons) {
                if (!lesson.is_locked && !lesson.is_completed) {
                    return lesson;
                }
            }
        }
        // If all completed or none unlocked, return first lesson
        return courseData.modules[0]?.lessons[0] || null;
    };

    const startQuiz = async () => {
        if (!currentLesson) return;

        setQuizLoading(true);
        setShowQuiz(true);
        setQuizResults(null);
        setSelectedAnswers({});

        try {
            const token = localStorage.getItem('auth_token');
            const apiBase = 'https://faty2002.pythonanywhere.com';
            const response = await fetch(`${apiBase}/api/academy/lessons/${currentLesson.id}/quiz`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });

            if (response.ok) {
                const data = await response.json();
                setQuizData(data);
            } else if (response.status === 403) {
                setError(t('academy.classroom.lockedMessage'));
                setShowQuiz(false);
            } else if (response.status === 404) {
                setError('Quiz not found');
                setShowQuiz(false);
            }
        } catch (err) {
            console.error("Error fetching quiz", err);
            setError(t('common.networkError'));
            setShowQuiz(false);
        } finally {
            setQuizLoading(false);
        }
    };

    const submitQuiz = async () => {
        if (!quizData) return;

        setQuizLoading(true);

        try {
            const token = localStorage.getItem('auth_token');
            const apiBase = 'https://faty2002.pythonanywhere.com';
            const response = await fetch(`${apiBase}/api/academy/quizzes/submit`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    quiz_id: quizData.id,
                    answers: selectedAnswers
                })
            });

            if (response.ok) {
                const results = await response.json();
                setQuizResults(results);

                // If passed, refresh course data to update progress and unlock next lesson
                if (results.passed) {
                    await fetchCourse();
                }
            }
        } catch (err) {
            console.error("Error submitting quiz", err);
        } finally {
            setQuizLoading(false);
        }
    };

    const handleLessonSelect = (lesson: Lesson) => {
        if (lesson.is_locked) return;
        setCurrentLesson(lesson);
        setShowQuiz(false);
        setQuizResults(null);
        setQuizData(null);
    };

    const goToNextLesson = () => {
        if (!course || !currentLesson) return;

        const allLessons = course.modules.flatMap(m => m.lessons);
        const currentIdx = allLessons.findIndex(l => l.id === currentLesson.id);

        if (currentIdx < allLessons.length - 1) {
            const nextLesson = allLessons[currentIdx + 1];
            if (!nextLesson.is_locked) {
                setCurrentLesson(nextLesson);
                setShowQuiz(false);
                setQuizResults(null);
                setQuizData(null);
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
        }
    };

    // =====================================
    // EFFECTS
    // =====================================

    useEffect(() => {
        fetchCourse();
    }, [courseId]);

    // =====================================
    // RENDER HELPERS
    // =====================================

    const renderLessonContent = () => {
        if (!currentLesson?.content) {
            return (
                <div className="p-12 rounded-2xl bg-white/5 border border-dashed border-white/10 text-center">
                    <i className="fas fa-file-alt text-6xl text-white/10 mb-6"></i>
                    <p className="text-gray-500">{t('academy.classroom.noContent')}</p>
                </div>
            );
        }

        // The content is already HTML from the upgrade_ui_academy.py script
        return (
            <div
                className="prose prose-invert max-w-none premium-content"
                dangerouslySetInnerHTML={{ __html: currentLesson.content }}
            />
        );
    };

    // =====================================
    // LOADING & ERROR STATES
    // =====================================

    if (loading) {
        return (
            <div className="flex items-center justify-center h-screen bg-[#0b0e11] text-white">
                <div className="flex flex-col items-center gap-4">
                    <div className="w-12 h-12 border-4 border-yellow-500 border-t-transparent rounded-full animate-spin"></div>
                    <p className="text-gray-400 font-medium">{t('common.loading')}</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="flex items-center justify-center h-screen bg-[#0b0e11] text-white">
                <div className="text-center space-y-4">
                    <i className="fas fa-exclamation-triangle text-4xl text-red-500"></i>
                    <p className="text-red-400">{error}</p>
                    <button
                        onClick={() => { setError(null); fetchCourse(); }}
                        className="px-6 py-2 bg-white/10 rounded-lg hover:bg-white/20 transition-all"
                    >
                        {t('settings.danger.btnReset')}
                    </button>
                </div>
            </div>
        );
    }

    if (!course) {
        return (
            <div className="flex items-center justify-center h-screen bg-[#0b0e11] text-white">
                <div className="text-center">
                    <i className="fas fa-book-dead text-6xl text-white/10 mb-4"></i>
                    <p className="text-gray-500">{t('academy.noCourses')}.</p>
                    <button
                        onClick={() => navigate('/academy')}
                        className="mt-4 px-6 py-2 bg-yellow-500 text-black rounded-lg font-bold"
                    >
                        {t('academy.classroom.backToAcademy')}
                    </button>
                </div>
            </div>
        );
    }

    // =====================================
    // MAIN RENDER
    // =====================================

    return (
        <div className="flex flex-col h-screen bg-[#0b0e11] text-white font-sans selection:bg-yellow-500/30">
            {/* ===== HEADER ===== */}
            <header className="h-16 border-b border-white/5 flex items-center px-6 justify-between bg-[#161a1e]/80 backdrop-blur-md sticky top-0 z-30">
                <div className="flex items-center gap-4">
                    <button
                        onClick={() => navigate('/academy')}
                        className="p-2 text-gray-400 hover:text-white hover:bg-white/5 rounded-full transition-all"
                    >
                        <i className="fas fa-arrow-left text-sm"></i>
                    </button>
                    <div>
                        <h1 className="text-lg font-bold bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">
                            {course.title}
                        </h1>
                        <div className="flex items-center gap-2 mt-0.5">
                            {course.is_completed && (
                                <span className="text-[10px] px-1.5 py-0.5 rounded bg-green-500/10 text-green-500 font-bold border border-green-500/20">
                                    ✅ {t('academy.classroom.completed')}
                                </span>
                            )}
                            <span className="text-[10px] text-gray-500 font-medium">
                                {course.modules.length} {t('academy.classroom.modules')} • {course.modules.reduce((acc, m) => acc + m.lessons.length, 0)} {t('academy.classroom.lessons')}
                            </span>
                        </div>
                    </div>
                </div>

                {/* Progress Indicator */}
                <div className="flex flex-col items-end">
                    <div className="flex items-center gap-3 mb-1">
                        <span className={`text-sm font-bold ${course.progress === 100 ? 'text-green-500' : 'text-yellow-500'}`}>
                            {course.progress}% {t('academy.classroom.progress')}
                        </span>
                    </div>
                    <div className="w-40 h-1.5 bg-white/5 rounded-full overflow-hidden">
                        <div
                            className={`h-full transition-all duration-1000 ease-out ${course.progress === 100
                                ? 'bg-gradient-to-r from-green-600 to-green-400'
                                : 'bg-gradient-to-r from-yellow-600 to-yellow-400'
                                }`}
                            style={{ width: `${course.progress}%` }}
                        />
                    </div>
                </div>
            </header>

            <div className="flex flex-1 overflow-hidden">
                {/* ===== MAIN CONTENT AREA ===== */}
                <main className="flex-1 overflow-y-auto bg-gradient-to-br from-[#0b0e11] to-[#161a1e] relative">
                    <div className="max-w-4xl mx-auto p-8 pb-32">

                        {/* ===== QUIZ VIEW ===== */}
                        {showQuiz ? (
                            <div className="bg-[#1e2329]/50 rounded-2xl border border-white/5 p-8 shadow-2xl backdrop-blur-sm animate-fade-in">
                                {quizLoading && !quizResults ? (
                                    <div className="py-20 flex flex-col items-center">
                                        <div className="w-10 h-10 border-2 border-yellow-500 border-t-transparent rounded-full animate-spin mb-4"></div>
                                        <p className="text-gray-400">{t('common.loading')}</p>
                                    </div>
                                ) : quizResults ? (
                                    /* ===== QUIZ RESULTS ===== */
                                    <div className="space-y-8">
                                        <div className={`p-8 rounded-xl text-center border ${quizResults.passed
                                            ? 'bg-green-500/10 border-green-500/30'
                                            : 'bg-red-500/10 border-red-500/30'
                                            }`}>
                                            <div className="text-6xl mb-4">
                                                {quizResults.passed ? '🏆' : '📚'}
                                            </div>
                                            <h3 className="text-2xl font-bold mb-2">
                                                {quizResults.passed ? t('academy.classroom.quizPassed') : t('academy.classroom.keepLearning')}
                                            </h3>
                                            <p className="text-lg font-medium opacity-80 mb-2">
                                                {t('leaderboard.table.funded')}: <span className={quizResults.passed ? 'text-green-400' : 'text-red-400'}>
                                                    {Math.round(quizResults.score_percent)}%
                                                </span>
                                            </p>
                                            <p className="text-sm text-gray-400 mb-6">
                                                Min: {quizResults.min_pass_score}%
                                            </p>

                                            {quizResults.passed && quizResults.xp_earned > 0 && (
                                                <div className="inline-flex items-center gap-2 px-4 py-2 bg-yellow-500/10 border border-yellow-500/30 rounded-full mb-6">
                                                    <i className="fas fa-star text-yellow-500"></i>
                                                    <span className="text-yellow-500 font-bold">+{quizResults.xp_earned} XP!</span>
                                                </div>
                                            )}

                                            <div className="flex justify-center gap-4">
                                                {quizResults.passed ? (
                                                    <button
                                                        onClick={goToNextLesson}
                                                        className="px-8 py-3 rounded-full font-bold bg-yellow-500 text-black hover:bg-yellow-400 transition-transform active:scale-95"
                                                    >
                                                        {t('academy.classroom.continueToNext')} →
                                                    </button>
                                                ) : (
                                                    <>
                                                        <button
                                                            onClick={() => { setShowQuiz(false); setQuizResults(null); }}
                                                            className="px-8 py-3 rounded-full font-bold bg-white/10 text-white hover:bg-white/20 transition-all"
                                                        >
                                                            {t('academy.classroom.reviewContent')}
                                                        </button>
                                                        <button
                                                            onClick={() => { setQuizResults(null); setSelectedAnswers({}); }}
                                                            className="px-8 py-3 rounded-full font-bold bg-yellow-500 text-black hover:bg-yellow-400 transition-all"
                                                        >
                                                            {t('academy.classroom.retryQuiz')}
                                                        </button>
                                                    </>
                                                )}
                                            </div>
                                        </div>

                                        {/* Detailed Feedback */}
                                        <div className="space-y-6">
                                            <h4 className="text-lg font-bold text-gray-300 px-2">{t('academy.classroom.detailedFeedback')}</h4>
                                            {quizResults.results.map((res, idx) => {
                                                const question = quizData?.questions.find(q => q.id === res.question_id);
                                                return (
                                                    <div key={idx} className={`p-6 rounded-xl border ${res.is_correct
                                                        ? 'bg-green-500/5 border-green-500/10'
                                                        : 'bg-red-500/5 border-red-500/10'
                                                        }`}>
                                                        <div className="flex gap-4">
                                                            <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center font-bold ${res.is_correct
                                                                ? 'bg-green-500/20 text-green-400'
                                                                : 'bg-red-500/20 text-red-400'
                                                                }`}>
                                                                {res.is_correct ? '✓' : '✗'}
                                                            </div>
                                                            <div className="flex-1">
                                                                <p className="font-bold mb-3">{question?.text}</p>
                                                                <div className="bg-white/5 p-4 rounded-lg text-sm italic text-gray-400 border-l-2 border-yellow-500/50">
                                                                    <span className="text-yellow-500 font-bold not-italic mr-2">{t('academy.classroom.explanation')}:</span>
                                                                    {res.explanation}
                                                                </div>
                                                            </div>
                                                        </div>
                                                    </div>
                                                );
                                            })}
                                        </div>
                                    </div>
                                ) : quizData ? (
                                    /* ===== QUIZ QUESTIONS ===== */
                                    <div className="space-y-8">
                                        <div className="flex items-center justify-between border-b border-white/5 pb-6">
                                            <div>
                                                <h2 className="text-2xl font-bold">{quizData.title}</h2>
                                                <p className="text-sm text-gray-400 mt-1">
                                                    Min: {quizData.min_pass_score}% • {quizData.questions.length} questions
                                                </p>
                                            </div>
                                            <button
                                                onClick={() => setShowQuiz(false)}
                                                className="text-gray-500 hover:text-white p-2"
                                            >
                                                <i className="fas fa-times"></i>
                                            </button>
                                        </div>

                                        <div className="space-y-10 py-4">
                                            {quizData.questions.map((q, qIdx) => (
                                                <div key={q.id} className="space-y-4">
                                                    <h4 className="text-lg font-medium leading-relaxed">
                                                        <span className="text-yellow-500 font-bold mr-2">{qIdx + 1}.</span>
                                                        {q.text}
                                                    </h4>
                                                    <div className="grid gap-3">
                                                        {q.options.map(opt => (
                                                            <label
                                                                key={opt.id}
                                                                className={`flex items-center p-4 rounded-xl border transition-all cursor-pointer group ${selectedAnswers[q.id] === opt.id
                                                                    ? 'bg-yellow-500/10 border-yellow-500 text-yellow-500 ring-1 ring-yellow-500'
                                                                    : 'bg-white/5 border-white/5 text-gray-400 hover:bg-white/10 hover:border-white/10'
                                                                    }`}
                                                            >
                                                                <input
                                                                    type="radio"
                                                                    name={`q-${q.id}`}
                                                                    className="hidden"
                                                                    onChange={() => setSelectedAnswers({ ...selectedAnswers, [q.id]: opt.id })}
                                                                />
                                                                <div className={`w-5 h-5 rounded-full border-2 mr-4 flex items-center justify-center transition-all ${selectedAnswers[q.id] === opt.id
                                                                    ? 'border-yellow-500 bg-yellow-500'
                                                                    : 'border-white/20 group-hover:border-white/40'
                                                                    }`}>
                                                                    {selectedAnswers[q.id] === opt.id && <div className="w-2 h-2 rounded-full bg-black"></div>}
                                                                </div>
                                                                <span className="font-medium">{opt.text}</span>
                                                            </label>
                                                        ))}
                                                    </div>
                                                </div>
                                            ))}
                                        </div>

                                        <div className="pt-6 flex items-center justify-between">
                                            <p className="text-sm text-gray-500">
                                                {Object.keys(selectedAnswers).length} / {quizData.questions.length}
                                            </p>
                                            <button
                                                onClick={submitQuiz}
                                                disabled={Object.keys(selectedAnswers).length < quizData.questions.length || quizLoading}
                                                className="px-8 py-4 bg-yellow-500 text-black font-bold uppercase tracking-widest rounded-xl hover:bg-yellow-400 disabled:opacity-30 disabled:cursor-not-allowed transition-all shadow-xl shadow-yellow-500/20"
                                            >
                                                {quizLoading ? t('common.loading') : t('academy.classroom.takeQuiz')}
                                            </button>
                                        </div>
                                    </div>
                                ) : (
                                    <div className="text-center py-20 text-gray-500">
                                        <i className="fas fa-exclamation-circle text-4xl mb-4"></i>
                                        <p>No quiz data found.</p>
                                    </div>
                                )}
                            </div>
                        ) : currentLesson ? (
                            /* ===== LESSON CONTENT VIEW ===== */
                            <div className="space-y-8 animate-fade-in">
                                {/* Lesson Hero */}
                                <div className="relative rounded-3xl overflow-hidden bg-gradient-to-br from-[#1e2329] to-[#0b0e11] border border-white/5 p-12">
                                    <div className="absolute top-0 right-0 w-1/2 h-full opacity-5">
                                        <i className="fas fa-book-open text-[300px] text-white transform rotate-12 translate-x-20"></i>
                                    </div>

                                    <div className="relative z-10">
                                        <div className="flex items-center gap-3 mb-4">
                                            <StatusIcon status={currentLesson.status} />
                                            <span className="text-xs font-black text-yellow-500 tracking-widest uppercase">
                                                {currentLesson.type}
                                            </span>
                                            {currentLesson.quiz_passed && (
                                                <span className="px-2 py-1 bg-green-500/10 border border-green-500/30 rounded text-green-400 text-[10px] font-bold">
                                                    ✅ {t('academy.classroom.quizPassed')}
                                                </span>
                                            )}
                                        </div>

                                        <h2 className="text-4xl md:text-5xl font-black mb-4">{currentLesson.title}</h2>

                                        <p className="text-gray-400 max-w-2xl">
                                            {t('academy.classroom.quizRequired')}
                                        </p>
                                    </div>
                                </div>

                                {/* Lesson Content */}
                                <div className="bg-[#161a1e]/50 rounded-2xl border border-white/5 p-8 md:p-10">
                                    {renderLessonContent()}
                                </div>

                                {/* Quiz CTA */}
                                {currentLesson.has_quiz && (
                                    <div className={`rounded-2xl border p-8 ${currentLesson.quiz_passed
                                        ? 'bg-green-500/5 border-green-500/20'
                                        : 'bg-yellow-500/5 border-yellow-500/20'
                                        }`}>
                                        <div className="flex flex-col md:flex-row items-center justify-between gap-6">
                                            <div className="flex items-center gap-4">
                                                <div className={`w-14 h-14 rounded-xl flex items-center justify-center ${currentLesson.quiz_passed
                                                    ? 'bg-green-500/20 text-green-400'
                                                    : 'bg-yellow-500/20 text-yellow-500'
                                                    }`}>
                                                    <i className={`fas fa-${currentLesson.quiz_passed ? 'medal' : 'question-circle'} text-2xl`}></i>
                                                </div>
                                                <div>
                                                    <h3 className="font-bold text-lg">
                                                        {currentLesson.quiz_passed ? t('academy.classroom.quizPassed') : t('academy.classroom.readyForQuiz')}
                                                    </h3>
                                                    <p className="text-sm text-gray-400">
                                                        {currentLesson.quiz_passed
                                                            ? t('academy.classroom.passedMessage')
                                                            : t('academy.classroom.passToUnlock')
                                                        }
                                                    </p>
                                                </div>
                                            </div>

                                            <button
                                                onClick={startQuiz}
                                                className={`px-8 py-4 rounded-xl font-black uppercase tracking-widest transition-all shadow-lg ${currentLesson.quiz_passed
                                                    ? 'bg-green-500/20 text-green-400 border border-green-500/30 hover:bg-green-500/30'
                                                    : 'bg-yellow-500 text-black hover:bg-yellow-400 shadow-yellow-500/20 active:scale-95'
                                                    }`}
                                            >
                                                {currentLesson.quiz_passed ? t('academy.classroom.reviewQuiz') : t('academy.classroom.takeQuiz') + ' →'}
                                            </button>
                                        </div>
                                    </div>
                                )}

                                {/* Next Lesson Preview (only if current completed) */}
                                {currentLesson.is_completed && (
                                    <div className="pt-6 flex justify-end">
                                        <button
                                            onClick={goToNextLesson}
                                            className="group flex items-center gap-4 px-8 py-5 bg-white/5 border border-white/10 rounded-2xl hover:bg-white/10 hover:border-yellow-500/50 transition-all text-left"
                                        >
                                            <div>
                                                <p className="text-[10px] font-black text-yellow-500 uppercase tracking-widest mb-1">{t('academy.classroom.upNext')}</p>
                                                <p className="font-bold text-white group-hover:text-yellow-500 transition-colors line-clamp-1">
                                                    {(() => {
                                                        const allLessons = course.modules.flatMap(m => m.lessons);
                                                        const currentIdx = allLessons.findIndex(l => l.id === currentLesson.id);
                                                        return allLessons[currentIdx + 1]?.title || "Course Complete! 🎉";
                                                    })()}
                                                </p>
                                            </div>
                                            <div className="w-12 h-12 rounded-xl bg-yellow-500 flex items-center justify-center text-black">
                                                <i className="fas fa-chevron-right"></i>
                                            </div>
                                        </button>
                                    </div>
                                )}
                            </div>
                        ) : (
                            /* ===== NO LESSON SELECTED ===== */
                            <div className="flex flex-col items-center justify-center h-full text-gray-500 py-32">
                                <i className="fas fa-book-reader text-6xl mb-6 opacity-20"></i>
                                <h3 className="text-xl font-bold text-white mb-2">{t('academy.classroom.selectLesson')}</h3>
                                <p>Start your learning journey one step at a time.</p>
                            </div>
                        )}
                    </div>
                </main>

                {/* ===== SIDEBAR NAVIGATION ===== */}
                <aside className="w-96 bg-[#161a1e] border-l border-white/5 flex flex-col z-20 shadow-[-10px_0_30px_rgba(0,0,0,0.5)]">
                    <div className="p-6 border-b border-white/5 bg-[#1e2329]/50">
                        <h3 className="text-sm font-black uppercase tracking-widest text-gray-400">{t('academy.classroom.syllabus')}</h3>
                        <div className="mt-2 flex items-center gap-3 text-xs text-gray-500">
                            <span className="flex items-center gap-1">
                                <div className="w-2 h-2 rounded-full bg-green-500"></div> {t('academy.classroom.completedStatus')}
                            </span>
                            <span className="flex items-center gap-1">
                                <div className="w-2 h-2 rounded-full bg-yellow-500"></div> {t('academy.classroom.currentStatus')}
                            </span>
                            <span className="flex items-center gap-1">
                                <div className="w-2 h-2 rounded-full bg-gray-600"></div> {t('academy.classroom.lockedStatus')}
                            </span>
                        </div>
                    </div>

                    <div className="flex-1 overflow-y-auto custom-scrollbar">
                        {course.modules.map((module, mIdx) => (
                            <div key={module.id} className="border-b border-white/5 last:border-0">
                                {/* Module Header */}
                                <div className="px-6 py-4 bg-[#1e2329]/20 flex items-center justify-between">
                                    <div className="flex items-center gap-3">
                                        <span className="text-[10px] font-black text-white/30">
                                            {t('academy.classroom.modules').toUpperCase()} {String(mIdx + 1).padStart(2, '0')}
                                        </span>
                                        <h4 className="text-sm font-bold text-gray-200 uppercase tracking-tight">
                                            {module.title}
                                        </h4>
                                    </div>
                                    {module.is_completed && (
                                        <div className="w-5 h-5 rounded-full bg-green-500 flex items-center justify-center">
                                            <i className="fas fa-check text-[8px] text-black"></i>
                                        </div>
                                    )}
                                </div>

                                {/* Module Lessons */}
                                <div className="py-2">
                                    {module.lessons.map((lesson, lIdx) => (
                                        <button
                                            key={lesson.id}
                                            disabled={lesson.is_locked}
                                            onClick={() => handleLessonSelect(lesson)}
                                            className={`w-full px-6 py-3 flex items-center justify-between group transition-all ${currentLesson?.id === lesson.id
                                                ? 'bg-yellow-500/10 border-r-2 border-yellow-500'
                                                : 'hover:bg-white/5'
                                                } ${lesson.is_locked ? 'opacity-40 cursor-not-allowed' : 'cursor-pointer'}`}
                                        >
                                            <div className="flex items-center gap-3">
                                                <StatusIcon status={lesson.status} small />
                                                <div className="text-left">
                                                    <p className={`text-sm font-medium transition-colors ${currentLesson?.id === lesson.id ? 'text-yellow-500' : 'text-gray-300 group-hover:text-white'}`}>
                                                        {lesson.title}
                                                    </p>
                                                    <p className="text-[10px] text-gray-500 uppercase tracking-tighter">
                                                        {lesson.type}
                                                    </p>
                                                </div>
                                            </div>
                                            {lesson.quiz_passed && <i className="fas fa-medal text-[10px] text-yellow-500"></i>}
                                        </button>
                                    ))}
                                </div>
                            </div>
                        ))}
                    </div>
                </aside>
            </div>
        </div>
    );
};

export default CourseClassroom;
