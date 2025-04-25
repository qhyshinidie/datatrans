# 金融新闻标题问答数据集处理工具

这个工具用于处理 AdaptLLM/finance-tasks 数据集中的 Headline 子集，将其转换为结构化的问答对格式。

## 项目结构

```
finance_headline_dataset/
├── process_headline.py    # 主处理脚本
├── README.md             # 项目说明文档
└── output/               # 输出目录
    ├── headline_qa.json  # 处理后的问答对数据
    └── processing_report.json  # 处理报告
```

## 环境要求

- Python 3.8+
- datasets 库
- numpy
- pandas

## 安装依赖

```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ datasets numpy pandas
```

## 数据格式

### 输入格式
原始数据中的每个条目包含多个问答对，格式如下：
```
Q1: 问题1
A1: 答案1
Q2: 问题2
A2: 答案2
...
```

### 输出格式
处理后的数据以 JSON 格式保存，每个问答对包含以下字段：
```json
{
  "id": "001",
  "Question": "问题内容",
  "Answer": "答案内容",
  "type": "headline",
  "source": "AdaptLLM/finance-tasks"
}
```

## 使用方法

1. 进入项目目录：
```bash
cd finance_headline_dataset
```

2. 运行处理脚本：
```bash
python process_headline.py
```

3. 查看输出：
- 处理后的数据保存在 `output/headline_qa.json`
- 处理报告保存在 `output/processing_report.json`

## 处理报告

处理报告包含以下信息：
- 总问答对数量
- 处理时间（秒和分钟）
- 数据集信息

## 注意事项

- 确保有稳定的网络连接
- 如果遇到网络问题，可以尝试使用代理或更换网络环境
- 处理大量数据时可能需要一些时间，请耐心等待 