import React from 'react';
import { Outlet, Link, useLocation } from 'react-router-dom';
import { useTheme } from '../contexts/ThemeContext';

const Layout: React.FC = () => {
    const { isDark, toggleTheme } = useTheme();
    const location = useLocation();

    const navigation = [
        { name: 'Dashboard', href: '/app', current: location.pathname === '/app' },
        { name: 'Groups', href: '/app/groups', current: location.pathname === '/app/groups' },
    ];

    return (
        <div className="min-h-screen bg-dark-900">
            <nav className="bg-dark-800 border-b border-dark-700">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between h-16">
                        <div className="flex">
                            <div className="flex-shrink-0 flex items-center">
                                <Link to="/app" className="text-2xl font-bold text-accent-neon">
                                    Rnkd
                                </Link>
                            </div>
                            <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                                {navigation.map((item) => (
                                    <Link
                                        key={item.name}
                                        to={item.href}
                                        className={`${item.current
                                                ? 'border-accent-neon text-white'
                                                : 'border-transparent text-dark-300 hover:text-white hover:border-dark-300'
                                            } inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors duration-200`}
                                    >
                                        {item.name}
                                    </Link>
                                ))}
                            </div>
                        </div>
                        <div className="flex items-center space-x-4">
                            <button
                                onClick={toggleTheme}
                                className="p-2 rounded-lg bg-dark-700 hover:bg-dark-600 transition-colors duration-200"
                            >
                                {isDark ? '🌙' : '☀️'}
                            </button>
                            <div className="flex items-center space-x-2">
                                <div className="w-8 h-8 bg-accent-cyan rounded-full flex items-center justify-center">
                                    <span className="text-sm font-medium text-white">J</span>
                                </div>
                                <span className="text-sm text-white">John Doe</span>
                            </div>
                        </div>
                    </div>
                </div>
            </nav>

            <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
                <Outlet />
            </main>
        </div>
    );
};

export default Layout; 