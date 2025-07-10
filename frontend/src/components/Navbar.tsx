import React, { useState, useEffect, useRef } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Navbar: React.FC = () => {
    const { user, isAuthenticated, logout, toggleAuth } = useAuth();
    const [isDropdownOpen, setIsDropdownOpen] = useState(false);
    const dropdownRef = useRef<HTMLDivElement>(null);
    const navigate = useNavigate();

    // Close dropdown when clicking outside
    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
                setIsDropdownOpen(false);
            }
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, []);

    const handleLogout = () => {
        logout();
        setIsDropdownOpen(false);
        navigate('/');
    };

    const handleAppNavigation = (path: string) => {
        navigate(path);
        setIsDropdownOpen(false);
    };

    return (
        <nav className="bg-dark-900/80 border-b border-dark-700 backdrop-blur-md sticky top-0 z-50">
            <div className="max-w-full mx-auto px-8">
                <div className="flex justify-between h-16 items-center">
                    {/* Logo */}
                    <Link to="/" className="flex items-center">
                        <img 
                            src="/images/logo/full_logo_green.png" 
                            alt="Rnkd logo" 
                            className="h-32 object-contain" 
                        />
                    </Link>

                    {/* Right side - Auth buttons or user dropdown */}
                    <div className="flex items-center space-x-4">
                        {/* Development toggle for testing */}
                        <button
                            onClick={toggleAuth}
                            className="px-3 py-1 text-xs bg-yellow-600 text-white rounded hover:bg-yellow-700 transition-colors"
                            title="Toggle auth for testing"
                        >
                            {isAuthenticated ? 'Logout (Test)' : 'Login (Test)'}
                        </button>

                        {!isAuthenticated ? (
                            // Unauthenticated state
                            <>
                                <Link 
                                    to="/login" 
                                    className="text-dark-300 hover:text-white transition-colors text-lg font-medium"
                                >
                                    Login
                                </Link>
                                <Link 
                                    to="/register" 
                                    className="btn-primary text-lg px-6 py-2 shadow-lg"
                                >
                                    Get Started
                                </Link>
                            </>
                        ) : (
                            // Authenticated state - dropdown
                            <div className="relative" ref={dropdownRef}>
                                <button
                                    onClick={() => setIsDropdownOpen(!isDropdownOpen)}
                                    className="flex items-center space-x-2 text-white hover:text-accent-neon transition-colors"
                                >
                                    <div className="w-8 h-8 bg-accent-cyan rounded-full flex items-center justify-center">
                                        <span className="text-sm font-medium text-white">
                                            {user?.name?.charAt(0)?.toUpperCase() || 'U'}
                                        </span>
                                    </div>
                                    <span className="text-sm font-medium">{user?.name}</span>
                                    <svg
                                        className={`w-4 h-4 transition-transform ${isDropdownOpen ? 'rotate-180' : ''}`}
                                        fill="none"
                                        stroke="currentColor"
                                        viewBox="0 0 24 24"
                                    >
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                                    </svg>
                                </button>

                                {/* Dropdown menu */}
                                {isDropdownOpen && (
                                    <div className="absolute right-0 mt-2 w-48 bg-dark-800 border border-dark-700 rounded-md shadow-lg z-10">
                                        <div className="py-1">
                                            <button
                                                onClick={() => handleAppNavigation('/app')}
                                                className="block w-full text-left px-4 py-2 text-sm text-dark-300 hover:text-white hover:bg-dark-700 transition-colors"
                                            >
                                                Dashboard
                                            </button>
                                            <button
                                                onClick={() => handleAppNavigation('/app/groups')}
                                                className="block w-full text-left px-4 py-2 text-sm text-dark-300 hover:text-white hover:bg-dark-700 transition-colors"
                                            >
                                                Groups
                                            </button>
                                            <div className="border-t border-dark-700 my-1"></div>
                                            <button
                                                onClick={handleLogout}
                                                className="block w-full text-left px-4 py-2 text-sm text-dark-300 hover:text-white hover:bg-dark-700 transition-colors"
                                            >
                                                Logout
                                            </button>
                                        </div>
                                    </div>
                                )}
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;