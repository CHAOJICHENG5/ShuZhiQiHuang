# 数智岐黄大语言模型微调框架

## 概述

这是数智岐黄大语言模型的专用微调框架，基于LLaMA-Factory简化而来，专门针对中西医融合医药领域的模型微调需求进行优化。

## 功能特色

- 🎯 **专业化设计**：专门针对数智岐黄模型和中西医融合医药数据优化
- 🚀 **简化架构**：去除冗余功能，保留核心微调能力
- 📊 **多种微调方式**：支持LoRA、QLoRA、Full Fine-tuning等
- 🔧 **DeepSpeed集成**：支持大模型分布式训练
- 📈 **训练监控**：集成wandb和本地日志监控

## 目录结构

```
finetune/
├── src/
│   ├── train_bash.py          # 核心训练脚本
│   ├── evaluate.py            # 模型评估
│   ├── export_model.py        # 模型导出
│   └── llmtuner/             # 核心微调框架
│       ├── data/             # 数据处理模块
│       ├── model/            # 模型处理模块
│       ├── train/            # 训练逻辑模块
│       ├── hparams/          # 超参数配置
│       └── extras/           # 工具函数
├── scripts/                  # 工具脚本
├── data/                     # 训练数据目录
├── configs/                  # 配置文件
├── deepspeed_config.json     # DeepSpeed配置
└── requirements.txt          # 依赖包
```

## 快速开始

### 1. 环境准备

```bash
cd finetune
pip install -r requirements.txt
```

### 2. 数据准备

将你的训练数据放入 `data/` 目录，支持格式：
- JSON格式的对话数据
- CSV格式的问答数据
- 自定义格式（需要配置数据处理器）

### 3. 配置模型

编辑训练脚本，设置：
- 基础模型路径
- 训练数据路径
- 输出目录
- 微调参数

### 4. 开始训练

```bash
# LoRA微调
bash run_sft_shuzhiqihuang.sh

# 预训练
bash run_pt_shuzhiqihuang.sh
```

## 支持的微调方式

### LoRA (Low-Rank Adaptation)
- 内存占用少
- 训练速度快
- 适合快速实验

### QLoRA (Quantized LoRA)
- 更低的内存占用
- 支持更大的模型
- 适合资源受限环境

### Full Fine-tuning
- 完整参数更新
- 最佳性能
- 需要更多计算资源

## 配置说明

### DeepSpeed配置
`deepspeed_config.json` 包含分布式训练的配置，支持：
- ZeRO优化器状态分片
- 梯度检查点
- 混合精度训练

### 训练参数
主要参数包括：
- `learning_rate`: 学习率
- `num_train_epochs`: 训练轮数
- `per_device_train_batch_size`: 批次大小
- `gradient_accumulation_steps`: 梯度累积步数

## 数据格式

### 对话数据格式
```json
[
  {
    "conversations": [
      {
        "from": "human",
        "value": "什么是人参的功效？"
      },
      {
        "from": "gpt", 
        "value": "人参具有大补元气、复脉固脱、补脾益肺、生津止渴、安神益智的功效..."
      }
    ]
  }
]
```

### 问答数据格式
```json
[
  {
    "instruction": "请介绍一下当归的药用价值",
    "input": "",
    "output": "当归是常用的中药材，具有补血活血、调经止痛、润肠通便的功效..."
  }
]
```

## 注意事项

1. **数据质量**：确保训练数据的专业性和准确性
2. **计算资源**：根据可用GPU内存调整批次大小
3. **训练监控**：关注loss变化和验证集性能
4. **模型保存**：定期保存检查点，防止训练中断

## 常见问题

### Q: 如何选择合适的学习率？
A: 建议从5e-5开始，根据loss变化调整。LoRA微调通常需要较高的学习率。

### Q: 训练过程中出现OOM怎么办？
A: 减少batch_size，增加gradient_accumulation_steps，或启用DeepSpeed ZeRO。

### Q: 如何评估微调效果？
A: 使用验证集监控perplexity，或在下游任务上测试性能。


