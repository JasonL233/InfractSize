import React, { useState } from "react";
import { BASE_URL } from "../App"

const UploadForm = () => {
    const [files, setFiles] = useState({
        images: [],
        targetMasks: [],
        totalMasks: []
    });     // Store files that are before uploading

    const [uploadedFiles, setUploadedFiles] = useState([]);     // Store uploaded files
    const [errorMessage, setErrorMessage] = useState(""); 

    const handleFileChange = (event, folder) => {
        setFiles((prevFiles) => ({
            ...prevFiles,
            [folder]: [...event.target.files]
        }));
    }

    const handleUploadAll = async () => {
        const { images, targetMasks, totalMasks } = files;

        // Validate that all three folders have the same number of files
        if (images.length !== targetMasks.length || images.length !== totalMasks.length) {
            setErrorMessage("Error: The number of images, target masks, and total masks must be the same.");
            return;
        }

        // Reset error message if validation passes
        setErrorMessage("");

        const formData = new FormData();
        let hasFiles = false;

        Object.entries(files).forEach(([folder, fileList]) => {
            if (fileList.length > 0) {
                hasFiles = true;
                fileList.forEach((file) => {
                    formData.append("files", file);
                    formData.append("folders", folder);
                })
            }
        });

        if (!hasFiles) return;
    
        try {
            const res = await fetch(BASE_URL + "/upload", {
                method: "POST",
                body: formData,
            });
    
            if (!res.ok) throw new Error(`Upload failed! Status: ${res.status}`);
    
            const data = await res.json();
            setUploadedFiles(data.files);
        } catch (error) {
            console.error("Upload error:", error);
        }

    };
    

    return (
        <div>
            {Object.keys(files).map((folder) => (
                <div key={folder}>
                    <h3>{folder}</h3>
                    <input type="file" multiple onChange={(e) => handleFileChange(e, folder)}/>
                </div>
            ))}

            {errorMessage && <p style={{color: "red"}}>{errorMessage}</p>}

            <button onClick={handleUploadAll}>
                Upload
            </button>

            {uploadedFiles && uploadedFiles.length > 0 && (
                <div>
                    <h2>Uploaded Files: </h2>
                    <ul>
                        {uploadedFiles.map((file, index) => (
                            <li key={index}>{file}</li>
                        ))}
                    </ul>
                </div>
            )};
        </div>
    );
};

export default UploadForm