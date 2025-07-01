import React, { useState } from 'react';
import { matchups } from '../dummyData';

const Voting: React.FC = () => {
    const [current, setCurrent] = useState(0);
    const matchup = matchups[current];

    const handleVote = (winner: 'A' | 'B') => {
        // For demo, just go to next matchup
        setCurrent((prev) => (prev + 1 < matchups.length ? prev + 1 : 0));
    };

    if (!matchup) return <div className="text-white text-2xl">No matchups available.</div>;

    return (
        <div className="space-y-10">
            <div>
                <h1 className="text-4xl font-extrabold text-white mb-2 tracking-tight">Voting</h1>
                <p className="text-dark-200 text-xl">Help your group decide! Pick your favorite in each matchup.</p>
            </div>

            <div className="card text-center shadow-xl max-w-xl mx-auto bg-gradient-to-br from-dark-800 to-dark-900 border border-dark-700">
                <h2 className="text-2xl font-bold text-white mb-6">Which do you prefer?</h2>
                <div className="flex justify-center items-center gap-8 mb-8">
                    <button
                        className="card bg-dark-700 hover:bg-accent-cyan text-white text-xl font-semibold px-8 py-6 rounded-xl shadow-lg transition-colors duration-200 focus:outline-none"
                        onClick={() => handleVote('A')}
                    >
                        {matchup.itemA}
                    </button>
                    <span className="text-3xl text-accent-coral font-bold">VS</span>
                    <button
                        className="card bg-dark-700 hover:bg-accent-neon text-white text-xl font-semibold px-8 py-6 rounded-xl shadow-lg transition-colors duration-200 focus:outline-none"
                        onClick={() => handleVote('B')}
                    >
                        {matchup.itemB}
                    </button>
                </div>
                <div className="text-dark-200 text-lg">Matchup {current + 1} of {matchups.length}</div>
            </div>
        </div>
    );
};

export default Voting; 