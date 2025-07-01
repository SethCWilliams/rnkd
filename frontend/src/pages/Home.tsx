import React from 'react';
import { Link } from 'react-router-dom';

const Home: React.FC = () => {
    return (
        <div className="min-h-screen bg-gradient-to-br from-dark-900 via-dark-800 to-dark-900">
            {/* Navigation */}
            <nav className="bg-dark-900/80 border-b border-dark-700 backdrop-blur-md sticky top-0 z-10">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between h-16 items-center">
                        <span className="text-3xl font-extrabold text-accent-neon tracking-tight">Rnkd</span>
                        <div className="flex items-center space-x-4">
                            <Link to="/login" className="text-dark-300 hover:text-white transition-colors text-lg font-medium">
                                Login
                            </Link>
                            <Link to="/register" className="btn-primary text-lg px-6 py-2 shadow-lg">
                                Get Started
                            </Link>
                        </div>
                    </div>
                </div>
            </nav>

            {/* Hero Section */}
            <section className="relative overflow-hidden py-24 flex flex-col items-center justify-center text-center">
                <div className="absolute inset-0 pointer-events-none">
                    <div className="absolute -top-32 left-1/2 -translate-x-1/2 w-[600px] h-[600px] bg-accent-cyan opacity-20 rounded-full blur-3xl animate-pulse-slow" />
                </div>
                <div className="relative z-10 max-w-3xl mx-auto px-4">
                    <h1 className="text-5xl md:text-7xl font-extrabold text-white mb-6 leading-tight drop-shadow-lg">
                        Decide What's Next<br />
                        <span className="text-accent-neon">Together</span>
                    </h1>
                    <p className="text-2xl text-dark-200 mb-10 max-w-2xl mx-auto font-medium">
                        Rnkd helps groups make decisions—fast. Whether it's <span className="text-accent-cyan font-semibold">books</span> for your club, <span className="text-accent-coral font-semibold">movies</span> for movie night, <span className="text-accent-neon font-semibold">games</span> for your squad, or anything else—get a fair, fun, and easy group ranking.
                    </p>
                    <div className="flex flex-col sm:flex-row gap-4 justify-center">
                        <Link to="/register" className="btn-primary text-xl px-10 py-4 shadow-xl animate-fade-in">
                            Start Ranking
                        </Link>
                        <a href="#how" className="btn-secondary text-xl px-10 py-4 animate-fade-in">
                            How It Works
                        </a>
                    </div>
                </div>
            </section>

            {/* Features Section */}
            <section id="how" className="py-24 bg-dark-800/80 backdrop-blur-md">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="text-center mb-16">
                        <h2 className="text-4xl font-bold text-white mb-4 tracking-tight">How Rnkd Works</h2>
                        <p className="text-dark-200 text-xl max-w-2xl mx-auto">
                            No more endless debates. Rnkd makes group decisions simple, fair, and fun—no matter what you're choosing.
                        </p>
                    </div>
                    <div className="grid md:grid-cols-3 gap-10">
                        <div className="card text-center shadow-xl hover:scale-105 transition-transform duration-200">
                            <div className="w-16 h-16 bg-accent-cyan rounded-full flex items-center justify-center mx-auto mb-4 text-3xl">
                                📚
                            </div>
                            <h3 className="text-2xl font-semibold text-white mb-2">Create a List</h3>
                            <p className="text-dark-200 text-lg">
                                Add anything your group wants to decide on—books, movies, games, restaurants, and more.
                            </p>
                        </div>
                        <div className="card text-center shadow-xl hover:scale-105 transition-transform duration-200">
                            <div className="w-16 h-16 bg-accent-coral rounded-full flex items-center justify-center mx-auto mb-4 text-3xl">
                                ⚔️
                            </div>
                            <h3 className="text-2xl font-semibold text-white mb-2">Vote Head-to-Head</h3>
                            <p className="text-dark-200 text-lg">
                                Everyone votes in quick, one-on-one matchups. Our smart system keeps it fair and fast.
                            </p>
                        </div>
                        <div className="card text-center shadow-xl hover:scale-105 transition-transform duration-200">
                            <div className="w-16 h-16 bg-accent-neon rounded-full flex items-center justify-center mx-auto mb-4 text-3xl">
                                🏆
                            </div>
                            <h3 className="text-2xl font-semibold text-white mb-2">See the Results</h3>
                            <p className="text-dark-200 text-lg">
                                Instantly reveal your group's top pick and see how everyone's choices stacked up.
                            </p>
                        </div>
                    </div>
                </div>
            </section>

            {/* Call to Action */}
            <section className="py-16 bg-gradient-to-r from-accent-cyan/20 via-dark-900 to-accent-neon/20 text-center">
                <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">Ready to make your next group decision easy?</h2>
                <Link to="/register" className="btn-primary text-xl px-10 py-4 shadow-xl animate-fade-in">
                    Get Started Free
                </Link>
            </section>
        </div>
    );
};

export default Home; 