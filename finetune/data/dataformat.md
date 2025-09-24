# 数智岐黄训练数据目录

## 目录结构

```
data/
├── tcm_qa.json           # 中医药问答数据
├── medical_instruction.json  # 医学指令数据
├── tcm_corpus.json       # 中医药语料数据
├── medical_textbook.json # 医学教科书数据
├── clinical_notes.json   # 临床病历数据
└── dataset_info.json     # 数据集配置信息
```

## 数据格式说明

### 1. 问答数据格式 (tcm_qa.json)

```json
[
  {
    "conversations": [
      {
        "from": "human",
        "value": "什么是人参的功效和作用？"
      },
      {
        "from": "gpt",
        "value": "人参具有以下主要功效：\n1. 大补元气：适用于气虚欲脱、脉微欲绝的危重症候\n2. 复脉固脱：用于心力衰竭、休克等症\n3. 补脾益肺：治疗脾肺气虚证\n4. 生津止渴：用于津伤口渴、消渴症\n5. 安神益智：改善失眠健忘、心神不安..."
      }
    ]
  }
]
```

### 2. 指令数据格式 (medical_instruction.json)

```json
[
  {
    "instruction": "请分析以下症状的可能病因",
    "input": "患者主诉：头痛、发热、恶寒、无汗、脉浮紧",
    "output": "根据症状分析，患者可能患有外感风寒证：\n1. 头痛、恶寒提示外邪侵袭\n2. 发热无汗说明风寒束表，卫阳被遏\n3. 脉浮紧为风寒表证的典型脉象\n建议使用麻黄汤或荆防败毒散进行治疗..."
  }
]
```

### 3. 语料数据格式 (tcm_corpus.json)

```json
[
  {
    "text": "《黄帝内经》云：春三月，此谓发陈。天地俱生，万物以荣，夜卧早起，广步于庭，被发缓形，以使志生，生而勿杀，予而勿夺，赏而勿罚，此春气之应，养生之道也。逆之则伤肝，夏为寒变，奉长者少..."
  }
]
```

## 数据集配置 (dataset_info.json)

```json
{
  "tcm_qa": {
    "file_name": "tcm_qa.json",
    "file_sha1": "abc123...",
    "columns": {
      "messages": "conversations"
    },
    "tags": {
      "role_tag": "from",
      "content_tag": "value",
      "user_tag": "human",
      "assistant_tag": "gpt"
    }
  },
  "medical_instruction": {
    "file_name": "medical_instruction.json",
    "file_sha1": "def456...",
    "columns": {
      "prompt": "instruction",
      "query": "input", 
      "response": "output"
    }
  },
  "tcm_corpus": {
    "file_name": "tcm_corpus.json",
    "file_sha1": "ghi789...",
    "columns": {
      "text": "text"
    }
  }
}
```

## 数据准备指南

### 1. 中医药问答数据 (tcm_qa.json)
- 收集中医药相关的问答对
- 包括疾病诊断、治疗方法、药物功效等
- 确保回答的专业性和准确性

### 2. 医学指令数据 (medical_instruction.json)  
- 医学任务指令和对应回答
- 包括症状分析、诊断建议、治疗方案等
- 格式化为指令-输入-输出三元组

### 3. 中医药语料数据 (tcm_corpus.json)
- 中医古籍文本
- 现代中医教材内容
- 临床病历记录（去除敏感信息）

## 注意事项

1. **数据质量**：确保所有医学内容的准确性，避免错误信息
2. **隐私保护**：临床数据必须完全去标识化
3. **版权合规**：确保使用的文本资料符合版权要求
4. **数据平衡**：保持不同类型数据的合理比例
5. **格式规范**：严格按照指定格式准备数据


```
