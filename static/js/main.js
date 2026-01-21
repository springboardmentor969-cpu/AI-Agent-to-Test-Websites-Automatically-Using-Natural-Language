// DOM Elements
const testDescriptionEl = document.getElementById('testDescription');
const parseBtn = document.getElementById('parseBtn');
const runBtn = document.getElementById('runBtn');
const useCodeGenEl = document.getElementById('useCodeGen');

const previewSection = document.getElementById('previewSection');
const previewContent = document.getElementById('previewContent');

const statusSection = document.getElementById('statusSection');
const statusText = document.getElementById('statusText');

const resultsSection = document.getElementById('resultsSection');
const resultsContent = document.getElementById('resultsContent');

const reportsList = document.getElementById('reportsList');

// Example test cases
const examples = {
    login: `Go to http://localhost:5000/test-page
Type 'john@example.com' in the email field
Type 'password123' in the password field
Click the 'Login' button
Verify that the page contains 'Welcome back'`,
    
    search: `Go to https://example.com
Type 'artificial intelligence' in the search box
Click the search button
Verify that search results are displayed`,
    
    form: `Navigate to http://localhost:5000/test-page
Fill 'John Doe' in the name field
Fill 'john@example.com' in the email field
Select 'Option 2' from dropdown
Click the Submit button
Verify success message appears`
};

// Event Listeners
parseBtn.addEventListener('click', handleParse);
runBtn.addEventListener('click', handleRun);

document.querySelectorAll('.example-card').forEach(card => {
    card.addEventListener('click', () => {
        const example = card.dataset.example;
        testDescriptionEl.value = examples[example];
        testDescriptionEl.scrollIntoView({ behavior: 'smooth' });
    });
});

// Load reports on page load
loadReports();

// Functions
async function handleParse() {
    const description = testDescriptionEl.value.trim();
    
    if (!description) {
        alert('Please enter a test description');
        return;
    }
    
    parseBtn.disabled = true;
    parseBtn.innerHTML = '<span>⏳ Parsing...</span>';
    
    try {
        const response = await fetch('/api/parse-test', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ test_description: description })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showPreview(data.parsed_test, data.summary);
        } else {
            showError('Parse Error', data.error);
        }
    } catch (error) {
        showError('Network Error', error.message);
    } finally {
        parseBtn.disabled = false;
        parseBtn.innerHTML = '<span>📝 Preview Test Steps</span>';
    }
}

async function handleRun() {
    const description = testDescriptionEl.value.trim();
    
    if (!description) {
        alert('Please enter a test description');
        return;
    }
    
    runBtn.disabled = true;
    parseBtn.disabled = true;
    runBtn.innerHTML = '<span>⏳ Running...</span>';
    
    // Hide previous results
    resultsSection.style.display = 'none';
    
    // Show status
    statusSection.style.display = 'block';
    statusText.textContent = 'Initializing test execution...';
    
    try {
        const response = await fetch('/api/run-test', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                test_description: description,
                use_code_generation: useCodeGenEl.checked
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showResults(data);
            loadReports(); // Refresh reports list
        } else {
            showError('Test Execution Error', data.error);
        }
    } catch (error) {
        showError('Network Error', error.message);
    } finally {
        runBtn.disabled = false;
        parseBtn.disabled = false;
        runBtn.innerHTML = '<span>🚀 Run Test</span>';
        statusSection.style.display = 'none';
    }
}

function showPreview(parsedTest, summary) {
    previewContent.textContent = summary;
    previewSection.style.display = 'block';
    previewSection.scrollIntoView({ behavior: 'smooth' });
}

    
function showResults(data) {
    const { test_name, status, duration, passed_steps, failed_steps, total_steps, execution_result } = data;
    
    const statusClass = status === 'passed' ? 'passed' : 'failed';
    const statusIcon = status === 'passed' ? '✓' : '✗';
    
    let html = `
        <div class="result-card">
            <div class="result-header">
                <h3 class="result-title">${test_name}</h3>
                <span class="status-badge ${statusClass}">[${statusIcon}]</span>
            </div>
            
            <div class="metrics">
                <div class="metric">
                    <div class="metric-value">${duration ? duration.toFixed(2) : '0.00'}s</div>
                    <div class="metric-label">Duration</div>
                </div>
                <div class="metric">
                    <div class="metric-value" style="color: #10b981;">${passed_steps || 0}</div>
                    <div class="metric-label">Passed</div>
                </div>
                <div class="metric">
                    <div class="metric-value" style="color: #ef4444;">${failed_steps || 0}</div>
                    <div class="metric-label">Failed</div>
                </div>
                <div class="metric">
                    <div class="metric-value">${total_steps || 0}</div>
                    <div class="metric-label">Total Steps</div>
                </div>
            </div>
    `;
    
    // Add step details if available
    if (execution_result && execution_result.step_results && execution_result.step_results.length > 0) {
        html += '<div class="step-list">';
        execution_result.step_results.forEach(step => {
            const stepClass = step.status === 'passed' ? 'passed' : 'failed';
            const stepIcon = step.status === 'passed' ? 'PASS' : 'FAIL';
            
            let errorHtml = '';
            if (step.error) {
                errorHtml = `<div class="step-error">Error: ${step.error}</div>`;
            }
            
            html += `
                <div class="step-item ${stepClass}">
                    <div class="step-header">
                        <span class="step-icon">[${stepIcon}]</span>
                        <span class="step-description">Step ${step.step_number}: ${step.action ? step.action.toUpperCase() : 'UNKNOWN'}</span>
                    </div>
                    ${errorHtml}
                </div>
            `;
        });
        html += '</div>';
    }
    
    // Download & View Options Section
    html += `
        <div style="margin-top: 30px; padding: 25px; background: linear-gradient(to bottom, #f9fafb, #ffffff); border-radius: 12px; border: 1px solid #e5e7eb;">
            <h3 style="margin-bottom: 20px; color: #374151; font-size: 18px; text-align: center;">📦 Download & View Options</h3>
            <div style="display: flex; gap: 12px; justify-content: center; flex-wrap: wrap;">
    `;
    
    // Extract report filename
    const reportFilename = data.report_path ? data.report_path.replace(/\\/g, '/').split('/').pop() : null;
    
    // ALWAYS show report buttons
    if (reportFilename) {
        // View Report Button
        html += `
            <a href="/report/${reportFilename}" target="_blank" 
               style="text-decoration: none; display: inline-flex; align-items: center; gap: 8px; padding: 14px 24px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 8px; font-weight: 600; transition: transform 0.2s;"
               onmouseover="this.style.transform='translateY(-2px)'" 
               onmouseout="this.style.transform='translateY(0)'">
                <span>👁️ View Report</span>
            </a>
        `;
        
        // Download Report Button
        html += `
            <a href="/report/${reportFilename}" download="${reportFilename}" 
               style="text-decoration: none; display: inline-flex; align-items: center; gap: 8px; padding: 14px 24px; background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; border-radius: 8px; font-weight: 600; transition: transform 0.2s;"
               onmouseover="this.style.transform='translateY(-2px)'" 
               onmouseout="this.style.transform='translateY(0)'">
                <span>📥 Download Report</span>
            </a>
        `;
    }
    
    // ONLY show code buttons if code was generated (checkbox was checked)
    if (data.code_path) {
        const codeFilename = data.code_path.replace(/\\/g, '/').split('/').pop();
        
        // Download Code Button
        html += `
            <a href="/report/${codeFilename}" download="${codeFilename}" 
               style="text-decoration: none; display: inline-flex; align-items: center; gap: 8px; padding: 14px 24px; background: linear-gradient(135deg, #667eea 0%, #5a67d8 100%); color: white; border-radius: 8px; font-weight: 600; transition: transform 0.2s;"
               onmouseover="this.style.transform='translateY(-2px)'" 
               onmouseout="this.style.transform='translateY(0)'">
                <span>💾 Download Code</span>
            </a>
        `;
    }
    
    // View Generated Code Button (inline modal)
    if (data.generated_code) {
        html += `
            <button onclick="showGeneratedCode()" 
                    style="display: inline-flex; align-items: center; gap: 8px; padding: 14px 24px; background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: white; border-radius: 8px; font-weight: 600; border: none; cursor: pointer; transition: transform 0.2s;"
                    onmouseover="this.style.transform='translateY(-2px)'" 
                    onmouseout="this.style.transform='translateY(0)'">
                <span>📄 View Generated Code</span>
            </button>
        `;
        
        // Store code in global variable
        window.generatedCode = data.generated_code;
    }
    
    html += `
            </div>
        </div>
    </div>`;
    
    resultsContent.innerHTML = html;
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

// Function to show generated code in modal
function showGeneratedCode() {
    if (!window.generatedCode) return;
    
    const modal = document.createElement('div');
    modal.style.cssText = 'position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.8); z-index: 9999; display: flex; align-items: center; justify-content: center; padding: 20px;';
    
    modal.innerHTML = `
        <div style="background: white; border-radius: 12px; max-width: 900px; width: 100%; max-height: 90vh; overflow: auto; position: relative;">
            <div style="position: sticky; top: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 12px 12px 0 0; display: flex; justify-content: space-between; align-items: center;">
                <h2 style="margin: 0; font-size: 20px;">💻 Generated Playwright Code</h2>
                <button onclick="this.closest('[style*=\"position: fixed\"]').remove()" 
                        style="background: white; color: #667eea; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-weight: 600;">
                    ✕ Close
                </button>
            </div>
            <div style="padding: 30px;">
                <pre style="background: #1f2937; color: #e5e7eb; padding: 20px; border-radius: 8px; overflow-x: auto; font-family: 'Courier New', monospace; font-size: 14px; line-height: 1.6;">${escapeHtml(window.generatedCode)}</pre>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Close on background click
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.remove();
        }
    });
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showError(title, message) {
    resultsContent.innerHTML = `
        <div class="error-message">
            <h4 style="margin-bottom: 8px;">${title}</h4>
            <p>${message}</p>
        </div>
    `;
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

async function loadReports() {
    try {
        const response = await fetch('/api/reports');
        const data = await response.json();
        
        if (data.success && data.reports.length > 0) {
            let html = '';
            
            data.reports.forEach(report => {
                const date = new Date(report.modified * 1000);
                const dateStr = date.toLocaleString();
                
                html += `
                    <div class="report-item">
                        <div class="report-info">
                            <h4>${report.filename}</h4>
                            <p>${dateStr} • ${(report.size / 1024).toFixed(1)} KB</p>
                        </div>
                        <div class="report-actions">
                            <a href="/report/${report.filename}" target="_blank" class="btn-small btn-view">
                                View Report
                            </a>
                        </div>
                    </div>
                `;
            });
            
            reportsList.innerHTML = html;
        } else {
            reportsList.innerHTML = '<p class="loading">No reports yet. Run a test to generate your first report!</p>';
        }
    } catch (error) {
        reportsList.innerHTML = '<p class="loading">Failed to load reports</p>';
    }
}