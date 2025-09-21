#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查模板中的占位符
"""

import os
from docxtpl import DocxTemplate
import re

def check_template_placeholders(template_path):
    """检查模板中的占位符"""
    print(f"检查模板: {template_path}")
    
    if not os.path.exists(template_path):
        print(f"❌ 模板文件不存在: {template_path}")
        return
    
    try:
        # 加载模板
        template = DocxTemplate(template_path)
        
        # 获取模板中的所有文本内容
        all_text = []
        for paragraph in template.docx.paragraphs:
            all_text.append(paragraph.text)
        
        # 获取表格中的所有文本内容
        for table in template.docx.tables:
            for row in table.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        all_text.append(paragraph.text)
        
        # 合并所有文本
        full_text = '\n'.join(all_text)
        
        # 查找所有 Jinja2 占位符
        jinja_placeholders = re.findall(r'\{\{[^}]+\}\}', full_text)
        
        print(f"📄 模板中的 Jinja2 占位符:")
        for placeholder in jinja_placeholders:
            print(f"  - {placeholder}")
        
        # 特别检查 activity_intent 相关的占位符
        activity_intent_placeholders = [p for p in jinja_placeholders if 'activity_intent' in p]
        
        if activity_intent_placeholders:
            print(f"\n🎯 找到 activity_intent 相关占位符:")
            for placeholder in activity_intent_placeholders:
                print(f"  - {placeholder}")
            
            # 检查是否是全局的 activity_intent
            global_activity_intent = [p for p in activity_intent_placeholders if p.strip() == '{{ activity_intent }}']
            if global_activity_intent:
                print(f"\n⚠️  发现全局 activity_intent 占位符，需要删除:")
                for placeholder in global_activity_intent:
                    print(f"  - {placeholder}")
                return True
            else:
                print(f"\n✅ 没有发现全局的 activity_intent 占位符")
                return False
        else:
            print(f"\n✅ 没有发现 activity_intent 相关占位符")
            return False
            
    except Exception as e:
        print(f"❌ 检查模板失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("检查模板中的占位符")
    print("=" * 60)
    
    try:
        # 检查当前默认模板
        current_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"当前目录: {current_dir}")
        
        default_template = os.path.join(current_dir, "templates", "teaching_design_template.docx")
        final_template = os.path.join(current_dir, "templates", "final_table_template.docx")
        
        print(f"默认模板路径: {default_template}")
        print(f"最终模板路径: {final_template}")
        
        templates_to_check = [
            ("默认模板", default_template),
            ("最终表格模板", final_template)
        ]
        
        need_fix = False
        for name, path in templates_to_check:
            print(f"\n{'='*20} {name} {'='*20}")
            if check_template_placeholders(path):
                need_fix = True
            print("-" * 60)
        
        if need_fix:
            print(f"\n🔧 需要修复模板中的全局 activity_intent 占位符")
        else:
            print(f"\n✅ 所有模板都没有全局 activity_intent 占位符，无需修复")
            
    except Exception as e:
        print(f"❌ 主函数执行失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("开始执行脚本...")
    main()
    print("脚本执行完毕")
