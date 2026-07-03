/**
 * YouTube Auto Republisher - Frontend App
 * Main application logic
 */

const API_BASE = '/api';
let currentUser = null;
let videos = [];
let queue = [];
let uploadTasks = [];

/**
 * Initialize application
 */
document.addEventListener('DOMContentLoaded', async () => {
    console.log('App initializing...');
    await checkAuthStatus();
    loadSettings();
    setupEventListeners();
    startRefreshInterval();
});

/**
 * Check authentication status
 */
async function checkAuthStatus() {
    try {
        const response = await fetch(`${API_BASE}/auth/status`);
        const data = await response.json();
        
        if (data.authenticated && data.user) {
            currentUser = data.user;
            showDashboard();
            await loadQueue();
            await loadStats();
        } else {
            showLoginScreen();
        }
    } catch (error) {
        console.error('Auth check failed:', error);
        showLoginScreen();
    }
}

/**
 * Show dashboard
 */
function showDashboard() {
    document.getElementById('loginScreen').classList.add('hidden');
    document.getElementById('dashboard').classList.remove('hidden');
    document.getElementById('loginBtn').classList.add('hidden');
    document.getElementById('userInfo').classList.remove('hidden');
    
    document.getElementById('userName').textContent = currentUser.channel_title;
    document.getElementById('userAvatar').src = currentUser.channel_thumbnail;
}

/**
 * Show login screen
 */
function showLoginScreen() {
    document.getElementById('loginScreen').classList.remove('hidden');
    document.getElementById('dashboard').classList.add('hidden');
    document.getElementById('loginBtn').classList.remove('hidden');
    document.getElementById('userInfo').classList.add('hidden');
}

/**
 * Connect to YouTube
 */
async function connectYouTube() {
    try {
        const response = await fetch(`${API_BASE}/auth/login`);
        const data = await response.json();
        
        if (data.success) {
            window.location.href = data.authorization_url;
        }
    } catch (error) {
        showToast('Failed to connect to YouTube', 'error');
        console.error('Connection failed:', error);
    }
}

/**
 * Logout
 */
async function logout() {
    try {
        await fetch(`${API_BASE}/auth/logout`, { method: 'POST' });
        currentUser = null;
        showLoginScreen();
        showToast('Logged out successfully', 'success');
    } catch (error) {
        showToast('Logout failed', 'error');
    }
}

/**
 * Load queue
 */
async function loadQueue() {
    try {
        const response = await fetch(`${API_BASE}/queue`);
        const data = await response.json();
        
        queue = data.queue || [];
        document.getElementById('queueCount').textContent = queue.length;
        
        renderQueue();
    } catch (error) {
        console.error('Failed to load queue:', error);
    }
}

/**
 * Render queue
 */
function renderQueue() {
    const queueList = document.getElementById('queueList');
    
    if (queue.length === 0) {
        queueList.innerHTML = `
            <div class="text-center py-12 text-gray-400">
                <i class="fas fa-inbox text-4xl mb-4"></i>
                <p>No items in queue</p>
            </div>
        `;
        return;
    }
    
    queueList.innerHTML = queue.map((item, index) => `
        <div class="glass-card p-4 rounded-lg animate-slide-in" style="animation-delay: ${index * 50}ms">
            <div class="flex items-start space-x-4">
                <img src="${item.thumbnail_url}" alt="${item.title}" class="w-24 h-16 rounded object-cover">
                <div class="flex-1">
                    <div class="flex items-start justify-between mb-2">
                        <div>
                            <h3 class="font-semibold line-clamp-2">${item.title}</h3>
                            <p class="text-gray-400 text-sm">Position: ${item.position}</p>
                        </div>
                        <span class="badge ${getStatusBadgeClass(item.status)}">${item.status}</span>
                    </div>
                    
                    <div class="flex items-center space-x-3 text-sm text-gray-400 mb-3">
                        <span><i class="fas fa-lock-alt mr-1"></i>${item.privacy}</span>
                        <span><i class="fas fa-redo mr-1"></i>Retries: ${item.retry_count}</span>
                    </div>
                    
                    <div class="progress-bar">
                        <div class="progress-bar-fill" style="width: ${item.progress_percent || 0}%"></div>
                    </div>
                    
                    <div class="flex space-x-2 mt-3">
                        <button onclick="editQueueItem(${item.id})" class="px-3 py-1 bg-blue-500/20 hover:bg-blue-500/40 text-blue-300 rounded text-sm transition">
                            <i class="fas fa-edit mr-1"></i>Edit
                        </button>
                        <button onclick="deleteQueueItem(${item.id})" class="px-3 py-1 bg-red-500/20 hover:bg-red-500/40 text-red-300 rounded text-sm transition">
                            <i class="fas fa-trash mr-1"></i>Delete
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `).join('');
}

/**
 * Get status badge class
 */
function getStatusBadgeClass(status) {
    const classes = {
        'pending': 'badge-info',
        'downloading': 'badge-warning',
        'queued': 'badge-info',
        'uploading': 'badge-warning',
        'completed': 'badge-success',
        'failed': 'badge-error'
    };
    return classes[status] || 'badge-info';
}

/**
 * Load statistics
 */
async function loadStats() {
    try {
        const response = await fetch(`${API_BASE}/queue`);
        const data = await response.json();
        
        const stats = {
            queue: data.count || 0,
            downloaded: data.queue?.filter(q => q.local_file_path).length || 0,
            uploaded: data.queue?.filter(q => q.status === 'completed').length || 0
        };
        
        document.getElementById('queueCount').textContent = stats.queue;
        document.getElementById('downloadedCount').textContent = stats.downloaded;
        document.getElementById('uploadedCount').textContent = stats.uploaded;
    } catch (error) {
        console.error('Failed to load stats:', error);
    }
}

/**
 * Search videos
 */
async function searchVideos() {
    const input = document.getElementById('searchInput');
    const query = input.value.trim();
    
    if (!query) {
        showToast('Please enter a search query', 'warning');
        return;
    }
    
    try {
        const sourceType = document.querySelector('input[name="source"]:checked').value;
        
        if (sourceType === 'channel') {
            const response = await fetch(`${API_BASE}/videos/list?max_results=50`);
            const data = await response.json();
            videos = data.videos || [];
        } else {
            const urls = query.split(',').map(url => url.trim());
            // Download videos from URLs
            for (const url of urls) {
                await downloadVideoFromUrl(url);
            }
        }
        
        renderVideosGrid();
    } catch (error) {
        showToast('Search failed', 'error');
        console.error('Search error:', error);
    }
}

/**
 * Render videos grid
 */
function renderVideosGrid() {
    const videosList = document.getElementById('videosList');
    
    if (videos.length === 0) {
        videosList.innerHTML = `
            <div class="text-center py-12 text-gray-400">
                <i class="fas fa-film text-4xl mb-4"></i>
                <p>No videos found</p>
            </div>
        `;
        return;
    }
    
    videosList.innerHTML = videos.map((video, index) => `
        <div class="glass-card rounded-lg overflow-hidden animate-slide-in" style="animation-delay: ${index * 50}ms">
            <img src="${video.thumbnail_url}" alt="${video.title}" class="w-full h-32 object-cover">
            <div class="p-4">
                <h3 class="font-semibold line-clamp-2 mb-2">${video.title}</h3>
                <p class="text-sm text-gray-400 line-clamp-2 mb-3">${video.description || 'No description'}</p>
                <button onclick="addToQueue(${video.id})" class="w-full px-4 py-2 bg-gradient-to-r from-pink-500 to-purple-500 hover:from-pink-600 hover:to-purple-600 rounded font-semibold transition">
                    <i class="fas fa-plus mr-2"></i>Add to Queue
                </button>
            </div>
        </div>
    `).join('');
}

/**
 * Add video to queue
 */
async function addToQueue(videoId) {
    try {
        const response = await fetch(`${API_BASE}/queue`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ video_id: videoId })
        });
        
        const data = await response.json();
        if (data.success) {
            showToast('Video added to queue', 'success');
            await loadQueue();
        } else {
            showToast(data.error || 'Failed to add to queue', 'error');
        }
    } catch (error) {
        showToast('Add to queue failed', 'error');
        console.error('Error:', error);
    }
}

/**
 * Delete queue item
 */
async function deleteQueueItem(queueItemId) {
    if (!confirm('Are you sure?')) return;
    
    try {
        const response = await fetch(`${API_BASE}/queue/${queueItemId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showToast('Removed from queue', 'success');
            await loadQueue();
        }
    } catch (error) {
        showToast('Delete failed', 'error');
    }
}

/**
 * Load settings
 */
async function loadSettings() {
    try {
        const response = await fetch(`${API_BASE}/settings`);
        const data = await response.json();
        
        if (data.success) {
            const settings = data.settings;
            document.getElementById('uploadInterval').value = settings.upload_interval_hours;
            document.getElementById('maxRetries').value = settings.max_retries;
            document.getElementById('defaultPrivacy').value = settings.default_privacy;
            document.getElementById('videoQuality').value = settings.video_quality;
            document.getElementById('autoSchedule').checked = settings.auto_schedule;
        }
    } catch (error) {
        console.error('Failed to load settings:', error);
    }
}

/**
 * Save settings
 */
async function saveSettings(e) {
    e.preventDefault();
    
    const settings = {
        upload_interval_hours: parseFloat(document.getElementById('uploadInterval').value),
        max_retries: parseInt(document.getElementById('maxRetries').value),
        default_privacy: document.getElementById('defaultPrivacy').value,
        video_quality: document.getElementById('videoQuality').value,
        auto_schedule: document.getElementById('autoSchedule').checked
    };
    
    try {
        const response = await fetch(`${API_BASE}/settings`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(settings)
        });
        
        const data = await response.json();
        if (data.success) {
            showToast('Settings saved successfully', 'success');
        } else {
            showToast('Failed to save settings', 'error');
        }
    } catch (error) {
        showToast('Save failed', 'error');
    }
}

/**
 * Load logs
 */
async function loadLogs() {
    try {
        const logType = document.getElementById('logTypeFilter').value;
        let url = `${API_BASE}/logs`;
        if (logType) url += `?type=${logType}`;
        
        const response = await fetch(url);
        const data = await response.json();
        
        const logsList = document.getElementById('logsList');
        if (data.logs.length === 0) {
            logsList.innerHTML = `
                <div class="text-center py-12 text-gray-400">
                    <i class="fas fa-inbox text-4xl mb-4"></i>
                    <p>No logs</p>
                </div>
            `;
            return;
        }
        
        logsList.innerHTML = data.logs.map(log => `
            <div class="glass-card p-3 rounded text-sm">
                <div class="flex items-start justify-between">
                    <div>
                        <p class="font-semibold">${log.message}</p>
                        <p class="text-gray-400 text-xs mt-1">${new Date(log.created_at).toLocaleString()}</p>
                    </div>
                    <span class="badge ${getLogLevelBadgeClass(log.level)}">${log.level}</span>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Failed to load logs:', error);
    }
}

/**
 * Get log level badge class
 */
function getLogLevelBadgeClass(level) {
    const classes = {
        'INFO': 'badge-info',
        'WARNING': 'badge-warning',
        'ERROR': 'badge-error',
        'DEBUG': 'badge-info'
    };
    return classes[level] || 'badge-info';
}

/**
 * Clear old logs
 */
async function clearLogs() {
    if (!confirm('Are you sure? This will delete logs older than 30 days.')) return;
    
    try {
        const response = await fetch(`${API_BASE}/logs/clear`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ days: 30 })
        });
        
        const data = await response.json();
        if (data.success) {
            showToast('Logs cleared', 'success');
            await loadLogs();
        }
    } catch (error) {
        showToast('Clear failed', 'error');
    }
}

/**
 * Show tab
 */
function showTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => tab.classList.add('hidden'));
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    
    // Show selected tab
    document.getElementById(tabName + 'Tab').classList.remove('hidden');
    event.target.closest('.tab-btn').classList.add('active');
    
    // Load data for specific tabs
    if (tabName === 'logs') {
        loadLogs();
    }
}

/**
 * Show toast notification
 */
function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    
    const bgClass = {
        'success': 'bg-green-500/20 border-green-500/50 text-green-300',
        'error': 'bg-red-500/20 border-red-500/50 text-red-300',
        'warning': 'bg-yellow-500/20 border-yellow-500/50 text-yellow-300',
        'info': 'bg-blue-500/20 border-blue-500/50 text-blue-300'
    }[type];
    
    const icon = {
        'success': 'fa-check-circle',
        'error': 'fa-exclamation-circle',
        'warning': 'fa-exclamation-triangle',
        'info': 'fa-info-circle'
    }[type];
    
    toast.className = `glass-card border p-4 rounded-lg animate-slide-in ${bgClass}`;
    toast.innerHTML = `
        <div class="flex items-center">
            <i class="fas ${icon} mr-3"></i>
            <span>${message}</span>
        </div>
    `;
    
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
    // Settings form
    document.getElementById('settingsForm')?.addEventListener('submit', saveSettings);
    
    // Source type change
    document.querySelectorAll('input[name="source"]').forEach(radio => {
        radio.addEventListener('change', () => {
            const label = document.getElementById('searchLabel');
            const input = document.getElementById('searchInput');
            
            if (radio.value === 'channel') {
                label.textContent = 'Search Videos';
                input.placeholder = 'Enter search query...';
            } else {
                label.textContent = 'Video URLs';
                input.placeholder = 'Enter video URLs (comma-separated)...';
            }
        });
    });
}

/**
 * Start refresh interval
 */
function startRefreshInterval() {
    // Refresh queue every 10 seconds
    setInterval(() => {
        if (currentUser) {
            loadQueue();
            loadStats();
        }
    }, 10000);
}

/**
 * Download video from URL
 */
async function downloadVideoFromUrl(url) {
    try {
        const response = await fetch(`${API_BASE}/videos/download`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                url: url,
                video_id: url.split('v=')[1] || url.split('youtu.be/')[1],
                quality: document.getElementById('videoQuality').value
            })
        });
        
        const data = await response.json();
        if (data.success) {
            showToast(`Video downloaded: ${data.title}`, 'success');
        }
    } catch (error) {
        console.error('Download error:', error);
    }
}