import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

interface User {
    id: number;
    name: string;
    email: string;
    profile_image_url?: string;
}

interface AuthContextType {
    user: User | null;
    isAuthenticated: boolean;
    token: string | null;
    login: (email: string, password: string) => Promise<void>;
    logout: () => void;
    register: (name: string, email: string, password: string) => Promise<void>;
    // For testing purposes
    toggleAuth: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};

interface AuthProviderProps {
    children: ReactNode;
}

const API_BASE_URL = 'http://localhost:8000/api/v1';

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
    const [user, setUser] = useState<User | null>(null);
    const [token, setToken] = useState<string | null>(null);
    
    // Initialize with saved token and fetch user data
    useEffect(() => {
        const savedToken = localStorage.getItem('rnkd_token');
        const savedFakeAuth = localStorage.getItem('rnkd_fake_auth');
        
        if (savedToken) {
            setToken(savedToken);
            fetchCurrentUser(savedToken);
        } else if (savedFakeAuth === 'true') {
            // Auto-login John Doe for testing
            login('john@example.com', 'password123');
        }
    }, []);

    const fetchCurrentUser = async (authToken: string) => {
        try {
            const response = await fetch(`${API_BASE_URL}/auth/me`, {
                headers: {
                    'Authorization': `Bearer ${authToken}`,
                    'Content-Type': 'application/json',
                },
            });
            
            if (response.ok) {
                const userData = await response.json();
                setUser(userData);
            } else {
                // Token might be invalid, clear it
                localStorage.removeItem('rnkd_token');
                setToken(null);
                setUser(null);
            }
        } catch (error) {
            console.error('Error fetching current user:', error);
            localStorage.removeItem('rnkd_token');
            setToken(null);
            setUser(null);
        }
    };

    const login = async (email: string, password: string) => {
        try {
            const response = await fetch(`${API_BASE_URL}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password }),
            });

            if (response.ok) {
                const data = await response.json();
                const authToken = data.access_token;
                setToken(authToken);
                localStorage.setItem('rnkd_token', authToken);
                localStorage.removeItem('rnkd_fake_auth'); // Remove fake auth flag
                await fetchCurrentUser(authToken);
            } else {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Login failed');
            }
        } catch (error) {
            console.error('Login error:', error);
            throw error;
        }
    };

    const logout = () => {
        setUser(null);
        setToken(null);
        localStorage.removeItem('rnkd_token');
        localStorage.removeItem('rnkd_fake_auth');
    };

    const register = async (name: string, email: string, password: string) => {
        try {
            const response = await fetch(`${API_BASE_URL}/auth/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ name, email, password }),
            });

            if (response.ok) {
                // After successful registration, log the user in
                await login(email, password);
            } else {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Registration failed');
            }
        } catch (error) {
            console.error('Registration error:', error);
            throw error;
        }
    };

    // For testing purposes - toggle authentication state
    const toggleAuth = () => {
        if (user) {
            logout();
        } else {
            login('john@example.com', 'password123');
        }
    };

    const value: AuthContextType = {
        user,
        token,
        isAuthenticated: !!user,
        login,
        logout,
        register,
        toggleAuth
    };

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
};