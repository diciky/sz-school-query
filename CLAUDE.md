# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

深圳中考高中志愿填报查询系统。Flask 后端 + 单一 HTML 前端，数据存储在 `schools.json`。

## 目录结构

```
sz-school-query/
├── backend/
│   ├── main.py        # Flask 应用入口
│   ├── parse_data.py  # 数据解析脚本
│   ├── schools.json   # 学校数据（93所）
│   └── requirements.txt
└── frontend/
    └── index.html     # 前端页面（Tailwind + Chart.js）
```

## 启动命令

```bash
cd ~/sz-school-query/backend
python3 main.py
# 访问 http://localhost:5188
```

## API 端点

| 端点 | 说明 |
|------|------|
| `GET /` | 前端页面 |
| `GET /api/schools` | 所有学校，参数：`district`, `type`, `level` |
| `GET /api/schools/<id>` | 单所学校详情 |
| `GET /api/recommend?score=&category=` | 志愿推荐（冲/稳/保） |

## 数据状态

- **93 所学校**，分数线数据完整（AC/D 类）
- 以下字段**全部为空**：address, phone, scale, boarding, transport, self_recruit（93所）；gaokao（73所）；features/pros/cons（12所）
- **警告**：不要批量爬取补充数据，会导致内存/磁盘耗尽死机

## 重启服务

```bash
pkill -f "python.*main.py"
cd ~/sz-school-query/backend && python3 main.py
```