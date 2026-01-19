import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { CheckCircle, XCircle, RotateCcw, Trophy } from 'lucide-react';

interface QuizOption {
    id: number;
    text: string;
    is_correct: boolean;
}

interface QuizQuestion {
    id: number;
    text: string;
    options: QuizOption[];
    explanation?: string;
    correct_index?: number; // legacy support
}

interface QuizProps {
    title: string;
    questions: any[]; // Accepts both frontend QuizQuestion and backend/offline structure
    passingScore?: number;
    onComplete?: (score: number, passed: boolean, answers: Record<number, number>) => void;
    onRetry?: () => void;
    onContinue?: () => void;
}

const Quiz: React.FC<QuizProps> = ({ title, questions, passingScore = 60, onComplete, onRetry, onContinue }) => {
    const [currentIndex, setCurrentIndex] = useState(0);
    const [userAnswers, setUserAnswers] = useState<Record<number, number>>({}); // qIndex -> optionIndex
    const [isSubmitted, setIsSubmitted] = useState(false);
    const [score, setScore] = useState(0);

    // Normalize data structures
    const normalizedQuestions = questions.map((q, idx) => ({
        id: q.id !== undefined ? q.id : idx,
        text: q.question || q.text,
        explanation: q.explanation,
        options: q.options.map((opt: any, optIdx: number) => {
            if (typeof opt === 'string') {
                return { id: optIdx, text: opt, is_correct: optIdx === q.correct_index };
            }
            return {
                ...opt,
                id: opt.id !== undefined ? opt.id : optIdx
            };
        })
    }));

    const handleAnswer = (optionIndex: number) => {
        if (isSubmitted) return;
        setUserAnswers(prev => ({ ...prev, [currentIndex]: optionIndex }));
    };

    const handleSubmit = () => {
        let correctCount = 0;
        const formattedAnswers: Record<number, number> = {};

        normalizedQuestions.forEach((q, idx) => {
            const selectedOptionId = userAnswers[idx];
            formattedAnswers[q.id] = selectedOptionId;

            const correctOpt = q.options.find(o => o.is_correct);
            if (correctOpt && selectedOptionId === correctOpt.id) {
                correctCount++;
            }
        });

        const finalScore = Math.round((correctCount / normalizedQuestions.length) * 100);
        setScore(finalScore);
        setIsSubmitted(true);
        if (onComplete) onComplete(finalScore, finalScore >= passingScore, formattedAnswers);
    };

    const handleRetry = () => {
        setUserAnswers({});
        setIsSubmitted(false);
        setScore(0);
        setCurrentIndex(0);
        if (onRetry) onRetry();
    };

    // Results View
    if (isSubmitted) {
        const passed = score >= passingScore;
        return (
            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="max-w-3xl mx-auto text-center space-y-8 py-10">
                <div className={`inline-flex p-6 rounded-full ${passed ? 'bg-green-500/10 text-green-400 border border-green-500' : 'bg-red-500/10 text-red-500 border border-red-500'}`}>
                    {passed ? <Trophy size={64} /> : <XCircle size={64} />}
                </div>

                <h2 className="text-4xl font-bold text-white">{passed ? 'Congratulations!' : 'Keep Trying'}</h2>
                <p className="text-xl text-gray-400">You scored <span className={passed ? 'text-green-400 font-bold' : 'text-red-400 font-bold'}>{score}%</span></p>
                <p className="text-gray-500">{passed ? "You've mastered this section." : `You need ${passingScore}% to pass.`}</p>

                <div className="flex justify-center gap-4 pt-6">
                    <button
                        onClick={handleRetry}
                        className="flex items-center px-6 py-3 bg-gray-800 hover:bg-gray-700 text-white rounded-lg transition-colors border border-gray-700"
                    >
                        <RotateCcw size={18} className="mr-2" />
                        Retry Quiz
                    </button>
                    {passed && (
                        <button
                            onClick={onContinue}
                            className="px-6 py-3 bg-blue-600 hover:bg-blue-500 text-white rounded-lg font-bold shadow-lg shadow-blue-900/20"
                        >
                            Continue Learning
                        </button>
                    )}
                </div>

                <div className="mt-12 text-left space-y-6">
                    <h3 className="text-2xl font-bold border-b border-gray-800 pb-4">Review Answers</h3>
                    {normalizedQuestions.map((q, idx) => {
                        const selected = userAnswers[idx];
                        const correctOpt = q.options.find(o => o.is_correct);
                        const isCorrect = correctOpt?.id === selected;

                        return (
                            <div key={idx} className={`p-4 rounded-lg border ${isCorrect ? 'border-green-900/30 bg-green-900/5' : 'border-red-900/30 bg-red-900/5'}`}>
                                <p className="font-semibold text-lg mb-2">{idx + 1}. {q.text}</p>
                                <div className="flex justify-between text-sm text-gray-400 mb-2">
                                    <span>Your answer: <span className={isCorrect ? 'text-green-400' : 'text-red-400'}>{q.options[selected]?.text || 'Skipped'}</span></span>
                                    {!isCorrect && <span>Correct: <span className="text-green-400">{correctOpt?.text}</span></span>}
                                </div>
                                {q.explanation && (
                                    <div className="mt-2 text-xs bg-gray-800/50 p-2 rounded text-gray-300">
                                        <strong>Why? </strong> {q.explanation}
                                    </div>
                                )}
                            </div>
                        )
                    })}
                </div>
            </motion.div>
        );
    }

    // Question View
    const currentQ = normalizedQuestions[currentIndex];
    const progress = ((currentIndex + 1) / normalizedQuestions.length) * 100;

    return (
        <div className="max-w-3xl mx-auto py-8">
            <div className="flex items-center justify-between mb-8">
                <div>
                    <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-400">
                        {title}
                    </h1>
                    <p className="text-gray-400 mt-1">Question {currentIndex + 1} of {normalizedQuestions.length}</p>
                </div>
                {/* Progress Bar */}
                <div className="w-32 h-2 bg-gray-800 rounded-full overflow-hidden">
                    <div className="h-full bg-blue-500 transition-all duration-300" style={{ width: `${progress}%` }} />
                </div>
            </div>

            <motion.div
                key={currentIndex}
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                className="bg-[#161920] border border-gray-800 rounded-xl p-8 shadow-xl"
            >
                <div className="mb-8">
                    <h3 className="text-xl font-medium text-white leading-relaxed">{currentQ.text}</h3>
                </div>

                <div className="space-y-3">
                    {currentQ.options.map((opt, idx) => (
                        <button
                            key={idx}
                            onClick={() => handleAnswer(opt.id)}
                            className={`w-full text-left p-4 rounded-lg border transition-all duration-200 flex items-center justify-between group
                                ${userAnswers[currentIndex] === opt.id
                                    ? 'border-blue-500 bg-blue-500/10 text-blue-400'
                                    : 'border-gray-700 hover:border-gray-500 hover:bg-gray-800 text-gray-300'
                                }`}
                        >
                            <span className="flex items-center">
                                <span className={`flex items-center justify-center w-6 h-6 rounded-full mr-4 text-xs font-bold border
                                    ${userAnswers[currentIndex] === opt.id ? 'border-blue-500 bg-blue-500 text-white' : 'border-gray-600 text-gray-500'}
                                `}>
                                    {String.fromCharCode(65 + idx)}
                                </span>
                                {opt.text}
                            </span>
                            {userAnswers[currentIndex] === opt.id && <CheckCircle size={18} className="text-blue-500" />}
                        </button>
                    ))}
                </div>
            </motion.div>

            <div className="flex justify-between mt-8">
                <button
                    onClick={() => setCurrentIndex(prev => Math.max(0, prev - 1))}
                    disabled={currentIndex === 0}
                    className="px-6 py-2 rounded-lg text-gray-400 hover:text-white disabled:opacity-30 disabled:hover:text-gray-400 transition-colors"
                >
                    Previous
                </button>

                {currentIndex === normalizedQuestions.length - 1 ? (
                    <button
                        onClick={handleSubmit}
                        disabled={Object.keys(userAnswers).length !== normalizedQuestions.length}
                        className="px-8 py-3 bg-green-600 hover:bg-green-500 text-white font-bold rounded-lg shadow-lg shadow-green-900/20 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                    >
                        Submit Quiz
                    </button>
                ) : (
                    <button
                        onClick={() => setCurrentIndex(prev => Math.min(normalizedQuestions.length - 1, prev + 1))}
                        // Allow next even if not answered? Usually yes for UX, warn at end
                        className="px-8 py-3 bg-blue-600 hover:bg-blue-500 text-white font-bold rounded-lg shadow-lg shadow-blue-900/20 transition-all"
                    >
                        Next Question
                    </button>
                )}
            </div>
        </div>
    );
};

export default Quiz;
