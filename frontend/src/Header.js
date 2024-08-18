import React from 'react';
import { FaPencilAlt, FaGithub } from 'react-icons/fa';
import { Link } from 'react-router-dom';
import ThemeToggle from './ThemeToggle';

const Header = ({ darkMode, setDarkMode }) => {
    React.useEffect(() => {
        const root = document.documentElement;
        root.style.setProperty('--background-color', darkMode ? '#2b2b2b' : '#f0f0f0');
        root.style.setProperty('--text-color', darkMode ? '#fff' : '#000');
    }, [darkMode]);

    return (
        <header style={headerStyle}>

            <Link to='/' style={navLinkStyle}>
                <div style={logoStyle}>
                    <FaPencilAlt style={{ marginRight: '10px' }} />
                    <h1>Adobe-Gensolve</h1>
                </div>
            </Link>

            <nav style={navStyle}>
                <Link to="/about" style={navLinkStyle}>About</Link>
                <a href="https://github.com/Bhuvantenguria/Adobe-Gensolve" target="_blank" rel="noopener noreferrer" style={navLinkStyle}>
                    <FaGithub style={{ marginRight: '10px' }} />
                    GitHub
                </a>
                <ThemeToggle darkMode={darkMode} setDarkMode={setDarkMode} />
            </nav>
        </header>
    );
};

const headerStyle = {
    width: '97%',
    padding: '10px 20px',
    backgroundColor: 'var(--background-color)',
    color: 'var(--text-color)',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
    zIndex: 1000,
};

const logoStyle = {
    display: 'flex',
    alignItems: 'center',
};

const linkStyle = {
    textDecoration: 'none',
    color: 'inherit',
};

const navStyle = {
    display: 'flex',
    alignItems: 'center',
};

const navLinkStyle = {
    marginRight: '80px',
    // margin: '20px',
    textDecoration: 'none',
    color: 'var(--text-color)',
    fontSize: '26px',
    display: 'flex',
    alignItems: 'center',
};

export default Header;
