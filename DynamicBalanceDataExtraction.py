"""
author: IYATT-yx
version: 0.0.2
"""
import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox
from datetime import datetime
import os

def generate_filename():
    formattedTime = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"导出数据文件_{formattedTime}.csv"

def user_input():
    # 选择原始数据文件
    print('\n请选择动平衡原始数据文件(支持同时选择多个文件)')
    filenames = filedialog.askopenfilenames(filetypes=[('动平衡原始数据文件', '*.csv')])
    if not filenames:
        messagebox.showinfo("提示", "未选择动平衡原始数据文件或操作已取消")
        exit(0)
        
    # 输入筛选关键词
    print('\n请选择用于筛选的关键词，留空不筛选')
    keyword = simpledialog.askstring('关键词筛选', '请输入用于筛选的关键词:')
    
    # 选择输出文件
    print('\n请选择输出文件路径')
    outputFilename = filedialog.asksaveasfilename(filetypes=[('输出数据文件', '*.csv')], initialfile=generate_filename())
    if not outputFilename:
        messagebox.showinfo("提示", "未选择输出数据文件或操作已取消")
        exit(0)

    return (filenames, keyword, outputFilename)
    
delimiter = ','

def splitData(lineString: str):
    parts = lineString.strip().split(delimiter)
    if len(parts) < 13:
        # 如果字段数量不足，返回空列表或打印警告
        print(f"跳过格式错误的行: {lineString}")
        return None

    data = []
    data.append(parts[0].strip()[5:].strip())  # 工件序号
    data.append(parts[1].strip()[4:].strip())  # 扫码编号
    data.append(parts[2].strip())              # 日期
    data.append(parts[3].strip())              # 时间
    data.append(parts[5].strip())              # 初测值
    data.append(parts[7].strip())              # 粗测相位
    data.append(parts[9].strip())              # 剩余值
    data.append(parts[11].strip())             # 剩余相位
    data.append(parts[12].strip()[5:])         # 产品情况
    return data

def main():
    print('正在启动动平衡数据提取器...')
    
    filenames, keyword, outputFilename = user_input()

    with open(outputFilename, 'w', encoding='gb2312') as wf:
        wf.write('工件序号,扫码编号,日期,时间,初测值,初测相位,剩余值,剩余相位,产品情况\n')
        for filename in filenames:
            print(f'正在读取文件：{filename}')
            with open(filename, 'r', encoding='gb2312') as rf:
                while True:
                    line = rf.readline()
                    if not line:
                        break 
                    
                    # 如果有关键词就筛选
                    if keyword and line.find(keyword) == -1:
                        continue

                    data = splitData(line)
                    if data is None:
                        continue
                    print(data)
                    wf.write(','.join(data) + '\n')
    print(f'写入文件{outputFilename}')
    os.system('PAUSE')


if __name__ == '__main__':
    main()
