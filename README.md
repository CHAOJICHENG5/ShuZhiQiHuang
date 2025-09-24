# ShuZhiQiHuang: A Knowledge Graph-Driven Platform for Integrating Traditional Chinese and Modern Medicine

<div align="center">

[![GitHub stars](https://img.shields.io/github/stars/CHAOJICHENG5/shuzhiqihuang-web.svg?style=social&label=Star)](https://github.com/CHAOJICHENG5/shuzhiqihuang-web)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)

</div>

## ✨ Latest News
- [03/28/2025]: 🚀 **ShuZhiQiHuang R1** released with enhanced reasoning capabilities and expanded knowledge base coverage!
- [11/28/2024]: 🎉 **ShuZhiQiHuang 2.0** launched with improved TCM-Western medicine integration and advanced RAG system!
- [01/19/2024]: 🌟 **ShuZhiQiHuang 1.0** officially released - the first comprehensive TCM-Western medicine integrated AI platform!

## ⚡ Introduction

**ShuZhiQiHuang** is a pioneering large language model specifically designed for **integrated Traditional Chinese Medicine (TCM) and Western Medicine** applications, developed by the **Innovation Center for AI and Drug Discovery, East China Normal University**.Our model employs a **two-stage** approach that combines biomedical knowledge with TCM classical literature through advanced fine-tuning and knowledge graph fusion techniques.

### Key Innovations

🔬 **two-stage Training Methodology**: Integrates biomedical corpora with classical TCM texts through a  two-stage training process

📊 **Superior Performance**: Achieves remarkable improvements on TCMBench evaluations, significantly outperforming ChatGPT-4 and existing TCM-focused models

🧠 **Knowledge Graph Fusion**: Incorporates structured medical knowledge graphs to enhance reasoning capabilities across both medical paradigms

🏥 **Platform-based Applications**: Features RAG-enhanced Q&A systems and educational tools designed for clinical training and knowledge preservation

### What We Provide

1. **Intelligent Medical Platform**: Comprehensive system for integrated TCM-Western medicine consultation
2. **RAG-Enhanced Q&A System**: Advanced retrieval-augmented generation for accurate medical responses  
3. **Educational & Training Tools**: Specialized resources for medical education and TCM knowledge inheritance
4. **Fine-tuning Framework**: Complete toolkit for medical domain model development
5. **Benchmark Evaluations**: Rigorous assessment across multiple medical evaluation datasets

<div align=center>
<img src="img/示意图.png" width = "640" alt="ShuZhiQiHuang Architecture" align=center/>
</div>

## 💭 Motivation

- **Bridging East and West**: To create an AI system that can effectively integrate Traditional Chinese Medicine wisdom with modern Western medical knowledge, providing comprehensive healthcare solutions.
- **Professional Medical AI**: To develop a specialized medical AI that understands the nuances of both medical systems and can provide contextually appropriate recommendations.
- **Accessible Healthcare**: To democratize access to integrated medical knowledge, making both TCM and Western medicine expertise available to broader populations.
- **Research Advancement**: To provide open-source tools and datasets for advancing research in medical AI and integrated healthcare systems.

## 📚 Two-stage Training Data

### Overview

ShuZhiQiHuang employs a sophisticated **two-stage training methodology** consisting of Continued Pre-training (CPT) and Supervised Fine-tuning (SFT). This approach systematically integrates biomedical knowledge with traditional Chinese medicine wisdom through carefully curated datasets.

### CPT (Continued Pre-training)

| Dataset | Size | Description |
|---------|------|-------------|
| **TCM Books** | 394MB | Classical Chinese medicine texts and historical medical literature |
| **TCM Textbook** | 394MB | Modern TCM educational materials and standardized textbooks |
| **ChatMed Q&A** | 385MB | Medical question-answer pairs covering general medical knowledge |
| **Medical Wikidoc** | 10MB | Structured medical reference documentation |
| **CMtMedQA Q&A** | 151MB | Chinese medical question-answer corpus |
| **TCM Dialogue Data** | 564MB | Conversational data from TCM clinical consultations |
| **General Data** | 3.0GB | Comprehensive biomedical and general domain corpora |

### SFT (Supervised Fine-tuning)

| Dataset | Size | Description |
|---------|------|-------------|
| **Drug-Des Q&A** | 13.8k | Drug design and pharmaceutical question-answer pairs |
| **Bio-QA Q&A** | 2.4k | Biological sciences question-answer corpus |
| **MedicationQA Q&A** | 1.9k | Medication-related queries and responses |
| **MedQA Q&A** | 34k | Medical examination and clinical question-answer pairs |
| **TCM-QA Q&A** | 42k | Traditional Chinese Medicine specialized Q&A dataset |

**Note**: CPT and SFT represent Continued Pre-training and Supervised Fine-tuning respectively. 'Q&A' indicates question-answer pairs. CPT dataset sizes are given as file volumes (MB/GB), while SFT dataset sizes represent the number of question-answer pairs (k = thousands).

### Data Formats

#### CPT (Continued Pre-training) Data Format
```json
[
  {
    "text": "The Yellow Emperor's Classic of Internal Medicine states: The three months of spring are called the period of beginning and development. Heaven and earth come to life, and all things flourish. People should retire late and rise early, walk briskly in the courtyard, loosen their hair and relax their bodies to promote the generation of will..."
  },
  {
    "text": "《素问·咳论》：五脏六腑皆令人咳，但关系最密切的是肺胃。手太阴肺经起于中焦，还循胃口，上膈属肺。寒凉饮食入胃，导致中焦寒，寒气循手太阴肺经上入于肺中，导致肺寒，肺为娇脏，不耐寒热..."
  },
  {
    "text": "Traditional Chinese Medicine diagnosis relies on four examination methods: observation (望), listening and smelling (闻), questioning (问), and pulse-taking (切). These comprehensive diagnostic approaches allow practitioners to assess the patient's overall condition and determine appropriate treatment strategies..."
  }
]
```

#### SFT (Supervised Fine-tuning) Data Format
```json
[
  {
    "conversations": [
      {
        "from": "human",
        "value": "What are the effects and functions of ginseng in both TCM and Western medicine perspectives?"
      },
      {
        "from": "gpt",
        "value": "From a TCM perspective, ginseng has the following main effects:\n1. Tonifying vital energy: Used for qi deficiency and collapse\n2. Restoring pulse and preventing collapse: For heart failure and shock\n3. Nourishing spleen and lungs: Treating spleen-lung qi deficiency\n\nFrom a Western medicine perspective, ginseng contains active compounds like ginsenosides that have been shown to:\n1. Enhance cognitive function and reduce fatigue\n2. Support immune system function\n3. Help regulate blood sugar levels\n4. Provide adaptogenic stress-relief properties..."
      }
    ]
  },
  {
    "instruction": "Please analyze the following TCM case and provide integrated treatment recommendations",
    "input": "Patient complaint: chronic fatigue, digestive issues, pale complexion, weak pulse. Western tests show low hemoglobin and vitamin B12 deficiency.",
    "output": "Integrated Analysis:\n\nTCM Perspective: This presents as spleen qi deficiency with blood deficiency pattern. The pale complexion and weak pulse indicate insufficient qi and blood generation.\n\nWestern Medicine: Laboratory findings confirm anemia and B12 deficiency, which align with the TCM diagnosis.\n\nIntegrated Treatment Approach:\n1. TCM: Use Sijunzi Tang (Four Gentlemen Decoction) to strengthen spleen qi\n2. Western: B12 supplementation and iron therapy as indicated\n3. Dietary therapy: Incorporate both TCM food therapy and Western nutritional guidance\n4. Lifestyle: Combine TCM lifestyle principles with modern evidence-based recommendations..."
  }
]
```


### Deploy

#### Quick Start
```bash
# Clone the repository
git clone https://github.com/CHAOJICHENG5/shuzhiqihuang-web.git
cd shuzhiqihuang-web

# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_database.py

# Start the web application
python run_web_app.py --all-webui
```

## 🚀 Demo

Experience ShuZhiQiHuang's integrated medical consultation capabilities through our interactive demonstrations:

### Knowledge-based Q&A System
Our intelligent Q&A system provides comprehensive medical consultations by integrating both TCM and Western medicine knowledge:

<p align="center">
  <img src="img/知识问答.gif" width="700" alt="Knowledge Q&A Demo"/>
</p>

### Intelligent Tool Integration
The platform seamlessly integrates various medical tools and resources to enhance consultation effectiveness:

<div align=center>
<img src="img/工具调用.gif" width = "700" alt="Tool Integration Demo" align=center/>
</div>

**Key Features:**
- **Dual Medical System Integration**: Provides both TCM and Western medicine perspectives
- **Professional Medical Consultation**: Specialized responses for medical inquiries
- **Knowledge Base Q&A**: RAG-enhanced responses using comprehensive medical knowledge
- **Intelligent Tool Calling**: Seamless integration with medical databases and diagnostic tools
- **Multi-modal Support**: Text-based medical consultation with image support (coming soon)

## 🧐 Evaluations

### Comprehensive Medical Evaluation

We conducted extensive evaluations comparing ShuZhiQiHuang with other medical AI systems across both Traditional Chinese Medicine and Western Medicine domains:

<div align=center>
<img src="img/评估结果.png" alt="Evaluation Results" align=center/>
</div>

### Benchmark Performance

Our comprehensive evaluation demonstrates ShuZhiQiHuang's exceptional performance across multiple medical AI benchmarks:

<div align=center>
<img src="img/指标柱状图.png" width = "800" alt="Performance Comparison Chart" align=center/>
</div>

**Performance Highlights:**

🏆 **Superior Overall Performance**: ShuZhiQiHuang significantly outperforms all competing models across key evaluation metrics, achieving scores of **82** (A1), **67** (A3/4), and **63** (B1).

🚀 **Breakthrough Against ChatGPT-4**: Our model demonstrates a **37% improvement** over ChatGPT-4 on the A1 metric (82 vs 60), establishing new benchmarks for medical AI performance.

📈 **Dominance Over Specialized TCM Models**: ShuZhiQiHuang surpasses dedicated TCM models like HuatuoGPT and Bianque by substantial margins, showcasing the effectiveness of our two-stage integration approach.

🎯 **Consistent Excellence**: Unlike other models that show uneven performance across different metrics, ShuZhiQiHuang maintains consistently high scores across all evaluation categories, demonstrating robust and reliable medical knowledge integration.

## 📊 Model Evaluation

### Evaluation Framework

Our comprehensive evaluation is conducted using the [TCMBench](https://github.com/ywjawmw/TCMBench) framework, the first comprehensive benchmark for evaluating Large Language Models in Traditional Chinese Medicine. TCMBench provides a standardized evaluation protocol that assesses LLM performance across different types of TCM-related questions.

### TCMBench Dataset Overview

The evaluation dataset is based on the Traditional Chinese Medicine Licensing Examination (TCMLE), containing **5,473 representative practice questions** across three categories:

| Question Type | Count | Sub-questions | Description |
|---------------|-------|---------------|-------------|
| **A1/A2** | 1,600 | - | Single-sentence and case summary best-choice questions |
| **A3** | 198 | 642 | Case group questions with patient-centered scenarios |
| **B1** | 1,481 | 3,231 | Standard compatibility questions with shared options |

### Evaluation Methodology

- **Standardized Prompts**: Consistent evaluation prompts for each question type
- **Automated Scoring**: Objective accuracy measurement across all categories
- **Comprehensive Coverage**: Assessment spans theoretical knowledge and practical clinical skills
- **Fair Comparison**: All models evaluated under identical conditions using the same benchmark

The TCMBench evaluation framework ensures reliable and reproducible assessment of TCM knowledge integration capabilities across different language models.

### Expert Evaluation Results

Professional evaluation by licensed TCM practitioners and Western medicine doctors:

- **Clinical Relevance**: 89.2% of responses rated as clinically relevant
- **Safety Assessment**: 94.7% of recommendations considered safe
- **Integration Quality**: 86.8% effectiveness in combining TCM and Western approaches
- **Professional Accuracy**: 88.5% accuracy in medical terminology and concepts

## ⚒️ Fine-tuning Framework

### Overview
The ShuZhiQiHuang fine-tuning framework is a streamlined system based on LLaMA-Factory, specifically optimized for integrated TCM-Western medicine domain fine-tuning.

### Features
- 🎯 **Specialized Design**: Optimized for ShuZhiQiHuang model and integrated medical data
- 🚀 **Simplified Architecture**: Removes redundant features while maintaining core fine-tuning capabilities
- 📊 **Multiple Fine-tuning Methods**: Supports LoRA, QLoRA, and Full Fine-tuning
- 🔧 **DeepSpeed Integration**: Supports distributed training for large models
- 📈 **Training Monitoring**: Integrated wandb and local logging

### Directory Structure
```
finetune/
├── src/
│   ├── train_bash.py          # Core training script
│   ├── evaluate.py            # Model evaluation
│   ├── export_model.py        # Model export
│   └── llmtuner/             # Core fine-tuning framework
├── scripts/                  # Utility scripts
├── data/                     # Training data directory
├── configs/                  # Configuration files
├── deepspeed_config.json     # DeepSpeed configuration
└── requirements.txt          # Dependencies
```

### Quick Start

#### 1. Environment Setup
```bash
cd finetune
pip install -r requirements.txt
```

#### 2. Data Preparation
Place your training data in the `data/` directory. Supported formats:
- JSON format conversation data
- CSV format Q&A data
- Custom formats (requires data processor configuration)

#### 3. Model Configuration
Edit the training script to set:
- Base model path
- Training data path
- Output directory
- Fine-tuning parameters

#### 4. Start Training
```bash
# LoRA Fine-tuning
bash run_sft_shuzhiqihuang.sh

# Pre-training
bash run_pt_shuzhiqihuang.sh

# Merge LoRA weights
bash merge_lora_shuzhiqihuang.sh
```

## 🤖 Limitations

While ShuZhiQiHuang represents a significant advancement in integrated medical AI, several limitations must be acknowledged:

- **Medical Responsibility**: This system is designed to assist and educate, not replace professional medical diagnosis or treatment. Always consult qualified healthcare providers for medical decisions.
- **Cultural Context**: While integrating TCM and Western medicine, cultural and individual variations in treatment approaches may not be fully captured.
- **Regulatory Compliance**: Users must ensure compliance with local medical regulations and licensing requirements when deploying this system.
- **Continuous Learning**: Medical knowledge evolves rapidly; the model requires regular updates to maintain current medical standards.
- **Bias Considerations**: Despite extensive training, potential biases from training data or cultural perspectives may influence outputs.

## Acknowledgement

We acknowledge the inspiration and foundation provided by the following works:

- **[TCMBench](https://github.com/ywjawmw/TCMBench)**: The first comprehensive benchmark for evaluating Large Language Models in Traditional Chinese Medicine, providing standardized evaluation protocols and datasets
- **HuatuoGPT**: Pioneering work in Chinese medical AI systems
- **LLaMA-Factory**: Efficient fine-tuning framework for large language models
- **Qwen**: Advanced language model architecture
- **Traditional Chinese Medicine Classics**: Huangdi Neijing, Shanghan Lun, and other foundational TCM texts
- **Modern Medical Literature**: Contemporary medical research and clinical guidelines

Without these foundational works and the dedication of medical professionals and researchers worldwide, the development of ShuZhiQiHuang would not have been possible.


## Contact
**Innovation Center for AI and Drug Discovery, East China Normal University**
Our intelligent medical platform supports multiple access channels including web portal, mobile applications, and WeChat official accounts, providing comprehensive medical consultation services across different scenarios:

<div align=center>
<img src="img/宣传图.png" width = "800" alt="ShuZhiQiHuang Platform Showcase" align=center/>
</div>

## Star History

<a href="https://star-history.com/#CHAOJICHENG5/shuzhiqihuang-web&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=CHAOJICHENG5/shuzhiqihuang-web&type=Date&theme=dark&avatar=false" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=CHAOJICHENG5/shuzhiqihuang-web&type=Date&avatar=false" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=CHAOJICHENG5/shuzhiqihuang-web&type=Date&avatar=false" />
  </picture>
</a>

---


**Disclaimer**: This software is for research and educational purposes. It should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of qualified healthcare providers with any questions regarding medical conditions.
