// MJ - Biochemistry AI Tool
// Frontend JavaScript

const API_URL = "https://mj-7.onrender.com";

// Analyze Sequence Function
async function analyzeSequence() {
    const sequence = document.getElementById('sequenceInput').value;
    
    if (!sequence.trim()) {
        alert('Please enter a sequence');
        return;
    }
    
    const resultBox = document.getElementById('sequenceResult');
    resultBox.innerHTML = '<p>Analyzing...</p>';
    resultBox.classList.add('active');
    
    try {
        const response = await fetch(`${API_URL}/api/analyze-sequence`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ sequence: sequence })
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            const result = data.data;
            resultBox.innerHTML = `
                <h4>Analysis Results:</h4>
                <p><strong>Sequence Type:</strong> ${result.sequence_type}</p>
                <p><strong>Length:</strong> ${result.length} nucleotides/amino acids</p>
                <p><strong>Preview:</strong> ${result.sequence}</p>
                <p style="color: green;">✅ Analysis complete!</p>
            `;
        } else {
            resultBox.innerHTML = `<p style="color: red;">Error: ${data.error}</p>`;
        }
    } catch (error) {
        resultBox.innerHTML = `
            <p style="color: red;">
                Error connecting to API. Make sure the server is running on port 5000.
            </p>
            <p style="font-size: 0.9rem; color: #666;">
                Error: ${error.message}
            </p>
        `;
    }
}

// Health Check Function
async function checkHealth() {
    const resultBox = document.getElementById('healthResult');
    resultBox.innerHTML = '<p>Checking API health...</p>';
    resultBox.classList.add('active');
    
    try {
        const response = await fetch(`${API_URL}/api/health`);
        const data = await response.json();
        
        if (data.status === 'healthy') {
            resultBox.innerHTML = `
                <h4>API Status:</h4>
                <p><strong>Status:</strong> ${data.status}</p>
                <p><strong>App:</strong> ${data.app}</p>
                <p><strong>Version:</strong> ${data.version}</p>
                <p style="color: green;">✅ API is running!</p>
            `;
        } else {
            resultBox.innerHTML = `<p style="color: red;">API is not healthy</p>`;
        }
    } catch (error) {
        resultBox.innerHTML = `
            <p style="color: red;">
                ❌ Cannot connect to API server.
            </p>
            <p style="font-size: 0.9rem; color: #666;">
                Make sure the Flask server is running on http://localhost:5000
            </p>
        `;
    }
}

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('MJ - Biochemistry AI Tool loaded');
    console.log('API URL:', API_URL);
});
