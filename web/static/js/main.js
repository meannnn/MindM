// 全局变量
let selectedFile = null;
let currentTaskId = null;
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
        // 显示进度区域
        showProgress();
        
        // 重置进度
        resetProgress();
        
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
        
        // 开始轮询进度
        startProgressPolling();
        
    } catch (error) {
        console.error('处理失败:', error);
        showError(`处理失败: ${error.message}`);
        hideProgress();
    }
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
    // 这里可以添加预览内容的逻辑
    // 暂时显示一个示例内容
    const previewContent = document.getElementById('previewContent');
    previewContent.innerHTML = `
        <h4>教学设计文档预览</h4>
        <p><strong>课程名称：</strong>示例课程</p>
        <p><strong>教师：</strong>示例教师</p>
        <p><strong>学校：</strong>示例学校</p>
        <p><strong>教学目标：</strong>通过本课程的学习，学生将能够...</p>
        <p><strong>教学重点：</strong>重点内容...</p>
        <p><strong>教学难点：</strong>难点内容...</p>
        <p><strong>教学方法：</strong>讲授法、讨论法、案例分析法</p>
        <hr>
        <p><em>注：这是预览内容，实际文档将包含完整的教学设计信息。</em></p>
    `;
    
    previewModal.style.display = 'block';
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

// 导出函数供测试使用
window.appFunctions = {
    validateAndSetFile,
    showError,
    showNotification,
    formatFileSize
};