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
            // FIX: Singular 'course'
            const res = await fetch(`${API_BASE}/academy/course/${courseId}`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });

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
            } else {
                setError("Cours introuvable (404).");
            }
        } catch (err) {
            console.error(err);
            setError("Erreur de connexion au serveur.");
        } finally {
            setLoading(false);
        }
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

    {/* MAIN CONTENT AREA */ }
    < div className = "flex-1 overflow-y-auto bg-[#0b0e11] flex flex-col items-center" >
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
            </div >
        </div >
    );
};

export default CourseViewer;
