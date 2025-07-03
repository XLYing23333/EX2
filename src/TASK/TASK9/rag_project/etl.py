import os

def etl_process(input_folder='Docs', output_folder='output'):
    """
    遍历input_folder下所有txt文件，读取内容，去除每行空白，
    用第一行作为新文件名，替换第一行内容为文件名，保存到output_folder。
    """
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            input_file_path = os.path.join(input_folder, filename)
            with open(input_file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            # 去除每行前后空格
            lines = [line.strip() for line in lines if line.strip() != '']

            # 防止空文件
            if not lines:
                print(f"{filename} 文件为空，跳过。")
                continue

            # 用第一行作为新文件名
            new_filename = lines[0] + '.txt'

            output_file_path = os.path.join(output_folder, new_filename)

            # 将第一行替换成文件名（也可以根据需求调整）
            lines[0] = new_filename

            with open(output_file_path, 'w', encoding='utf-8') as file:
                file.write('\n'.join(lines) + '\n')

    print("所有文件已处理并保存到 output 文件夹中。")


if __name__ == '__main__':
    etl_process()