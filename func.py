import re
def replace_x_with_space(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            print(content)
            # 使用正则表达式将所有 "x" 替换为空格
            modified_content = re.sub(r'\bx\b', ' ', content)
            
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(modified_content)
        # 打印内容content

        print(f'Successfully replaced all occurrences of "x" with space in {file_path}')
    except Exception as e:
        print(f'Error: {e}')

file_path = '每日安排.md'
replace_x_with_space(file_path)
