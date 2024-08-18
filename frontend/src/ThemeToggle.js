import React, { useState, useEffect } from 'react';
import './toggle.css';

const ThemeToggle = ({ darkMode, setDarkMode }) => {
    const [isDarkMode, setIsDarkMode] = useState(darkMode);

    useEffect(() => {
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            setIsDarkMode(savedTheme === 'dark');
            document.body.className = savedTheme;
        }
    }, []);

    useEffect(() => {
        setDarkMode(isDarkMode);
        const newTheme = !isDarkMode ? 'dark' : 'light';
        document.body.className = newTheme;
        localStorage.setItem('theme', newTheme);
    }, [isDarkMode, setDarkMode]);

    const toggleTheme = () => {
        setIsDarkMode(prevMode => !prevMode);
    };

    return (
        <div
            className="theme-switch-container mt-2"
            style={{
                top: '20px',
                right: '20px',
                zIndex: 1000,
            }}
        >
            <div className="theme-switch">
                <input
                    type="checkbox"
                    className="theme-switch__input"
                    id="themeSwitch"
                    checked={isDarkMode}
                    onChange={toggleTheme}
                />
                <label className="theme-switch__label" htmlFor="themeSwitch">
                    <span className="theme-switch__indicator"></span>
                    <span className="theme-switch__decoration"></span>
                </label>
            </div>
        </div>
    );
};

export default ThemeToggle;
