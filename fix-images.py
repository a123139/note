import os
import re
import shutil

def fix_image_paths(md_file_path, assets_dir):
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    typora_pattern = r'C:\\Users\\Administrator\\AppData\\Roaming\\Typora\\typora-user-images\\([^"\'\)]+)'
    
    matches = re.findall(typora_pattern, content)
    
    if not matches:
        print(f"未找到需要修复的图片路径: {md_file_path}")
        return 0
    
    print(f"找到 {len(matches)} 个需要修复的图片路径")
    
    typora_src_dir = r"C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images"
    
    for image_name in matches:
        src_path = os.path.join(typora_src_dir, image_name)
        dest_path = os.path.join(assets_dir, image_name)
        
        if os.path.exists(src_path):
            shutil.copy2(src_path, dest_path)
            print(f"复制图片: {image_name} -> {assets_dir}")
        else:
            print(f"警告: 源图片不存在 {src_path}")
    
    new_content = re.sub(
        r'C:\\Users\\Administrator\\AppData\\Roaming\\Typora\\typora-user-images\\([^"\'\)]+)',
        r'./assets/\1',
        content
    )
    
    with open(md_file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"路径替换完成: {md_file_path}")
    return len(matches)

def main():
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    for folder in os.listdir(project_root):
        folder_path = os.path.join(project_root, folder)
        
        if not os.path.isdir(folder_path):
            continue
        
        if folder.startswith('.') or folder in ['node_modules', 'dist', 'build']:
            continue
        
        assets_dir = os.path.join(folder_path, 'assets')
        os.makedirs(assets_dir, exist_ok=True)
        
        for file in os.listdir(folder_path):
            if file.endswith('.md'):
                md_file_path = os.path.join(folder_path, file)
                print(f"\n处理文件: {md_file_path}")
                fix_image_paths(md_file_path, assets_dir)
    
    print("\n\n所有图片路径修复完成！")

if __name__ == '__main__':
    main()
