#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复状态接口问题
"""

# 修复后的状态接口代码
status_route_code = '''
@app.route('/status/<task_id>')
def get_task_status(task_id):
    """获取任务状态"""
    try:
        # 查找对应的文件信息
        file_info = None
        for file_id, info in uploaded_files.items():
            if info.get('task_id') == task_id:
                file_info = info
                break
        
        if not file_info:
            return jsonify({'success': False, 'error': '任务不存在'})
        
        # 检查任务状态
        status = file_info.get('status', 'processing')
        
        if status == 'completed':
            return jsonify({
                'success': True,
                'status': 'completed',
                'progress': 100,
                'result': file_info.get('result', ''),
                'message': '文件处理完成'
            })
        elif status == 'failed':
            return jsonify({
                'success': False,
                'status': 'failed',
                'error': file_info.get('error', '处理失败')
            })
        else:
            return jsonify({
                'success': True,
                'status': 'processing',
                'progress': 50,
                'message': '文件正在处理中...'
            })
            
    except Exception as e:
        logger.error(f"获取任务状态失败: {e}")
        return jsonify({'success': False, 'error': str(e)})
'''

print("修复后的状态接口代码:")
print(status_route_code)
