// 聊天界面JavaScript
let currentFile = null;
let conversationHistory = [];

// DOM元素
const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const sendMessageBtn = document.getElementById('sendMessage');
const attachFileBtn = document.getElementById('attachFile');
const fileInput = document.getElementById('fileInput');
const uploadArea = document.getElementById('uploadArea');
const uploadedFiles = document.getElementById('uploadedFiles');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const removeFileBtn = document.getElementById('removeFile');
const clearChatBtn = document.getElementById('clearChat');
const charCount = document.getElementById('charCount');
const typingIndicator = document.getElementById('typingIndicator');
const loadingOverlay = document.getElementById('loadingOverlay');

// 初始化
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    initializeUI();
});

// 初始化事件监听器
function initializeEventListeners() {
    // 消息输入
    messageInput.addEventListener('input', handleMessageInput);
    messageInput.addEventListener('keydown', handleKeyDown);
    sendMessageBtn.addEventListener('click', sendMessage);
    
    // 文件上传
    attachFileBtn.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', handleFileSelect);
    removeFileBtn.addEventListener('click', removeFile);
    
    // 拖拽上传
    uploadArea.addEventListener('click', () => fileInput.click());
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
    
    // 其他功能
    clearChatBtn.addEventListener('click', clearChat);
}

// 初始化UI
function initializeUI() {
    updateSendButton();
    updateCharCount();
}

// 处理消息输入
function handleMessageInput() {
    updateSendButton();
    updateCharCount();
    autoResizeTextarea();
}

// 处理键盘事件
function handleKeyDown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

// 更新发送按钮状态
function updateSendButton() {
    const hasText = messageInput.value.trim().length > 0;
    sendMessageBtn.disabled = !hasText;
}

// 更新字符计数
function updateCharCount() {
    const count = messageInput.value.length;
    charCount.textContent = `${count}/2000`;
    
    if (count > 1800) {
        charCount.style.color = '#e74c3c';
    } else if (count > 1500) {
        charCount.style.color = '#f39c12';
    } else {
        charCount.style.color = '#6c757d';
    }
}

// 自动调整文本框高度
function autoResizeTextarea() {
    messageInput.style.height = 'auto';
    messageInput.style.height = Math.min(messageInput.scrollHeight, 120) + 'px';
}

// 发送消息
async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;
    
    // 添加用户消息到界面
    addMessageToUI('user', message);
    
    // 清空输入框
    messageInput.value = '';
    updateSendButton();
    updateCharCount();
    autoResizeTextarea();
    
    // 显示加载状态
    showTypingIndicator();
    
    try {
        // 发送到后端
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                file: currentFile ? {
                    name: currentFile.name,
                    size: currentFile.size,
                    type: currentFile.type
                } : null,
                conversation_history: conversationHistory
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // 添加AI回复到界面
            addMessageToUI('assistant', data.response);
            
            // 更新对话历史
            conversationHistory.push(
                { role: 'user', content: message },
                { role: 'assistant', content: data.response }
            );
        } else {
            // 显示错误消息
            addMessageToUI('assistant', `抱歉，处理您的请求时出现了错误：${data.error}`);
        }
    } catch (error) {
        console.error('发送消息失败:', error);
        addMessageToUI('assistant', '抱歉，网络连接出现问题，请稍后重试。');
    } finally {
        hideTypingIndicator();
    }
}

// 添加消息到界面
function addMessageToUI(role, content) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}-message`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.innerHTML = role === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    
    const messageText = document.createElement('div');
    messageText.className = 'message-text';
    messageText.textContent = content;
    
    const messageTime = document.createElement('div');
    messageTime.className = 'message-time';
    messageTime.textContent = getCurrentTime();
    
    messageContent.appendChild(messageText);
    messageContent.appendChild(messageTime);
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(messageContent);
    
    chatMessages.appendChild(messageDiv);
    
    // 滚动到底部
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// 获取当前时间
function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString('zh-CN', { 
        hour: '2-digit', 
        minute: '2-digit' 
    });
}

// 显示打字指示器
function showTypingIndicator() {
    typingIndicator.style.display = 'flex';
}

// 隐藏打字指示器
function hideTypingIndicator() {
    typingIndicator.style.display = 'none';
}

// 处理文件选择
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        validateAndSetFile(file);
    }
}

// 处理拖拽
function handleDragOver(event) {
    event.preventDefault();
    uploadArea.classList.add('dragover');
}

function handleDragLeave(event) {
    event.preventDefault();
    uploadArea.classList.remove('dragover');
}

function handleDrop(event) {
    event.preventDefault();
    uploadArea.classList.remove('dragover');
    
    const files = event.dataTransfer.files;
    if (files.length > 0) {
        validateAndSetFile(files[0]);
    }
}

// 验证并设置文件
function validateAndSetFile(file) {
    // 检查文件类型
    const allowedTypes = [
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/msword'
    ];
    
    if (!allowedTypes.includes(file.type)) {
        alert('请选择Word文档文件（.docx 或 .doc）');
        return;
    }
    
    // 检查文件大小（10MB限制）
    const maxSize = 10 * 1024 * 1024;
    if (file.size > maxSize) {
        alert('文件大小不能超过10MB');
        return;
    }
    
    // 设置当前文件
    currentFile = file;
    
    // 显示文件信息
    fileName.textContent = file.name;
    fileSize.textContent = formatFileSize(file.size);
    uploadedFiles.style.display = 'block';
    
    // 添加文件上传消息
    addMessageToUI('user', `已上传文件：${file.name}`);
    
    console.log('文件已选择:', file);
}

// 移除文件
function removeFile() {
    currentFile = null;
    uploadedFiles.style.display = 'none';
    fileInput.value = '';
    
    addMessageToUI('user', '已移除文件');
}

// 格式化文件大小
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// 清空对话
function clearChat() {
    if (confirm('确定要清空所有对话吗？')) {
        // 清空消息区域，只保留欢迎消息
        chatMessages.innerHTML = `
            <div class="message assistant-message">
                <div class="message-avatar">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="message-content">
                    <div class="message-text">
                        你好！我是AI文档助手。你可以上传Word文档，我会帮你分析文档内容并回答相关问题。
                    </div>
                    <div class="message-time">刚刚</div>
                </div>
            </div>
        `;
        
        // 清空对话历史
        conversationHistory = [];
        
        // 移除文件
        removeFile();
        
        console.log('对话已清空');
    }
}

// 显示加载覆盖层
function showLoadingOverlay() {
    loadingOverlay.style.display = 'flex';
}

// 隐藏加载覆盖层
function hideLoadingOverlay() {
    loadingOverlay.style.display = 'none';
}

// 工具函数：防抖
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// 工具函数：节流
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}

// 导出函数供其他模块使用
window.ChatInterface = {
    addMessage: addMessageToUI,
    clearChat: clearChat,
    showLoading: showLoadingOverlay,
    hideLoading: hideLoadingOverlay
};