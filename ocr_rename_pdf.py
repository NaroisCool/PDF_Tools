import base64
import urllib
import requests
import os

#百度AI开放平台手写文字识别api应用授权
API_KEY = "DMQlrERM07******"
SECRET_KEY = "bB0jVdhMhy********"
#一次多个文件夹里的文件批处理（延迟原因，可以偷跑api接口次数限制500次/月）
input_directories = ['6', '7', '8', '5']
output_directories = ['6p', '7p', '8p', '5p']

def main():
    for i in range(len(input_directories)):
        input_dir = input_directories[i]
        output_dir = output_directories[i]
        input_path = os.path.join('.', input_dir)
        output_path = os.path.join('.', output_dir)
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        for pdf_file in os.listdir(input_path):
            if pdf_file.endswith('.pdf'):
                pdf_path = os.path.join(input_path, pdf_file)
                url = "https://aip.baidubce.com/rest/2.0/ocr/v1/handwriting?access_token=" + get_access_token()
                payload = 'pdf_file=' + get_file_content_as_base64(pdf_path, True) + '&detect_direction=false&probability=false&detect_alteration=false'
                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Accept': 'application/json'
                }
                response = requests.request("POST", url, headers=headers, data=payload)
                words_result = response.json().get('words_result')
                #根据自己的特定需求，通过接口测试来确定自己想要的数据特征
                # 遍历words_result,找到第一个数字字符串
                for j in range(len(words_result)):
                    if words_result[j]['words'].isdigit():
                        content = words_result[j]['words']
                        location = words_result[j]['location']
                        print(content)
                        print(location)
                        new_filename = content+'.pdf'
                        new_file_path = os.path.join(output_path, new_filename)
                        if os.path.exists(new_file_path):
                            print('文件名存在，加后缀。')
                            base, ext = os.path.splitext(new_filename)
                            k = 1
                            while True:
                                new_filename = base+"_"+str(k)+ext
                                new_file_path = os.path.join(output_path, new_filename)
                                if not os.path.exists(new_file_path):
                                    break
                                k += 1
                        # 移动文件到新位置
                        os.rename(pdf_path, new_file_path)
                        print("文件迁移成功")
                        break

def get_file_content_as_base64(path, urlencoded=False):
    """
    获取文件base64编码
    :param path: 文件路径
    :param urlencoded: 是否对结果进行urlencoded 
    :return: base64编码信息
    """
    with open(path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf8")
        if urlencoded:
            content = urllib.parse.quote_plus(content)
    return content

def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))

if __name__ == '__main__':
    main()
