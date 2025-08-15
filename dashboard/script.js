document.addEventListener('DOMContentLoaded', () => {
    const statsDiv = document.getElementById('stats');
    statsDiv.innerHTML = `
        <p>Total Applications: <span id="total">Loading...</span></p>
        <p>Successful: <span id="success">Loading...</span></p>
        <p>Failed: <span id="failed">Loading...</span></p>
    `;
    // Add Flask backend to fetch stats from applications.db
});