"""Frontend JavaScript application"""
// Main application entry point

const app = {
    currentUser: null,
    currentTab: 'dashboard',
    queue: [],
    
    async init() {
        console.log('Initializing YouTube Auto Republisher');
        await this.checkAuth();
        this.setupEventListeners();
    },
    
    async checkAuth() {
        try {
            const response = await fetch('/api/auth/status');
            const data = await response.json();
            
            if (data.authenticated) {
                this.currentUser = data.user;
                this.showDashboard();
            } else {
                this.showLogin();
            }
        } catch (error) {
            console.error('Auth check failed:', error);
            this.showLogin();
        }
    },
    
    showLogin() {
        const app = document.getElementById('app');
        app.innerHTML = `
            <div class="flex items-center justify-center min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black">
                <div class="glass p-8 rounded-lg max-w-md w-full mx-4">
                    <h1 class="text-3xl font-bold mb-2 text-center">🎬 YouTube Auto Republisher</h1>
                    <p class="text-center text-gray-400 mb-6">Automatically republish your videos on schedule</p>
                    <a href="/api/auth/login" class="btn-primary w-full text-center py-3 rounded-lg font-semibold">
                        <i class="fab fa-google mr-2"></i>Connect Your YouTube Channel
                    </a>
                    <p class="text-center text-gray-500 text-sm mt-4">Only videos you own or have permission to reuse</p>
                </div>
            </div>
        `;
    },
    
    showDashboard() {
        const app = document.getElementById('app');
        app.innerHTML = `
            <div class="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black">
                <!-- Navigation -->
                <nav class="glass border-b border-gray-700 sticky top-0 z-50">
                    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
                        <div class="flex items-center justify-between">
                            <h1 class="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-green-400">🎬 YouTube Auto Republisher</h1>
                            <div class="flex items-center gap-4">
                                <img src="${this.currentUser.channel_thumbnail}" alt="Channel" class="w-10 h-10 rounded-full" />
                                <span class="text-sm font-medium">${this.currentUser.channel_title}</span>
                                <button class="btn-secondary" onclick="app.logout()">
                                    <i class="fas fa-sign-out-alt mr-2"></i>Logout
                                </button>
                            </div>
                        </div>
                    </div>
                </nav>
                
                <!-- Main Content -->
                <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                    <!-- Tab Navigation -->
                    <div class="flex gap-6 mb-8 border-b border-gray-700">
                        <button class="tab active" onclick="app.switchTab('dashboard')"><i class="fas fa-chart-line mr-2"></i>Dashboard</button>
                        <button class="tab" onclick="app.switchTab('queue')"><i class="fas fa-list mr-2"></i>Queue</button>
                        <button class="tab" onclick="app.switchTab('source')"><i class="fas fa-search mr-2"></i>Find Videos</button>
                        <button class="tab" onclick="app.switchTab('settings')"><i class="fas fa-cog mr-2"></i>Settings</button>
                        <button class="tab" onclick="app.switchTab('logs')"><i class="fas fa-file-alt mr-2"></i>Logs</button>
                    </div>
                    
                    <!-- Dashboard Tab -->
                    <div id="dashboard-tab" class="tab-content">
                        <div class="grid-3">
                            <div class="stat-card">
                                <div class="stat-number" id="queued-count">0</div>
                                <div class="stat-label">Videos in Queue</div>
                            </div>
                            <div class="stat-card">
                                <div class="stat-number" id="uploaded-count">0</div>
                                <div class="stat-label">Uploaded Today</div>
                            </div>
                            <div class="stat-card">
                                <div class="stat-number" id="storage-used">0 GB</div>
                                <div class="stat-label">Storage Used</div>
                            </div>
                        </div>
                        <div class="card mt-8">
                            <h2 class="text-xl font-bold mb-4">Auto-Upload Status</h2>
                            <div class="flex items-center justify-between">
                                <div>
                                    <p class="text-green-400 font-semibold">Next Upload: In 2h 15m</p>
                                    <p class="text-gray-400 text-sm mt-1">Scheduled for 6:45 PM</p>
                                </div>
                                <span class="badge badge-success">Active</span>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Queue Tab -->
                    <div id="queue-tab" class="tab-content hidden">
                        <div class="card">
                            <h2 class="text-xl font-bold mb-4">Upload Queue</h2>
                            <div id="queue-list">
                                <p class="text-gray-400 text-center py-8">No videos in queue. Add some videos to get started!</p>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Source Tab -->
                    <div id="source-tab" class="tab-content hidden">
                        <div class="card">
                            <h2 class="text-xl font-bold mb-4">Find Videos</h2>
                            <div class="flex gap-4 mb-6">
                                <input type="text" id="search-input" class="input-field flex-1" placeholder="Search for videos..." />
                                <button class="btn-primary" onclick="app.searchVideos()"><i class="fas fa-search mr-2"></i>Search</button>
                            </div>
                            <div id="search-results" class="grid-2"></div>
                        </div>
                    </div>
                    
                    <!-- Settings Tab -->
                    <div id="settings-tab" class="tab-content hidden">
                        <div class="card">
                            <h2 class="text-xl font-bold mb-4">Settings</h2>
                            <div class="space-y-6">
                                <div>
                                    <label class="block text-sm font-medium mb-2">Upload Interval (hours)</label>
                                    <input type="number" class="input-field w-full" value="2.5" step="0.5" />
                                </div>
                                <div>
                                    <label class="block text-sm font-medium mb-2">Default Privacy</label>
                                    <select class="input-field w-full">
                                        <option>Private</option>
                                        <option>Unlisted</option>
                                        <option>Public</option>
                                    </select>
                                </div>
                                <div>
                                    <label class="flex items-center">
                                        <input type="checkbox" class="mr-3" checked />
                                        <span class="text-sm font-medium">Enable Auto Upload</span>
                                    </label>
                                </div>
                                <button class="btn-primary w-full"><i class="fas fa-save mr-2"></i>Save Settings</button>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Logs Tab -->
                    <div id="logs-tab" class="tab-content hidden">
                        <div class="card">
                            <h2 class="text-xl font-bold mb-4">Application Logs</h2>
                            <div id="logs-list" class="space-y-2">
                                <p class="text-gray-400 text-center py-8">No logs yet</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        this.loadQueue();
    },
    
    switchTab(tabName) {
        // Hide all tabs
        document.querySelectorAll('.tab-content').forEach(tab => tab.classList.add('hidden'));
        document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
        
        // Show selected tab
        const tabElement = document.getElementById(`${tabName}-tab`);
        if (tabElement) {
            tabElement.classList.remove('hidden');
        }
        
        // Mark tab as active
        event.target.classList.add('active');
        this.currentTab = tabName;
    },
    
    async loadQueue() {
        try {
            const response = await fetch('/api/queue');
            const data = await response.json();
            this.queue = data.queue || [];
            
            const queueList = document.getElementById('queue-list');
            if (this.queue.length === 0) {
                queueList.innerHTML = '<p class="text-gray-400 text-center py-8">No videos in queue</p>';
            } else {
                queueList.innerHTML = this.queue.map((item, index) => `
                    <div class="list-item">
                        <div>
                            <p class="font-semibold">${item.title}</p>
                            <p class="text-sm text-gray-400">Position #${index + 1} • ${item.status}</p>
                        </div>
                        <div class="flex gap-2">
                            <button class="btn-secondary" onclick="app.removeFromQueue(${item.id})"><i class="fas fa-trash"></i></button>
                        </div>
                    </div>
                `).join('');
            }
            
            document.getElementById('queued-count').textContent = this.queue.length;
        } catch (error) {
            console.error('Failed to load queue:', error);
        }
    },
    
    async searchVideos() {
        const query = document.getElementById('search-input').value;
        if (!query) return;
        
        try {
            const response = await fetch('/api/videos/search', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query })
            });
            const data = await response.json();
            
            const results = document.getElementById('search-results');
            results.innerHTML = (data.videos || []).map(video => `
                <div class="card">
                    <img src="${video.thumbnail_url}" alt="${video.title}" class="w-full h-40 object-cover rounded mb-3" />
                    <p class="font-semibold text-sm">${video.title}</p>
                    <button class="btn-primary w-full mt-3" onclick="app.addToQueue(${video.id})">Add to Queue</button>
                </div>
            `).join('');
        } catch (error) {
            console.error('Search failed:', error);
        }
    },
    
    async addToQueue(videoId) {
        try {
            const response = await fetch('/api/queue', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ video_id: videoId })
            });
            
            if (response.ok) {
                this.showToast('Video added to queue', 'success');
                await this.loadQueue();
            }
        } catch (error) {
            console.error('Failed to add video:', error);
            this.showToast('Failed to add video', 'error');
        }
    },
    
    async removeFromQueue(itemId) {
        try {
            const response = await fetch(`/api/queue/${itemId}`, { method: 'DELETE' });
            if (response.ok) {
                this.showToast('Video removed from queue', 'success');
                await this.loadQueue();
            }
        } catch (error) {
            console.error('Failed to remove video:', error);
        }
    },
    
    async logout() {
        try {
            await fetch('/api/auth/logout', { method: 'POST' });
            location.reload();
        } catch (error) {
            console.error('Logout failed:', error);
        }
    },
    
    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast badge badge-${type}`;
        toast.textContent = message;
        document.body.appendChild(toast);
        
        setTimeout(() => toast.remove(), 3000);
    },
    
    setupEventListeners() {
        // Add any additional event listeners here
    }
};

// Initialize app when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => app.init());
} else {
    app.init();
}
