import React from 'react';
import { Link } from 'react-router-dom';
import { lists, groups, activity } from '../dummyData';

const Dashboard: React.FC = () => {
    return (
        <div className="space-y-10">
            <div>
                <h1 className="text-4xl font-extrabold text-white mb-2 tracking-tight">Dashboard</h1>
                <p className="text-dark-200 text-xl">Welcome! Here's what's happening in your groups and lists.</p>
            </div>

            {/* Lists Overview */}
            <div className="grid md:grid-cols-3 gap-8">
                {lists.map((list) => (
                    <div key={list.id} className="card shadow-xl bg-gradient-to-br from-dark-800 to-dark-900 border border-dark-700 hover:scale-105 transition-transform duration-200">
                        <h3 className="text-2xl font-bold text-white mb-1 flex items-center gap-2">
                            {list.name}
                            <span className="text-xs bg-accent-cyan text-black px-2 py-1 rounded-full font-semibold uppercase ml-2">{list.type}</span>
                        </h3>
                        <p className="text-dark-200 mb-2">{list.items} items • Status: <span className="font-semibold text-accent-neon">{list.status}</span></p>
                        <Link to={`/app/voting/${list.id}`} className="btn-primary text-sm px-4 py-2 mt-2 inline-block">Go to Voting</Link>
                    </div>
                ))}
            </div>

            {/* Groups Overview */}
            <div>
                <h2 className="text-2xl font-bold text-white mb-4">Your Groups</h2>
                <div className="flex flex-wrap gap-6">
                    {groups.map((group) => (
                        <div key={group.id} className="card bg-dark-800 border border-dark-700 shadow-md flex flex-col items-center px-8 py-6 min-w-[200px]">
                            <h3 className="text-xl font-semibold text-white mb-1">{group.name}</h3>
                            <p className="text-dark-200 mb-2">{group.members} members</p>
                            <Link to="/app/groups" className="btn-secondary text-sm px-4 py-2">View Group</Link>
                        </div>
                    ))}
                </div>
            </div>

            {/* Recent Activity */}
            <div className="card bg-dark-900 border border-dark-700 shadow-lg">
                <h3 className="text-2xl font-bold text-white mb-4">Recent Activity</h3>
                <div className="space-y-3">
                    {activity.map((activity) => (
                        <div key={activity.id} className="flex items-center justify-between py-3 border-b border-dark-800 last:border-b-0">
                            <div>
                                <p className="text-white text-lg">{activity.text}</p>
                                <p className="text-dark-300 text-sm">{activity.time}</p>
                            </div>
                            <Link to={activity.link} className="btn-primary text-sm px-4 py-2">{activity.action}</Link>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default Dashboard; 