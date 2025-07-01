import React from 'react';

const dummyResults = [
    { rank: 1, title: 'The Great Gatsby', type: 'Book', percent: 95, label: 'Group Winner', accent: 'neon' },
    { rank: 2, title: 'Codenames', type: 'Game', percent: 87, label: 'Runner Up', accent: 'coral' },
    { rank: 3, title: 'Inception', type: 'Movie', percent: 72, label: 'Third Place', accent: 'cyan' },
];

const Results: React.FC = () => {
    return (
        <div className="space-y-10">
            <div>
                <h1 className="text-4xl font-extrabold text-white mb-2 tracking-tight">Results</h1>
                <p className="text-dark-200 text-xl">Here's how your group ranked the options!</p>
            </div>

            <div className="card bg-gradient-to-br from-dark-800 to-dark-900 border border-dark-700 shadow-xl max-w-2xl mx-auto">
                <h2 className="text-2xl font-bold text-white mb-6">Group Consensus</h2>
                <div className="space-y-4">
                    {dummyResults.map((result) => (
                        <div key={result.rank} className="flex items-center justify-between p-4 bg-dark-700 rounded-xl shadow-md">
                            <div className="flex items-center space-x-4">
                                <span className={`text-3xl font-bold text-accent-${result.accent}`}>{result.rank}</span>
                                <div>
                                    <h3 className="text-white font-semibold text-xl">{result.title}</h3>
                                    <p className="text-dark-200 text-sm">{result.type} • {result.label}</p>
                                </div>
                            </div>
                            <span className={`text-accent-${result.accent} font-semibold text-xl`}>{result.percent}%</span>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default Results; 