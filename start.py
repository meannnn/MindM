import os
import sys
import socket
import webbrowser
import time
from dotenv import load_dotenv

def find_free_port(start_port=None, max_port=None):
    """查找可用端口"""
    if start_port is None:
        start_port = int(os.getenv('PORT_RANGE_START', 5000))
    if max_port is None:
        max_port = int(os.getenv('PORT_RANGE_END', 5100))
    
    for port in range(start_port, max_port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    return None

def open_browser(url, delay=2):
    """延迟打开浏览器"""
    def _open():
        time.sleep(delay)
        try:
            webbrowser.open(url)
            print(f"浏览器已打开: {url}")
        except Exception as e:
            print(f"无法自动打开浏览器: {e}")
            print(f"请手动访问: {url}")
    
    import threading
    browser_thread = threading.Thread(target=_open, daemon=True)
    browser_thread.start()

def main():
    print("=" * 50)
    print("AI文档助手 v0.1.0")
    print("=" * 50)
    
    load_dotenv()
    
    api_key = os.getenv('DASHSCOPE_API_KEY')
    if not api_key or api_key == 'your_dashscope_api_key_here':
        print("警告: 未配置API密钥")
        print("请在.env文件中设置DASHSCOPE_API_KEY")
        print()
    
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('outputs', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    try:
        from app import app
        
        # 查找可用端口
        default_port = int(os.getenv('PORT', 5000))
        port = find_free_port(default_port)
        
        if port is None:
            print("错误: 无法找到可用端口")
            sys.exit(1)
        
        debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
        
        print("启动应用...")
        print(f"使用端口: {port}")
        print(f"访问地址: http://localhost:{port}")
        print("按 Ctrl+C 停止服务")
        print("=" * 50)
        
        # 准备浏览器URL
        browser_url = f"http://localhost:{port}"
        
        # 启动应用（在后台线程中）
        import threading
        app_thread = threading.Thread(
            target=lambda: app.run(host='0.0.0.0', port=port, debug=debug, threaded=True, use_reloader=False),
            daemon=True
        )
        app_thread.start()
        
        # 等待应用启动
        print("等待应用启动...")
        time.sleep(3)
        
        # 自动打开浏览器（根据配置）
        auto_open = os.getenv('AUTO_OPEN_BROWSER', 'true').lower() == 'true'
        if auto_open:
            print("正在打开浏览器...")
            open_browser(browser_url)
        else:
            print("自动打开浏览器已禁用")
            print(f"请手动访问: {browser_url}")
        
        # 保持主线程运行
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n正在停止应用...")
            sys.exit(0)
        
    except ImportError as e:
        print(f"导入应用失败: {e}")
        print("请确保所有依赖包已正确安装")
        sys.exit(1)
    except Exception as e:
        print(f"启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
