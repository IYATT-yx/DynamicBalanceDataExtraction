"""
author: IYATT-yx
version: 0.0.1
"""
import os
import re

cDefaultInputFile = 'EXEHG.txt' # 默认的待处理文件
cSettingsFile = 'settings.txt' # 设置文件
cDefaultKey = '' # 默认的筛选关键词
cDefaultOutputFile = 'output.csv' # 默认的输出文件
cDelimiter = r'[;；]' # 分隔符：英文分号或中文分号
cSeg = ',' # 输出文件分隔符：英文逗号

def checkFileExists(filename):
    """检查文件是否存在"""
    if os.path.exists(filename):
        return True
    else:
        return False
    
def createSettingsFile():
    """创建设置文件"""
    try:
        with open(cSettingsFile, 'w') as f:
            f.write(cDefaultInputFile + os.linesep + cDefaultKey + os.linesep)
    except Exception as e:
        return False, e
    return True, ''

def readSettingsFile():
    """读取设置文件"""
    try:
        with open(cSettingsFile, 'r') as f:
            line1InputFile = f.readline().strip()
            if not line1InputFile:
                print(f'[cSettingFile] 为空，或读取失败。')
                return False, '', '', False
            print(f'读取到待处理文件为 {line1InputFile}')
        
            line2keyword = f.readline().strip()
            if not line2keyword:
                print('读取到关键词为空，将不做筛选。')
            else:
                print(f'读取到关键词为 {line2keyword}')

        return True, line1InputFile, line2keyword
    except Exception as e:
        print('读取设置文件失败：', e)
        os.system('PAUSE')
        exit(1)

def main():
    if not checkFileExists(cSettingsFile):
        ret, err = createSettingsFile()
        if ret:
            print(f'创建设置文件 {cSettingsFile} 成功。')
            print(f'首行为待处理文本文件路径，默认值为 {cDefaultInputFile}。')
            answer = input('次行为筛选关键词，默认为空，代表不筛选。请确认是否不筛选继续？(Y/N)')
            if answer.lower() != 'y':
                os.system('PAUSE')
                exit(0)
        else:
            print(f'创建文件失败，请检查路径是否要求高权限，可尝试以管理员权限运行。错误消息：{err}')
            os.system('PAUSE')
            exit(1)

    ret, inputFile, keyword = readSettingsFile()
    if not ret:
        print(f'读取 {cSettingsFile} 失败，请检查文件是否存在或权限是否足够。')
        os.system('PAUSE')
        exit(1)

    if not os.path.exists(inputFile):
        print(f'待处理文件 {inputFile} 不存在，请检查路径是否正确或权限是否足够。')
        os.system('PAUSE')
        exit(1)

    try:
        with open(cDefaultOutputFile, 'w', encoding='gb2312') as w:
            w.write('日期' + cSeg +
                    '时间' + cSeg +
                    '工件序号' + cSeg +
                    '工件型号' + cSeg +
                    '工件编号' + cSeg +
                    '工人编号' + cSeg +
                    '剩余量幅值' + cSeg +
                    '剩余量相位' + cSeg +
                    '合格量值' + '\n')
            with open(inputFile, 'r', encoding='gb2312') as r:
                while True:
                    lineBuffer = r.readline()
                    if not lineBuffer:
                        break

                    if keyword and lineBuffer.find(keyword) == -1:
                        continue

                    parts = re.split(cDelimiter, lineBuffer)
                    output = '\'' + parts[0].replace(' ', '') + cSeg + \
                          parts[1].replace(' ', '') + cSeg + \
                          parts[2][4:].strip() + cSeg + \
                          parts[3][4:].strip() + cSeg + \
                          parts[4][4:].strip() + cSeg + \
                          parts[5][4:].strip() + cSeg + \
                          parts[6][5:].strip() + cSeg + \
                          parts[7][5:].strip() + cSeg + \
                          parts[8][4:].strip() + '\n'
                    print(output, end='')
                    w.write(output)
                print(f'提取完成，按任意键确认保存到 {cDefaultOutputFile}。')
                os.system('PAUSE')

    except Exception as e:
        print(f'读取文件 {inputFile} 失败，请检查文件是否存在或权限是否足够。错误消息：{e}')
        os.system('PAUSE')
        exit(1)

if __name__ == '__main__':
    main()