// 全局变量
let selectedFile = null;
let currentTaskId = null;
let currentFileId = null;
let progressInterval = null;

// DOM元素（延迟初始化）
let uploadArea, fileInput, selectFileBtn, fileInfo, fileName, fileSize;
let removeFileBtn, processBtn, progressSection, resultSection, errorSection;
let previewModal, closePreviewModal;

// 初始化
document.addEventListener('DOMContentLoaded', function() {
    initializeDOMElements();
    initializeEventListeners();
    initializeUI();
    loadTemplates();
});

// 初始化DOM元素
function initializeDOMElements() {
    uploadArea = document.getElementById('uploadArea');
    fileInput = document.getElementById('fileInput');
    selectFileBtn = document.getElementById('selectFileBtn');
    fileInfo = document.getElementById('fileInfo');
    fileName = document.getElementById('fileName');
    fileSize = document.getElementById('fileSize');
    removeFileBtn = document.getElementById('removeFileBtn');
    processBtn = document.getElementById('processBtn');
    progressSection = document.getElementById('progressSection');
    resultSection = document.getElementById('resultSection');
    errorSection = document.getElementById('errorSection');
    previewModal = document.getElementById('previewModal');
    closePreviewModal = document.getElementById('closePreviewModal');
    
    // 检查关键元素是否存在
    if (!selectFileBtn) {
        console.error('selectFileBtn 元素未找到');
    }
    if (!fileInput) {
        console.error('fileInput 元素未找到');
    }
}

// 初始化事件监听器
function initializeEventListeners() {
    // 文件选择相关
    if (selectFileBtn && fileInput) {
        selectFileBtn.addEventListener('click', () => {
            console.log('选择文件按钮被点击');
            fileInput.click();
        });
        fileInput.addEventListener('change', handleFileSelect);
    } else {
        console.error('文件选择相关元素未找到');
    }
    
    if (removeFileBtn) {
        removeFileBtn.addEventListener('click', removeFile);
    }
    
    // 拖拽上传
    if (uploadArea) {
        uploadArea.addEventListener('dragover', handleDragOver);
        uploadArea.addEventListener('dragleave', handleDragLeave);
        uploadArea.addEventListener('drop', handleDrop);
    }
    
    // 处理按钮
    if (processBtn) {
        processBtn.addEventListener('click', startProcessing);
    }
    
    // 模态框相关
    if (closePreviewModal) {
        closePreviewModal.addEventListener('click', function() {
            closePreviewModalFunction();
        });
    }
    
    const closePreviewBtn = document.getElementById('closePreviewBtn');
    if (closePreviewBtn) {
        closePreviewBtn.addEventListener('click', closePreviewModalFunction);
    }
    
    const downloadFromPreviewBtn = document.getElementById('downloadFromPreviewBtn');
    if (downloadFromPreviewBtn) {
        downloadFromPreviewBtn.addEventListener('click', downloadFile);
    }
    
    // 结果页面按钮
    const downloadBtn = document.getElementById('downloadBtn');
    if (downloadBtn) {
        downloadBtn.addEventListener('click', downloadFile);
    }
    
    const previewBtn = document.getElementById('previewBtn');
    if (previewBtn) {
        previewBtn.addEventListener('click', showPreview);
    }
    
    const newProcessBtn = document.getElementById('newProcessBtn');
    if (newProcessBtn) {
        newProcessBtn.addEventListener('click', resetProcess);
    }
    
    const retryBtn = document.getElementById('retryBtn');
    if (retryBtn) {
        retryBtn.addEventListener('click', retryProcess);
    }
    
    // 复制按钮
    initializeCopyButton();
    
    // 点击模态框外部关闭
    if (previewModal) {
        previewModal.addEventListener('click', function(e) {
            if (e.target === previewModal) {
                closePreviewModalFunction();
            }
        });
    }
}

// 初始化UI
function initializeUI() {
    // 隐藏所有结果区域
    hideAllSections();
    
    // 禁用处理按钮
    if (processBtn) {
        processBtn.disabled = true;
    }
    
    // 添加淡入动画
    document.querySelectorAll('.upload-section, .options-section, .action-section').forEach(section => {
        section.classList.add('fade-in');
    });
}

// 文件选择处理
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        validateAndSetFile(file);
    }
}

// 拖拽处理
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

// 文件验证和设置
function validateAndSetFile(file) {
    // 验证文件类型
    if (!file.name.toLowerCase().endsWith('.docx')) {
        showError('请选择 .docx 格式的Word文档');
        return;
    }
    
    // 验证文件大小 (10MB)
    const maxSize = 10 * 1024 * 1024;
    if (file.size > maxSize) {
        showError('文件大小不能超过 10MB');
        return;
    }
    
    // 设置文件
    selectedFile = file;
    displayFileInfo(file);
    if (processBtn) processBtn.disabled = false;
    
    // 隐藏错误信息
    hideError();
    
    // 添加成功动画
    if (fileInfo) {
        fileInfo.classList.add('success-pulse');
        setTimeout(() => {
            fileInfo.classList.remove('success-pulse');
        }, 600);
    }
}

// 显示文件信息
function displayFileInfo(file) {
    if (fileName) fileName.textContent = file.name;
    if (fileSize) fileSize.textContent = `文件大小：${formatFileSize(file.size)}`;
    if (fileInfo) fileInfo.style.display = 'block';
    
    // 隐藏上传区域
    if (uploadArea) uploadArea.style.display = 'none';
}

// 移除文件
function removeFile() {
    selectedFile = null;
    if (fileInput) fileInput.value = '';
    if (fileInfo) fileInfo.style.display = 'none';
    if (uploadArea) uploadArea.style.display = 'block';
    if (processBtn) processBtn.disabled = true;
    hideAllSections();
}

// 开始处理
async function startProcessing() {
    if (!selectedFile) {
        showError('请先选择一个文件');
        return;
    }
    
    try {
        // 切换到两列布局
        switchToTwoColumnLayout();
        
        // 初始化流式输出
        initializeStreamingDisplay();
        
        hideError();
        
        // 上传文件
        const formData = new FormData();
        formData.append('file', selectedFile);
        formData.append('template', document.getElementById('templateSelect').value);
        formData.append('ai_model', document.getElementById('aiModel').value);
        
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error(`上传失败: ${response.status}`);
        }
        
        const result = await response.json();
        currentTaskId = result.task_id;
        currentFileId = result.file_id;
        
        // 开始流式轮询
        startStreamingPolling();
        
    } catch (error) {
        console.error('处理失败:', error);
        showError(`处理失败: ${error.message}`);
        hideStreamingDisplay();
    }
}

// 新的教学设计生成函数
async function generateTeachingDesign() {
    if (!currentFileId) {
        showError('请先上传文件');
        return;
    }
    
    try {
        // 显示处理状态
        updateStreamingStatus({
            message: '正在生成教学设计...',
            status: 'processing'
        });
        
        // 获取选择的模板
        const templateSelect = document.getElementById('templateSelect');
        const selectedTemplate = templateSelect ? templateSelect.value : 'default';
        
        // 调用教学设计生成API
        const response = await fetch('/generate_teaching_design', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                file_id: currentFileId,
                template_id: selectedTemplate
            })
        });
        
        if (!response.ok) {
            throw new Error(`生成失败: ${response.status}`);
        }
        
        const result = await response.json();
        
        if (result.success) {
            // 生成成功
            updateStreamingStatus({
                message: '教学设计生成完成',
                status: 'completed'
            });
            
            // 显示生成结果
            showTeachingDesignResult(result);
            
        } else {
            throw new Error(result.error || '生成失败');
        }
        
    } catch (error) {
        console.error('生成教学设计失败:', error);
        updateStreamingStatus({
            message: `生成失败: ${error.message}`,
            status: 'failed'
        });
        showError(`生成教学设计失败: ${error.message}`);
    }
}

// 显示教学设计生成结果
function showTeachingDesignResult(result) {
    const streamingContent = document.getElementById('streamingContent');
    
    // 设置下载URL
    if (result.download_url) {
        window.teachingDesignDownloadUrl = result.download_url;
    } else if (currentFileId) {
        // 如果没有直接的下载URL，使用文件ID构建下载链接
        window.teachingDesignDownloadUrl = `/download_design/${currentFileId}`;
    }
    
    if (streamingContent) {
        streamingContent.innerHTML = `
            <div class="teaching-design-result">
                <div class="result-header">
                    <i class="fas fa-check-circle" style="color: #2ecc71; font-size: 2em; margin-bottom: 15px;"></i>
                    <h3 style="color: #2ecc71; margin-bottom: 10px;">教学设计生成成功！</h3>
                    <p style="color: #666; margin-bottom: 20px;">您的教学设计文档已成功生成，可以下载查看。</p>
                </div>
                <div class="result-info">
                    <div class="info-item">
                        <i class="fas fa-file-word"></i>
                        <span>文件大小: ${formatFileSize(result.file_size || 0)}</span>
                    </div>
                    <div class="info-item">
                        <i class="fas fa-clock"></i>
                        <span>生成时间: ${new Date().toLocaleString()}</span>
                    </div>
                </div>
                <div class="result-actions">
                    <button type="button" class="btn btn-primary" onclick="downloadTeachingDesign()">
                        <i class="fas fa-download"></i> 下载教学设计
                    </button>
                    <button type="button" class="btn btn-success" onclick="previewTeachingDesign()">
                        <i class="fas fa-eye"></i> 预览内容
                    </button>
                    <button type="button" class="btn btn-outline" onclick="resetProcess()">
                        <i class="fas fa-plus"></i> 处理新文件
                    </button>
                </div>
            </div>
        `;
    }
    
    // 存储下载URL
    window.teachingDesignDownloadUrl = result.download_url;
}

// 下载教学设计
function downloadTeachingDesign() {
    if (window.teachingDesignDownloadUrl) {
        const link = document.createElement('a');
        link.href = window.teachingDesignDownloadUrl;
        link.download = '教学设计文档.docx';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        showNotification('教学设计下载已开始', 'success');
    } else {
        showError('下载链接不可用');
    }
}

// 预览教学设计
function previewTeachingDesign() {
    // 这里可以添加预览功能
    showNotification('预览功能开发中...', 'info');
}

// 开始进度轮询
function startProgressPolling() {
    progressInterval = setInterval(async () => {
        try {
            const response = await fetch(`/status/${currentTaskId}`);
            const status = await response.json();
            
            updateProgress(status);
            
            if (status.status === 'completed') {
                clearInterval(progressInterval);
                showResult(status.result);
            } else if (status.status === 'failed') {
                clearInterval(progressInterval);
                showError(status.error || '处理失败');
            }
            
        } catch (error) {
            console.error('获取状态失败:', error);
            clearInterval(progressInterval);
            showError('获取处理状态失败');
        }
    }, 1000);
}

// 更新进度
function updateProgress(status) {
    const progressFill = document.getElementById('progressFill');
    const progressText = document.getElementById('progressText');
    
    // 更新进度条
    progressFill.style.width = `${status.progress}%`;
    
    // 更新进度文本
    progressText.textContent = status.message || '处理中...';
    
    // 更新步骤
    updateSteps(status.step);
}

// 更新步骤
function updateSteps(currentStep) {
    const steps = document.querySelectorAll('.step');
    
    steps.forEach((step, index) => {
        step.classList.remove('active', 'completed');
        
        if (index < currentStep) {
            step.classList.add('completed');
        } else if (index === currentStep) {
            step.classList.add('active');
        }
    });
}

// 重置进度
function resetProgress() {
    const progressFill = document.getElementById('progressFill');
    const progressText = document.getElementById('progressText');
    
    progressFill.style.width = '0%';
    progressText.textContent = '准备中...';
    
    // 重置所有步骤
    const steps = document.querySelectorAll('.step');
    steps.forEach(step => {
        step.classList.remove('active', 'completed');
    });
    
    // 激活第一步
    if (steps.length > 0) {
        steps[0].classList.add('active');
    }
}

// 显示结果
function showResult(result) {
    hideAllSections();
    
    // 更新结果信息
    document.getElementById('resultFileName').textContent = result.filename || '教学设计文档.docx';
    document.getElementById('resultFileSize').textContent = `文件大小：${formatFileSize(result.size || 0)}`;
    document.getElementById('resultGenerateTime').textContent = `生成时间：${new Date().toLocaleString()}`;
    
    // 存储AI生成的内容，用于预览
    window.generatedContent = result.result || result;
    
    // 显示结果区域
    resultSection.style.display = 'block';
    resultSection.classList.add('fade-in');
    
    // 添加成功动画
    resultSection.classList.add('success-pulse');
    setTimeout(() => {
        resultSection.classList.remove('success-pulse');
    }, 600);
}

// 显示预览
function showPreview() {
    const previewContent = document.getElementById('previewContent');
    
    // 检查是否有生成的内容
    if (window.generatedContent) {
        // 格式化AI生成的内容
        const formattedContent = formatGeneratedContent(window.generatedContent);
        previewContent.innerHTML = formattedContent;
    } else {
        // 如果没有生成内容，显示提示
        previewContent.innerHTML = `
            <div class="no-content">
                <i class="fas fa-info-circle"></i>
                <p>暂无生成内容，请先完成文件处理。</p>
            </div>
        `;
    }
    
    previewModal.style.display = 'block';
}

// 格式化生成的内容
function formatGeneratedContent(content) {
    if (typeof content !== 'string') {
        return '<p>内容格式错误</p>';
    }
    
    // 将换行符转换为HTML换行
    let formattedContent = content
        .replace(/\n\n/g, '</p><p>')  // 双换行转换为段落
        .replace(/\n/g, '<br>')        // 单换行转换为<br>
        .replace(/【([^】]+)】/g, '<h4 class="section-title">【$1】</h4>')  // 标题格式
        .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')  // 粗体
        .replace(/\*([^*]+)\*/g, '<em>$1</em>');  // 斜体
    
    // 添加样式类
    formattedContent = `
        <div class="generated-content">
            <div class="content-header">
                <h3><i class="fas fa-file-alt"></i> 教学设计内容预览</h3>
                <p class="content-info">以下是由AI生成的教学设计内容：</p>
            </div>
            <div class="content-body">
                <p>${formattedContent}</p>
            </div>
            <div class="content-footer">
                <p class="content-note">
                    <i class="fas fa-lightbulb"></i> 
                    提示：这是AI生成的教学设计内容预览，您可以复制文本或下载完整文档。
                </p>
            </div>
        </div>
    `;
    
    return formattedContent;
}

// 关闭预览模态框
function closePreviewModalFunction() {
    if (previewModal) {
        previewModal.style.display = 'none';
    }
}

// 下载文件
function downloadFile() {
    if (currentTaskId) {
        // 创建下载链接
        const downloadUrl = `/download/${currentTaskId}`;
        
        // 创建临时链接并点击
        const link = document.createElement('a');
        link.href = downloadUrl;
        link.download = document.getElementById('resultFileName').textContent;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        // 显示下载成功提示
        showNotification('文件下载已开始', 'success');
    }
}

// 重置处理流程
function resetProcess() {
    hideAllSections();
    removeFile();
    currentTaskId = null;
    
    // 清除进度轮询
    if (progressInterval) {
        clearInterval(progressInterval);
        progressInterval = null;
    }
    
    // 隐藏流式输出
    hideStreamingDisplay();
    
    // 清除生成的内容
    window.generatedContent = null;
}

// 重试处理
function retryProcess() {
    hideError();
    startProcessing();
}

// 显示错误
function showError(message) {
    hideAllSections();
    
    const errorMessage = document.getElementById('errorMessage');
    if (errorMessage) errorMessage.textContent = message;
    
    if (errorSection) {
        errorSection.style.display = 'block';
        errorSection.classList.add('fade-in');
        
        // 添加错误动画
        errorSection.classList.add('error-shake');
        setTimeout(() => {
            errorSection.classList.remove('error-shake');
        }, 500);
    }
}

// 隐藏错误
function hideError() {
    if (errorSection) errorSection.style.display = 'none';
}

// 显示进度
function showProgress() {
    hideAllSections();
    if (progressSection) {
        progressSection.style.display = 'block';
        progressSection.classList.add('fade-in');
    }
}

// 隐藏进度
function hideProgress() {
    if (progressSection) progressSection.style.display = 'none';
}

// 隐藏所有区域
function hideAllSections() {
    if (progressSection) progressSection.style.display = 'none';
    if (resultSection) resultSection.style.display = 'none';
    if (errorSection) errorSection.style.display = 'none';
}

// 显示通知
function showNotification(message, type = 'info') {
    // 创建通知元素
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
        <span>${message}</span>
    `;
    
    // 添加样式
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#2ecc71' : type === 'error' ? '#e74c3c' : '#3498db'};
        color: white;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        z-index: 1001;
        display: flex;
        align-items: center;
        gap: 10px;
        font-weight: 500;
        animation: slideInRight 0.3s ease;
    `;
    
    // 添加到页面
    document.body.appendChild(notification);
    
    // 3秒后自动移除
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// 格式化文件大小
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// 添加CSS动画
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// 错误处理
window.addEventListener('error', function(event) {
    console.error('JavaScript错误:', event.error);
    showNotification('发生了一个错误，请刷新页面重试', 'error');
});

// 未处理的Promise拒绝
window.addEventListener('unhandledrejection', function(event) {
    console.error('未处理的Promise拒绝:', event.reason);
    showNotification('网络请求失败，请检查网络连接', 'error');
});

// 页面可见性变化处理
document.addEventListener('visibilitychange', function() {
    if (document.hidden && progressInterval) {
        // 页面隐藏时暂停轮询
        clearInterval(progressInterval);
    } else if (!document.hidden && currentTaskId && !progressInterval) {
        // 页面显示时恢复轮询
        startProgressPolling();
    }
});

// 复制内容功能
function copyContentToClipboard() {
    if (!window.generatedContent) {
        showNotification('没有可复制的内容', 'warning');
        return;
    }
    
    // 创建临时文本区域
    const textArea = document.createElement('textarea');
    textArea.value = window.generatedContent;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        const successful = document.execCommand('copy');
        if (successful) {
            showNotification('内容已复制到剪贴板', 'success');
        } else {
            showNotification('复制失败，请手动选择复制', 'error');
        }
    } catch (err) {
        console.error('复制失败:', err);
        showNotification('复制失败，请手动选择复制', 'error');
    }
    
    document.body.removeChild(textArea);
}

// 初始化复制按钮事件
function initializeCopyButton() {
    const copyBtn = document.getElementById('copyContentBtn');
    if (copyBtn) {
        copyBtn.addEventListener('click', copyContentToClipboard);
    }
}

// 流式输出相关函数
function switchToTwoColumnLayout() {
    const mainContent = document.getElementById('mainContent');
    const rightColumn = document.getElementById('rightColumn');
    
    if (mainContent && rightColumn) {
        mainContent.classList.add('two-column');
        rightColumn.style.display = 'block';
    }
}

function hideStreamingDisplay() {
    const mainContent = document.getElementById('mainContent');
    const rightColumn = document.getElementById('rightColumn');
    
    if (mainContent && rightColumn) {
        mainContent.classList.remove('two-column');
        rightColumn.style.display = 'none';
    }
}

function initializeStreamingDisplay() {
    const streamingContent = document.getElementById('streamingContent');
    const statusText = document.getElementById('statusText');
    const statusIndicator = document.getElementById('statusIndicator');
    
    if (streamingContent) {
        streamingContent.innerHTML = `
            <div class="streaming-placeholder">
                <i class="fas fa-robot"></i>
                <p>AI正在分析您的文档并生成教学设计...</p>
            </div>
        `;
    }
    
    if (statusText) {
        statusText.textContent = '准备中';
    }
    
    if (statusIndicator) {
        statusIndicator.className = 'status-indicator';
    }
}

function startStreamingPolling() {
    progressInterval = setInterval(async () => {
        try {
            const response = await fetch(`/status/${currentTaskId}`);
            const status = await response.json();
            
            updateStreamingStatus(status);
            
            if (status.status === 'completed') {
                clearInterval(progressInterval);
                // 文件上传完成，自动开始生成教学设计
                updateStreamingStatus({
                    message: '文件上传完成，开始生成教学设计...',
                    status: 'processing'
                });
                
                // 延迟一秒后开始生成教学设计
                setTimeout(() => {
                    generateTeachingDesign();
                }, 1000);
                
            } else if (status.status === 'failed') {
                clearInterval(progressInterval);
                stopStreaming(status.error || '处理失败');
            }
            
        } catch (error) {
            console.error('获取状态失败:', error);
            clearInterval(progressInterval);
            stopStreaming('获取处理状态失败');
        }
    }, 1000);
}

function updateStreamingStatus(status) {
    const statusText = document.getElementById('statusText');
    const statusIndicator = document.getElementById('statusIndicator');
    
    if (statusText) {
        statusText.textContent = status.message || '处理中...';
    }
    
    if (statusIndicator) {
        statusIndicator.className = 'status-indicator';
    }
}

function completeStreaming(result) {
    const streamingContent = document.getElementById('streamingContent');
    const statusText = document.getElementById('statusText');
    const statusIndicator = document.getElementById('statusIndicator');
    
    // 存储生成的内容
    window.generatedContent = result;
    
    // 格式化并显示内容
    if (streamingContent) {
        const formattedContent = formatGeneratedContent(result);
        streamingContent.innerHTML = formattedContent;
    }
    
    if (statusText) {
        statusText.textContent = '生成完成';
    }
    
    if (statusIndicator) {
        statusIndicator.className = 'status-indicator stopped';
    }
    
    // 显示完成按钮
    showCompletionActions();
}

function stopStreaming(error) {
    const statusText = document.getElementById('statusText');
    const statusIndicator = document.getElementById('statusIndicator');
    
    if (statusText) {
        statusText.textContent = '处理失败';
    }
    
    if (statusIndicator) {
        statusIndicator.className = 'status-indicator stopped';
    }
    
    // 显示错误信息
    const streamingContent = document.getElementById('streamingContent');
    if (streamingContent) {
        streamingContent.innerHTML = `
            <div class="streaming-placeholder">
                <i class="fas fa-exclamation-triangle" style="color: #e74c3c;"></i>
                <p style="color: #e74c3c;">${error}</p>
            </div>
        `;
    }
}

function showCompletionActions() {
    const streamingControls = document.querySelector('.streaming-controls');
    if (streamingControls) {
        streamingControls.innerHTML = `
            <button type="button" class="btn btn-primary btn-sm" id="downloadStreamBtn">
                <i class="fas fa-download"></i> 下载文件
            </button>
            <button type="button" class="btn btn-success btn-sm" id="copyStreamBtn">
                <i class="fas fa-copy"></i> 复制内容
            </button>
            <button type="button" class="btn btn-outline btn-sm" id="newStreamBtn">
                <i class="fas fa-plus"></i> 处理新文件
            </button>
        `;
        
        // 绑定新按钮事件
        const downloadBtn = document.getElementById('downloadStreamBtn');
        const copyBtn = document.getElementById('copyStreamBtn');
        const newBtn = document.getElementById('newStreamBtn');
        
        if (downloadBtn) downloadBtn.addEventListener('click', downloadFile);
        if (copyBtn) copyBtn.addEventListener('click', copyContentToClipboard);
        if (newBtn) newBtn.addEventListener('click', resetProcess);
    }
}

// 加载模板列表
async function loadTemplates() {
    try {
        const response = await fetch('/templates');
        const result = await response.json();
        
        if (result.success) {
            const templateSelect = document.getElementById('templateSelect');
            if (templateSelect) {
                // 清空现有选项
                templateSelect.innerHTML = '';
                
                // 添加模板选项
                result.templates.forEach(template => {
                    const option = document.createElement('option');
                    option.value = template.id;
                    option.textContent = template.name;
                    templateSelect.appendChild(option);
                });
                
                console.log('模板列表加载成功:', result.templates);
            }
        } else {
            console.error('加载模板列表失败:', result.error);
        }
    } catch (error) {
        console.error('加载模板列表异常:', error);
    }
}

// 导出函数供测试使用
window.appFunctions = {
    validateAndSetFile,
    showError,
    showNotification,
    formatFileSize,
    copyContentToClipboard,
    switchToTwoColumnLayout,
    initializeStreamingDisplay,
    loadTemplates
};