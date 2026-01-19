import React, { useState, useEffect } from 'react';
import {
    Users, Activity, CheckCircle, XCircle, Search,
    Filter, ChevronLeft, ChevronRight, Shield, RefreshCw
} from 'lucide-react';
import { toast } from 'react-hot-toast';
import { useStore, API_BASE } from '../store';

// Types
interface Challenge {
    challenge_id: number;
    user_name: string;
    user_email: string;
    user_avatar: string | null;
    plan: string;
    equity: number;
    profit_loss: number;
    status: string;
    created_at: string;
}

interface DashboardStats {
    total_users: number;
    active_challenges: number;
    passed_challenges: number;
    failed_challenges: number;
}

const AdminDashboard: React.FC = () => {
    const { currentUser } = useStore();

    // State
    const [stats, setStats] = useState<DashboardStats>({
        total_users: 0,
        active_challenges: 0,
        passed_challenges: 0,
        failed_challenges: 0
    });

    const [challenges, setChallenges] = useState<Challenge[]>([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');
    const [statusFilter, setStatusFilter] = useState('All');
    const [currentPage, setCurrentPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const [refreshTrigger, setRefreshTrigger] = useState(0);

    // Fetch Stats
    useEffect(() => {
        const fetchStats = async () => {
            try {
                // Use Admin Key directly for instant access
                const res = await fetch(`${API_BASE}/admin/dashboard`, {
                    headers: {
                        'Authorization': `Bearer demo`, // Dummy token if needed
                        'X-ADMIN-KEY': 'TRADESENSE_SUPER_SECRET_2026'
                    }
                });

                if (res.ok) {
                    const data = await res.json();
                    setStats(data);
                } else {
                    const errorText = await res.text();
                    console.error("Failed to fetch stats:", errorText);
                    // Don't toast here to avoid spamming on mount if auth fails
                }
            } catch (err) {
                console.error("Failed to fetch stats", err);
            }
        };
        fetchStats();
    }, [refreshTrigger]);

    // Fetch Challenges
    useEffect(() => {
        const fetchChallenges = async () => {
            setLoading(true);
            try {
                const query = new URLSearchParams({
                    page: currentPage.toString(),
                    limit: '10',
                    search: searchTerm,
                    status: statusFilter
                });

                const res = await fetch(`${API_BASE}/admin/challenges?${query.toString()}`, {
                    headers: {
                        'Authorization': `Bearer demo`,
                        'X-ADMIN-KEY': 'TRADESENSE_SUPER_SECRET_2026'
                    }
                });

                if (res.ok) {
                    const data = await res.json();
                    setChallenges(data.challenges);
                    setTotalPages(data.pages);
                } else {
                    const errData = await res.json().catch(() => ({ message: 'Unknown Error' }));
                    console.error("Fetch Challenges Error:", errData);
                    toast.error(`Error loading data: ${errData.message}`);
                }
            } catch (err) {
                console.error("Network Error:", err);
                toast.error("Failed to load challenges: Network Error");
            } finally {
                setLoading(false);
            }
        };

        // Debounce search
        const timeout = setTimeout(fetchChallenges, 300);
        return () => clearTimeout(timeout);
    }, [currentPage, searchTerm, statusFilter, refreshTrigger]);

    const handleStatusChange = async (id: number, newStatus: string) => {
        if (!window.confirm(`Are you sure you want to set this challenge to ${newStatus}?`)) return;

        try {
            const res = await fetch(`${API_BASE}/admin/challenges/${id}/status`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer demo`,
                    'X-ADMIN-KEY': 'TRADESENSE_SUPER_SECRET_2026'
                },
                body: JSON.stringify({ status: newStatus })
            });

            const data = await res.json().catch(() => null);

            if (res.ok) {
                toast.success(`Challenge #${id} marked as ${newStatus}`);
                setRefreshTrigger(prev => prev + 1); // Refresh list and stats
            } else {
                console.error("Update Error:", data);
                // IF server returns 500, data might be { message: '...' }
                const errorMsg = data?.message || "Server Error";
                toast.error(`Failed to update: ${errorMsg}`);
            }
        } catch (err) {
            console.error("Network Error in handleStatusChange:", err);
            toast.error("Network error. Please check your connection.");
        }
    };

    return (
        <div className="min-h-screen bg-[#0b0e11] text-white p-8 font-sans">
            <div className="max-w-7xl mx-auto space-y-8">

                {/* Header */}
                <div className="flex justify-between items-end border-b border-gray-800 pb-6">
                    <div>
                        <h1 className="text-3xl font-bold tracking-tight text-white mb-2">ADMIN DASHBOARD</h1>
                        <p className="text-gray-400">Manage all user challenges and manually pass or fail accounts.</p>
                    </div>
                    <div className="flex items-center gap-3">
                        {currentUser?.role === 'SUPERADMIN' && (
                            <a
                                href="/admin/paypal"
                                className="flex items-center gap-2 text-sm bg-blue-500/10 hover:bg-blue-500/20 text-blue-400 px-4 py-2 rounded-lg border border-blue-500/20 transition-all"
                            >
                                <svg className="w-4 h-4" viewBox="0 0 24 24">
                                    <path fill="currentColor" d="M20.905 9.5c.21-1.302.024-2.19-.59-2.811-.673-.68-1.902-1-3.445-1h-5.113c-.341 0-.632.248-.686.584l-2.024 12.845c-.04.254.156.482.413.482h3.007l.755-4.784-.024.15c.054-.335.343-.584.686-.584h1.429c2.808 0 5.005-1.14 5.647-4.437.02-.099.037-.195.053-.288.199-1.28.09-2.153-.587-2.777l-.521-.42z" />
                                </svg>
                                <span className="font-semibold">PayPal Config</span>
                            </a>
                        )}
                        <div className="flex items-center gap-2 text-sm text-yellow-500 bg-yellow-500/10 px-3 py-1 rounded-full border border-yellow-500/20">
                            <Shield size={16} />
                            <span className="font-bold">SUPERADMIN ACCESS</span>
                        </div>
                    </div>
                </div>

                {/* Stats Cards */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <StatCard
                        title="Total Users"
                        value={stats.total_users}
                        icon={<Users className="text-blue-500" />}
                        subColor="bg-blue-500/10"
                    />
                    <StatCard
                        title="Active Challenges"
                        value={stats.active_challenges}
                        icon={<Activity className="text-yellow-500" />}
                        subColor="bg-yellow-500/10"
                    />
                    <StatCard
                        title="Passed Challenges"
                        value={stats.passed_challenges}
                        icon={<CheckCircle className="text-green-500" />}
                        subColor="bg-green-500/10"
                    />
                    <StatCard
                        title="Failed Challenges"
                        value={stats.failed_challenges}
                        icon={<XCircle className="text-red-500" />}
                        subColor="bg-red-500/10"
                    />
                </div>

                {/* Filters & Actions */}
                <div className="flex flex-col md:flex-row justify-between gap-4 bg-[#15191e] p-4 rounded-xl border border-gray-800">
                    <div className="relative flex-1 max-w-md">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 w-5 h-5" />
                        <input
                            type="text"
                            placeholder="Search by name or email..."
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                            className="w-full bg-[#0b0e11] border border-gray-800 rounded-lg pl-10 pr-4 py-2 text-sm focus:border-yellow-500 focus:outline-none focus:ring-1 focus:ring-yellow-500 transition-all"
                        />
                    </div>

                    <div className="flex items-center gap-4">
                        <div className="flex items-center gap-2 bg-[#0b0e11] px-3 py-2 rounded-lg border border-gray-800">
                            <span className="text-gray-400 text-sm">Challenge Status:</span>
                            <select
                                value={statusFilter}
                                onChange={(e) => setStatusFilter(e.target.value)}
                                className="bg-transparent text-white text-sm font-medium focus:outline-none"
                            >
                                <option value="All">All</option>
                                <option value="ACTIVE">Active</option>
                                <option value="PASSED">Passed</option>
                                <option value="FAILED">Failed</option>
                            </select>
                        </div>
                        <button
                            onClick={() => setRefreshTrigger(prev => prev + 1)}
                            className="p-2 hover:bg-gray-800 rounded-lg transition-colors text-gray-400 hover:text-white"
                        >
                            <RefreshCw size={20} />
                        </button>
                    </div>
                </div>

                {/* Table */}
                <div className="bg-[#15191e] border border-gray-800 rounded-xl overflow-hidden shadow-2xl">
                    <div className="overflow-x-auto">
                        <table className="w-full text-left border-collapse">
                            <thead>
                                <tr className="text-gray-500 text-xs uppercase tracking-wider bg-[#1a2026] border-b border-gray-800">
                                    <th className="p-4 font-medium">User</th>
                                    <th className="p-4 font-medium">Email</th>
                                    <th className="p-4 font-medium">Plan</th>
                                    <th className="p-4 font-medium">Current Equity</th>
                                    <th className="p-4 font-medium">Profit / Loss</th>
                                    <th className="p-4 font-medium">Status</th>
                                    <th className="p-4 text-right font-medium">Actions</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-gray-800">
                                {loading ? (
                                    <tr>
                                        <td colSpan={7} className="p-8 text-center text-gray-500 animate-pulse">
                                            Loading challenges data...
                                        </td>
                                    </tr>
                                ) : challenges.length === 0 ? (
                                    <tr>
                                        <td colSpan={7} className="p-8 text-center text-gray-500">
                                            No challenges found matching your filters.
                                        </td>
                                    </tr>
                                ) : (
                                    challenges.map((row) => (
                                        <tr key={row.challenge_id} className="hover:bg-[#1f252b] transition-colors group">
                                            <td className="p-4">
                                                <div className="flex items-center gap-3">
                                                    <div className="w-8 h-8 rounded-full bg-gradient-to-br from-gray-700 to-gray-600 flex items-center justify-center text-xs font-bold text-white ring-2 ring-[#15191e]">
                                                        {row.user_name.charAt(0).toUpperCase()}
                                                    </div>
                                                    <span className="font-medium text-white">{row.user_name}</span>
                                                </div>
                                            </td>
                                            <td className="p-4 text-gray-400 text-sm">{row.user_email}</td>
                                            <td className="p-4">
                                                <span className="px-2 py-1 bg-gray-800 border border-gray-700 rounded text-xs text-gray-300 font-medium">
                                                    {row.plan}
                                                </span>
                                            </td>
                                            <td className="p-4 font-mono text-white">
                                                {row.equity.toLocaleString()} MAD
                                            </td>
                                            <td className={`p-4 font-mono font-bold ${row.profit_loss >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                                                {row.profit_loss > 0 && '+'}{row.profit_loss.toLocaleString()} MAD
                                            </td>
                                            <td className="p-4">
                                                <StatusBadge status={row.status} />
                                            </td>
                                            <td className="p-4 text-right">
                                                <div className="flex justify-end gap-2 opacity-50 group-hover:opacity-100 transition-opacity">
                                                    {row.status === 'ACTIVE' ? (
                                                        <>
                                                            <ActionButton
                                                                onClick={() => handleStatusChange(row.challenge_id, 'PASSED')}
                                                                label="Set as Passed"
                                                                icon={<CheckCircle size={14} />}
                                                                color="text-green-500 border-green-500/20 hover:bg-green-500/10"
                                                            />
                                                            <ActionButton
                                                                onClick={() => handleStatusChange(row.challenge_id, 'FAILED')}
                                                                label="Set as Failed"
                                                                icon={<XCircle size={14} />}
                                                                color="text-red-500 border-red-500/20 hover:bg-red-500/10"
                                                            />
                                                        </>
                                                    ) : (
                                                        <span className="text-xs text-gray-600 italic px-2 py-1">Locked</span>
                                                    )}
                                                </div>
                                            </td>
                                        </tr>
                                    ))
                                )}
                            </tbody>
                        </table>
                    </div>

                    {/* Pagination */}
                    <div className="flex items-center justify-between p-4 border-t border-gray-800 bg-[#1a2026]">
                        <span className="text-sm text-gray-500">
                            Page {currentPage} of {totalPages}
                        </span>
                        <div className="flex gap-2">
                            <button
                                onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                                disabled={currentPage === 1}
                                className="p-2 rounded bg-[#0b0e11] border border-gray-800 text-gray-400 hover:text-white disabled:opacity-50 transition-colors"
                            >
                                <ChevronLeft size={16} />
                            </button>
                            <button
                                onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
                                disabled={currentPage === totalPages}
                                className="p-2 rounded bg-[#0b0e11] border border-gray-800 text-gray-400 hover:text-white disabled:opacity-50 transition-colors"
                            >
                                <ChevronRight size={16} />
                            </button>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    );
};

// Sub-components for cleaner code
const StatCard = ({ title, value, icon, subColor }: { title: string, value: number, icon: React.ReactNode, subColor: string }) => (
    <div className="bg-[#15191e] p-6 rounded-xl border border-gray-800 hover:border-gray-700 transition-all shadow-lg flex flex-col justify-between h-32 relative overflow-hidden group">
        <div className={`absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity transform group-hover:scale-110 ${subColor.replace('bg-', 'text-')}`}>
            {React.cloneElement(icon as React.ReactElement, { size: 64 })}
        </div>
        <div className="flex items-center gap-2 text-gray-400 text-sm font-medium z-10">
            {icon} {title}
        </div>
        <div className="text-4xl font-bold text-white tracking-tight z-10">
            {value.toLocaleString()}
        </div>
    </div>
);

const StatusBadge = ({ status }: { status: string }) => {
    const styles: Record<string, string> = {
        ACTIVE: 'bg-blue-500/10 text-blue-500 border-blue-500/20',
        PASSED: 'bg-green-500/10 text-green-500 border-green-500/20',
        FAILED: 'bg-red-500/10 text-red-500 border-red-500/20',
        PENDING: 'bg-yellow-500/10 text-yellow-500 border-yellow-500/20',
    };
    return (
        <span className={`px-3 py-1 rounded-full text-xs font-bold border ${styles[status] || 'bg-gray-700 text-gray-400'}`}>
            {status}
        </span>
    );
};

const ActionButton = ({ onClick, label, icon, color }: { onClick: () => void, label: string, icon: React.ReactNode, color: string }) => (
    <button
        onClick={onClick}
        className={`flex items-center gap-2 px-3 py-1.5 rounded-lg border text-xs font-bold transition-all ${color}`}
    >
        {icon} {label}
    </button>
);

export default AdminDashboard;
