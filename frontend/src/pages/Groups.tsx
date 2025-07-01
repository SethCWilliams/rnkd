import React from 'react';
import { groups } from '../dummyData';

const Groups: React.FC = () => {
    return (
        <div className="space-y-10">
            <div className="flex flex-col sm:flex-row justify-between items-center mb-6 gap-4">
                <div>
                    <h1 className="text-4xl font-extrabold text-white mb-2 tracking-tight">Your Groups</h1>
                    <p className="text-dark-200 text-xl">Manage your book clubs, game squads, movie crews, and more.</p>
                </div>
                <button className="btn-primary text-lg px-6 py-2 shadow-lg">Create Group</button>
            </div>

            <div className="grid md:grid-cols-3 gap-10">
                {groups.map((group) => (
                    <div key={group.id} className={`card shadow-xl border border-dark-700 bg-gradient-to-br from-dark-800 to-dark-900 hover:scale-105 transition-transform duration-200`}>
                        <div className="flex justify-between items-center mb-4">
                            <div>
                                <h3 className="text-2xl font-bold text-white mb-1">{group.name}</h3>
                                <p className="text-dark-200">{group.members} members</p>
                            </div>
                            <span className={`text-xs px-3 py-1 rounded-full font-semibold bg-accent-${group.accent} text-black`}>{group.status}</span>
                        </div>
                        <p className="text-dark-200 mb-2">{group.description}</p>
                        <p className="text-accent-neon mb-4 font-medium">{group.example}</p>
                        <div className="flex space-x-2">
                            <button className="btn-secondary text-sm">View</button>
                            <button className="btn-primary text-sm">Join Voting</button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Groups; 