// Bank Check Extractor Dashboard JavaScript

class CheckExtractorApp {
    constructor() {
        this.processedChecks = 0;
        this.successfulChecks = 0;
        this.totalAmount = 0;
        this.results = [];
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupTabs();
        this.setupFileUpload();
        this.updateStats();
        this.initCharts();
        this.loadSampleData();
    }

    setupEventListeners() {
        // Navigation
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const target = e.target.getAttribute('href').substring(1);
                this.showTab(target);
                
                // Update nav active state
                document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
                e.target.classList.add('active');
            });
        });

        // File processing
        document.getElementById('processBtn').addEventListener('click', () => {
            this.processFiles();
        });

        document.getElementById('clearBtn').addEventListener('click', () => {
            this.clearFiles();
        });
    }

    setupTabs() {
        // Show dashboard by default
        this.showTab('dashboard');
    }

    showTab(tabName) {
        // Hide all tabs
        document.querySelectorAll('.tab-content').forEach(tab => {
            tab.classList.remove('active');
        });

        // Show selected tab
        const targetTab = document.getElementById(tabName);
        if (targetTab) {
            targetTab.classList.add('active');
        }
    }

    setupFileUpload() {
        const fileInput = document.getElementById('fileInput');
        const uploadArea = document.getElementById('uploadArea');
        const fileList = document.getElementById('fileList');

        // File input change
        fileInput.addEventListener('change', (e) => {
            this.handleFiles(e.target.files);
        });

        // Drag and drop
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });

        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            this.handleFiles(e.dataTransfer.files);
        });

        // Click to upload
        uploadArea.addEventListener('click', () => {
            fileInput.click();
        });
    }

    handleFiles(files) {
        const fileList = document.getElementById('fileList');
        const processBtn = document.getElementById('processBtn');

        // Clear existing files
        fileList.innerHTML = '';

        if (files.length === 0) {
            processBtn.disabled = true;
            return;
        }

        Array.from(files).forEach((file, index) => {
            const fileItem = document.createElement('div');
            fileItem.className = 'file-item';
            fileItem.innerHTML = `
                <div class="file-info">
                    <i class="fas fa-file-${this.getFileIcon(file.type)}"></i>
                    <span>${file.name}</span>
                    <small class="text-muted ms-2">(${this.formatFileSize(file.size)})</small>
                </div>
                <div class="file-actions">
                    <button class="btn btn-sm btn-outline-danger" onclick="checkExtractor.removeFile(${index})">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            `;
            fileList.appendChild(fileItem);
        });

        this.selectedFiles = files;
        processBtn.disabled = false;
    }

    getFileIcon(fileType) {
        if (fileType.includes('pdf')) return 'pdf';
        if (fileType.includes('image')) return 'image';
        return 'alt';
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    removeFile(index) {
        const filesArray = Array.from(this.selectedFiles);
        filesArray.splice(index, 1);
        this.handleFiles(filesArray);
    }

    clearFiles() {
        document.getElementById('fileInput').value = '';
        document.getElementById('fileList').innerHTML = '';
        document.getElementById('processBtn').disabled = true;
        this.selectedFiles = [];
    }

    async processFiles() {
        if (!this.selectedFiles || this.selectedFiles.length === 0) return;

        const processingStatus = document.getElementById('processingStatus');
        const loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));

        // Show loading
        loadingModal.show();

        // Simulate processing (in real app, this would call the backend)
        for (let i = 0; i < this.selectedFiles.length; i++) {
            const file = this.selectedFiles[i];
            
            // Update processing status
            processingStatus.innerHTML = `
                <div class="status-item status-processing">
                    <h6><i class="fas fa-spinner fa-spin me-2"></i>Processing: ${file.name}</h6>
                    <div class="progress mt-2">
                        <div class="progress-bar" style="width: ${((i + 1) / this.selectedFiles.length) * 100}%"></div>
                    </div>
                </div>
            `;

            // Simulate processing delay
            await new Promise(resolve => setTimeout(resolve, 1500));

            // Simulate extraction results
            const result = this.simulateExtraction(file.name);
            this.results.push(result);
            this.updateResultsTable();
            this.updateStats();
        }

        // Hide loading
        loadingModal.hide();

        // Show success
        processingStatus.innerHTML = `
            <div class="status-item status-success">
                <h6><i class="fas fa-check-circle me-2"></i>Processing Complete!</h6>
                <p class="mb-0">Successfully processed ${this.selectedFiles.length} files</p>
            </div>
        `;

        // Switch to results tab
        this.showTab('results');
        document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
        document.querySelector('[href="#results"]').classList.add('active');

        // Clear files
        this.clearFiles();
    }

    simulateExtraction(filename) {
        // Simulate realistic check data extraction
        const checkNumbers = ['1001', '1002', '1003', '1004', '1005'];
        const accounts = ['230995329781824', '445566778899', '123456789012'];
        const amounts = [250.00, 1500.75, 89.99, 3200.00, 450.25];
        const payees = ['John Doe', 'ABC Corp', 'Electric Company', 'Jane Smith'];
        
        const isSuccess = Math.random() > 0.1; // 90% success rate
        
        const result = {
            filename: filename,
            checkNumber: isSuccess ? checkNumbers[Math.floor(Math.random() * checkNumbers.length)] : 'Not found',
            date: isSuccess ? this.randomDate() : 'Not found',
            accountNumber: isSuccess ? accounts[Math.floor(Math.random() * accounts.length)] : 'Not found',
            amount: isSuccess ? amounts[Math.floor(Math.random() * amounts.length)] : 0,
            payTo: isSuccess ? payees[Math.floor(Math.random() * payees.length)] : 'Not found',
            status: isSuccess ? 'success' : 'error',
            timestamp: new Date().toISOString()
        };

        return result;
    }

    randomDate() {
        const start = new Date(2024, 0, 1);
        const end = new Date();
        const date = new Date(start.getTime() + Math.random() * (end.getTime() - start.getTime()));
        return date.toLocaleDateString();
    }

    updateResultsTable() {
        const tbody = document.getElementById('resultsTableBody');
        
        if (this.results.length === 0) {
            tbody.innerHTML = '<tr><td colspan="8" class="text-center text-muted">No results available</td></tr>';
            return;
        }

        tbody.innerHTML = this.results.map(result => `
            <tr>
                <td><i class="fas fa-file-${this.getFileIcon(result.filename)} me-2"></i>${result.filename}</td>
                <td>${result.checkNumber}</td>
                <td>${result.date}</td>
                <td>${result.accountNumber}</td>
                <td>${result.amount > 0 ? '$' + result.amount.toFixed(2) : 'Not found'}</td>
                <td>${result.payTo}</td>
                <td><span class="status-badge status-${result.status}">${result.status}</span></td>
                <td>
                    <button class="btn btn-sm btn-outline-primary" onclick="checkExtractor.viewDetails('${result.filename}')">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger ms-1" onclick="checkExtractor.deleteResult('${result.filename}')">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            </tr>
        `).join('');
    }

    updateStats() {
        this.processedChecks = this.results.length;
        this.successfulChecks = this.results.filter(r => r.status === 'success').length;
        this.totalAmount = this.results.reduce((sum, r) => sum + (r.amount || 0), 0);

        const successRate = this.processedChecks > 0 ? (this.successfulChecks / this.processedChecks * 100) : 0;

        document.getElementById('processedCount').textContent = this.processedChecks;
        document.getElementById('successRate').textContent = successRate.toFixed(1) + '%';
        document.getElementById('totalAmount').textContent = '$' + this.totalAmount.toLocaleString('en-US', {minimumFractionDigits: 2});

        this.updateRecentActivity();
    }

    updateRecentActivity() {
        const tbody = document.getElementById('recentActivity');
        const recent = this.results.slice(-5).reverse();

        if (recent.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted">No data available</td></tr>';
            return;
        }

        tbody.innerHTML = recent.map(result => `
            <tr>
                <td>${result.checkNumber}</td>
                <td>${result.date}</td>
                <td>${result.amount > 0 ? '$' + result.amount.toFixed(2) : 'N/A'}</td>
                <td><span class="status-badge status-${result.status}">${result.status}</span></td>
                <td>
                    <button class="btn btn-sm btn-outline-primary" onclick="checkExtractor.viewDetails('${result.filename}')">
                        <i class="fas fa-eye"></i>
                    </button>
                </td>
            </tr>
        `).join('');
    }

    viewDetails(filename) {
        const result = this.results.find(r => r.filename === filename);
        if (!result) return;

        alert(`Details for ${filename}:\n\nCheck Number: ${result.checkNumber}\nDate: ${result.date}\nAccount: ${result.accountNumber}\nAmount: $${result.amount}\nPay To: ${result.payTo}\nStatus: ${result.status}`);
    }

    deleteResult(filename) {
        if (confirm('Are you sure you want to delete this result?')) {
            this.results = this.results.filter(r => r.filename !== filename);
            this.updateResultsTable();
            this.updateStats();
        }
    }

    exportData(format) {
        if (this.results.length === 0) {
            alert('No data to export');
            return;
        }

        if (format === 'csv') {
            this.exportCSV();
        } else if (format === 'excel') {
            this.exportExcel();
        }
    }

    exportCSV() {
        const headers = ['Filename', 'Check Number', 'Date', 'Account Number', 'Amount', 'Pay To', 'Status'];
        const csvContent = [
            headers.join(','),
            ...this.results.map(r => [
                r.filename,
                r.checkNumber,
                r.date,
                r.accountNumber,
                r.amount,
                r.payTo,
                r.status
            ].join(','))
        ].join('\n');

        this.downloadFile(csvContent, 'check_extraction_results.csv', 'text/csv');
    }

    exportExcel() {
        // For simplicity, export as CSV with .xlsx extension
        // In a real app, you'd use a library like SheetJS
        this.exportCSV();
        alert('Excel export feature coming soon! CSV file downloaded instead.');
    }

    downloadFile(content, filename, contentType) {
        const a = document.createElement('a');
        const file = new Blob([content], { type: contentType });
        a.href = URL.createObjectURL(file);
        a.download = filename;
        a.click();
        URL.revokeObjectURL(a.href);
    }

    initCharts() {
        // Initialize Chart.js charts
        this.initTrendsChart();
        this.initSuccessChart();
    }

    initTrendsChart() {
        const ctx = document.getElementById('trendsChart');
        if (!ctx) return;

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'Checks Processed',
                    data: [120, 190, 300, 500, 200, 300],
                    borderColor: '#0d6efd',
                    backgroundColor: 'rgba(13, 110, 253, 0.1)',
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    initSuccessChart() {
        const ctx = document.getElementById('successChart');
        if (!ctx) return;

        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Successful', 'Failed'],
                datasets: [{
                    data: [94, 6],
                    backgroundColor: ['#198754', '#dc3545']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }

    loadSampleData() {
        // Load some sample data for demonstration
        const sampleResults = [
            {
                filename: 'sample_check_1.pdf',
                checkNumber: '1001',
                date: '01/15/2024',
                accountNumber: '230995329781824',
                amount: 1250.00,
                payTo: 'John Doe',
                status: 'success',
                timestamp: new Date('2024-01-15').toISOString()
            },
            {
                filename: 'sample_check_2.pdf',
                checkNumber: '1002',
                date: '01/16/2024',
                accountNumber: '445566778899',
                amount: 750.50,
                payTo: 'ABC Corporation',
                status: 'success',
                timestamp: new Date('2024-01-16').toISOString()
            }
        ];

        this.results = sampleResults;
        this.updateResultsTable();
        this.updateStats();
    }
}

// Initialize the application
let checkExtractor;
document.addEventListener('DOMContentLoaded', () => {
    checkExtractor = new CheckExtractorApp();
});

// Export for global access
window.checkExtractor = checkExtractor;
