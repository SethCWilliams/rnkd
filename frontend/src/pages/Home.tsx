import React from 'react';
import { Link } from 'react-router-dom';

const Home: React.FC = () => {
    return (
        <div className="min-h-screen bg-gradient-to-br from-dark-900 via-dark-800 to-dark-900">
            {/* Navigation */}
            <nav className="bg-dark-900/80 border-b border-dark-700 backdrop-blur-md sticky top-0 z-10">
                <div className="max-w-full mx-auto px-8">
                    <div className="flex justify-between h-16 items-center">
                        <img src="/images/logo/full_logo_green.png" alt="Rnkd logo" className="h-32 object-contain" />
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

            {/* Hero Section with How Rnkd Works */}
            <section className="relative min-h-[calc(100vh-4rem)] flex flex-col items-center justify-start text-center overflow-hidden py-6">
                <div className="absolute inset-0 w-full h-full flex items-center justify-center overflow-hidden">
                    <div className="w-[80vw] h-[80vw] max-w-[1200px] max-h-[1200px] bg-accent-cyan opacity-20 rounded-full blur-3xl animate-pulse-slow scale-125" />
                </div>
                <div className="relative z-10 w-full max-w-5xl mx-auto px-4 flex flex-col items-center justify-start flex-1 pt-8 md:pt-14">
                    <h1 className="text-5xl md:text-7xl font-extrabold text-white mb-3 md:mb-5 leading-tight drop-shadow-lg">
                        Decide What's Next<br />
                        <span className="text-accent-neon">Together</span>
                    </h1>
                    <p className="text-lg md:text-2xl text-dark-200 mb-6 md:mb-8 max-w-2xl mx-auto font-medium">
                        Rnkd helps groups make decisions—fast. Whether it's <span className="text-accent-cyan font-semibold">books</span> for your club, <span className="text-accent-coral font-semibold">movies</span> for movie night, <span className="text-accent-neon font-semibold">games</span> for your squad, or anything else—get a fair, fun, and easy group ranking.
                    </p>
                    {/* Stepper */}
                    <div className="w-full flex flex-col items-center mb-4 md:mb-6">
                        <div className="inline-block mb-6">
                            <h2 className="text-3xl md:text-4xl font-extrabold text-white mb-2 tracking-tight drop-shadow-lg">How Rnkd Works</h2>
                            <div className="h-1 w-full rounded bg-accent-neon"></div>
                        </div>
                        <div className="flex flex-row items-center justify-center gap-2 md:gap-4 w-full max-w-4xl">
                            {/* Step 1 */}
                            <div className="flex flex-col items-center w-56 max-w-full px-2">
                                <div className="w-16 h-16 rounded-full flex items-center justify-center mb-3 text-2xl font-extrabold text-white bg-accent-cyan">
                                    1
                                </div>
                                <div className="min-h-[60px] flex items-center">
                                    <h3 className="text-2xl font-bold text-white mb-2 text-center">Create a List</h3>
                                </div>
                                <p className="text-dark-200 text-lg leading-snug">Add anything your group wants to decide on—books, movies, games, restaurants, and more.</p>
                            </div>
                            {/* Line between steps */}
                            <div className="hidden md:block h-1 w-8 bg-dark-400 mx-2 rounded-full" />
                            {/* Step 2 */}
                            <div className="flex flex-col items-center w-56 max-w-full px-2">
                                <div className="w-16 h-16 rounded-full flex items-center justify-center mb-3 text-2xl font-extrabold text-white bg-accent-coral">
                                    2
                                </div>
                                <div className="min-h-[60px] flex items-center">
                                    <h3 className="text-2xl font-bold text-white mb-2 text-center">Vote Head-to-Head</h3>
                                </div>
                                <p className="text-dark-200 text-lg leading-snug">Everyone votes in quick, one-on-one matchups. Our smart system keeps it fair and fast.</p>
                            </div>
                            {/* Line between steps */}
                            <div className="hidden md:block h-1 w-8 bg-dark-400 mx-2 rounded-full" />
                            {/* Step 3 */}
                            <div className="flex flex-col items-center w-56 max-w-full px-2">
                                <div className="w-16 h-16 rounded-full flex items-center justify-center mb-3 text-2xl font-extrabold text-white bg-accent-neon">
                                    3
                                </div>
                                <div className="min-h-[60px] flex items-center">
                                    <h3 className="text-2xl font-bold text-white mb-2 text-center">See the Results</h3>
                                </div>
                                <p className="text-dark-200 text-lg leading-snug">Instantly reveal your group's top pick and see how everyone's choices stacked up.</p>
                            </div>
                        </div>
                    </div>
                    {/* Final CTA */}
                    <div className="text-center mt-10 md:mt-16">
                        <h2 className="text-lg md:text-xl font-bold text-white mb-6">Ready to make your next group decision easy?</h2>
                        <Link to="/register" className="btn-primary text-lg md:text-xl px-8 md:px-10 py-3 md:py-4 shadow-xl animate-fade-in">
                            Get Started Free
                        </Link>
                    </div>
                </div>
            </section>
        </div>
    );
};

export default Home; 