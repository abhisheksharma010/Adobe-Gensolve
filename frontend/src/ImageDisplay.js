// ImageDisplay.js
import React from "react";

const ImageDisplay = ({ url, title }) => {
    return (
        <div style={{ flex: 1, textAlign: "center" }}>
            <h3 style={{ color: "#007bff", marginBottom: "10px" }}>{title}</h3>
            <img
                src={url}
                alt={title}
                style={{
                    maxWidth: "100%",
                    maxHeight: "550px",
                    borderRadius: "8px",
                    boxShadow: "0 4px 8px rgba(0, 0, 0, 0.3)",
                }}
            />
        </div>
    );
};

export default ImageDisplay;
