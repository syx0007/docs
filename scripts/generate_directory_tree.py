#!/usr/bin/env python3
import os
import re
from pathlib import Path

def escape_filename(filename):
    """
    转义文件名中的特殊字符，如果包含特殊字符则添加引号
    """
    # 检查是否包含可能影响Markdown链接解析的特殊字符
    special_chars = r'[\[\]()<>]'
    if re.search(special_chars, filename):
        # 使用反引号包裹文件名（Markdown的内联代码格式）
        return f"`{filename}`"
    return filename

def generate_directory_tree(root_dir="content", output_file="DIRECTORY_TREE.md"):
    """
    递归生成带路径的目录树结构并保存为Markdown文件
    
    参数:
        root_dir: 要扫描的根目录 (默认: 'content')
        output_file: 输出文件路径 (默认: 'DIRECTORY_TREE.md')
    """
    root_path = Path(root_dir)
    
    if not root_path.exists():
        print(f"错误: 目录 '{root_dir}' 不存在")
        return
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("#\n\n")
        
        # 存储所有文件和它们的相对路径
        file_entries = []
        
        # 递归收集所有文件
        for dirpath, _, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename.endswith('.md'):  # 只处理Markdown文件
                    file_path = Path(dirpath) / filename
                    rel_path = os.path.relpath(file_path, root_dir)
                    # 存储目录路径(显示用)和完整路径(链接用)
                    display_dir = os.path.relpath(dirpath, root_dir)
                    file_entries.append((display_dir, filename, f"./{root_dir}/{rel_path.replace(os.sep, '/')}"))
        
        # 按目录层级和文件名排序
        file_entries.sort(key=lambda x: (x[0], x[1].lower()))

        current_dir = None
        for display_dir, filename, full_path in file_entries:
            # 如果目录改变了，添加目录标题
            if display_dir != current_dir:
                if current_dir is not None:
                    f.write("\n")
                # 显示相对于root_dir的目录路径
                if display_dir == ".":
                    f.write("# 根目录\n")
                else:
                    f.write(f"# {display_dir.replace(os.sep, '/')}\n")
                current_dir = display_dir
            
            # 写入文件项，转义文件名中的特殊字符
            escaped_filename = escape_filename(filename)
            if f"- [{escaped_filename}]({full_path})" != "- [index.md](./content/index.md)":
                f.write(f"- [{escaped_filename}]({full_path})\n")

        print(f"目录树已生成到 {output_file}")

if __name__ == "__main__":
    generate_directory_tree()
