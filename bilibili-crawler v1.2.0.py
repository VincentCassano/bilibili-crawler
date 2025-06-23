# python库导入部分
from DrissionPage import WebPage, ChromiumOptions
from colorama import init, Fore, Style
import sys, time, csv, os, logging

########################################################################################################################################
# 函数部分
def print_stage_start(stage, message):
    sys.stdout.write(Fore.YELLOW)
    print("══════════════════════════════════════════════════════════════════════════════")
    print(f"[提示] 阶段{stage}：{message}")
    print("══════════════════════════════════════════════════════════════════════════════")
    logging.info(f"[提示] 阶段{stage}：{message}")
    sys.stdout.write(Style.RESET_ALL)


def print_stage_result(stage, total, success, error):
    sys.stdout.write(Fore.YELLOW)
    print("══════════════════════════════════════════════════════════════════════════════")
    print(f"[结果] 阶段{stage}：一共 {total} 条数据, 成功 {success}, 失败 {error}")
    print("══════════════════════════════════════════════════════════════════════════════")
    logging.info(f"[结果] 阶段{stage}：一共 {total} 条数据, 成功 {success}, 失败 {error}")
    sys.stdout.write(Style.RESET_ALL)


########################################################################################################################################
# 初始化部分
init()  # colorama
v_info_list1 = [["ID", "视频标题", "BVID", "封面图片"],]    # 阶段一数据存储列表
v_info_list2 = [["观看量", "点赞量", "投币量", "标签"],]     # 阶段二数据存储列表
existing_bvid_list = []     # CSV中存在的BVID列表
id = 0                      # 数据ID
num = 0                     # 获取数据计数器
error_num1 = 0              # 阶段一报错计数器
success_num1 = 0            # 阶段一成功计数器
error_num2 = 0              # 阶段二报错计数器
success_num2 = 0            # 阶段二成功计数器
stop_flag = True            # 是否遇到重复BVID的标志

# 配置日志，添加 encoding 参数指定编码为 utf-8
logging.basicConfig(
    level=logging.DEBUG,  # 设置日志级别为 DEBUG，这意味着会记录所有级别（DEBUG、INFO、WARNING、ERROR、CRITICAL）的日志
    format='%(asctime)s - %(levelname)s - %(message)s',  # 定义日志的输出格式
    filename='app.log',  # 指定日志输出到的文件
    filemode='w',  # 以写入模式打开文件，每次运行程序都会覆盖之前的日志文件
    encoding='utf-8'  # 指定文件编码为 utf-8，确保中文能正常显示
)

########################################################################################################################################
# 欢迎使用：工具LOGO 介绍 注意事项
sys.stdout.write(Fore.CYAN)
print(r"""
                     //           ________   ___   ___        ___   ________   ___   ___        ___   
          \\        //           |\   __  \ |\  \ |\  \      |\  \ |\   __  \ |\  \ |\  \      |\  \
           \\      //            \ \  \|\ /_\ \  \\ \  \     \ \  \\ \  \|\ /_\ \  \\ \  \     \ \  \
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
                                                                             bilibili-crawler v1.2.0
""")

sys.stdout.write(Fore.LIGHTGREEN_EX)
print("\t\t╔═══════════════════════════════════════════════════════════════════╗")
print("\t\t║             欢迎使用 Bilibili-Crawler@v1.2.0 工具                 ║")
print("\t\t║───────────────────────────────────────────────────────────────────║")
print("\t\t║   创作者 ：陆炳阳（Vincent Cassano）                              ║")
print("\t\t║  程序描述：初代版本，用于爬取指定B站UP主的视频列表及详细数据      ║")
print("\t\t║            视频标题、BVID、封面图片、播放、点赞、投币、标签       ║")
print("\t\t║  构建时间：2025 年 6 月 15 日  |  发布时间：2025 年 6 月 16 日    ║")
print("\t\t╚═══════════════════════════════════════════════════════════════════╝\n")
print("\t\t📢 本版本更新发布时间：2025 年 6 月 23 日，欢迎提交 issues 与反馈。")
print("\t\t🔗 GitHub: https://github.com/VincentCassano/bilibili-crawler")

sys.stdout.write(Fore.LIGHTRED_EX)
print("\n## ========================================= 这是一条分割线 ========================================= ##\n")
print("📌 注意事项：")
print("   在阶段二过程中，若出现此报错：'bool' object has no attribute 'response'")
print("   ├─ 📍 原因：B站返回了异常格式的数据包，无法匹配常规接口：x/web-interface/wbi/view/detail")
print("   ├─ ✅ 状态：程序会自动切换为备用方案（方法二）尝试获取页面可视数据")
print("   ├─ ⚠️ 说明：为确保数据准确，方法二将过滤包含小数点或“万”等中文单位的数据")
print("   └─ 💡 提示：若部分数据字段显示为空（如点赞量、播放量等），属正常行为，可放心忽略")
print("\n## ========================================= 这是一条分割线 ========================================= ##\n")
sys.stdout.write(Style.RESET_ALL)

########################################################################################################################################
# 获取并确认当前工作路径
current_dir = os.getcwd()
print("────────────────────────────────────────────────────────────────────────")
print(f"📂 当前工作路径：{current_dir}")
print("────────────────────────────────────────────────────────────────────────")
while 1:
    queren_current_dir = input("\n请确认工作路径(Y/n)：")
    if queren_current_dir in ["Y","y"]:
        logging.info(f"工作路径：{current_dir}")
        break
    elif queren_current_dir in ["N","n"]:
        print(f"{Fore.YELLOW}[警告] 正在退出程序！请更换工作路径再运行此程序！{Style.RESET_ALL}")
        time.sleep(2)
        sys.exit(0)
    else:
        print("请输入Y/n")

#访问up投稿视频主页
while 1:
    up_uid = input("请输入UP的uid：")
    try:
        up_uid = str(int(up_uid))
        logging.info(f"UP_UID：{up_uid}")
        break
    except: 
        print("输入错误，类型需为数字！")   

########################################################################################################################################
# 程序主要部分
start_time = time.time()  # 程序开始计时

# 配置无头模式和浏览器指纹
co = ChromiumOptions()
co.headless(True)
co.set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

# 初始化浏览器 发送访问请求 获取up名称 关闭页面
wp = WebPage(chromium_options=co)
wp.listen.start('x/space/wbi/acc/info')
wp.get(f"https://space.bilibili.com/{up_uid}/upload/video?tid=0&pn=4&keyword=&order=pubdate")
packet = wp.listen.wait()
up_name = packet.response.body['data']['name']
wp.quit()

print("\n────────────────────────────────────────────────────────────────────────")
print(f"up名称：{up_name}")
print("────────────────────────────────────────────────────────────────────────\n")
logging.info(f"up名称：{up_name}")

time.sleep(1)

# 定义文件名
file_name = f"B站UP-{up_name}视频数据.csv"
file_path = os.path.join(current_dir, file_name)

# 判断是否有同名文件（重复文件）读取是否含有数据
if os.path.exists(file_path):
    print(f"[提示] 检测到已有数据文件：“{file_name}”  准备读取已有BVID用于去重处理。")
    logging.info(f"[提示] 检测到已有数据文件：“{file_name}”。")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader, None)  # 读取表头
            data_rows = list(reader)     # 读取剩余行
            
            if not data_rows:
                print(f"{Fore.YELLOW}[警告] 数据文件仅有表头，没有实际数据，视为无历史数据。{Style.RESET_ALL}")
                logging.warning(f"[警告] 数据文件仅有表头，没有实际数据，视为无历史数据。")
            else:
                for row in data_rows:
                    if len(row) >= 3:  # 第三列是 BVID
                        csv_bvid = row[2].strip()
                        if csv_bvid:
                            existing_bvid_list.append(csv_bvid)
                Li_Shi_Shu_Ju_num = len(existing_bvid_list)
                print(f"{Fore.GREEN}[完成] 已加载 {Li_Shi_Shu_Ju_num} 条历史 BVID !\n{Style.RESET_ALL}")
                logging.info(f"[完成] 已加载 {Li_Shi_Shu_Ju_num} 条历史 BVID !")

    except Exception as e:
        print(f"{Fore.RED}[错误] 读取文件时发生错误：{e}{Style.RESET_ALL}")
        logging.error(f"[错误] 读取文件时发生错误：{e}")
        existing_bvid_list = []  # 防止程序中断
else:
    print(f"[提示] 未检测到同名UP主的数据文件，将从头开始爬取。\n")
    logging.info(f"[提示] 未检测到同名UP主的数据文件，将从头开始爬取。")

########################################################################################################################################
# 阶段一：爬取up主页投稿视频

##################################################################################################
# 阶段一开始                                                                                      #
print_stage_start("一", "开始爬取视频数据：视频标题, BVID, 封面图片")                               #
##################################################################################################

# 初始化浏览器 发送访问请求 获取up视频列表
wp = WebPage(chromium_options=co)
wp.listen.start('/space/wbi/arc/search')
wp.get(f"https://space.bilibili.com/{up_uid}/upload/video?tid=0&pn=4&keyword=&order=pubdate")

while stop_flag:
    packet = wp.listen.wait()
    vlist1 = packet.response.body['data']['list']['vlist']
    try:
        for v in vlist1:
            title = v['title']
            pic = v['pic']
            bvid = v['bvid']
            if bvid not in existing_bvid_list:
                id += 1
                v_info1 = [id,title,bvid,pic]
                print(f"{Fore.GREEN}[√]添加{v_info1}{Style.RESET_ALL}")
                v_info_list1.append(v_info1)
                success_num1 += 1
            else:
                print(f"[提示] {bvid}已经存在")
        else:
            try:
                xyy = wp.ele('text=下一页')
                xyy.click()
                time.sleep(1)
            except:
                break

    except Exception as e:
        print(f"{Fore.RED}[错误] 报错：{e}{Style.RESET_ALL}")
        logging.error(f"[错误] 阶段一报错：{e}")
        error_num1 += 1

##################################################################################################
# 阶段一结果                                                                                      #
print_stage_result("一", len(v_info_list1)-1, success_num1, error_num1)                          #
##################################################################################################

########################################################################################################################################
# 将阶段一结果写入 CSV 文件
if len(v_info_list1) > 1:
    try:
        with open(file_path, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # 将列表中的列表写入 CSV 文件
            writer.writerows(v_info_list1)
        print(f"\n{Fore.GREEN}[完成] 文件 '{file_name}' 已成功创建或覆盖！{Style.RESET_ALL}")
        logging.info(f"[完成] 阶段一：文件 '{file_name}' 已成功创建或覆盖！")
    except Exception as e:
        print(f"{Fore.RED}[错误] 写入文件时发生错误：{e}{Style.RESET_ALL}")
        logging.error(f"[错误] 阶段一：写入文件时发生错误：{e}")

# 读取 CSV 文件并遍历第三列内容从第二行开始，遇到空值停止
print("[提示] 读取CSV文件加载BVID！\n")
logging.info(f"[提示] 阶段二：读取CSV文件加载BVID！")
try:
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        # 跳过表头行
        next(reader, None)
        third_column_values = []
        for row in reader:
            if len(row) >= 3:                # 确保行有至少三列
                cell_value = row[2].strip()  # 获取第三列的值并去除首尾空白
                if cell_value:               # 如果不是空值，添加到列表
                    third_column_values.append(cell_value)
                else:  # 如果是空值，停止遍历
                    break
except Exception as e:
    print(f"\n{Fore.RED}[错误] 读取文件时发生错误：{e}{Style.RESET_ALL}\n")
    logging.error(f"[错误] 读取文件时发生错误：{e}")
########################################################################################################################################
# 阶段二：爬取up视频数据

##################################################################################################
# 阶段二开始                                                                                      #
print_stage_start("二", "开始爬取视频数据：观看量, 点赞量, 投币量, 标签")                            #
##################################################################################################

for bvid in third_column_values:
    num += 1
    tab = wp.new_tab("https://www.bilibili.com/video/"+bvid)
    tab.listen.start('x/web-interface/wbi/view/detail')
    packet = tab.listen.wait(timeout=3)

    # 方法一
    try:
        vlist2 = packet.response.body['data']['View']['stat']
        participle = packet.response.body['data']['participle']
        participle = '、'.join(participle)
        v_info2 = [vlist2['view'],vlist2['like'],vlist2['coin'],participle]
        print(f"{Fore.GREEN}[√]添加{num}{v_info2}{Style.RESET_ALL}")
        v_info_list2.append(v_info2)
        success_num2 += 1

    # 方法二
    except Exception as e1:
        try:
            tab.listen.start(f'{bvid}')
            tab.get(f"https://www.bilibili.com/video/{bvid}/")
            packet = tab.listen.wait(timeout=2)

            # 观看数
            f2_view = ""
            tags0 = tab.eles('.view-text')
            if tags0:
                view_text = tags0[0].text.strip()
                if '.' not in view_text and view_text.isdigit():
                    f2_view = int(view_text)
            else:
                print("[提示] 未获取到观看量数据")
                logging.warning("[提示] 未获取到观看量数据")

            # 点赞数 + 投币数
            f2_like = f2_coin = ""
            tags1 = tab.eles('.:video-toolbar-item-text')
            if len(tags1) >= 2:
                like_raw = tags1[0].text.strip()
                coin_raw = tags1[1].text.strip()
                if '.' not in like_raw and like_raw.isdigit():
                    f2_like = int(like_raw)
                if '.' not in coin_raw and coin_raw.isdigit():
                    f2_coin = int(coin_raw)
            else:
                print("[提示] 点赞量和投币量未获取到数据")
                logging.warning("[提示] 点赞量和投币量未获取到数据")

            # 标签
            f2_tags = ""
            tags2 = tab.eles('.tag-link')
            if tags2:
                f2_tags = '、'.join(tag.text for tag in tags2)

            # 四项中只要有任意一项非空就添加
            if any([f2_view, f2_like, f2_coin, f2_tags]):
                v_info2 = [f2_view, f2_like, f2_coin, f2_tags]
                print(f"{Fore.GREEN}[√]添加{num}{v_info2}{Style.RESET_ALL}")
                v_info_list2.append(v_info2)
                success_num2 += 1

            else:
                raise ValueError(f"⚠️ 方法二失败\n四项数据均为空或非法: 观看量{view_text}、点赞量{like_raw}、投币量{coin_raw}、标签{f2_tags}")
                
        except Exception as e2:
            Error = f"[错误]{bvid}报错：{e2}"
            logging.error(Error)
            v_info_list2.append([Error])
            error_num2 += 1
            print(f"{Fore.RED}{Error}{Style.RESET_ALL}")

    tab.close()
wp.quit()

##################################################################################################
# 阶段二结果                                                                                      #
print_stage_result(2, num, success_num2, error_num2)                                             #
##################################################################################################

########################################################################################################################################
# 将阶段二结果写入 CSV 文件
print(f"\n[提示] 开始写入CSV文件")
logging.info(f"[提示] 阶段二：开始写入CSV文件")
try:
    with open(file_name, 'r', encoding='utf-8') as f:
        rows = list(csv.reader(f))
except FileNotFoundError:
    print(f"{Fore.RED}[错误] 找不到文件: {file_name}{Style.RESET_ALL}")
    logging.error(f"[错误] 找不到文件: {file_name}")
    rows = []
except Exception as e:
    print(f"{Fore.RED}[错误] 读取文件时发生异常: {e}{Style.RESET_ALL}")
    logging.error(f"[错误] 读取文件时发生异常: {e}")
    rows = []

try:
    # 确保行数足够
    if len(rows) < len(v_info_list2):
        rows.extend([[] for _ in range(len(v_info_list2) - len(rows))])

    # 处理每一行数据
    for i in range(len(v_info_list2)):
        if len(rows[i]) < 8:    # 扩展列数（如果不够）
            rows[i].extend([''] * (8 - len(rows[i])))

        if v_info_list2[i]:     # 写入有效数据（非空列表）
            # 处理标签列（如果是列表）
            if len(v_info_list2[i]) > 3 and isinstance(v_info_list2[i][3], list):
                v_info_list2[i][3] = ','.join(v_info_list2[i][3])

            # 填充第5~8列（下标4~7）
            for j in range(min(len(v_info_list2[i]), 4)):
                rows[i][4 + j] = str(v_info_list2[i][j])

except IndexError as e:
    print(f"{Fore.RED}[索引错误] 行或列索引越界：{e}{Style.RESET_ALL}")
    logging.error(f"[索引错误] 行或列索引越界：{e}")
except Exception as e:
    print(f"{Fore.RED}[错误] 处理数据时出错：{e}{Style.RESET_ALL}")
    logging.error(f"[错误] 处理数据时出错：{e}")

try:
    # 写入原始文件（覆盖）
    with open(file_name, 'w', encoding='utf-8', newline='') as f:
        csv.writer(f).writerows(rows)
except Exception as e:
    print(f"{Fore.RED}[错误] 写入文件时发生异常: {e}{Style.RESET_ALL}")
    logging.error(f"[错误] 写入文件时发生异常: {e}")

########################################################################################################################################
# 打印前十行数据预览
print(f"{Fore.GREEN}[完成] 已成功写入文件！{Style.RESET_ALL}")
logging.info(f"[完成] 已成功写入文件！")

try:
    with open(file_name, 'r', encoding='utf-8') as f:
        reader = list(csv.reader(f))
        print("\n────────────────────────────────────────────────────────────────────────")
        print("📄 CSV 文件前 10 行预览（含表头）：")
        print("────────────────────────────────────────────────────────────────────────\n")
        for i, row in enumerate(reader[:10]):
            print(f"第{i}行：{row}")
except Exception as e:
    print(f"{Fore.RED}[错误] 无法读取或打印 CSV 文件内容：{e}{Style.RESET_ALL}")
    logging.error(f"[错误] 无法读取或打印 CSV 文件内容：{e}")

########################################################################################################################
#结果（绿色）                                                                                                           #
sys.stdout.write(Fore.LIGHTGREEN_EX)                                                                                   #
print("\n##########################################################################################")                  #
print(rf"文件位置：{file_path}")                                                                                        #
print("##########################################################################################\n")                  #
logging.info(rf"文件位置：{file_path}")
sys.stdout.write(Style.RESET_ALL)                                                                                      #
########################################################################################################################

end_time = time.time()  # 程序结束计时
elapsed_time = end_time - start_time

print("\n────────────────────────────────────────────────────────────────────────")
print(f"本次程序一共爬取{num}条数据，总运行时长：{elapsed_time:.2f} 秒")
print(f"感谢使用！程序结束运行正在退出！\n")
logging.info(f"本次程序一共爬取{num}条数据，总运行时长：{elapsed_time:.2f} 秒! 程序结束运行! ")
sys.exit(0)