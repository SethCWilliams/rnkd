import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { apiService, Group, MovieList, User } from '../services/api';

interface EnhancedGroup extends Group {
    memberCount: number;
    members: User[];
    lists: MovieList[];
}

const Groups: React.FC = () => {
    const { user } = useAuth();
    const [userGroups, setUserGroups] = useState<EnhancedGroup[]>([]);
    const [allGroups, setAllGroups] = useState<EnhancedGroup[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [activeTab, setActiveTab] = useState<'my-groups' | 'all-groups'>('my-groups');

    useEffect(() => {
        const fetchGroupsData = async () => {
            if (!user) return;

            try {
                setLoading(true);
                setError(null);

                // Fetch all groups
                const groups = await apiService.getGroups();
                const allLists = await apiService.getMovieLists();

                // Enhance groups with member info and lists
                const enhancedGroups = await Promise.all(
                    groups.map(async (group) => {
                        try {
                            const members = await apiService.getGroupMembers(group.id);
                            const groupLists = allLists.filter(list => list.group_id === group.id);
                            
                            return {
                                ...group,
                                memberCount: members.length,
                                members,
                                lists: groupLists,
                            };
                        } catch (error) {
                            console.error(`Error fetching data for group ${group.id}:`, error);
                            return {
                                ...group,
                                memberCount: 0,
                                members: [],
                                lists: [],
                            };
                        }
                    })
                );

                // Separate user's groups from all groups
                const userGroupsList = enhancedGroups.filter(group => 
                    group.members.some(member => member.id === user.id)
                );

                setUserGroups(userGroupsList);
                setAllGroups(enhancedGroups);
            } catch (error) {
                console.error('Error fetching groups data:', error);
                setError('Failed to load groups data');
            } finally {
                setLoading(false);
            }
        };

        fetchGroupsData();
    }, [user]);

    const getGroupAccentColor = (groupName: string) => {
        // Simple hash function to get consistent colors
        const colors = ['cyan', 'neon', 'coral'];
        const hash = groupName.split('').reduce((a, b) => a + b.charCodeAt(0), 0);
        return colors[hash % colors.length];
    };

    const getActiveVotingLists = (group: EnhancedGroup) => {
        return group.lists.filter(list => list.status === 'voting');
    };

    if (loading) {
        return (
            <div className="space-y-10">
                <div>
                    <h1 className="text-4xl font-extrabold text-white mb-2 tracking-tight">Your Groups</h1>
                    <p className="text-dark-200 text-xl">Loading groups...</p>
                </div>
                <div className="grid md:grid-cols-3 gap-10">
                    {[1, 2, 3].map((i) => (
                        <div key={i} className="card shadow-xl border border-dark-700 bg-gradient-to-br from-dark-800 to-dark-900 animate-pulse">
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
                    <h1 className="text-4xl font-extrabold text-white mb-2 tracking-tight">Your Groups</h1>
                    <p className="text-red-400 text-xl">{error}</p>
                </div>
            </div>
        );
    }

    const displayGroups = activeTab === 'my-groups' ? userGroups : allGroups;

    return (
        <div className="space-y-10">
            <div className="flex flex-col sm:flex-row justify-between items-center mb-6 gap-4">
                <div>
                    <h1 className="text-4xl font-extrabold text-white mb-2 tracking-tight">Groups</h1>
                    <p className="text-dark-200 text-xl">Manage your book clubs, game squads, movie crews, and more.</p>
                </div>
                <button className="btn-primary text-lg px-6 py-2 shadow-lg" disabled>
                    Create Group (Coming Soon)
                </button>
            </div>

            {/* Tab Navigation */}
            <div className="flex space-x-1 bg-dark-800 p-1 rounded-lg w-fit">
                <button
                    onClick={() => setActiveTab('my-groups')}
                    className={`px-4 py-2 rounded-md font-medium transition-all ${
                        activeTab === 'my-groups'
                            ? 'bg-accent-neon text-black'
                            : 'text-dark-300 hover:text-white'
                    }`}
                >
                    My Groups ({userGroups.length})
                </button>
                <button
                    onClick={() => setActiveTab('all-groups')}
                    className={`px-4 py-2 rounded-md font-medium transition-all ${
                        activeTab === 'all-groups'
                            ? 'bg-accent-neon text-black'
                            : 'text-dark-300 hover:text-white'
                    }`}
                >
                    All Groups ({allGroups.length})
                </button>
            </div>

            {displayGroups.length === 0 ? (
                <div className="card bg-dark-800 border border-dark-700 text-center py-12">
                    <p className="text-dark-200 text-lg mb-4">
                        {activeTab === 'my-groups' 
                            ? "You're not in any groups yet." 
                            : "No groups found."}
                    </p>
                    {activeTab === 'my-groups' && (
                        <button 
                            onClick={() => setActiveTab('all-groups')}
                            className="btn-primary"
                        >
                            Browse All Groups
                        </button>
                    )}
                </div>
            ) : (
                <div className="grid md:grid-cols-3 gap-10">
                    {displayGroups.map((group) => {
                        const accentColor = getActiveVotingLists(group).length > 0 ? 'neon' : 'cyan';
                        const isUserMember = group.members.some(member => member.id === user?.id);
                        
                        return (
                            <div key={group.id} className="card shadow-xl border border-dark-700 bg-gradient-to-br from-dark-800 to-dark-900 hover:scale-105 transition-transform duration-200">
                                <div className="flex justify-between items-start mb-4">
                                    <div>
                                        <h3 className="text-2xl font-bold text-white mb-1">{group.name}</h3>
                                        <p className="text-dark-200">{group.memberCount} members</p>
                                    </div>
                                    <div className="flex flex-col items-end gap-2">
                                        {isUserMember && (
                                            <span className="text-xs px-3 py-1 rounded-full font-semibold bg-accent-cyan text-black">
                                                Member
                                            </span>
                                        )}
                                        {getActiveVotingLists(group).length > 0 && (
                                            <span className="text-xs px-3 py-1 rounded-full font-semibold bg-accent-neon text-black">
                                                Active Voting
                                            </span>
                                        )}
                                    </div>
                                </div>
                                
                                <div className="mb-4">
                                    <p className="text-dark-300 text-sm mb-2">
                                        Invite Code: <span className="font-mono text-accent-cyan">{group.invite_code}</span>
                                    </p>
                                    <p className="text-dark-200">
                                        {group.lists.length} lists • {getActiveVotingLists(group).length} active votes
                                    </p>
                                </div>

                                {group.lists.length > 0 && (
                                    <div className="mb-4">
                                        <p className="text-white font-medium mb-2">Recent Lists:</p>
                                        <div className="space-y-1">
                                            {group.lists.slice(0, 2).map(list => (
                                                <p key={list.id} className="text-dark-300 text-sm">
                                                    • {list.name} ({list.media_type}, {list.status})
                                                </p>
                                            ))}
                                            {group.lists.length > 2 && (
                                                <p className="text-dark-400 text-xs">
                                                    +{group.lists.length - 2} more...
                                                </p>
                                            )}
                                        </div>
                                    </div>
                                )}

                                <div className="flex space-x-2">
                                    {isUserMember ? (
                                        <>
                                            <button className="btn-secondary text-sm flex-1">
                                                View Details
                                            </button>
                                            {getActiveVotingLists(group).length > 0 && (
                                                <button className="btn-primary text-sm flex-1">
                                                    Join Voting
                                                </button>
                                            )}
                                        </>
                                    ) : (
                                        <button className="btn-primary text-sm w-full" disabled>
                                            Join Group (Coming Soon)
                                        </button>
                                    )}
                                </div>
                            </div>
                        );
                    })}
                </div>
            )}
        </div>
    );
};

export default Groups; 