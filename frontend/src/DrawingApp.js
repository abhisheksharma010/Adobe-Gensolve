import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import { Stage, Layer, Line } from "react-konva";
import { FaPencilAlt } from "react-icons/fa";
import Controls from "./Controls";
import ImageDisplay from "./ImageDisplay";
// import Header from "./Header.js";

const DrawingApp = () => {
    const [lines, setLines] = useState([]);
    const [isDrawing, setIsDrawing] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [inputImageUrl, setInputImageUrl] = useState("");
    const [outputImageUrl, setOutputImageUrl] = useState("");
    const [refreshTrigger, setRefreshTrigger] = useState(0);
    const lastPosRef = useRef(null);
    const fileInputRef = useRef(null);

    const DRAWING_WIDTH = 800;
    const DRAWING_HEIGHT = 550;

    const handleMouseDown = (e) => {
        if (isLoading) return;
        const pos = e.target.getStage().getPointerPosition();
        lastPosRef.current = pos;
        setIsDrawing(true);
        setLines([...lines, { points: [{ x: pos.x, y: pos.y }] }]);
    };

    const handleMouseMove = (e) => {
        if (!isDrawing || isLoading) return;
        const stage = e.target.getStage();
        const pos = stage.getPointerPosition();
        const newLines = [...lines];
        const lastLine = newLines[newLines.length - 1];
        lastLine.points = [...lastLine.points, { x: pos.x, y: pos.y }];
        setLines(newLines);
        lastPosRef.current = pos;
    };

    const handleMouseUp = () => {
        setIsDrawing(false);
    };

    const generateCSVData = () => {
        let csvContent = "";
        lines.forEach((line, polylineIndex) => {
            line.points.forEach((point) => {
                csvContent += `${polylineIndex},0,${point.x},${point.y}\n`;
            });
        });
        return csvContent;
    };

    const downloadResults = async () => {
        setIsLoading(true);
        const csvData = generateCSVData();
        const blob = new Blob([csvData], { type: "text/csv" });
        const formData = new FormData();
        formData.append("file", blob, "polylines.csv");

        try {
            const response = await axios.post(
                `https://shadow-fd0n.onrender.com/upload-csv`,
                formData,
                { responseType: "blob" }
            );

            const zipBlob = new Blob([response.data], { type: "application/zip" });
            const url = window.URL.createObjectURL(zipBlob);
            const a = document.createElement("a");
            a.style.display = "none";
            a.href = url;
            a.download = "results.zip";
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            setRefreshTrigger((prev) => prev + 1);
        } catch (error) {
            console.error("Error during file download:", error);
        } finally {
            setIsLoading(false);
        }
    };

    const processCSV = async (file) => {
        setIsLoading(true);
        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await axios.post(
                `https://shadow-fd0n.onrender.com/upload-csv`,
                formData,
                { responseType: "blob" }
            );

            const zipBlob = new Blob([response.data], { type: "application/zip" });
            const url = window.URL.createObjectURL(zipBlob);
            const a = document.createElement("a");
            a.style.display = "none";
            a.href = url;
            a.download = "results.zip";
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            setRefreshTrigger((prev) => prev + 1);
        } catch (error) {
            console.error("Error during file download:", error);
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        setInputImageUrl(
            `https://firebasestorage.googleapis.com/v0/b/adobe-gensolve.appspot.com/o/images%2Finput_image.png?alt=media&refresh=${refreshTrigger}`
        );
        setOutputImageUrl(
            `https://firebasestorage.googleapis.com/v0/b/adobe-gensolve.appspot.com/o/images%2Foutput_image.png?alt=media&refresh=${refreshTrigger}`
        );
    }, [refreshTrigger]);

    return (
        <div className={`theme-container ${document.body.classList.contains("dark") ? "dark" : "light"}`} style={{ padding: "20px", minHeight: "100vh" }}>
            {/* <Header /> */}


            <div
                style={{
                    border: "10px solid var(--text-color)",
                    backgroundColor: "var(--background-color)",
                    marginTop: "80px",
                    borderRadius: "12px",
                    boxShadow: "0 4px 8px rgba(0, 0, 0, 0.3)",
                    position: "relative",
                    padding: "10px",
                    display: "flex",
                    flexDirection: "row",
                    alignItems: "flex-start",
                    gap: "20px",
                    overflowX: "auto",
                    paddingBottom: "20px",
                }}
            >
                <Stage
                    width={DRAWING_WIDTH}
                    height={DRAWING_HEIGHT}
                    onMouseDown={handleMouseDown}
                    onMouseMove={handleMouseMove}
                    onMouseUp={handleMouseUp}
                    style={{
                        backgroundColor: "transparent",
                        borderRadius: "8px",
                        boxShadow: "inset 0 0 10px rgba(0, 0, 0, 0.5)",
                        flexShrink: 0,
                    }}
                >
                    <Layer>
                        {lines.map((line, i) => (
                            <Line
                                key={i}
                                points={line.points.flatMap((p) => [p.x, p.y])}
                                stroke="yellow"
                                strokeWidth={2}
                                tension={0.5}
                                lineCap="round"
                                globalCompositeOperation="source-over"
                            />
                        ))}
                    </Layer>
                </Stage>

                <ImageDisplay url={inputImageUrl} title="Input Image" />
                <ImageDisplay url={outputImageUrl} title="Output Image" />
            </div>

            <Controls
                fileInputRef={fileInputRef}
                handleProcessCSVClick={() => fileInputRef.current.click()}
                handleFileChange={(event) => {
                    const file = event.target.files[0];
                    if (file) processCSV(file);
                }}
                downloadResults={downloadResults}
                isLoading={isLoading}
            />
        </div>
    );
};

export default DrawingApp;
