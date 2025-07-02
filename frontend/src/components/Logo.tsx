import React from 'react';

interface LogoProps {
    size?: 'sm' | 'md' | 'lg';
    className?: string;
}

const Logo: React.FC<LogoProps> = ({ size = 'md', className = '' }) => {
    const sizeClasses = {
        sm: 'h-6 w-6',
        md: 'h-8 w-8',
        lg: 'h-20 w-20'
    };

    const textSizes = {
        sm: 'text-lg',
        md: 'text-xl',
        lg: 'text-3xl'
    };

    return (
        <div className={`flex items-center ${className}`}>
            <img
                src="/images/logo/icon.png"
                alt="Rnkd Logo"
                className={`${sizeClasses[size]} object-contain`}
            />
            <span className={`font-extrabold text-accent-neon tracking-tight ${textSizes[size]}`}>
                RNKD
            </span>
        </div>
    );
};

export default Logo; 