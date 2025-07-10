import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { apiService, MovieList, Group } from '../services/api';

interface DashboardList extends MovieList {
    itemCount?: number;
}

interface DashboardGroup extends Group {
    memberCount?: number;
}

const Dashboard: React.FC = () => {
    const { user } = useAuth();
    const [lists, setLists] = useState<DashboardList[]>([]);
    const [groups, setGroups] = useState<DashboardGroup[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchDashboardData = async () => {
            if (!user) return;

            try {
                setLoading(true);
                setError(null);

                // Fetch user's movie lists
                const userLists = await apiService.getUserMovieLists(user.id);
                
                // Fetch user's groups
                const userGroups = await apiService.getUserGroups(user.id);

                // Enhance lists with item counts
                const enhancedLists = await Promise.all(
                    userLists.map(async (list) => {
                        try {
                            const items = await apiService.getMovieListItems(list.id);
                            return { ...list, itemCount: items.length };
                        } catch (error) {
                            console.error(`Error fetching items for list ${list.id}:`, error);
                            return { ...list, itemCount: 0 };
                        }
                    })
                );

                // Enhance groups with member counts
                const enhancedGroups = await Promise.all(
                    userGroups.map(async (group) => {
                        try {
                            const members = await apiService.getGroupMembers(group.id);
                            return { ...group, memberCount: members.length };
                        } catch (error) {
                            console.error(`Error fetching members for group ${group.id}:`, error);
                            return { ...group, memberCount: 0 };
                        }
                    })
                );

                setLists(enhancedLists);
                setGroups(enhancedGroups);
            } catch (error) {
                console.error('Error fetching dashboard data:', error);
                setError('Failed to load dashboard data');
            } finally {
                setLoading(false);
            }
        };

        fetchDashboardData();
    }, [user]);

    if (loading) {
        return (
            <div className="space-y-10">
                <div>
                    <h1 className="text-4xl font-extrabold text-white mb-2 tracking-tight">Dashboard</h1>
                    <p className="text-dark-200 text-xl">Loading your data...</p>
                </div>
                <div className="grid md:grid-cols-3 gap-8">
                    {[1, 2, 3].map((i) => (
                        <div key={i} className="card shadow-xl bg-gradient-to-br from-dark-800 to-dark-900 border border-dark-700 animate-pulse">
                            <div className="h-6 bg-dark-600 rounded mb-2"></div>
                            <div className="h-4 bg-dark-600 rounded mb-4"></div>
                            <div className="h-8 bg-dark-600 rounded"></div>
                        </div>
                    ))}
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="space-y-10">
                <div>
                    <h1 className="text-4xl font-extrabold text-white mb-2 tracking-tight">Dashboard</h1>
                    <p className="text-red-400 text-xl">{error}</p>
                </div>
            </div>
        );
    }

    return (
        <div className="space-y-10">
            <div>
                <h1 className="text-4xl font-extrabold text-white mb-2 tracking-tight">Dashboard</h1>
                <p className="text-dark-200 text-xl">Welcome back, {user?.name}! Here's what's happening in your groups and lists.</p>
            </div>

            {/* Lists Overview */}
            <div>
                <h2 className="text-2xl font-bold text-white mb-4">Your Lists</h2>
                {lists.length === 0 ? (
                    <div className="card bg-dark-800 border border-dark-700 text-center py-8">
                        <p className="text-dark-200 text-lg mb-4">You don't have any lists yet.</p>
                        <Link to="/app/groups" className="btn-primary">Join a Group to Get Started</Link>
                    </div>
                ) : (
                    <div className="grid md:grid-cols-3 gap-8">
                        {lists.map((list) => (
                            <div key={list.id} className="card shadow-xl bg-gradient-to-br from-dark-800 to-dark-900 border border-dark-700 hover:scale-105 transition-transform duration-200">
                                <h3 className="text-2xl font-bold text-white mb-1 flex items-center gap-2">
                                    {list.name}
                                    <span className="text-xs bg-accent-cyan text-black px-2 py-1 rounded-full font-semibold uppercase ml-2">{list.media_type}</span>
                                </h3>
                                <p className="text-dark-200 mb-2">
                                    {list.itemCount || 0} items • Status: <span className="font-semibold text-accent-neon capitalize">{list.status}</span>
                                </p>
                                <p className="text-dark-300 text-sm mb-3 capitalize">{list.type} list</p>
                                {list.status === 'voting' ? (
                                    <Link to={`/app/voting/${list.id}`} className="btn-primary text-sm px-4 py-2 mt-2 inline-block">Go to Voting</Link>
                                ) : list.status === 'closed' ? (
                                    <Link to={`/app/results/${list.id}`} className="btn-secondary text-sm px-4 py-2 mt-2 inline-block">View Results</Link>
                                ) : (
                                    <span className="text-dark-400 text-sm px-4 py-2 mt-2 inline-block">Adding items...</span>
                                )}
                            </div>
                        ))}
                    </div>
                )}
            </div>

            {/* Groups Overview */}
            <div>
                <h2 className="text-2xl font-bold text-white mb-4">Your Groups</h2>
                {groups.length === 0 ? (
                    <div className="card bg-dark-800 border border-dark-700 text-center py-8">
                        <p className="text-dark-200 text-lg mb-4">You're not in any groups yet.</p>
                        <Link to="/app/groups" className="btn-primary">Find Groups to Join</Link>
                    </div>
                ) : (
                    <div className="flex flex-wrap gap-6">
                        {groups.map((group) => (
                            <div key={group.id} className="card bg-dark-800 border border-dark-700 shadow-md flex flex-col items-center px-8 py-6 min-w-[200px]">
                                <h3 className="text-xl font-semibold text-white mb-1">{group.name}</h3>
                                <p className="text-dark-200 mb-2">{group.memberCount || 0} members</p>
                                <p className="text-dark-400 text-xs mb-3">Invite: {group.invite_code}</p>
                                <Link to="/app/groups" className="btn-secondary text-sm px-4 py-2">View Group</Link>
                            </div>
                        ))}
                    </div>
                )}
            </div>

            {/* Quick Actions */}
            <div className="card bg-dark-900 border border-dark-700 shadow-lg">
                <h3 className="text-2xl font-bold text-white mb-4">Quick Actions</h3>
                <div className="grid md:grid-cols-2 gap-4">
                    <Link to="/app/groups" className="btn-primary text-center py-4">
                        Browse Groups
                    </Link>
                    <button className="btn-secondary py-4" disabled>
                        Create New List (Coming Soon)
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Dashboard; 