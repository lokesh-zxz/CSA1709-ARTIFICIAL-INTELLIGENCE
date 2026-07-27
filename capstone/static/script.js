document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('drawingCanvas');
    const ctx = canvas.getContext('2d');
    const clearBtn = document.getElementById('clearBtn');
    const resultEl = document.getElementById('predictionResult');
    const confidenceVal = document.getElementById('confidenceValue');
    const confidenceFill = document.getElementById('confidenceFill');

    // Setup canvas
    ctx.lineWidth = 15;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.strokeStyle = '#000000'; // Black ink
    ctx.fillStyle = '#ffffff'; // White background
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    let isDrawing = false;
    let lastX = 0;
    let lastY = 0;
    let predictionTimeout = null;

    // Drawing functions
    function startDrawing(e) {
        isDrawing = true;
        const pos = getPos(e);
        lastX = pos.x;
        lastY = pos.y;
    }

    function draw(e) {
        if (!isDrawing) return;
        e.preventDefault(); // Prevent scrolling on touch

        const pos = getPos(e);
        
        ctx.beginPath();
        ctx.moveTo(lastX, lastY);
        ctx.lineTo(pos.x, pos.y);
        ctx.stroke();

        lastX = pos.x;
        lastY = pos.y;

        // Debounce prediction to avoid sending too many requests
        clearTimeout(predictionTimeout);
        predictionTimeout = setTimeout(sendPredictionRequest, 300); // Wait 300ms after drawing stops
    }

    function stopDrawing() {
        if (isDrawing) {
            isDrawing = false;
            sendPredictionRequest();
        }
    }

    function getPos(e) {
        const rect = canvas.getBoundingClientRect();
        // Handle both mouse and touch events
        const clientX = e.touches ? e.touches[0].clientX : e.clientX;
        const clientY = e.touches ? e.touches[0].clientY : e.clientY;
        
        // Scale appropriately if canvas is resized
        const scaleX = canvas.width / rect.width;
        const scaleY = canvas.height / rect.height;

        return {
            x: (clientX - rect.left) * scaleX,
            y: (clientY - rect.top) * scaleY
        };
    }

    // Clear canvas
    clearBtn.addEventListener('click', () => {
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        resultEl.textContent = '-';
        confidenceVal.textContent = '0%';
        confidenceFill.style.width = '0%';
    });

    // Event listeners
    canvas.addEventListener('mousedown', startDrawing);
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseup', stopDrawing);
    canvas.addEventListener('mouseout', stopDrawing);

    canvas.addEventListener('touchstart', startDrawing, {passive: false});
    canvas.addEventListener('touchmove', draw, {passive: false});
    canvas.addEventListener('touchend', stopDrawing);
    canvas.addEventListener('touchcancel', stopDrawing);

    // Image Upload
    const uploadBtn = document.getElementById('uploadBtn');
    const imageUpload = document.getElementById('imageUpload');

    uploadBtn.addEventListener('click', () => {
        imageUpload.click();
    });

    imageUpload.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (event) => {
            const img = new Image();
            img.onload = () => {
                // Clear canvas first
                ctx.fillStyle = '#ffffff';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                
                // Draw image centered and scaled to fit
                // We want to scale it down if it's too big, but not scale up small images excessively
                const scale = Math.min(canvas.width / img.width, canvas.height / img.height, 1);
                const x = (canvas.width / 2) - (img.width / 2) * scale;
                const y = (canvas.height / 2) - (img.height / 2) * scale;
                ctx.drawImage(img, x, y, img.width * scale, img.height * scale);
                
                // Reset file input so same file can be uploaded again if needed
                imageUpload.value = '';
                
                // Send prediction request
                sendPredictionRequest();
            };
            img.src = event.target.result;
        };
        reader.readAsDataURL(file);
    });

    // API Call
    async function sendPredictionRequest() {
        // Check if canvas is basically empty before sending
        // (A simple heuristic could be used, but for now we send and let backend handle)
        const imageData = canvas.toDataURL('image/png');
        
        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ image: imageData })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Server error');
            }

            const data = await response.json();
            
            // Update UI
            resultEl.textContent = data.prediction;
            const confPercent = (data.confidence * 100).toFixed(2);
            confidenceVal.textContent = `${confPercent}%`;
            confidenceFill.style.width = `${confPercent}%`;
            
            // Change color based on confidence
            if (data.confidence > 0.8) {
                confidenceFill.style.backgroundColor = '#4caf50'; // Green
            } else if (data.confidence > 0.5) {
                confidenceFill.style.backgroundColor = '#ff9800'; // Orange
            } else {
                confidenceFill.style.backgroundColor = '#f44336'; // Red
            }

        } catch (error) {
            console.error('Prediction failed:', error);
            // Optionally show error to user
        }
    }
});
