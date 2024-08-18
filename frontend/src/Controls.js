// Controls.js
import React from "react";

const Controls = ({ fileInputRef, handleProcessCSVClick, handleFileChange, downloadResults, isLoading }) => {
    return (
        <div style={{ display: "flex", marginTop: "20px", justifyContent: "center", gap: "20px" }}>
            <input
                type="file"
                ref={fileInputRef}
                onChange={handleFileChange}
                style={{ display: "none" }}
            />
            <button
                onClick={handleProcessCSVClick}
                style={{
                    padding: "10px 20px",
                    fontSize: "16px",
                    color: "#fff",
                    backgroundColor: "#007bff",
                    border: "none",
                    borderRadius: "8px",
                    cursor: "pointer",
                    boxShadow: "0 4px 8px rgba(0, 0, 0, 0.3)",
                    transition: "background-color 0.3s ease",
                }}
            >
                Process CSV
            </button>
            <button
                onClick={downloadResults}
                disabled={isLoading}
                style={{
                    padding: "10px 20px",
                    fontSize: "16px",
                    color: "#fff",
                    backgroundColor: isLoading ? "#ccc" : "#28a745",
                    border: "none",
                    borderRadius: "8px",
                    cursor: isLoading ? "not-allowed" : "pointer",
                    boxShadow: "0 4px 8px rgba(0, 0, 0, 0.3)",
                    transition: "background-color 0.3s ease",
                }}
            >
                {isLoading ? "Processing..." : "Download Results"}
            </button>
        </div>
    );
};

export default Controls;
