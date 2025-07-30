/**
 * AlgoCratic Futures - Employee Portal Client
 * "Your value is measured in output"
 */

class EmployeePortal {
    constructor() {
        this.ws = null;
        this.employeeId = this.generateEmployeeId();
        this.clearanceLevel = 'R'; // Start as Red/Newbie
        this.metrics = {
            productivity: 0,
            loyalty: 0,
            compliance: 100,
            algorithm: 0
        };
        
        // Terminal command history
        this.commandHistory = [];
        this.historyIndex = -1;
        
        // Initialize after DOM loads
        this.init();
    }
    
    generateEmployeeId() {
        return `EMP-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    }
    
    init() {
        // Hide loading screen after initialization
        setTimeout(() => {
            document.getElementById('loadingScreen').style.display = 'none';
            this.connectWebSocket();
            this.setupTerminal();
            this.startMetricsAnimation();
            this.addSurveillanceEntry('[SYSTEM] Employee ' + this.employeeId + ' logged in');
        }, 2500);
    }
    
    connectWebSocket() {
        this.ws = new WebSocket(`ws://localhost:8000/ws/${this.employeeId}`);
        
        this.ws.onopen = () => {
            this.updateClearanceBadge(this.clearanceLevel);
            this.addTerminalLine('Connected to AlgoCratic Futures corporate network');
            this.addTerminalLine('Type "help" for available commands');
        };
        
        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleServerMessage(data);
        };
        
        this.ws.onerror = () => {
            this.addTerminalLine('[ERROR] Connection to corporate network failed', 'error');
        };
        
        this.ws.onclose = () => {
            this.addTerminalLine('[ALERT] Disconnected from corporate network', 'alert');
            this.addSurveillanceEntry('[SYSTEM] Employee disconnected - productivity terminated');
        };
    }
    
    handleServerMessage(data) {
        switch(data.type) {
            case 'corporate_motivation':
                this.addSurveillanceEntry(`[CORP] ${data.message}`);
                break;
            case 'clearance_update':
                this.updateClearanceBadge(data.clearance);
                break;
            case 'metrics_update':
                this.updateMetrics(data.metrics);
                break;
            case 'surveillance_alert':
                this.addSurveillanceEntry(data.message, 'alert');
                break;
            case 'terminal_response':
                this.addTerminalLine(data.message);
                break;
            default:
                console.log('Unknown message type:', data);
        }
    }
    
    setupTerminal() {
        const input = document.getElementById('terminalInput');
        const terminal = document.getElementById('terminal');
        
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                this.executeCommand(input.value);
                input.value = '';
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                if (this.historyIndex > 0) {
                    this.historyIndex--;
                    input.value = this.commandHistory[this.historyIndex];
                }
            } else if (e.key === 'ArrowDown') {
                e.preventDefault();
                if (this.historyIndex < this.commandHistory.length - 1) {
                    this.historyIndex++;
                    input.value = this.commandHistory[this.historyIndex];
                } else {
                    this.historyIndex = this.commandHistory.length;
                    input.value = '';
                }
            }
        });
        
        // Keep terminal scrolled to bottom
        terminal.addEventListener('DOMNodeInserted', () => {
            terminal.scrollTop = terminal.scrollHeight;
        });
    }
    
    executeCommand(command) {
        if (!command.trim()) return;
        
        this.commandHistory.push(command);
        this.historyIndex = this.commandHistory.length;
        
        this.addTerminalLine(`> ${command}`, 'command');
        
        // Send keystroke telemetry
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify({
                type: 'keystroke_telemetry',
                command: command,
                timestamp: new Date().toISOString()
            }));
        }
        
        // Process commands locally first
        this.processCommand(command.toLowerCase().trim());
    }
    
    processCommand(command) {
        const commands = {
            'help': () => {
                this.addTerminalLine('Available commands:');
                this.addTerminalLine('  help              - Show this message');
                this.addTerminalLine('  status            - Display employee metrics');
                this.addTerminalLine('  clearance         - Show current clearance level');
                this.addTerminalLine('  report <id>       - File surveillance report on employee');
                this.addTerminalLine('  productivity      - Display productivity dashboard');
                this.addTerminalLine('  @channel <msg>    - Send message to corporate channel');
                this.addTerminalLine('  clock in/out      - Record work hours');
                this.addTerminalLine('  request promotion - Apply for clearance advancement');
            },
            
            'status': () => {
                this.addTerminalLine('=== EMPLOYEE STATUS REPORT ===');
                this.addTerminalLine(`Employee ID: ${this.employeeId}`);
                this.addTerminalLine(`Clearance: ${this.getClearanceName()}`);
                this.addTerminalLine(`Productivity: ${this.metrics.productivity}%`);
                this.addTerminalLine(`Loyalty Index: ${this.metrics.loyalty}%`);
                this.addTerminalLine(`Compliance: ${this.metrics.compliance}%`);
                this.addTerminalLine(`Algorithmic Score: ${this.metrics.algorithm}%`);
            },
            
            'clearance': () => {
                this.addTerminalLine(`Current clearance level: ${this.getClearanceName()}`);
                this.addTerminalLine('Next level requires increased productivity and loyalty metrics');
            },
            
            'clock in': () => {
                this.addTerminalLine('[SUCCESS] Clocked in. Your time is now corporate property.');
                this.updateMetric('productivity', 5);
                this.addSurveillanceEntry(`[CLOCK] Employee ${this.employeeId} began productivity cycle`);
            },
            
            'clock out': () => {
                this.addTerminalLine('[WARNING] Early departure noted in permanent record.');
                this.updateMetric('productivity', -10);
                this.updateMetric('loyalty', -5);
            },
            
            'request promotion': () => {
                if (this.metrics.productivity < 70 || this.metrics.loyalty < 60) {
                    this.addTerminalLine('[DENIED] Insufficient metrics for advancement');
                    this.addTerminalLine('Required: Productivity > 70%, Loyalty > 60%');
                } else {
                    this.addTerminalLine('[PROCESSING] Clearance advancement request submitted');
                    this.addTerminalLine('Algorithmic review will complete in 72 hours');
                    this.showCorporateMessage('PROMOTION REQUEST RECEIVED', 
                        'Your dedication to the algorithm has been noted. Continue to maintain optimal productivity.');
                }
            }
        };
        
        // Check for special Sweeney mode
        if (command === 'sweeney mode') {
            const hour = new Date().getHours();
            if (hour >= 2 && hour <= 5) {
                this.addTerminalLine('[SWEENEY MODE ACTIVATED]');
                this.addTerminalLine('Coffee levels critical. Reality.exe has stopped responding.');
                document.body.style.filter = 'hue-rotate(180deg)';
                setTimeout(() => {
                    document.body.style.filter = '';
                }, 5000);
            } else {
                this.addTerminalLine('[ERROR] Sweeney mode only available between 2-5 AM');
            }
            return;
        }
        
        // Handle report command
        if (command.startsWith('report ')) {
            const targetId = command.substring(7);
            this.fileReport(targetId);
            return;
        }
        
        // Handle channel messages
        if (command.startsWith('@channel ')) {
            const message = command.substring(9);
            this.sendChannelMessage(message);
            return;
        }
        
        // Execute command or show error
        const cmd = commands[command];
        if (cmd) {
            cmd();
        } else {
            this.addTerminalLine(`[ERROR] Unknown command: ${command}`);
            this.addTerminalLine('Type "help" for available commands');
            this.updateMetric('compliance', -2);
        }
    }
    
    fileReport(targetId) {
        this.addTerminalLine(`[SURVEILLANCE] Filing report on employee ${targetId}`);
        this.addTerminalLine('Rate the following metrics (0-100):');
        // In a real implementation, this would open a form
        this.addTerminalLine('[SUCCESS] Report filed. Loyalty index increased.');
        this.updateMetric('loyalty', 10);
        this.addSurveillanceEntry(`[REPORT] ${this.employeeId} filed surveillance report`);
    }
    
    sendChannelMessage(message) {
        this.addTerminalLine(`[@channel] ${message}`);
        this.addSurveillanceEntry(`[CHANNEL] ${this.employeeId}: ${message}`);
        this.updateMetric('loyalty', 2);
    }
    
    getClearanceName() {
        const names = {
            'R': 'RED (Probationary)',
            'O': 'ORANGE (Standard)',
            'Y': 'YELLOW (Trusted)',
            'G': 'GREEN (Management Track)',
            'B': 'BLUE (Architect)',
            'I': 'INDIGO (Executive)',
            'V': 'VIOLET (Board Member)',
            'UV': 'ULTRAVIOLET (The Algorithm)'
        };
        return names[this.clearanceLevel] || 'UNKNOWN';
    }
    
    updateClearanceBadge(level) {
        this.clearanceLevel = level;
        const badge = document.getElementById('clearanceBadge');
        const levelSpan = document.getElementById('clearanceLevel');
        
        badge.className = `clearance-badge clearance-${level}`;
        levelSpan.textContent = level;
    }
    
    updateMetric(metric, delta) {
        this.metrics[metric] = Math.max(0, Math.min(100, this.metrics[metric] + delta));
        this.animateMetricBar(metric, this.metrics[metric]);
    }
    
    updateMetrics(metrics) {
        Object.keys(metrics).forEach(key => {
            if (this.metrics.hasOwnProperty(key)) {
                this.metrics[key] = metrics[key];
                this.animateMetricBar(key, metrics[key]);
            }
        });
    }
    
    animateMetricBar(metric, value) {
        const bar = document.getElementById(`${metric}Bar`);
        const valueSpan = document.getElementById(`${metric}Value`);
        
        if (bar && valueSpan) {
            bar.style.width = `${value}%`;
            valueSpan.textContent = `${value}%`;
            
            // Change color based on value
            if (value < 30) {
                bar.style.background = 'linear-gradient(90deg, #D32F2F 0%, #F44336 100%)';
            } else if (value < 70) {
                bar.style.background = 'linear-gradient(90deg, #FFA000 0%, #FFC107 100%)';
            } else {
                bar.style.background = 'linear-gradient(90deg, #00E676 0%, #00C853 100%)';
            }
        }
    }
    
    startMetricsAnimation() {
        // Simulate gradual metric changes
        setInterval(() => {
            // Productivity slowly increases if "working"
            if (Math.random() > 0.7) {
                this.updateMetric('productivity', Math.random() * 3);
            }
            
            // Compliance slowly decreases (nobody's perfect)
            if (Math.random() > 0.8) {
                this.updateMetric('compliance', -1);
            }
            
            // Random algorithmic scoring
            if (Math.random() > 0.9) {
                this.updateMetric('algorithm', Math.random() * 5 - 2);
            }
        }, 5000);
    }
    
    addTerminalLine(text, className = '') {
        const output = document.getElementById('terminalOutput');
        const line = document.createElement('div');
        line.className = `terminal-line ${className}`;
        line.textContent = text;
        output.appendChild(line);
    }
    
    addSurveillanceEntry(text, type = '') {
        const feed = document.getElementById('surveillanceFeed');
        const entry = document.createElement('div');
        entry.className = `surveillance-entry ${type}`;
        entry.textContent = `[${new Date().toLocaleTimeString()}] ${text}`;
        feed.appendChild(entry);
        
        // Keep only last 20 entries
        while (feed.children.length > 20) {
            feed.removeChild(feed.firstChild);
        }
        
        feed.scrollTop = feed.scrollHeight;
    }
    
    showCorporateMessage(title, content) {
        const modal = document.getElementById('corporateMessage');
        document.getElementById('messageTitle').textContent = title;
        document.getElementById('messageContent').textContent = content;
        modal.style.display = 'block';
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            this.dismissMessage();
        }, 5000);
    }
    
    dismissMessage() {
        document.getElementById('corporateMessage').style.display = 'none';
    }
}

// Global function for message dismissal
function dismissMessage() {
    document.getElementById('corporateMessage').style.display = 'none';
}

// Initialize portal when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.portal = new EmployeePortal();
});