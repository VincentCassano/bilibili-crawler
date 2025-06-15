# python库导入部分
from DrissionPage import WebPage
from colorama import init, Fore, Style
import sys, time, csv, os

# 初始化部分 #################################################################################

# colorama
init()
# 列表
v_info_list1 = [["ID", "视频标题", "BVID", "封面图片"],]
v_info_list2 = [["观看量", "点赞量", "投币量", "标签"],]
# 化序号
num1 = 0
num2 = 0
error_num1 = 0
success_num1 = 0
error_num2 = 0
success_num2 = 0

# 设置全局颜色（比如青色）
sys.stdout.write(Fore.CYAN)

# 欢迎使用本工具 ############################################################################
print(r"""
                    //            ________   ___   ___        ___   ________   ___   ___        ___   
        \\         //            |\   __  \ |\  \ |\  \      |\  \ |\   __  \ |\  \ |\  \      |\  \
         \\       //             \ \  \|\ /_\ \  \\ \  \     \ \  \\ \  \|\ /_\ \  \\ \  \     \ \  \
   ##WWWWWWWWWWWWWWWWWWWWWW##     \ \   __  \\ \  \\ \  \     \ \  \\ \   __  \\ \  \\ \  \     \ \  \
   ## WWWWWWWWWWWWWWWWWWWW ##      \ \  \|\  \\ \  \\ \  \____ \ \  \\ \  \|\  \\ \  \\ \  \____ \ \  \
   ## hh                hh ##       \ \_______\\ \__\\ \_______\\ \__\\ \_______\\ \__\\ \_______\\ \__\
   ## hh    //    \\    hh ##        \|_______| \|__| \|_______| \|__| \|_______| \|__| \|_______| \|__| 
   ## hh   //      \\   hh ##
   ## hh                hh ##         ██████╗ ██████╗  █████╗ ██╗    ██╗██╗     ███████╗██████╗ 
   ## hh      wwww      hh ##        ██╔════╝ ██╔══██╗██╔══██╗██║    ██║██║     ██╔════╝██╔══██╗
   ## hh                hh ##        ██║  ███╗██████╔╝███████║██║ █╗ ██║██║     █████╗  ██████╔╝
   ## MMMMMMMMMMMMMMMMMMMM ##        ██║   ██║██╔═══╝ ██╔══██║██║███╗██║██║     ██╔══╝  ██╔═══╝ 
   ##MMMMMMMMMMMMMMMMMMMMMM##        ╚██████╔╝██║     ██║  ██║╚███╔███╔╝███████╗███████╗██║     
        \/            \/              ╚═════╝ ╚═╝     ╚═╝  ╚═╝ ╚══╝╚══╝ ╚══════╝╚══════╝╚═╝    
                                                                             bilibili-crawler v1.0.0-beta
""")


# 改变颜色（比如亮绿色）
sys.stdout.write(Fore.LIGHTGREEN_EX)

print("\t\t╔═══════════════════════════════════════════════════════════════════╗")
print("\t\t║             欢迎使用 Bilibili-Crawler@v1.0.0-Beta 工具            ║")
print("\t\t║───────────────────────────────────────────────────────────────────║")
print("\t\t║   创作者 ：陆炳阳（Vincent Cassano）                              ║")
print("\t\t║  程序描述：初代版本，用于爬取指定B站UP主的视频列表及详细数据      ║")
print("\t\t║            视频标题、BVID、封面图片、播放、点赞、投币、标签       ║")
print("\t\t║  构建时间：2025 年 6 月 15 日  |  发布时间：2025 年 6 月 16 日    ║")
print("\t\t╚═══════════════════════════════════════════════════════════════════╝\n")
print("\t\t⚠️ 本版本为测试发布，欢迎提交 issues 与反馈。\n")


# 分割线（用红色）
sys.stdout.write(Fore.LIGHTRED_EX)

print("\n## ========================================= 这是一条分割线 ========================================= ##\n")

print("📌 ps：如果在阶段二中看到报错：'bool' object has no attribute 'response'")
print("   请不要担心，这是由于 B 站返回了异常数据，程序无法找到'x/web-interface/wbi/view/detail'指定的数据包。")
print("   ⚠ 当前暂无解决方案，疑似部分视频数据未通过常规接口传输至前端。")

print("\n## ========================================= 这是一条分割线 ========================================= ##\n")

# 恢复默认颜色
sys.stdout.write(Style.RESET_ALL)

# 获取并确认当前工作路径 #####################################################################
current_dir = os.getcwd()
print(f"当前工作路径：{current_dir}")
print("##----------------------------------------------\n")
while 1:
    queren_current_dir = input("请确认工作路径(Y/n)：")
    if queren_current_dir in ["Y","y"]:
        break
    elif queren_current_dir in ["N","n"]:
        print("正在退出程序！请更换工作路径再运行此程序！")
        time.sleep(2)
        sys.exit(0)
    else:
        print("请输入Y/n")

#访问up投稿视频主页 ##########################################################################
while 1:
    print("\n##----------------------------------------------")
    uid = input("\n请输入UP的uid：")
    try:
        uid = int(uid)
        uid = str(uid)
        break
    except: 
        print("输入错误，类型需为数字！")   

wp = WebPage()
wp.listen.start('x/space/wbi/acc/info')
wp.get(f"https://space.bilibili.com/{uid}/upload/video?tid=0&pn=4&keyword=&order=pubdate")
packet = wp.listen.wait()
up_name = packet.response.body['data']['name']

print("\n##----------------------------------------------\n")
print(f"up名称：{up_name}")

#重新更换监听位置
wp.listen.start('/space/wbi/arc/search')

# 定义文件名
file_name = f"综合项目一B站知名UP主-{up_name}视频数据.csv"
file_path = os.path.join(current_dir, file_name)

#第一个循环 #################################################################################

print("\n################################################")
print("阶段一：开始爬取视频数据：视频标题, BVID, 封面图片")
print("################################################\n")

while True:
    time.sleep(2)
    packet = wp.listen.wait()
    vlist1 = packet.response.body['data']['list']['vlist']
    try:
        for v in vlist1:
            num1 += 1
            title = v['title']
            pic = v['pic']
            bvid = v['bvid']
            v_info1 = [num1,title,bvid,pic]
            print(f"添加{v_info1}")
            v_info_list1.append(v_info1)
            success_num1 += 1
        try:
            xyy = wp.ele('text=下一页')
            xyy.click()
            time.sleep(1)
        except:
            break

    except Exception as e:
        print(f"报错：{e}")
        error_num2 += 1

# 打印第一阶段结果
print("\n################################################")
print(f"阶段一结果：一共{num1}条数据，成功 {success_num1}，失败 {error_num1}")
print("################################################\n")

# 写入 CSV 文件 #############################################################################

try:
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # 将列表中的列表写入 CSV 文件
        writer.writerows(v_info_list1)
    print(f"文件 '{file_name}' 已成功创建或覆盖！")
except Exception as e:
    print(f"写入文件时发生错误：{e}")


# 读取 CSV 文件并遍历第三列内容从第二行开始，遇到空值停止 #######################################
print("\n##----------------------------------------------")
print("开始读取CSV文件中的BVID，准备爬取")
print("##----------------------------------------------\n")
try:
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        # 跳过表头行
        next(reader, None)
        third_column_values = []
        for row in reader:
            if len(row) >= 3:  # 确保行有至少三列
                cell_value = row[2].strip()  # 获取第三列的值并去除首尾空白
                if cell_value:  # 如果不是空值，添加到列表
                    third_column_values.append(cell_value)
                else:  # 如果是空值，停止遍历
                    break
except Exception as e:
    print(f"读取文件时发生错误：{e}")


# 第二个循环 ################################################################################
print("\n################################################")
print("阶段二：开始爬取视频数据：观看量、点赞量、投币量、标签")
print("################################################\n")

for bvid in third_column_values:    
    num2 += 1
    tab = wp.new_tab("https://www.bilibili.com/video/"+bvid)
    tab.listen.start('x/web-interface/wbi/view/detail')
    packet = tab.listen.wait(timeout=2)
    #time.sleep(2)
    try:
        vlist2 = packet.response.body['data']['View']['stat']
        participle = packet.response.body['data']['participle']
        participle = '、'.join(participle)
        v_info2 = [vlist2['view'],vlist2['like'],vlist2['coin'],participle]
        print(f"添加{num2}{v_info2}")
        v_info_list2.append(v_info2)
        success_num2 += 1
    except Exception as e:
        Error = f"错误！{bvid}报错：{e}"
        Null = []
        v_info_list2.append(Null)
        error_num2 += 1
        print(Error)
    tab.close()

print(f"一共{num2}条数据，成功 {success_num2}，失败 {error_num2}")

# 读取 CSV 文件并在第5~8列写入数据 ###########################################################
print("\n##----------------------------------------------")
print("开始写入CSV文件")
# 读取现有CSV文件
import csv

try:
    # 读取现有CSV文件
    with open(file_name, 'r', encoding='utf-8') as f:
        rows = list(csv.reader(f))
except FileNotFoundError:
    print(f"[错误] 找不到文件: {file_name}")
    rows = []
except Exception as e:
    print(f"[错误] 读取文件时发生异常: {e}")
    rows = []

try:
    # 确保行数足够
    if len(rows) < len(v_info_list2):
        rows.extend([[] for _ in range(len(v_info_list2) - len(rows))])

    # 处理每一行数据
    for i in range(len(v_info_list2)):
        # 扩展列数（如果不够）
        if len(rows[i]) < 8:
            rows[i].extend([''] * (8 - len(rows[i])))

        # 写入有效数据（非空列表）
        if v_info_list2[i]:
            # 处理标签列（如果是列表）
            if len(v_info_list2[i]) > 3 and isinstance(v_info_list2[i][3], list):
                v_info_list2[i][3] = ','.join(v_info_list2[i][3])

            # 填充第5~8列（下标4~7）
            for j in range(min(len(v_info_list2[i]), 4)):
                rows[i][4 + j] = str(v_info_list2[i][j])

except IndexError as e:
    print(f"[索引错误] 行或列索引越界：{e}")
except Exception as e:
    print(f"[错误] 处理数据时出错：{e}")

try:
    # 写入原始文件（覆盖）
    with open(file_name, 'w', encoding='utf-8', newline='') as f:
        csv.writer(f).writerows(rows)
except Exception as e:
    print(f"[错误] 写入文件时发生异常: {e}")


# 写入完成并打印前十行数据 ###################################################################
print("\n##----------------------------------------------")
print(f"已成功写入文件！")
print("##----------------------------------------------\n")

try:
    with open(file_name, 'r', encoding='utf-8') as f:
        reader = list(csv.reader(f))
        print("📄 CSV 文件前 10 行预览（含表头）：\n")
        for i, row in enumerate(reader[:10]):
            print(f"第{i}行：{row}")
except Exception as e:
    print(f"[错误] 无法读取或打印 CSV 文件内容：{e}")

# 写入完成并查看文件：
print("\n################################################")
print(rf"文件位置：{file_path}\{file_name}")
print("################################################\n")

print("程序结束运行, 感谢使用, 正在退出！")
sys.exit(0)