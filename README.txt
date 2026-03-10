# MySQL 数据库巡检工具

一个基于 **Flask + MySQL** 的数据库巡检工具，支持：

- 运维巡检（表行数、索引、表状态等）
- 开发巡检（表结构、前几行数据展示）
- 自定义 SQL 巡检
- 巡检结果 **HTML 报告导出**
- 支持 Windows / Linux

项目参考 **阿里云 DMS 风格 UI**，操作简单，方便日常数据库运维。

---

## 🚀 功能特点

1. **巡检类型**

| 类型       | 内容示例 |
|-----------|----------|
| 运维巡检   | `COUNT(*)`、`SHOW INDEX`、`SHOW TABLE STATUS` |
| 开发巡检   | `DESC table`、`SELECT * LIMIT 5` |
| 自定义 SQL | 用户自定义 SQL 脚本 |

2. **HTML 报告导出**

- 点击“导出HTML巡检报告”，生成包含 SQL、表头和结果的 HTML 文件  
- 支持 Windows / Linux 下载  
- 无需写入磁盘（使用 BytesIO 直接下载）

3. **前端交互**

- 单页面巡检操作  
- 运维巡检、开发巡检、手动执行 SQL 三个按钮  
- 巡检结果表格展示，支持表头和多行数据  

---

## 💻 环境要求

- Python 3.8+  
- Flask 2.x  
- PyMySQL  
- 浏览器：Chrome / Firefox / Edge  
- MySQL 5.7+ 或 8.x  

---

## ⚙️ 安装与启动

1. 克隆项目

```bash
git clone https://github.com/yourname/mysql-inspect-tool.git
cd mysql-inspect-tool