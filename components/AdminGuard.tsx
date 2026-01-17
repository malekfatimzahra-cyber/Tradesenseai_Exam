import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useStore } from '../store';
import { UserRole } from '../types';

interface AdminGuardProps {
    children: React.ReactNode;
    requiredRole?: UserRole; // If specified, strictly requires this role (e.g., SUPERADMIN)
}

const AdminGuard: React.FC<AdminGuardProps> = ({ children, requiredRole }) => {
    const { currentUser } = useStore();
    const navigate = useNavigate();

    useEffect(() => {
        if (!currentUser) {
            navigate('/'); // Not logged in -> Home
            return;
        }

        if (requiredRole && currentUser.role !== requiredRole) {
            navigate('/'); // Doesn't match specific role -> Home
            return;
        }

        if (currentUser.role !== 'ADMIN' && currentUser.role !== 'SUPERADMIN') {
            navigate('/'); // Not an admin -> Home (Dashboard removed)
        }
    }, [currentUser, navigate, requiredRole]);

    if (!currentUser || (currentUser.role !== 'ADMIN' && currentUser.role !== 'SUPERADMIN')) {
        return null; // or a loading spinner while redirecting
    }

    if (requiredRole && currentUser.role !== requiredRole) {
        return null;
    }

    return <>{children}</>;
};

export default AdminGuard;
