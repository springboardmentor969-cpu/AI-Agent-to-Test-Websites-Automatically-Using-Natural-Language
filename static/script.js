// Global variable to store test results
let testResults = null;

// ========================================
// Dark Mode Toggle
// ========================================
document.addEventListener('DOMContentLoaded', function () {
    const darkModeToggle = document.getElementById('darkModeToggle');
    const html = document.documentElement;

    // Check for saved theme preference or default to 'light'
    const savedTheme = localStorage.getItem('theme') || 'light';
    html.setAttribute('data-theme', savedTheme);
    updateToggleIcon(savedTheme);

    // Toggle theme on button click
    darkModeToggle.addEventListener('click', function () {
        const currentTheme = html.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

        html.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateToggleIcon(newTheme);
    });

    function updateToggleIcon(theme) {
        darkModeToggle.textContent = theme === 'dark' ? '☀️' : '🌙';
    }

    // ========================================
    // Example Cards Click Handlers
    // ========================================
    const exampleCards = document.querySelectorAll('.example-card');
    const textarea = document.getElementById('instruction');

    exampleCards.forEach(card => {
        card.addEventListener('click', function () {
            const exampleText = this.getAttribute('data-example');
            textarea.value = exampleText;
            textarea.focus();

            // Visual feedback
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = '';
            }, 200);
        });
    });
});

// ========================================
// Form Submission
// ========================================
async function submitTest(event) {
    event.preventDefault();

    const instruction = document.getElementById('instruction').value.trim();
    if (!instruction) {
        alert('Please enter a test instruction');
        return;
    }

    const submitBtn = document.getElementById('submitBtn');
    const resultsSection = document.getElementById('resultsSection');

    // Show loading state
    submitBtn.classList.add('loading');
    submitBtn.innerHTML = '<span class="spinner"></span><span class="btn-text">Running Test...</span>';
    submitBtn.disabled = true;

    // Hide previous results
    resultsSection.style.display = 'none';

    try {
        const response = await fetch('/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ instruction })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        testResults = data;

        // Display results
        displayResults(data);

        // Scroll to results
        setTimeout(() => {
            resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 300);

    } catch (error) {
        console.error('Error:', error);

        // Try to get more detailed error info
        let errorMessage = 'An error occurred while running the test.';
        if (error.message) {
            errorMessage += '\n\nDetails: ' + error.message;
        }

        alert(errorMessage);
    } finally {
        // Reset button state
        submitBtn.classList.remove('loading');
        submitBtn.innerHTML = '<span class="btn-icon">▶️</span><span class="btn-text">Run Test</span>';
        submitBtn.disabled = false;
    }
}

// ========================================
// Display Results
// ========================================
function displayResults(data) {
    const resultsSection = document.getElementById('resultsSection');
    const stepsList = document.getElementById('stepsList');

    // Show results section
    resultsSection.style.display = 'block';

    // Calculate statistics
    const totalSteps = data.results ? data.results.length : 0;
    const passedSteps = data.results ? data.results.filter(r => r.success).length : 0;
    const failedSteps = totalSteps - passedSteps;
    const totalTime = data.results ? data.results.reduce((sum, r) => sum + (r.execution_time || 0), 0) : 0;

    // Update statistics cards
    document.getElementById('totalSteps').textContent = totalSteps;
    document.getElementById('passedSteps').textContent = passedSteps;
    document.getElementById('failedSteps').textContent = failedSteps;
    document.getElementById('executionTime').textContent = (totalTime / 1000).toFixed(2) + 's';

    // Display execution steps with collapsible functionality
    if (data.results && data.results.length > 0) {
        stepsList.innerHTML = data.results.map((result, index) => {
            const statusClass = result.success ? 'success' : 'error';
            const statusIcon = result.success ? '✓' : '✗';
            const statusText = result.success ? 'SUCCESS' : 'FAILED';

            // Build details HTML
            let detailsHTML = '<div class="step-details">';

            if (result.selector) {
                detailsHTML += `
                    <div class="step-detail-row">
                        <div class="step-detail-label">Selector:</div>
                        <div class="step-detail-value">${result.selector}</div>
                    </div>
                `;
            }

            if (result.value) {
                detailsHTML += `
                    <div class="step-detail-row">
                        <div class="step-detail-label">Value:</div>
                        <div class="step-detail-value">${result.value}</div>
                    </div>
                `;
            }

            if (result.execution_time) {
                detailsHTML += `
                    <div class="step-detail-row">
                        <div class="step-detail-label">Time:</div>
                        <div class="step-detail-value">${result.execution_time}ms</div>
                    </div>
                `;
            }

            if (result.error) {
                detailsHTML += `
                    <div class="step-detail-row">
                        <div class="step-detail-label">Error:</div>
                        <div class="step-detail-value" style="color: var(--error);">${result.error}</div>
                    </div>
                `;
            }

            // Add screenshot if available - use the screenshot_path from this specific result
            if (result.screenshot_path) {
                detailsHTML += `
                    <div class="step-screenshot" onclick="window.open('${result.screenshot_path}', '_blank')">
                        <img src="${result.screenshot_path}" alt="Step ${index + 1} Screenshot" loading="lazy" onerror="this.parentElement.style.display='none'">
                    </div>
                `;
            }

            detailsHTML += '</div>';

            return `
                <div class="step-item collapsed" onclick="toggleStep(this)">
                    <div class="step-header">
                        <div class="step-title-wrapper">
                            <div class="step-number">${index + 1}</div>
                            <div class="step-title">${result.action_type || 'Action'}</div>
                        </div>
                        <div class="step-status ${statusClass}">
                            ${statusIcon} ${statusText}
                        </div>
                    </div>
                    ${detailsHTML}
                </div>
            `;
        }).join('');
    } else {
        stepsList.innerHTML = '<p style="color: var(--text-secondary); padding: 1rem;">No execution steps recorded.</p>';
    }

    // Scroll to results
    setTimeout(() => {
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 300);
}

// Toggle step collapse/expand
function toggleStep(stepElement) {
    stepElement.classList.toggle('collapsed');
}

// ========================================
// Download Report (TXT)
// ========================================
function downloadReport() {
    if (!testResults) {
        alert('No test results available to download');
        return;
    }

    const timestamp = new Date().toISOString();
    const allSuccess = testResults.results && testResults.results.every(r => r.success);
    const status = allSuccess ? 'PASS' : 'FAIL';

    let reportText = `========================================
AI WEBSITE TESTING REPORT
========================================

Test Status: ${status}
Timestamp: ${timestamp}
Instruction: ${testResults.instruction || 'N/A'}

========================================
EXECUTION STEPS
========================================

`;

    if (testResults.results && testResults.results.length > 0) {
        testResults.results.forEach((result, index) => {
            reportText += `Step ${index + 1}: ${result.action_type || 'Action'}\n`;
            reportText += `Status: ${result.success ? 'SUCCESS' : 'FAILED'}\n`;
            if (result.selector) reportText += `Selector: ${result.selector}\n`;
            if (result.value) reportText += `Value: ${result.value}\n`;
            if (result.error) reportText += `Error: ${result.error}\n`;
            if (result.execution_time) reportText += `Execution Time: ${result.execution_time}ms\n`;
            reportText += '\n';
        });
    }

    reportText += `========================================
END OF REPORT
========================================`;

    // Create and download file
    const blob = new Blob([reportText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `test-report-${Date.now()}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// ========================================
// Download JSON
// ========================================
function downloadJSON() {
    if (!testResults) {
        alert('No test results available to download');
        return;
    }

    const allSuccess = testResults.results && testResults.results.every(r => r.success);
    const status = allSuccess ? 'PASS' : 'FAIL';

    const jsonData = {
        timestamp: new Date().toISOString(),
        status: status,
        instruction: testResults.instruction,
        results: testResults.results || [],
        plan: testResults.plan || null,
        report: testResults.report || null,
        snapshots: testResults.snapshots || []
    };

    // Create and download file
    const jsonString = JSON.stringify(jsonData, null, 2);
    const blob = new Blob([jsonString], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `test-results-${Date.now()}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}
