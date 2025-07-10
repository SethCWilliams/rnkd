import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider } from './contexts/ThemeContext';
import { AuthProvider } from './contexts/AuthContext';
import Layout from './components/Layout';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Groups from './pages/Groups';
import Voting from './pages/Voting';
import Results from './pages/Results';

function App() {
    return (
        <ThemeProvider>
            <AuthProvider>
                <div className="min-h-screen bg-dark-900">
                    <Routes>
                        <Route path="/" element={<Home />} />
                        <Route path="/login" element={<Login />} />
                        <Route path="/register" element={<Register />} />
                        <Route path="/app/*" element={<Layout />}>
                            <Route index element={<Dashboard />} />
                            <Route path="groups" element={<Groups />} />
                            <Route path="voting/:listId" element={<Voting />} />
                            <Route path="results/:listId" element={<Results />} />
                        </Route>
                    </Routes>
                </div>
            </AuthProvider>
        </ThemeProvider>
    );
}

export default App; 