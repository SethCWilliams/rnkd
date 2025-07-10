import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

interface User {
    id: string;
    name: string;
    email: string;
    profileImage?: string;
}

interface AuthContextType {
    user: User | null;
    isAuthenticated: boolean;
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

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
    const [user, setUser] = useState<User | null>(null);
    
    // Initialize with fake auth state from localStorage for testing
    useEffect(() => {
        const savedAuthState = localStorage.getItem('rnkd_fake_auth');
        if (savedAuthState === 'true') {
            setUser({
                id: '1',
                name: 'John Doe',
                email: 'john@example.com',
                profileImage: undefined
            });
        }
    }, []);

    const login = async (email: string, password: string) => {
        // Mock login - in real app, this would call the API
        const mockUser: User = {
            id: '1',
            name: 'John Doe',
            email: email,
            profileImage: undefined
        };
        setUser(mockUser);
        localStorage.setItem('rnkd_fake_auth', 'true');
    };

    const logout = () => {
        setUser(null);
        localStorage.removeItem('rnkd_fake_auth');
    };

    const register = async (name: string, email: string, password: string) => {
        // Mock registration - in real app, this would call the API
        const mockUser: User = {
            id: '1',
            name: name,
            email: email,
            profileImage: undefined
        };
        setUser(mockUser);
        localStorage.setItem('rnkd_fake_auth', 'true');
    };

    // For testing purposes - toggle authentication state
    const toggleAuth = () => {
        if (user) {
            logout();
        } else {
            login('test@example.com', 'password');
        }
    };

    const value: AuthContextType = {
        user,
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