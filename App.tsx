import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation, useNavigate, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import Terminal from './components/Terminal';
import Pricing from './components/Pricing';
import Community from './components/Community';
import AcademyDashboard from './components/academy/AcademyDashboard';
import CourseViewer from './components/CourseViewer';

import NewsHub from './components/NewsHub';
import Leaderboard from './components/Leaderboard';
import MarketFeeds from './components/MarketFeedsComponent';
import Settings from './components/Settings';
import AdminDashboard from './components/AdminDashboard';
import PayPalSettings from './components/admin/PayPalSettings';
import ChallengesPage from './components/challenges/ChallengesPage';
import LandingPage from './components/LandingPage';

import { useStore } from './store';
import AdminGuard from './components/AdminGuard';
import Login from './components/auth/Login';
import Register from './components/auth/Register';
import ErrorBoundary from './components/ErrorBoundary';

import GeminiChatWidget from './components/GeminiChatWidget';

const AppContent: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { currentUser, hydrateFromBackend } = useStore();

  const isLoggedIn = !!currentUser;

  // Hydrate from backend on app mount
  useEffect(() => {
    const token = localStorage.getItem('auth_token');
    if (token && !currentUser) {
      hydrateFromBackend();
    }
  }, []);

  const handleStartChallenge = () => {
    navigate('/register');
  };

  const handleLogin = () => {
    navigate('/login');
  };

  // List of public paths
  const publicPaths = ['/', '/login', '/register'];
  const isPublicPage = publicPaths.includes(location.pathname);

  // Auto-redirect if trying to access private page while logged out
  useEffect(() => {
    if (!isLoggedIn && !isPublicPage) {
      console.log('Redirecting to login: not logged in and accessing private page');
      navigate('/login');
    }

    // Redirect logged-in users away from login/register only
    // We allow them to stay on Home ('/') if they want.
    /* 
    // REMOVED: Allow access to Login/Register even if logged in (for switching accounts or testing)
    if (isLoggedIn && (location.pathname === '/login' || location.pathname === '/register')) {
      console.log('Redirecting to challenges: already logged in');
      navigate('/challenges');
    } 
    */

    // Guard: Require Active Challenge for Terminal
    const protectedRoutes = ['/terminal'];
    if (isLoggedIn && !currentUser?.status /* checking if loaded */ && !isLoading && !activeAccount && protectedRoutes.includes(location.pathname)) {
      // Wait, currentUser status isn't reliable for challenge existence. activeAccount is.
      // If hydration finished (isLoading false) and no activeAccount, redirect.
    }
  }, [isLoggedIn, isPublicPage, location.pathname, navigate, currentUser]);

  // Dedicated Guard Effect for Challenge
  const { isLoading, activeAccount } = useStore();

  /*
  useEffect(() => {
    if (isLoggedIn && !isLoading && !activeAccount && location.pathname === '/terminal') {
      console.log('Redirecting to challenges: no active challenge');
      navigate('/challenges');
    }
  }, [isLoggedIn, isLoading, activeAccount, location.pathname, navigate]);
  */

  // Public wrapper (no sidebar)
  // Fix: Check path ONLY, do not check !isLoggedIn. 
  // This ensures Home stays stable even if user is logged in (or hydration finishes).
  if (isPublicPage) {
    if (location.pathname === '/login') return <><Login /><GeminiChatWidget /></>;
    if (location.pathname === '/register') return <><Register /><GeminiChatWidget /></>;
    // Pass different handler if logged in? 
    // If logged in, "Se connecter" -> Go to Dashboard
    const handleLandingLogin = () => {
      if (isLoggedIn) navigate('/terminal');
      else navigate('/login');
    };

    return <><LandingPage onStartChallenge={handleStartChallenge} onLogin={handleLandingLogin} /><GeminiChatWidget /></>;
  }

  // Fallback for transition state (checking auth)
  // Only show spinner if we are on a PRIVATE page and waiting for auth
  if (isLoading && !isPublicPage) {
    return (
      <div className="h-screen w-full bg-[#0b0e11] flex items-center justify-center">
        <div className="w-12 h-12 border-4 border-yellow-500/20 border-t-yellow-500 rounded-full animate-spin"></div>
      </div>
    );
  }

  // Otherwise show the full layout with sidebar and route content
  return (
    <Layout location={location} navigate={navigate}>
      <GeminiChatWidget />
      <Routes>

        <Route path="/terminal" element={<Terminal />} />
        <Route path="/news" element={<NewsHub />} />
        <Route path="/challenges" element={<ChallengesPage />} />
        <Route path="/community" element={<Community />} />
        <Route path="/education" element={<AcademyDashboard />} />
        <Route path="/academy/course/:courseId" element={<CourseViewer />} />
        <Route path="/leaderboard" element={<Leaderboard />} />
        <Route path="/marketfeeds" element={<MarketFeeds />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/admin" element={
          <AdminGuard>
            <AdminDashboard />
          </AdminGuard>
        } />
        <Route path="/admin/paypal" element={
          <AdminGuard requiredRole="SUPERADMIN">
            <PayPalSettings />
          </AdminGuard>
        } />
        <Route path="*" element={<Navigate to="/challenges" />} />
      </Routes>
    </Layout>
  );
};

import { Toaster } from 'react-hot-toast';

const App: React.FC = () => {
  return (
    <ErrorBoundary>
      <Toaster position="top-right" toastOptions={{
        style: {
          background: '#333',
          color: '#fff',
        },
      }} />
      <Router>
        <AppContent />
      </Router>
    </ErrorBoundary>
  );
};

export default App;