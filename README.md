# 📦 bilibili-crawler

> **版本：v1.1.0** ｜ 作者：陆炳阳（Vincent Cassano）  

---

## 🧩 项目简介

`bilibili-crawler` 是一个用于抓取指定 B 站 UP 主视频数据的命令行工具，支持多页爬取、导出为 CSV、解析视频封面和互动数据，适用于数据分析、信息挖掘与内容研究。

---

## 🚀 功能特性

- ✅ 支持通过 UID 抓取指定 UP 主的视频信息
- ✅ 自动翻页，爬取up投稿页所有可见视频
- ✅ 获取视频标题、BVID、封面链接、播放量、点赞量、投币量、标签等
- ✅ 输出为 CSV 文件，便于分析与可视化处理
- ✅ 命令行交互式流程，友好提示

---

## 📦 安装方式

```bash
git clone https://github.com/VincentCassano/bilibili-crawler.git
cd bilibili-crawler
pip install -r requirements.txt
python bilibili-crawler.py
#国内下载
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```