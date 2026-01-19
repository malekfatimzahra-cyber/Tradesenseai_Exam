import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ChevronRight, ChevronDown, CheckCircle, PlayCircle, Trophy, Loader2 } from 'lucide-react';
import { motion } from 'framer-motion';
import Quiz from './academy/Quiz';
import { API_BASE } from '../store';

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
    has_final_exam?: boolean;
    final_exam_id?: number | null;
}

const CourseViewer: React.FC = () => {
    // ... (existing state) ...

    const fetchCourseStructure = async () => {
        setLoading(true);
        try {
            const token = localStorage.getItem('auth_token');
            const url = `${API_BASE}/academy/course/${courseId}`;
            console.log("📡 Fetching Course:", courseId, "URL:", url);

            const res = await fetch(url, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            console.log("📡 Response Status:", res.status);

            if (res.ok) {
                const data = await res.json();
                setCourse(data);

                // Expand first module by default
                if (data.modules && data.modules.length > 0) {
                    setExpandedModules(prev => ({ ...prev, [data.modules[0].id]: true }));
                    // Auto-select first lesson if nothing selected
                    if (!selectedLessonId && data.modules[0].lessons.length > 0) {
                        handleSelectLesson(data.modules[0].lessons[0].id);
                    }
                }
                setError(null);
            } else {
                console.warn(`Course ${courseId} not found (404). Backend might be empty.`);
                const text = await res.text();
                setError(`Erreur ${res.status}: ${res.statusText} | Détails: ${text.substring(0, 100)}...`);
            }
        } catch (err: any) {
            console.error(err);
            setError(`Erreur Technique: ${err.message}. Vérifiez la console (F12).`);
        } finally {
            setLoading(false);
        }
    };

    // Diagnostic Tools
    const [showDebug, setShowDebug] = useState(false);
    const RENDER_URL = "https://tradesenseai-exam.onrender.com"; // Direct Backend URL

    const forceDirectFetch = async () => {
        setLoading(true);
        setError(null);
        try {
            const url = `${RENDER_URL}/api/academy/course/${courseId}`;
            console.log("⚡ Force Fetching Direct:", url);
            const res = await fetch(url);
            if (res.ok) {
                const data = await res.json();
                setCourse(data);
                if (data.modules?.length > 0) setExpandedModules(prev => ({ ...prev, [data.modules[0].id]: true }));
            } else {
                setError(`Direct Fetch Failed: ${res.status}`);
            }
        } catch (e: any) {
            setError(`Direct Fetch Error: ${e.message}`);
        }
        setLoading(false);
    };

    // ... (existing handlers) ...

    const handleStartFinalExam = async () => {
        if (!course?.final_exam_id) return;

        setLoading(true);
        try {
            const token = localStorage.getItem('auth_token');
            const res = await fetch(`${API_BASE}/academy/course/${course.id}/final-exam`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });

            if (res.ok) {
                const quizData = await res.json();
                setActiveQuizTitle(quizData.title);
                setActiveQuizQuestions(quizData.questions);
                setActiveQuizId(quizData.id);
                setActiveModuleId(null); // It's a course exam, not module
                setViewMode('MODULE_QUIZ');
                setSelectedLessonId(null);
                setActiveLesson(null);
            }
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    // ... (render) ...

    <div className="mt-8 pt-6 border-t border-[#1e2329]">
        {course.has_final_exam && (
            <button
                onClick={handleStartFinalExam}
                className="w-full flex items-center justify-center p-4 rounded-2xl font-bold border-2 border-dashed border-[#1e2329] text-gray-500 hover:border-yellow-500/50 hover:text-yellow-500 transition-all group"
            >
                <Trophy size={20} className="mr-2 group-hover:scale-110 transition-transform" />
                FINAL EXAM
            </button>
        )}
    </div>                </div >
            </div >

    { error && (
        <div className="bg-red-500/10 border border-red-500/30 p-6 rounded-xl text-center space-y-4 my-8">
            <i className="fas fa-exclamation-triangle text-3xl text-red-500"></i>
            <h3 className="text-xl font-bold text-red-500">Erreur de chargement</h3>
            <p className="text-red-400 font-mono text-sm bg-black/20 p-2 rounded">{error}</p>

            <div className="flex gap-4 justify-center">
                <button
                    onClick={() => window.location.reload()}
                    className="px-6 py-2 bg-gray-700 text-white rounded-lg hover:bg-gray-600 transition-all font-bold"
                >
                    <i className="fas fa-sync mr-2"></i> Rafraîchir
                </button>
                <button
                    onClick={forceDirectFetch}
                    className="px-6 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-500 transition-all font-bold"
                >
                    <i className="fas fa-bolt mr-2"></i> Mode Secours (Direct)
                </button>
            </div>

            <div className="pt-4 text-xs text-gray-500 cursor-pointer hover:text-gray-300" onClick={() => setShowDebug(!showDebug)}>
                {showDebug ? 'Masquer détails techniques' : 'Afficher détails techniques'}
            </div>

            {showDebug && (
                <div className="text-left bg-black/40 p-4 rounded text-xs font-mono text-gray-400 overflow-auto max-h-40">
                    <p>API Base: {API_BASE}</p>
                    <p>Course ID: {courseId}</p>
                    <p>Direct URL: {RENDER_URL}/api/academy/course/{courseId}</p>
                </div>
            )}
        </div>
    )}

{
    loading ? (
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
    )
}
        </main >
            </div >
        </div >
    );
};

export default CourseViewer;
