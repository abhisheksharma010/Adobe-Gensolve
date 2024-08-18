import React from 'react';

const About = ({ darkMode }) => {
    // Inline styles
    const containerStyle = {
        maxWidth: '900px',
        margin: '40px auto',
        padding: '20px',
        backgroundColor: !darkMode ? '#2b2b2b' : '#f9f9f9',
        color: !darkMode ? '#f0f0f0' : '#333',
        borderRadius: '8px',
        boxShadow: !darkMode ? '0 4px 8px rgba(0, 0, 0, 0.3)' : '0 4px 8px rgba(0, 0, 0, 0.1)',
        fontFamily: 'Arial, sans-serif',
        transition: 'background-color 0.3s ease, color 0.3s ease, box-shadow 0.3s ease'
    };

    const imageStyle = {
        width: '100%',
        height: 'auto',
        borderRadius: '8px',
        marginBottom: '20px'
    };

    const titleStyle = {
        fontSize: '2rem',
        fontWeight: 'bold',
        marginBottom: '20px',
        color: !darkMode ? '#f0f0f0' : '#333'
    };

    const descriptionStyle = {
        fontSize: '1rem',
        lineHeight: '1.6',
        color: !darkMode ? '#d0d0d0' : '#666'
    };

    return (
        <div style={containerStyle}>
            <h1 style={titleStyle}>About Adobe Gensolve</h1>
            <p style={descriptionStyle}>
                Adobe Gensolve is an innovative platform designed to simplify complex data interactions and enhance visual representation. With advanced drawing capabilities using `react-konva`, users can create and manipulate graphical elements with precision.
            </p>
            <p style={descriptionStyle}>
                The platform supports effortless CSV file uploads, integrates with Firebase Storage for reliable image management, and offers a user-friendly interface for managing and visualizing data. Adobe Gensolve aims to empower users with intuitive tools that make data handling efficient and accessible.
            </p>
        </div>
    );
};

export default About;
