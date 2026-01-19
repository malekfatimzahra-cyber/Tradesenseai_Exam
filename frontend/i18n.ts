import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

// Translations
const resources = {
    en: {
        translation: {
            common: {
                loading: 'Loading...',
                error: 'An error occurred',
                networkError: 'Network error, please check your connection',
                back: 'Back',
                save: 'Save Changes',
                cancel: 'Cancel'
            },
            sidebar: {
                challenges: 'Challenges',
                terminal: 'Terminal',
                propHealth: 'Prop Health',
                leaderboard: 'Leaderboard',
                newsHub: 'News Hub',
                community: 'Community',
                academy: 'Academy',
                settings: 'Settings',
                liveEquity: 'Live Equity',
                premiumExpert: 'Premium Expert',
                marketFeeds: 'Market Feeds',
                adminConsole: 'Admin Console',
                feedsStatus: 'NY & Casablanca Feeds'
            },
            dashboard: {
                title: 'Become a Funded Trader',
                subtitle: 'Choose your challenge level, prove your skills in our simulation, and get access to institutional capital.',
                buyChallenge: 'Buy Challenge',
                funded: 'Funded',
                profitTarget: 'Profit Target',
                dailyLoss: 'Daily Loss Limit',
                maxDrawdown: 'Max Drawdown',
                leverage: 'Leverage',
                phase: 'Phase',
                accountBalance: 'Account Balance',
                institutionalSimulation: 'Institutional Simulation',
                newChallenge: 'New Challenge',
                withdrawPayout: 'Withdraw Payout',
                totalDrawdown: 'Total Drawdown',
                used: 'used',
                evaluationHistory: 'Evaluation History',
                aiAnalyzing: 'AI ANALYZING...',
                generateReport: 'GENERATE PERFORMANCE REPORT',
                date: 'DATE',
                asset: 'ASSET',
                type: 'TYPE',
                pnl: 'PNL',
                aiCoach: 'AI Prop Coach',
                grade: 'Grade',
                disciplineScore: 'Discipline Score',
                riskViolations: 'Risk Violations',
                allRulesRespected: 'All rules respected',
                noEvaluation: 'Complete at least 5 trades to unlock AI coaching insights.',
                totalPnl: 'Total PnL',
                activeTrades: 'Active Trades',
                winRate: 'Win Rate',
                weeklyPerformance: 'Weekly Performance',
                daily: 'Daily',
                weekly: 'Weekly',
                aiOptimization: 'AI Optimization',
                executionHistory: 'Execution History',
                table: {
                    asset: 'ASSET',
                    type: 'TYPE',
                    entry: 'ENTRY',
                    exit: 'EXIT',
                    pnl: 'PNL',
                    status: 'STATUS',
                    noTrades: 'No historical trades found.',
                    closed: 'Closed'
                }
            },
            newsHub: {
                title: 'Live News Hub',
                subtitle: 'Stay informed with real-time financial news and AI summaries.',
                features: {
                    realTime: 'Real-time financial news',
                    aiSummary: 'AI-generated market summaries',
                    alerts: 'Economic event alerts',
                    ahead: 'Always stay ahead'
                },
                latestNews: 'Latest News',
                aiMarketSummary: 'AI Market Summary',
                generating: 'Generating...',
                generateNew: 'Generate New Summary',
                economicCalendar: 'Economic Calendar',
                impact: {
                    high: 'High Impact',
                    medium: 'Medium',
                    low: 'Low'
                },
                forecast: 'Forecast',
                sentiment: {
                    bullish: 'Bullish',
                    bearish: 'Bearish',
                    neutral: 'Neutral'
                }
            },
            community: {
                title: 'Community Zone',
                subtitle: 'Build a strong network around your growth.',
                navigation: 'Navigation',
                feed: 'News Feed',
                friends: 'My Friends',
                groups: 'Groups',
                events: 'Events',
                myGroups: 'My Groups',
                members: 'members',
                whatsYourStrategy: 'What is your strategy today?',
                publish: 'Publish',
                topTraders: 'Top Traders to Follow',
                follow: 'Follow',
                following: 'Following',
                trendingTopics: 'Trending Topics',
                posts: 'posts',
                thisMonth: 'this month',
                tradingChart: 'Trading Chart',
                expert: 'Expert',
                inviteFriends: 'Invite Friends',
                manageConnections: 'Manage your connections and invite new traders.',
                createGroup: 'Create a Group',
                discoverGroups: 'Discover and join trading groups.',
                viewEvents: 'View Events',
                participateEvents: 'Participate in webinars and live trading sessions.',
                nextEventMsg: 'Next Event: Live Trading Masterclass (Tuesday 10AM)',
                groupJoined: 'Joined group:',
                syncing: 'Syncing...',
                loadingTraders: 'Loading traders...',
                createdGroups: 'Your Created Groups'
            },
            terminal: {
                executionPrice: 'Execution Price (Real-Time)',
                institutionalBlotter: 'Institutional Blotter',
                totalExposure: 'TOTAL EXPOSURE',
                noActiveExposure: 'No active market exposure',
                asset: 'Asset',
                type: 'Type',
                size: 'Size',
                action: 'Action',
                close: 'Close',
                executeTrade: 'Execute Trade',
                positionSize: 'Position Size (Lot)',
                buyLong: 'Buy / Long',
                sellShort: 'Sell / Short',
                brokerSpread: 'Broker Spread',
                estMargin: 'Est. Margin Req',
                accountEquity: 'Account Equity',
                lockedPool: 'Locked Evaluation Pool',
                noActiveChallenge: 'No evaluation active. Start a challenge to access institutional liquidity.',
                selectPlanFirst: 'Select a challenge plan first.',
                dayPnL: 'Day PnL',
                discipline: 'Discipline',
                proMode: 'Pro Mode',
                liteMode: 'Lite Mode',
                aiBias: 'AI Bias',
                volatilityWarning: 'High Volatility Warning',
                tabs: {
                    positions: 'Positions',
                    journal: 'Journal',
                    analytics: 'Analytics'
                },
                table: {
                    ticker: 'Ticker',
                    type: 'Type',
                    size: 'Size',
                    entry: 'Entry',
                    current: 'Current',
                    pnl: 'PnL',
                    actions: 'Actions'
                },
                journal: {
                    placeholder: 'Log your thoughts, emotions, and thesis...',
                    save: 'Save Entry',
                    empty: 'No entries yet. Discipline starts here.',
                    confident: 'Confident',
                    anxious: 'Anxious'
                },
                analytics: {
                    active: 'Analytics Module Active',
                    processing: 'Processing trade history for behavioral patterns...'
                },
                execution: 'Execution',
                smartSize: 'Smart Size',
                amountMad: 'Amount (MAD)',
                leverage: 'Leverage',
                long: 'LONG',
                short: 'SHORT'
            },
            leaderboard: {
                title: 'Elite Hall of Fame',
                subtitle: 'Verify the performance of our funded traders. Real data, real payouts.',
                adminControl: 'Admin Control Space',
                fetching: 'Fetching rankings...',
                noTraders: 'No traders ranked yet',
                beFirst: 'Be the first to pass a challenge and claim your spot on the Hall of Fame!',
                table: {
                    rank: 'Rank',
                    trader: 'Trader',
                    country: 'Country',
                    funded: 'Funded',
                    profit: 'Profit',
                    roi: 'ROI',
                    winRate: 'Win Rate'
                },
                drawer: {
                    totalPayouts: 'Total Payouts',
                    fundedCap: 'Funded Cap',
                    locked: 'Advanced Stats Locked',
                    lockedDesc: 'Consistency score, trade history, and risk breakdown are reserved for Pro members.',
                    unlock: 'Unlock Data',
                    audit: 'Performance Audit',
                    consistency: 'Consistency Score',
                    riskMgmt: 'Risk Management',
                    latestTrades: 'Latest Trades'
                }
            },
            academy: {
                title: 'MasterClass Academy',
                subtitle: 'Accelerate your trading career with structured, high-level education.',
                rank: 'Academy Rank',
                aiRec: 'AI Personalized Recommendation',
                analyzing: 'Analyzing your trading DNA...',
                focusOn: 'Focus on:',
                resume: 'RESUME LEARNING',
                modules: 'Modules',
                start: 'START MODULE',
                progress: 'Progress',
                aiReason: 'Our AI detected inconsistencies in your exit strategies. This module will help you master psychological barriers and maximize profit targets.',
                searchPlaceholder: 'Search for courses...',
                experience: 'Experience:',
                category: 'Category:',
                noCourses: 'No courses available',
                noCoursesDesc: 'No courses match your filters. Please try again later.',
                refresh: 'Refresh Academy',
                loading: 'Loading Academic Experience...',
                levels: {
                    all: 'ALL',
                    beginner: 'BEGINNER',
                    intermediate: 'INTERMEDIATE',
                    advanced: 'ADVANCED',
                    expert: 'EXPERT'
                },
                classroom: {
                    backToAcademy: 'Back to Academy',
                    completed: 'COMPLETED',
                    modules: 'Modules',
                    lessons: 'Lessons',
                    progress: 'Progress',
                    takeQuiz: 'Take Quiz',
                    reviewContent: 'Review Content',
                    quizPassed: 'Quiz Passed!',
                    keepLearning: 'Keep Learning!',
                    retryQuiz: 'Retry Quiz',
                    detailedFeedback: 'Detailed Feedback',
                    explanation: 'Explanation',
                    continueToNext: 'Continue to Next Lesson',
                    lockedMessage: 'This lesson is locked. Complete the previous lesson first.',
                    syllabus: 'Course Syllabus',
                    completedStatus: 'Completed',
                    currentStatus: 'Current',
                    lockedStatus: 'Locked',
                    upNext: 'Up Next',
                    selectLesson: 'Select a lesson to begin',
                    noContent: 'No content available for this lesson.',
                    quizRequired: 'A quiz is required at the end to proceed to the next lesson.',
                    readyForQuiz: 'Ready for the Quiz?',
                    passedMessage: 'You have successfully passed this lesson\'s quiz.',
                    passToUnlock: 'Pass the quiz to complete this lesson and unlock the next one.',
                    reviewQuiz: 'Review Quiz'
                }
            },
            pricing: {
                title: 'Pick Your Challenge',
                subtitle: 'Pass the evaluation, respect the drawdown, and manage up to 1M MAD.',
                initialFunding: 'Initial Funding Potential',
                mostPopular: 'MOST POPULAR',
                pay: 'PAY',
                securing: 'SECURING ACCESS...'
            },
            settings: {
                title: 'Account Settings',
                subtitle: 'Manage your TradeSense Prop account preferences',
                nav: {
                    profile: 'Profile',
                    security: 'Security',
                    preferences: 'Preferences',
                    appearance: 'Appearance'
                },
                groups: {
                    management: 'Management',
                    appSettings: 'App Settings',
                    system: 'System'
                },
                profile: {
                    title: 'Profile Settings',
                    fullName: 'Full Name',
                    email: 'Email Address',
                    accountType: 'Account Type',
                    accountNumber: 'Account Number',
                    joinDate: 'Join Date',
                    updateBtn: 'Update Profile'
                },
                security: {
                    title: 'Security Settings',
                    currentPwd: 'Current Password',
                    newPwd: 'New Password',
                    confirmPwd: 'Confirm New Password',
                    updateBtn: 'Update Password',
                    matchError: 'New passwords do not match!',
                    success: 'Password updated successfully!'
                },
                preferences: {
                    title: 'Preferences',
                    riskLevel: 'Risk Level'
                },
                appearance: {
                    title: 'Appearance',
                    darkMode: 'Dark Mode',
                    lightMode: 'Light Mode',
                    system: 'System'
                },
                language: {
                    title: 'Language',
                    en: 'English',
                    fr: 'Français',
                    ar: 'العربية'
                },
                notifications: {
                    title: 'Notifications',
                    email: { title: 'Email Notifications', desc: 'Receive email updates' },
                    push: { title: 'Push Notifications', desc: 'Receive push notifications' },
                    market: { title: 'Market News', desc: 'Receive market updates' },
                    promo: { title: 'Promotional', desc: 'Receive promotional offers' },
                    priceAlerts: 'Price Alerts',
                    priceDesc: 'Get notified when assets hit your target prices.',
                    riskAlerts: 'Risk Checks',
                    riskDesc: 'Alerts when positions exceed risk parameters.',
                    newsAlerts: 'Breaking News',
                    newsDesc: 'Important market news alerts.',
                    weekly: 'Weekly Progress Report',
                    weeklyDesc: 'Receive a summary of your trading performance via email.'
                },
                trading: {
                    title: 'Trading Preferences',
                    defaultMarket: 'Default Market',
                    defaultMarketDesc: 'Which market to show when opening the terminal.',
                    positionSize: 'Default Position Size ($)',
                    positionDesc: 'This amount will be pre-filled in the order form.',
                    confirm: 'Confirm Before Executing',
                    confirmDesc: 'Show a confirmation modal before placing any trade.',
                    oneClick: 'One-Click Trading Mode',
                    oneClickDesc: 'Execute trades instantly without confirmation (Dangerous).'
                },
                privacy: {
                    title: 'Privacy & Data',
                    public: 'Public Profile',
                    publicDesc: 'Show your username and win-rate on the public leaderboard.',
                    analytics: 'Share Analytics',
                    analyticsDesc: 'Allow TradeSense to use anonymized trading data to improve AI models.'
                },
                session: {
                    title: 'Session Management',
                    signOut: 'Sign Out',
                    signOutDesc: 'End your current session securely.',
                    btn: 'Log Out',
                    modalTitle: 'Log Out?',
                    modalDesc: 'Are you sure you want to end your session?'
                },
                danger: {
                    title: 'Danger Zone',
                    reset: 'Reset Local Data',
                    resetDesc: 'Clears all settings and cached data from this browser.',
                    btnReset: 'Reset Data',
                    clear: 'Clear Course Progress',
                    clearDesc: 'Resets all your Academy learning progress to 0%.',
                    btnClear: 'Clear Progress'
                }
            },
            common: {
                live: 'Live',
                save: 'Save',
                cancel: 'Cancel',
                loading: 'Loading...',
                loginRequired: 'Please login to publish.',
                commentPlaceholder: 'Write a comment...',
                noComments: 'No comments yet.',
                justNow: 'Just now',
                ago: 'ago',
                h: 'h',
                m: 'm',
                member: 'member',
                members: 'members',
                yourGroups: 'Your Groups',
                traderProp: 'Prop Firm Trader'
            }
        }
    },
    fr: {
        translation: {
            sidebar: {
                challenges: 'Défis',
                terminal: 'Terminal',
                propHealth: 'Santé Prop',
                leaderboard: 'Classement',
                newsHub: 'Actualités',
                community: 'Communauté',
                academy: 'Académie',
                settings: 'Paramètres',
                liveEquity: 'CP Actuels',
                premiumExpert: 'Expert Premium',
                marketFeeds: 'Marchés Live',
                adminConsole: 'Console Admin',
                feedsStatus: 'Flux NY & Casablanca'
            },
            dashboard: {
                title: 'Devenez un Trader Financé',
                subtitle: 'Choisissez votre niveau, prouvez vos compétences et accédez au capital institutionnel.',
                buyChallenge: 'Acheter le Défi',
                funded: 'Financé',
                profitTarget: 'Objectif de Profit',
                dailyLoss: 'Limite Perte Journ.',
                maxDrawdown: 'Perte Max Totale',
                leverage: 'Levier',
                phase: 'Phase',
                accountBalance: 'Solde du Compte',
                institutionalSimulation: 'Simulation Institutionnelle',
                newChallenge: 'Nouveau Défi',
                withdrawPayout: 'Retirer les Gains',
                totalDrawdown: 'Perte Totale',
                used: 'utilisé',
                evaluationHistory: 'Historique d\'Évaluation',
                aiAnalyzing: 'ANALYSE IA...',
                generateReport: 'GÉNÉRER RAPPORT PERFORMANCE',
                date: 'DATE',
                asset: 'ACTIF',
                type: 'TYPE',
                pnl: 'P&L',
                aiCoach: 'Coach Prop IA',
                grade: 'Note',
                disciplineScore: 'Score de Discipline',
                riskViolations: 'Violations de Risque',
                allRulesRespected: 'Toutes les règles respectées',
                noEvaluation: 'Complétez au moins 5 trades pour débloquer le coaching IA.',
                totalPnl: 'P&L Total',
                activeTrades: 'Trades Actifs',
                winRate: 'Taux de Réussite',
                weeklyPerformance: 'Performance Hebdomadaire',
                daily: 'Journalier',
                weekly: 'Hebdomadaire',
                aiOptimization: 'Optimisation IA',
                executionHistory: 'Historique d\'Exécution',
                table: {
                    asset: 'ACTIF',
                    type: 'TYPE',
                    entry: 'ENTRÉE',
                    exit: 'SORTIE',
                    pnl: 'P&L',
                    status: 'STATUT',
                    noTrades: 'Aucun trade historique trouvé.',
                    closed: 'Fermé'
                }
            },
            newsHub: {
                title: 'Hub d\'Actualités en Direct',
                subtitle: 'Restez informé avec des actualités financières en temps réel et des résumés IA.',
                features: {
                    realTime: 'Actualités financières en temps réel',
                    aiSummary: 'Résumés de marché créés par l\'IA',
                    alerts: 'Alertes d\'événements économiques',
                    ahead: 'Gardez toujours une longueur d\'avance'
                },
                latestNews: 'Dernières Actualités',
                aiMarketSummary: 'Résumé de Marché par IA',
                generating: 'Génération en cours...',
                generateNew: 'Générer Nouveau Résumé',
                economicCalendar: 'Calendrier Économique',
                impact: {
                    high: 'Impact Élevé',
                    medium: 'Moyen',
                    low: 'Faible'
                },
                forecast: 'Prévision',
                sentiment: {
                    bullish: 'Haussier',
                    bearish: 'Baissier',
                    neutral: 'Neutre'
                }
            },
            community: {
                title: 'Zone Communautaire',
                subtitle: 'Cela construit un réseau solide autour de votre croissance.',
                navigation: 'Navigation',
                feed: 'Fil d\'actualité',
                friends: 'Mes Amis',
                groups: 'Groupes',
                events: 'Événements',
                myGroups: 'Mes Groupes',
                members: 'membres',
                whatsYourStrategy: 'Quelle est votre stratégie aujourd\'hui ?',
                publish: 'Publier',
                topTraders: 'Top Traders à Suivre',
                follow: 'Suivre',
                following: 'Suivi',
                trendingTopics: 'Sujets Tendances',
                posts: 'posts',
                thisMonth: 'ce mois',
                tradingChart: 'Graphique de Trading',
                expert: 'Expert',
                inviteFriends: 'Inviter des Amis',
                manageConnections: 'Gérez vos connexions et invitez de nouveaux traders.',
                createGroup: 'Créer un Groupe',
                discoverGroups: 'Découvrez et rejoignez des groupes de trading.',
                viewEvents: 'Voir les Événements',
                participateEvents: 'Participez aux webinaires et sessions de trading en direct.',
                nextEventMsg: 'Prochain événement : Masterclass Trading Live (Mardi 10h)',
                groupJoined: 'Entrée dans le groupe :',
                syncing: 'Synchronisation...',
                loadingTraders: 'Chargement des traders...',
                createdGroups: 'Vos Groupes Créés'
            },
            terminal: {
                executionPrice: 'Prix d\'Exécution (Temps Réel)',
                institutionalBlotter: 'Carnet d\'Ordres Institutionnel',
                totalExposure: 'EXPOSITION TOTALE',
                noActiveExposure: 'Aucune exposition active',
                asset: 'Actif',
                type: 'Type',
                size: 'Taille',
                action: 'Action',
                close: 'Fermer',
                executeTrade: 'Exécuter Trade',
                positionSize: 'Taille Position (Lot)',
                buyLong: 'Achat / Long',
                sellShort: 'Vente / Short',
                brokerSpread: 'Spread Courtier',
                estMargin: 'Marge Est.',
                accountEquity: 'Capitaux Propres',
                lockedPool: 'Pool d\'Évaluation Verrouillé',
                noActiveChallenge: 'Aucune évaluation active. Commencez un défi.',
                selectPlanFirst: 'Sélectionnez un plan de défi d\'abord.',
                dayPnL: 'P&L du Jour',
                discipline: 'Discipline',
                proMode: 'Mode Pro',
                liteMode: 'Mode Lite',
                aiBias: 'Biais IA',
                volatilityWarning: 'Alerte de Volatilité Élevée',
                tabs: {
                    positions: 'Positions',
                    journal: 'Journal',
                    analytics: 'Analyses'
                },
                table: {
                    ticker: 'Ticker',
                    type: 'Type',
                    size: 'Taille',
                    entry: 'Entrée',
                    current: 'Actuel',
                    pnl: 'P&L',
                    actions: 'Actions'
                },
                journal: {
                    placeholder: 'Notez vos pensées, émotions et thèses...',
                    save: 'Enregistrer l\'Entrée',
                    empty: 'Aucune entrée pour le moment. La discipline commence ici.',
                    confident: 'Confiant',
                    anxious: 'Anxieux'
                },
                analytics: {
                    active: 'Module d\'Analyse Actif',
                    processing: 'Traitement de l\'historique des transactions pour les schémas comportementaux...'
                },
                execution: 'Exécution',
                smartSize: 'Taille Intelligente',
                amountMad: 'Montant (MAD)',
                leverage: 'Levier',
                long: 'ACHAT',
                short: 'VENTE'
            },
            leaderboard: {
                title: 'Hall of Fame Élite',
                subtitle: 'Vérifiez la performance de nos traders financés. Données réelles, paiements réels.',
                adminControl: 'Espace Contrôle Admin',
                fetching: 'Récupération du classement...',
                noTraders: 'Aucun trader classé pour le moment',
                beFirst: 'Soyez le premier à réussir un défi et réclamez votre place !',
                table: {
                    rank: 'Rang',
                    trader: 'Trader',
                    country: 'Pays',
                    funded: 'Financé',
                    profit: 'Profit',
                    roi: 'ROI',
                    winRate: 'Taux Réussite'
                },
                drawer: {
                    totalPayouts: 'Paiements Totaux',
                    fundedCap: 'Capital Financé',
                    locked: 'Stats Avancées Verrouillées',
                    lockedDesc: 'Score de cohérence et historique réservés aux membres Pro.',
                    unlock: 'Débloquer Données',
                    audit: 'Audit de Performance',
                    consistency: 'Score Cohérence',
                    riskMgmt: 'Gestion Risque',
                    latestTrades: 'Derniers Trades'
                }
            },
            academy: {
                title: 'Académie MasterClass',
                subtitle: 'Accélérez votre carrière de trading avec une éducation structurée.',
                rank: 'Rang Académie',
                aiRec: 'Recommandation Personnalisée IA',
                analyzing: 'Analyse de votre ADN de trading...',
                focusOn: 'Concentrez-vous sur :',
                resume: 'REPRENDRE',
                modules: 'Modules',
                start: 'COMMENCER',
                progress: 'Progression',
                searchPlaceholder: 'Rechercher un cours...',
                experience: 'Expérience :',
                category: 'Catégorie :',
                noCourses: 'Aucun cours disponible',
                noCoursesDesc: 'Aucun cours ne correspond à vos filtres. Veuillez réessayer plus tard.',
                refresh: 'Actualiser l\'Académie',
                loading: 'Chargement de l\'expérience académique...',
                levels: {
                    all: 'TOUS',
                    beginner: 'DÉBUTANT',
                    intermediate: 'INTERMÉDIAIRE',
                    advanced: 'AVANCÉ',
                    expert: 'EXPERT'
                },
                classroom: {
                    backToAcademy: 'Retour à l\'Académie',
                    completed: 'TERMINÉ',
                    modules: 'Modules',
                    lessons: 'Leçons',
                    progress: 'Progression',
                    takeQuiz: 'Passer le Quiz',
                    reviewContent: 'Réviser le contenu',
                    quizPassed: 'Quiz réussi !',
                    keepLearning: 'Continuez à apprendre !',
                    retryQuiz: 'Réessayer le Quiz',
                    detailedFeedback: 'Commentaires détaillés',
                    explanation: 'Explication',
                    continueToNext: 'Leçon suivante',
                    lockedMessage: 'Cette leçon est verrouillée. Terminez la leçon précédente d\'abord.',
                    syllabus: 'Programme du cours',
                    completedStatus: 'Terminé',
                    currentStatus: 'En cours',
                    lockedStatus: 'Verrouillé',
                    upNext: 'À suivre',
                    selectLesson: 'Sélectionnez une leçon pour commencer',
                    noContent: 'Aucun contenu disponible pour cette leçon.',
                    quizRequired: 'Un quiz est requis à la fin pour passer à la leçon suivante.',
                    readyForQuiz: 'Prêt pour le Quiz ?',
                    passedMessage: 'Vous avez réussi le quiz de cette leçon.',
                    passToUnlock: 'Réussissez le quiz pour terminer cette leçon et débloquer la suivante.',
                    reviewQuiz: 'Voir le Quiz'
                }
            },
            pricing: {
                title: 'Choisissez Votre Défi',
                subtitle: 'Passez l\'évaluation, respectez le drawdown et gérez jusqu\'à 1M MAD.',
                initialFunding: 'Potentiel de Financement Initial',
                mostPopular: 'LE PLUS POPULAIRE',
                pay: 'PAYER',
                securing: 'SÉCURISATION...'
            },
            settings: {
                title: 'Paramètres du compte',
                subtitle: 'Gérez vos préférences de compte TradeSense Prop',
                nav: {
                    profile: 'Profil',
                    security: 'Sécurité',
                    preferences: 'Préférences',
                    appearance: 'Apparence'
                },
                groups: {
                    management: 'Gestion',
                    appSettings: 'Paramètres App',
                    system: 'Système'
                },
                profile: {
                    title: 'Paramètres du profil',
                    fullName: 'Nom complet',
                    email: 'Adresse e-mail',
                    accountType: 'Type de compte',
                    accountNumber: 'Numéro de compte',
                    joinDate: "Date d'inscription",
                    updateBtn: 'Mettre à jour'
                },
                security: {
                    title: 'Sécurité',
                    currentPwd: 'Mot de passe actuel',
                    newPwd: 'Nouveau mot de passe',
                    confirmPwd: 'Confirmer le mot de passe',
                    updateBtn: 'Mettre à jour mot de passe',
                    matchError: 'Les mots de passe ne correspondent pas !',
                    success: 'Mot de passe mis à jour avec succès !'
                },
                preferences: {
                    title: 'Préférences',
                    riskLevel: 'Niveau de risque'
                },
                appearance: {
                    title: 'Apparence',
                    darkMode: 'Mode Sombre',
                    lightMode: 'Mode Clair',
                    system: 'Système'
                },
                language: {
                    title: 'Langue',
                    en: 'English',
                    fr: 'Français',
                    ar: 'العربية'
                },
                notifications: {
                    title: 'Notifications',
                    email: { title: 'Notifications Email', desc: 'Recevoir des mises à jour par email' },
                    push: { title: 'Notifications Push', desc: 'Recevoir des notifications push' },
                    market: { title: "Actualités du marché", desc: 'Recevoir des mises à jour du marché' },
                    promo: { title: 'Offres promotionnelles', desc: 'Recevoir des offres promotionnelles' },
                    priceAlerts: 'Alertes de Prix',
                    priceDesc: 'Recevez une notification lorsque les actifs atteignent vos prix cibles.',
                    riskAlerts: 'Vérifications des Risques',
                    riskDesc: 'Alertes lorsque les positions dépassent les paramètres de risque.',
                    newsAlerts: 'Dernières Nouvelles',
                    newsDesc: 'Alertes importantes sur les nouvelles du marché.',
                    weekly: 'Rapport de Progrès Hebdomadaire',
                    weeklyDesc: 'Recevez un résumé de vos performances de trading par email.'
                },
                trading: {
                    title: 'Préférences de Trading',
                    defaultMarket: 'Marché par Défaut',
                    defaultMarketDesc: 'Quel marché afficher lors de l\'ouverture du terminal.',
                    positionSize: 'Taille de Position par Défaut ($)',
                    positionDesc: 'Ce montant sera pré-rempli dans le formulaire d\'ordre.',
                    confirm: 'Confirmer Avant l\'Exécution',
                    confirmDesc: 'Afficher une modale de confirmation avant de placer un trade.',
                    oneClick: 'Mode de Trading en Un Clic',
                    oneClickDesc: 'Exécuter des trades instantanément sans confirmation (Dangereux).'
                },
                privacy: {
                    title: 'Confidentialité et Données',
                    public: 'Profil Public',
                    publicDesc: 'Afficher votre nom d\'utilisateur et votre taux de réussite sur le classement public.',
                    analytics: 'Partager les Analyses',
                    analyticsDesc: 'Autoriser TradeSense à utiliser des données de trading anonymisées pour améliorer les modèles d\'IA.'
                },
                session: {
                    title: 'Gestion de Session',
                    signOut: 'Se Déconnecter',
                    signOutDesc: 'Terminez votre session actuelle en toute sécurité.',
                    btn: 'Se Déconnecter',
                    modalTitle: 'Se Déconnecter ?',
                    modalDesc: 'Êtes-vous sûr de vouloir terminer votre session ?'
                },
                danger: {
                    title: 'Zone de Danger',
                    reset: 'Réinitialiser Données Locales',
                    resetDesc: 'Efface tous les paramètres et données en cache de ce navigateur.',
                    btnReset: 'Réinitialiser',
                    clear: 'Effacer Progression Cours',
                    clearDesc: 'Réinitialise toute votre progression d\'apprentissage Académie à 0%.',
                    btnClear: 'Effacer Progression'
                }
            },
            common: {
                live: 'En Direct',
                save: 'Enregistrer',
                cancel: 'Annuler',
                loading: 'Chargement...',
                error: 'Une erreur est survenue',
                networkError: 'Erreur réseau, veuillez vérifier votre connexion',
                back: 'Retour',
                loginRequired: 'Veuillez vous connecter pour publier.',
                commentPlaceholder: 'Écrivez un commentaire...',
                noComments: 'Aucun commentaire pour le moment.',
                justNow: 'À l\'instant',
                ago: 'il y a',
                h: 'h',
                m: 'm',
                member: 'membre',
                members: 'membres',
                yourGroups: 'Vos Groupes',
                traderProp: 'Trader Prop Firm'
            }
        }
    },
    ar: {
        translation: {
            sidebar: {
                challenges: 'التحديات',
                terminal: 'محطة التداول',
                propHealth: 'صحة الحساب',
                leaderboard: 'المتصدرين',
                newsHub: 'مركز الأخبار',
                community: 'المجتمع',
                academy: 'الأكاديمية',
                levels: {
                    all: 'الكل',
                    beginner: 'مبتدئ',
                    intermediate: 'متوسط',
                    advanced: 'متقدم',
                    expert: 'خبير'
                },
                settings: 'الإعدادات',
                liveEquity: 'السيولة الحية',
                premiumExpert: 'خبير مميز',
                marketFeeds: 'تغذية السوق',
                adminConsole: 'وحة التحكم',
                feedsStatus: 'تغذية نيويورك والدار البيضاء'
            },
            dashboard: {
                title: 'كن متداولاً ممولاً',
                subtitle: 'اختر مستوى التحدي الخاص بك، وأثبت مهاراتك، واحصل على رأس المال.',
                buyChallenge: 'شراء التحدي',
                funded: 'ممول',
                profitTarget: 'هدف الربح',
                dailyLoss: 'حد الخسارة اليومي',
                maxDrawdown: 'الحد الأقصى للتراجع',
                leverage: 'الرافعة المالية',
                phase: 'المرحلة',
                accountBalance: 'رصيد الحساب',
                institutionalSimulation: 'محاكاة مؤسسية',
                newChallenge: 'تحدي جديد',
                withdrawPayout: 'سحب الأرباح',
                totalDrawdown: 'إجمالي التراجع',
                used: 'مستخدم',
                evaluationHistory: 'سجل التقييم',
                aiAnalyzing: 'تحليل الذكاء الاصطناعي...',
                generateReport: 'إنشاء تقرير الأداء',
                date: 'التاريخ',
                asset: 'الأصل',
                type: 'النوع',
                pnl: 'الربح/الخسارة',
                aiCoach: 'مدرب الذكاء الاصطناعي',
                grade: 'الدرجة',
                disciplineScore: 'درجة الانضباط',
                riskViolations: 'مخالفات المخاطر',
                allRulesRespected: 'تم احترام جميع القواعد',
                noEvaluation: 'أكمل ما لا يقل عن 5 صفقات لفتح رؤى التدريب بالذكاء الاصطناعي.',
                totalPnl: 'إجمالي الربح/الخسارة',
                activeTrades: 'الصفقات النشطة',
                winRate: 'معدل النجاح',
                weeklyPerformance: 'الأداء الأسبوعي',
                daily: 'يومي',
                weekly: 'أسبوعي',
                aiOptimization: 'تحسين الذكاء الاصطناعي',
                executionHistory: 'سجل التنفيذ',
                noTrades: 'لا توجد صفقات سابقة.',
                status: 'الحالة',
                closed: 'مغلق',
            },
            newsHub: {
                title: 'مركز الأخبار المباشر',
                subtitle: 'ابق على اطلاع مع الأخبار المالية في الوقت الحقيقي وملخصات الذكاء الاصطناعي.',
                features: {
                    realTime: 'أخبار مالية في الوقت الحقيقي',
                    aiSummary: 'ملخصات السوق المولدة بالذكاء الاصطناعي',
                    alerts: 'تنبيهات الأحداث الاقتصادية',
                    ahead: 'كن دائما في المقدمة'
                },
                latestNews: 'آخر الأخبار',
                aiMarketSummary: 'ملخص السوق بالذكاء الاصطناعي',
                generating: 'جار التوليد...',
                generateNew: 'توليد ملخص جديد',
                economicCalendar: 'التقويم الاقتصادي',
                impact: {
                    high: 'تأثير قوي',
                    medium: 'متوسط',
                    low: 'ضعيف'
                },
                forecast: 'التوقعات',
                sentiment: {
                    bullish: 'صعودي',
                    bearish: 'هبوطي',
                    neutral: 'محايد'
                }
            },
            community: {
                title: 'منطقة المجتمع',
                subtitle: 'ابن شبكة قوية حول نموك.',
                navigation: 'تصفح',
                feed: 'تغذية الأخبار',
                friends: 'أصدقائي',
                groups: 'المجموعات',
                events: 'الأحداث',
                myGroups: 'مجموعاتي',
                members: 'أعضاء',
                whatsYourStrategy: 'ما هي استراتيجيتك اليوم؟',
                publish: 'نشر',
                topTraders: 'أهم المتداولين',
                follow: 'متابعة',
                following: 'يتابع',
                trendingTopics: 'المواضيع الشائعة',
                posts: 'منشورات',
                thisMonth: 'هذا الشهر',
                tradingChart: 'رسم بياني للتداول',
                expert: 'خبير',
                inviteFriends: 'دعوة الأصدقاء',
                manageConnections: 'أدر اتصالاتك وادع متداولين جدد.',
                createGroup: 'إنشاء مجموعة',
                discoverGroups: 'اكتشف وانضم لمجموعات التداول.',
                viewEvents: 'عرض الأحداث',
                participateEvents: 'شارك في ندوات الإنترنت وجلسات التداول المباشرة.',
                nextEventMsg: 'الحدث التالي: ماستر كلاس التداول المباشر (الثلاثاء 10 صباحًا)',
                groupJoined: 'تم الانضمام إلى المجموعة:',
                syncing: 'جار المزامنة...',
                loadingTraders: 'جار تحميل المتداولين...',
                createdGroups: 'مجموعاتك التي أنشأتها'
            },
            terminal: {
                executionPrice: 'سعر التنفيذ (فوري)',
                institutionalBlotter: 'سجل الأوامر المؤسسي',
                totalExposure: 'إجمالي التعرض',
                noActiveExposure: 'لا يوجد تعرض نشط للسوق',
                asset: 'الأصل',
                type: 'النوع',
                size: 'الحجم',
                action: 'إجراء',
                close: 'إغلاق',
                executeTrade: 'تنفيذ صفقة',
                positionSize: 'حجم المركز (لوت)',
                buyLong: 'شراء / طويل',
                sellShort: 'بيع / قصير',
                brokerSpread: 'فارق السعر',
                estMargin: 'الهامش المقدر',
                accountEquity: 'حقوق الملكية',
                lockedPool: 'مجمع التقييم المقفل',
                noActiveChallenge: 'لا يوجد تقييم نشط. ابدأ تحدياً للوصول.',
                selectPlanFirst: 'اختر خطة تحدي أولاً.',
                dayPnL: 'ربح/خسارة اليوم',
                discipline: 'الانضباط',
                proMode: 'وضع المحترفين',
                liteMode: 'الوضع المبسط',
                aiBias: 'انحياز الذكاء الاصطناعي',
                volatilityWarning: 'تحذير من تقلبات عالية',
                tabs: {
                    positions: 'المراكز',
                    journal: 'المذكرة',
                    analytics: 'التحليلات'
                },
                table: {
                    ticker: 'الرمز',
                    type: 'النوع',
                    size: 'الحجم',
                    entry: 'الدخول',
                    current: 'الحالي',
                    pnl: 'الربح/الخسارة',
                    actions: 'الإجراءات'
                },
                journal: {
                    placeholder: 'سجل أفكارك ومشاعرك وأطروحتك...',
                    save: 'حفظ المدخلة',
                    empty: 'لا توجد مدخلات بعد. الانضباط يبدأ من هنا.',
                    confident: 'واثق',
                    anxious: 'قلق'
                },
                analytics: {
                    active: 'وحدة التحليلات نشطة',
                    processing: 'معالجة سجل التداول للأنماط السلوكية...'
                },
                execution: 'التنفيذ',
                smartSize: 'الحجم الذكي',
                amountMad: 'المبلغ (درهم)',
                leverage: 'الرافعة المالية',
                long: 'شراء',
                short: 'بيع'
            },
            leaderboard: {
                title: 'قاعة المشاهير للنخبة',
                subtitle: 'تحقق من أداء المتداولين الممولين لدينا.',
                adminControl: 'لوحة تحكم المسؤول',
                fetching: 'جلب التصنيفات...',
                noTraders: 'لا يوجد متداولين مصنفين بعد',
                beFirst: 'كن أول من يجتاز التحدي ويحجز مكانه!',
                table: {
                    rank: 'الرتبة',
                    trader: 'المتداول',
                    country: 'الدولة',
                    funded: 'ممول',
                    profit: 'الربح',
                    roi: 'العائد',
                    winRate: 'نسبة النجاح'
                },
                drawer: {
                    totalPayouts: 'إجمالي المدفوعات',
                    fundedCap: 'رأس المال الممول',
                    locked: 'الإحصائيات المتقدمة مقفلة',
                    lockedDesc: 'نتائج التناسق وسجل التداول محجوزة للأعضاء المحترفين.',
                    unlock: 'فتح البيانات',
                    audit: 'تدقيق الأداء',
                    consistency: 'نتيجة التناسق',
                    riskMgmt: 'إدارة المخاطر',
                    latestTrades: 'أحدث التداولات'
                }
            },
            academy: {
                title: 'أكاديمية الاحتراف',
                subtitle: 'سرع مسيرتك في التداول بتعليم منظم وعالي المستوى.',
                rank: 'رتبة الأكاديمية',
                aiRec: 'توصيات الذكاء الاصطناعي',
                analyzing: 'تحليل نمط تداولك...',
                focusOn: 'ركز على:',
                resume: 'استئناف التعلم',
                modules: 'وحدات',
                start: 'ابدأ الوحدة',
                progress: 'التقدم',
                aiReason: 'اكتشف الذكاء الاصطناعي لدينا تناقضات في استراتيجيات الخروج الخاصة بك. ستساعدك هذه الوحدة على اتقان الحواجز النفسية وتعظيم أهداف الربح.'
            },
            pricing: {
                title: 'اختر التحدي الخاص بك',
                subtitle: 'اجتز التقييم، واحترم قواعد التراجع، وأدر ما يصل إلى مليون درهم.',
                initialFunding: 'إمكانية التمويل الأولي',
                mostPopular: 'الأكثر شعبية',
                pay: 'دفع',
                securing: 'تأمين الوصول...'
            },
            settings: {
                title: 'إعدادات الحساب',
                subtitle: 'إدارة تفضيلات حساب TradeSense الخاص بك',
                nav: {
                    profile: 'الملف الشخصي',
                    security: 'الأمان',
                    preferences: 'التفضيلات',
                    appearance: 'المظهر'
                },
                groups: {
                    management: 'إدارة',
                    appSettings: 'إعدادات التطبيق',
                    system: 'النظام'
                },
                profile: {
                    title: 'إعدادات الملف الشخصي',
                    fullName: 'الاسم الكامل',
                    email: 'البريد الإلكتروني',
                    accountType: 'نوع الحساب',
                    accountNumber: 'رقم الحساب',
                    joinDate: 'تاريخ الانضمام',
                    updateBtn: 'تحديث الملف الشخصي'
                },
                security: {
                    title: 'إعدادات الأمان',
                    currentPwd: 'كلمة المرور الحالية',
                    newPwd: 'كلمة مرور جديدة',
                    confirmPwd: 'تأكيد كلمة المرور',
                    updateBtn: 'تحديث كلمة المرور',
                    matchError: 'كلمات المرور غير متطابقة!',
                    success: 'تم تحديث كلمة المرور بنجاح!'
                },
                preferences: {
                    title: 'التفضيلات',
                    riskLevel: 'مستوى المخاطرة'
                },
                appearance: {
                    title: 'المظهر',
                    darkMode: 'الوضع الداكن',
                    lightMode: 'الوضع الفاتح',
                    system: 'النظام'
                },
                language: {
                    title: 'اللغة',
                    en: 'English',
                    fr: 'Français',
                    ar: 'العربية'
                },
                notifications: {
                    title: 'الإشعارات',
                    email: { title: 'إشعارات البريد', desc: 'تلقي التحديثات عبر البريد الإلكتروني' },
                    push: { title: 'إشعارات الهاتف', desc: 'تلقي الإشعارات الفورية' },
                    market: { title: 'أخبار السوق', desc: 'تلقي تحديثات السوق' },
                    promo: { title: 'العروض الترويجية', desc: 'تلقي العروض الخاصة' },
                    priceAlerts: 'تنبيهات الأسعار',
                    priceDesc: 'احصل على إشعار عندما تصل الأصول إلى أسعارك المستهدفة.',
                    riskAlerts: 'فحوصات المخاطر',
                    riskDesc: 'تنبيهات عندما تتجاوز المراكز معايير المخاطر.',
                    newsAlerts: 'أخبار عاجلة',
                    newsDesc: 'تنبيهات أخبار السوق المهمة.',
                    weekly: 'تقرير التقدم الأسبوعي',
                    weeklyDesc: 'تلقي ملخص لأدائك في التداول عبر البريد الإلكتروني.'
                },
                trading: {
                    title: 'تفضيلات التداول',
                    defaultMarket: 'السوق الافتراضي',
                    defaultMarketDesc: 'أي سوق يظهر عند فتح المحطة.',
                    positionSize: 'حجم المركز الافتراضي ($)',
                    positionDesc: 'سيتم ملء هذا المبلغ مسبقًا في نموذج الطلب.',
                    confirm: 'تأكيد قبل التنفيذ',
                    confirmDesc: 'إظهار نافذة تأكيد قبل وضع أي صفقة.',
                    oneClick: 'وضع التداول بنقرة واحدة',
                    oneClickDesc: 'تنفيد الصفقات فوراً بدون تأكيد (خطر).'
                },
                privacy: {
                    title: 'الخصوصية والبيانات',
                    public: 'الملف العام',
                    publicDesc: 'إظهار اسم المستخدم ونسبة الفوز في لوحة المتصدرين العامة.',
                    analytics: 'مشاركة التحليلات',
                    analyticsDesc: 'السماح لـ TradeSense باستخدام بيانات تداول مجهولة المصدر لتحسين نماذج الذكاء الاصطناعي.'
                },
                session: {
                    title: 'إدارة الجلسة',
                    signOut: 'تسجيل الخروج',
                    signOutDesc: 'إنهاء جلستك الحالية بأمان.',
                    btn: 'تسجيل الخروج',
                    modalTitle: 'تسجيل الخروج؟',
                    modalDesc: 'هل أنت متأكد أنك تريد إنهاء جلستك؟'
                },
                danger: {
                    title: 'منطقة الخطر',
                    reset: 'إعادة تعيين البيانات المحلية',
                    resetDesc: 'يمسح جميع الإعدادات والبيانات المخزنة مؤقتًا من هذا المتصفح.',
                    btnReset: 'إعادة تعيين البيانات',
                    clear: 'مسح تقدم الدورة',
                    clearDesc: 'يعيد تعيين جميع تقدمك في الأكاديمية إلى 0٪.',
                    btnClear: 'مسح التقدم'
                }
            },
            common: {
                save: 'حفظ',
                cancel: 'إلغاء',
                loading: 'جار التحميل...',
                error: 'حدث خطأ ما',
                networkError: 'خطأ في الشبكة ، يرجى التحقق من اتصالك',
                back: 'رجوع',
                loginRequired: 'يرجى تسجيل الدخول للنشر.',
                commentPlaceholder: 'اكتب تعليقاً...',
                noComments: 'لا توجد تعليقات بعد.',
                justNow: 'الآن',
                ago: 'منذ',
                h: 'ساعة',
                m: 'دقيقة',
                member: 'عضو',
                members: 'أعضاء',
                yourGroups: 'مجموعاتك',
                traderProp: 'متداول شركة تمويل'
            }
        }
    }
};

i18n
    .use(LanguageDetector)
    .use(initReactI18next)
    .init({
        resources,
        fallbackLng: 'en',
        interpolation: {
            escapeValue: false // react already safes from xss
        },
        detection: {
            order: ['localStorage', 'navigator'],
            caches: ['localStorage']
        }
    });

// Handle RTL direction
i18n.on('languageChanged', (lng) => {
    document.dir = lng === 'ar' ? 'rtl' : 'ltr';
    document.documentElement.lang = lng;
});

export default i18n;
