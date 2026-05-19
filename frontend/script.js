const API_URL = "https://mj-7.onrender.com";

async function analyzeSequence() {
    const sequence = document.getElementById('sequenceInput').value;
    const resultBox = document.getElementById('sequenceResult');
    
    if (!sequence) {
        resultBox.innerHTML = '<p style="color:red;">Please enter a sequence first.</p>';
        return;
    }

    resultBox.innerHTML = '<p>Analyzing sequence locally...</p>';

    try {
        const response = await fetch(`${API_URL}/api/analyze-sequence`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ sequence: sequence })
        });

        const data = await response.json();

        if (data.success) {
            resultBox.innerHTML = `
                <h4>Analysis Complete:</h4>
                <p><strong>Classification:</strong> ${data.analysis.sequence_type}</p>
                <p><strong>Length:</strong> ${data.analysis.length} residues</p>
                <p><strong>GC Content:</strong> ${data.analysis.gc_content}%</p>
                <hr>
                <p>${data.analysis.summary.replace(/\n/g, '<br>')}</p>
            `;
        } else {
            resultBox.innerHTML = `<p style="color:red;">Analysis failed: ${data.error}</p>`;
        }
    } catch (error) {
        resultBox.innerHTML = `<p style="color:red;">Network Error: Backend is waking up. Try again in 30 seconds!</p>`;
    }
}
