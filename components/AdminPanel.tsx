import React, { useState, useEffect } from 'react';
import { Shield, Search, CheckCircle, XCircle, AlertTriangle, User, DollarSign, Activity } from 'lucide-react';
import { toast } from 'react-hot-toast';
import { API_BASE } from '../store';

interface Challenge {
    id: number;
    plan: string;
    start_balance: number;
    equity: number;
    profit_percent: number;
    status: string;
    created_at: string;
    admin_note?: string;
    reason?: string;
}

interface UserData {
    user_id: number;
    name: string;
    email: string;
    role: string;
    challenges: Challenge[];
    joined_at: string;
}

const AdminPanel: React.FC = () => {
    const [keyInput, setKeyInput] = useState('');
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [users, setUsers] = useState<UserData[]>([]);
    const [loading, setLoading] = useState(false);
    const [searchTerm, setSearchTerm] = useState('');
    const [filterStatus, setFilterStatus] = useState<string>('ALL');
    const [paypalData, setPaypalData] = useState({ client_id: '', email: '', is_configured: false });

    const fetchPaypalConfig = async () => {
        const token = localStorage.getItem('auth_token');
        try {
            const res = await fetch(`${API_BASE}/payments/config/paypal`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (res.ok) {
                const data = await res.json();
                setPaypalData(data);
            }
        } catch (error) { console.error(error); }
    };

    const savePaypalConfig = async () => {
        const token = localStorage.getItem('auth_token');
        try {
            const res = await fetch(`${API_BASE}/payments/config/paypal`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    client_id: paypalData.client_id,
                    email: paypalData.email,
                    secret: 'MOCK_SECRET_FOR_EXAM' // backend normally expects a secret
                })
            });
            if (res.ok) {
                toast.success('PayPal Config Saved');
                fetchPaypalConfig();
            }
        } catch (error) { toast.error('Failed to save config'); }
    };

    // Hardcoded key for demo convenience (matches backend default)
    const DEMO_KEY = 'TRADESENSE_SUPER_SECRET_2026';

    useEffect(() => {
        const storedKey = sessionStorage.getItem('ADMIN_KEY');
        if (storedKey) {
            verifyAndFetch(storedKey);
        }
    }, []);

    const verifyAndFetch = async (key: string) => {
        setLoading(true);
        try {
            const response = await fetch(`${API_BASE}/admin/users`, {
                headers: {
                    'X-ADMIN-KEY': key
                }
            });

            if (response.ok) {
                const data = await response.json();
                setUsers(data);
                setIsAuthenticated(true);
                sessionStorage.setItem('ADMIN_KEY', key);
                fetchPaypalConfig();
            } else {
                sessionStorage.removeItem('ADMIN_KEY');
                toast.error('Invalid Admin Key');
                setIsAuthenticated(false);
            }
        } catch (error) {
            console.error('Admin Fetch Error', error);
            toast.error('Connection Error');
        } finally {
            setLoading(false);
        }
    };

    const handleLogin = (e: React.FormEvent) => {
        e.preventDefault();
        verifyAndFetch(keyInput);
    };

    const updateStatus = async (challengeId: number, newStatus: string, currentNote?: string) => {
        if (!window.confirm(`Are you sure you want to set status to ${newStatus}?`)) return;

        const key = sessionStorage.getItem('ADMIN_KEY') || '';
        try {
            // Optional: Prompt for note
            const note = window.prompt("Add Admin Note (Optional):", currentNote || "");

            const res = await fetch(`${API_BASE}/admin/challenges/${challengeId}/status`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'X-ADMIN-KEY': key
                },
                body: JSON.stringify({
                    status: newStatus,
                    admin_note: note
                })
            });

            if (res.ok) {
                toast.success(`Status updated to ${newStatus}`);
                verifyAndFetch(key); // Refresh
            } else {
                toast.error('Update failed');
            }
        } catch (error) {
            toast.error('Network error');
        }
    };

    const filteredUsers = users.filter(user => {
        const matchesSearch = user.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            user.email.toLowerCase().includes(searchTerm.toLowerCase());

        if (filterStatus === 'ALL') return matchesSearch;
        // Check if user has ANY challenge with the filter status
        const hasStatus = user.challenges.some(c => c.status === filterStatus);
        return matchesSearch && hasStatus;
    });

    if (!isAuthenticated) {
        return (
            <div className="min-h-screen bg-[#0b0e11] flex items-center justify-center p-4">
                <div className="bg-[#15191e] border border-gray-800 p-8 rounded-xl max-w-md w-full shadow-2xl">
                    <div className="flex justify-center mb-6">
                        <Shield className="w-16 h-16 text-yellow-500" />
                    </div>
                    <h2 className="text-2xl font-bold text-white text-center mb-2">Restricted Area</h2>
                    <p className="text-gray-400 text-center mb-6">Enter Admin Access Key to continue</p>

                    <form onSubmit={handleLogin} className="space-y-4">
                        <input
                            type="password"
                            value={keyInput}
                            onChange={(e) => setKeyInput(e.target.value)}
                            className="w-full bg-[#0b0e11] border border-gray-700 text-white px-4 py-3 rounded-lg focus:border-yellow-500 focus:outline-none"
                            placeholder="Enter Key..."
                        />
                        <button
                            type="submit"
                            className="w-full bg-yellow-500 hover:bg-yellow-600 text-black font-bold py-3 rounded-lg transition-colors"
                            disabled={loading}
                        >
                            {loading ? 'Verifying...' : 'Access Panel'}
                        </button>
                    </form>
                    <div className="mt-4 text-center">
                        <span className="text-xs text-gray-600">Hint for Exam: {DEMO_KEY}</span>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-[#0b0e11] text-white p-6">
            <div className="max-w-7xl mx-auto">
                {/* Header */}
                <div className="flex justify-between items-center mb-8">
                    <div>
                        <h1 className="text-3xl font-bold flex items-center gap-2">
                            <Shield className="text-yellow-500" />
                            Admin Control Center
                        </h1>
                        <p className="text-gray-400 mt-1">Manage users, challenges, and risk.</p>
                    </div>
                    <button
                        onClick={() => {
                            sessionStorage.removeItem('ADMIN_KEY');
                            setIsAuthenticated(false);
                        }}
                        className="px-4 py-2 bg-red-500/10 text-red-500 hover:bg-red-500/20 rounded-lg border border-red-500/20"
                    >
                        Logout
                    </button>
                </div>

                {/* Filters */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                    <div className="relative">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 w-5 h-5" />
                        <input
                            type="text"
                            placeholder="Search user..."
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                            className="w-full bg-[#15191e] border border-gray-800 rounded-lg pl-10 pr-4 py-2 focus:border-yellow-500 outline-none"
                        />
                    </div>
                    <div className="flex gap-2">
                        {['ALL', 'ACTIVE', 'PASSED', 'FAILED'].map(status => (
                            <button
                                key={status}
                                onClick={() => setFilterStatus(status)}
                                className={`px-4 py-2 rounded-lg border text-sm font-medium transition-colors ${filterStatus === status
                                    ? 'bg-yellow-500 text-black border-yellow-500'
                                    : 'bg-[#15191e] text-gray-400 border-gray-800 hover:border-gray-600'
                                    }`}
                            >
                                {status}
                            </button>
                        ))}
                    </div>
                </div>

                {/* PayPal Config Section */}
                <div className="bg-[#15191e] border border-[#1e2329] rounded-xl p-6 mb-8">
                    <div className="flex items-center justify-between mb-4">
                        <h3 className="text-sm font-bold uppercase tracking-widest text-yellow-500">Module B: Payment & Access (PayPal Config)</h3>
                        <div className={`px-3 py-1 rounded-full text-[10px] font-black uppercase ${paypalData.is_configured ? 'bg-green-500/10 text-green-500' : 'bg-red-500/10 text-red-500'}`}>
                            {paypalData.is_configured ? 'PayPal Connected ✅' : 'PayPal Not Configured ❌'}
                        </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div className="space-y-1">
                            <label className="text-[10px] text-gray-500 font-bold uppercase">PayPal Email</label>
                            <input
                                className="w-full bg-[#0b0e11] border border-gray-800 rounded-lg px-4 py-2 text-sm focus:border-yellow-500 outline-none"
                                value={paypalData.email}
                                onChange={(e) => setPaypalData({ ...paypalData, email: e.target.value })}
                                placeholder="merchant@example.com"
                            />
                        </div>
                        <div className="space-y-1">
                            <label className="text-[10px] text-gray-500 font-bold uppercase">PayPal Client ID</label>
                            <input
                                className="w-full bg-[#0b0e11] border border-gray-800 rounded-lg px-4 py-2 text-sm focus:border-yellow-500 outline-none"
                                value={paypalData.client_id}
                                onChange={(e) => setPaypalData({ ...paypalData, client_id: e.target.value })}
                                placeholder="A...Z"
                            />
                        </div>
                        <div className="space-y-1 flex flex-col justify-end">
                            <button
                                onClick={savePaypalConfig}
                                className="bg-yellow-500 hover:bg-yellow-600 text-black font-black text-[10px] uppercase py-3 rounded-lg transition-colors"
                            >
                                Save Configuration
                            </button>
                        </div>
                    </div>
                </div>

                {/* Content */}
                {loading ? (
                    <div className="text-center py-20 animate-pulse text-gray-500">Loading admin data...</div>
                ) : (

                    <div className="space-y-6">
                        {filteredUsers.length === 0 ? (
                            <div className="text-center py-20 text-gray-500">No users found matching filters.</div>
                        ) : (
                            filteredUsers.map(user => (
                                <div key={user.user_id} className="bg-[#15191e] border border-gray-800 rounded-xl overflow-hidden">
                                    <div className="bg-gray-800/30 px-6 py-4 flex justify-between items-center">
                                        <div className="flex items-center gap-3">
                                            <div className="w-10 h-10 rounded-full bg-blue-500/20 flex items-center justify-center text-blue-400">
                                                <User className="w-5 h-5" />
                                            </div>
                                            <div>
                                                <h3 className="font-bold text-lg">{user.name}</h3>
                                                <p className="text-sm text-gray-400">{user.email} • Joined {new Date(user.joined_at).toLocaleDateString()}</p>
                                            </div>
                                        </div>
                                        <span className="px-3 py-1 bg-gray-700 rounded text-xs uppercase tracking-wider">{user.role}</span>
                                    </div>

                                    <div className="p-6">
                                        <h4 className="text-sm font-medium text-gray-500 mb-4 uppercase tracking-wider">Challenges</h4>
                                        {user.challenges.length === 0 ? (
                                            <p className="text-gray-500 italic">No challenges active.</p>
                                        ) : (
                                            <div className="overflow-x-auto">
                                                <table className="w-full text-left">
                                                    <thead>
                                                        <tr className="border-b border-gray-800 text-gray-500 text-xs uppercase">
                                                            <th className="pb-3 pl-2">Plan</th>
                                                            <th className="pb-3">Balance / Equity</th>
                                                            <th className="pb-3">Profit %</th>
                                                            <th className="pb-3">Status</th>
                                                            <th className="pb-3 text-right">Actions</th>
                                                        </tr>
                                                    </thead>
                                                    <tbody className="divide-y divide-gray-800">
                                                        {user.challenges.map(challenge => (
                                                            <tr key={challenge.id} className="group hover:bg-gray-800/20 transition-colors">
                                                                <td className="py-4 pl-2 font-medium">
                                                                    <div className="text-white">{challenge.plan}</div>
                                                                    <div className="text-xs text-gray-500">ID: #{challenge.id}</div>
                                                                </td>
                                                                <td className="py-4">
                                                                    <div className="text-white">{challenge.equity.toFixed(2)} MAD</div>
                                                                    <div className="text-xs text-gray-500">Init: {challenge.start_balance.toLocaleString()} MAD</div>
                                                                </td>
                                                                <td className="py-4">
                                                                    <span className={`font-bold ${challenge.profit_percent >= 0 ? 'text-green-500' : 'text-red-500'}`}>
                                                                        {challenge.profit_percent > 0 ? '+' : ''}{challenge.profit_percent}%
                                                                    </span>
                                                                </td>
                                                                <td className="py-4">
                                                                    <StatusBadge status={challenge.status} />
                                                                    {challenge.admin_note && (
                                                                        <div className="mt-1 text-xs text-yellow-500/80 italic">
                                                                            Note: {challenge.admin_note}
                                                                        </div>
                                                                    )}
                                                                    {challenge.reason && !challenge.admin_note && (
                                                                        <div className="mt-1 text-xs text-gray-500 italic">
                                                                            Note: {challenge.reason}
                                                                        </div>
                                                                    )}
                                                                </td>
                                                                <td className="py-4 text-right space-x-2">
                                                                    <button
                                                                        onClick={() => updateStatus(challenge.id, 'PASSED', challenge.admin_note)}
                                                                        title="Mark Passed"
                                                                        className="p-2 bg-green-500/10 text-green-500 hover:bg-green-500/20 rounded border border-green-500/20 transition-colors"
                                                                    >
                                                                        <CheckCircle className="w-4 h-4" />
                                                                    </button>
                                                                    <button
                                                                        onClick={() => updateStatus(challenge.id, 'FAILED', challenge.admin_note)}
                                                                        title="Mark Failed"
                                                                        className="p-2 bg-red-500/10 text-red-500 hover:bg-red-500/20 rounded border border-red-500/20 transition-colors"
                                                                    >
                                                                        <XCircle className="w-4 h-4" />
                                                                    </button>
                                                                    <button
                                                                        onClick={() => updateStatus(challenge.id, 'ACTIVE', challenge.admin_note)}
                                                                        title="Reset to Active"
                                                                        className="p-2 bg-blue-500/10 text-blue-500 hover:bg-blue-500/20 rounded border border-blue-500/20 transition-colors"
                                                                    >
                                                                        <Activity className="w-4 h-4" />
                                                                    </button>
                                                                </td>
                                                            </tr>
                                                        ))}
                                                    </tbody>
                                                </table>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            ))
                        )}
                    </div>
                )}
            </div>
        </div>
    );
};

const StatusBadge = ({ status }: { status: string }) => {
    const styles: Record<string, string> = {
        ACTIVE: 'bg-blue-500/10 text-blue-500 border-blue-500/20',
        PASSED: 'bg-green-500/10 text-green-500 border-green-500/20',
        FAILED: 'bg-red-500/10 text-red-500 border-red-500/20',
        PENDING: 'bg-yellow-500/10 text-yellow-500 border-yellow-500/20',
        FUNDED: 'bg-purple-500/10 text-purple-500 border-purple-500/20',
    };

    return (
        <span className={`px-2 py-1 rounded text-xs font-bold border ${styles[status] || 'bg-gray-500/10 text-gray-500'}`}>
            {status}
        </span>
    );
};

export default AdminPanel;
