import React from 'react';
import { Outlet, Link, useLocation } from 'react-router-dom';
import Navbar from './Navbar';

const Layout: React.FC = () => {
    const location = useLocation();

    const navigation = [
        { name: 'Dashboard', href: '/app', current: location.pathname === '/app' },
        { name: 'Groups', href: '/app/groups', current: location.pathname === '/app/groups' },
    ];

    return (
        <div className="min-h-screen bg-dark-900 flex flex-col">
            <Navbar />
            
            {/* Sub-navigation for app pages */}
            <nav className="bg-dark-800 border-b border-dark-700 flex-shrink-0">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-center h-12">
                        <div className="flex space-x-8">
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
                </div>
            </nav>

            <main className="flex-1 overflow-y-auto">
                <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
                    <Outlet />
                </div>
            </main>
        </div>
    );
};

export default Layout; 