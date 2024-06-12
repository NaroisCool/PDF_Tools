import os
import PyPDF2

def split_pdf_files(input_dir, output_dir):
    """
    将指定目录下的PDF文件拆分成单个PDF文件,并保存到输出目录。
    
    参数:
    input_dir (str): 包含PDF文件的输入目录路径
    output_dir (str): 保存拆分后的PDF文件的输出目录路径
    """
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 遍历输入目录下的文件
    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            # 拼接输入文件路径
            input_path = os.path.join(input_dir, filename)
            
            # 打开PDF文件
            with open(input_path, "rb") as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                # 获取页数
                num_pages = len(pdf_reader.pages)
                
                # 逐页拆分PDF文件
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    
                    # 创建新的PDF文件
                    output_filename = f"{os.path.splitext(filename)[0]}_page{page_num + 1}.pdf"
                    output_path = os.path.join(output_dir, output_filename)
                    
                    with open(output_path, "wb") as output_file:
                        pdf_writer = PyPDF2.PdfWriter()
                        pdf_writer.add_page(page)
                        pdf_writer.write(output_file)
                        
                        print(f"已保存文件: {output_filename}")

# 修改成你的待处理的pdf文件目录
input_dir = "/path/to/input/directory" 
# 修改成你的处理完存放pdf文件的目录
output_dir = "/path/to/output/directory"
split_pdf_files(input_dir, output_dir)
