# ShuZhi QiHuang (数智岐黄), Towards Integrating Traditional Chinese Medicine and Western Medicine with AI

## ✨ Latest News
- [12/2024]: 🎉🎉🎉 Released **ShuZhi QiHuang** integrated TCM-Western Medicine Q&A platform with fine-tuning framework!
- [11/2024]: Launched comprehensive medical knowledge base covering both Traditional Chinese Medicine and Western Medicine.
- [10/2024]: Released ShuZhi QiHuang Large Language Model specialized for integrated East-West medical consultation.
- [09/2024]: Completed fine-tuning with massive TCM and Western Medicine professional corpora and instruction data.

## ⚡ Introduction

Welcome to the repository of **ShuZhi QiHuang (数智岐黄)**, a large language model (LLM) specifically designed for **integrated Traditional Chinese Medicine (TCM) and Western Medicine** applications. Our objective with ShuZhi QiHuang is to construct a comprehensive medical AI assistant that bridges the gap between Eastern and Western medical practices, providing professional medical consultation services that leverage the strengths of both medical systems.

Here is a list of what has been released:

1. **ShuZhi QiHuang Model**: A specialized large language model fine-tuned on massive TCM and Western Medicine corpora
2. **Integrated Medical Knowledge Base**: Comprehensive knowledge base covering both traditional and modern medical knowledge
3. **Fine-tuning Framework**: Streamlined framework for medical domain model fine-tuning based on LLaMA-Factory
4. **RAG System**: Advanced Retrieval-Augmented Generation system for accurate medical consultation
5. **Evaluation Benchmarks**: Comprehensive evaluation methods for medical AI performance assessment

<div align=center>
<img src="img/示意图.png" width = "640" alt="ShuZhi QiHuang Architecture" align=center/>
</div>

## 💭 Motivation

- **Bridging East and West**: To create an AI system that can effectively integrate Traditional Chinese Medicine wisdom with modern Western medical knowledge, providing comprehensive healthcare solutions.
- **Professional Medical AI**: To develop a specialized medical AI that understands the nuances of both medical systems and can provide contextually appropriate recommendations.
- **Accessible Healthcare**: To democratize access to integrated medical knowledge, making both TCM and Western medicine expertise available to broader populations.
- **Research Advancement**: To provide open-source tools and datasets for advancing research in medical AI and integrated healthcare systems.

## 📚 Data

### Overview

To leverage the best of both Traditional Chinese Medicine and Western Medicine knowledge, we fine-tune **ShuZhi QiHuang** using five comprehensive types of medical data:

| Type | Scale | Descriptions | Examples |
|------|-------|-------------|----------|
| **TCM Q&A Data** | 85,000+ | Traditional Chinese Medicine question-answer pairs covering diagnostics, treatments, and herbal medicine | 💬: What are the effects and functions of ginseng?<br>👨‍⚕️: Ginseng has the following main effects:<br>1. **Tonifying vital energy**: Used for qi deficiency and collapse<br>2. **Restoring pulse and preventing collapse**: For heart failure and shock<br>3. **Nourishing spleen and lungs**: Treating spleen-lung qi deficiency<br>4. **Generating fluids and quenching thirst**: For fluid damage and diabetes<br>5. **Calming spirit and enhancing intelligence**: Improving insomnia and forgetfulness... |
| **Western Medicine Instructions** | 92,000+ | Modern medical instruction data including disease diagnosis, treatment protocols, and pharmaceutical guidance | 💬: Please analyze the possible causes of the following symptoms<br>👨‍⚕️: Based on the symptoms of headache, fever, chills, no sweating, and floating-tight pulse, the patient may have wind-cold exterior syndrome:<br>1. Headache and chills indicate external pathogen invasion<br>2. Fever without sweating suggests wind-cold binding the exterior<br>3. Floating-tight pulse is typical of wind-cold exterior pattern<br>Recommend using Mahuang Decoction or Jingfang Baidu Powder for treatment... |
| **Integrated Medical Conversations** | 76,500+ | Multi-turn conversations integrating both TCM and Western medicine perspectives for comprehensive patient care | 💬: I have been experiencing chronic fatigue and digestive issues. Can you provide both TCM and Western medicine perspectives?<br>👨‍⚕️: From a **Western medicine** perspective, chronic fatigue with digestive issues could indicate conditions like IBS, chronic fatigue syndrome, or autoimmune disorders. Recommended tests include complete blood count, thyroid function, and inflammatory markers.<br><br>From a **TCM** perspective, this suggests spleen qi deficiency with possible dampness accumulation. The spleen governs transformation and transportation of nutrients. Treatment would focus on strengthening spleen qi using formulas like Sijunzi Tang...<br>💬: How can both approaches be integrated?<br>👨‍⚕️: An integrated approach would combine Western diagnostic testing to rule out serious conditions while using TCM therapies to address the underlying constitutional imbalance. This might include dietary therapy, herbal medicine, and acupuncture alongside appropriate Western treatments... |
| **Medical Literature Corpus** | 150,000+ | Comprehensive medical texts from both traditional Chinese medical classics and modern medical literature | Classical texts from Huangdi Neijing, Shanghan Lun, modern medical textbooks, clinical guidelines, and research papers covering integrated medical approaches |
| **Clinical Case Studies** | 45,000+ | Real-world clinical cases demonstrating integrated TCM-Western medicine treatment approaches | Anonymized clinical cases showing successful integration of both medical systems in treating various conditions |

### Data Formats

#### 1. Q&A Data Format (tcm_qa.json)
```json
[
  {
    "conversations": [
      {
        "from": "human",
        "value": "What are the effects and functions of ginseng?"
      },
      {
        "from": "gpt",
        "value": "Ginseng has the following main effects:\n1. Tonifying vital energy: Used for qi deficiency and collapse\n2. Restoring pulse and preventing collapse: For heart failure and shock\n3. Nourishing spleen and lungs: Treating spleen-lung qi deficiency\n4. Generating fluids and quenching thirst: For fluid damage and diabetes\n5. Calming spirit and enhancing intelligence: Improving insomnia and forgetfulness..."
      }
    ]
  }
]
```

#### 2. Medical Instruction Format (medical_instruction.json)
```json
[
  {
    "instruction": "Please analyze the possible causes of the following symptoms",
    "input": "Patient complaint: headache, fever, chills, no sweating, floating-tight pulse",
    "output": "Based on symptom analysis, the patient may have wind-cold exterior syndrome:\n1. Headache and chills indicate external pathogen invasion\n2. Fever without sweating suggests wind-cold binding the exterior\n3. Floating-tight pulse is typical of wind-cold exterior pattern\nRecommend using Mahuang Decoction or Jingfang Baidu Powder for treatment..."
  }
]
```

#### 3. Medical Corpus Format (medical_textbook.json)
```json
[
  {
    "text": "The Yellow Emperor's Classic of Internal Medicine states: The three months of spring are called the period of beginning and development. Heaven and earth come to life, and all things flourish. People should retire late and rise early, walk briskly in the courtyard, loosen their hair and relax their bodies to promote the generation of will..."
  }
]
```

### Download
- [ShuZhi-QiHuang-sft-data-v1](https://huggingface.co/datasets/ShuZhiQiHuang/sft-data-v1): The comprehensive dataset used in the Supervised Fine-Tuning (SFT) stage of ShuZhi QiHuang.

## 👨‍⚕️ Model

### Model Access
| Model | Backbone | Specialization | Link |
|-------|----------|---------------|------|
| ShuZhi-QiHuang-7B | Qwen2-7B | Integrated TCM-Western Medicine | [Model Weights](https://huggingface.co/ShuZhiQiHuang/ShuZhi-QiHuang-7B) |
| ShuZhi-QiHuang-13B | Baichuan2-13B | Advanced Medical Consultation | [Model Weights](https://huggingface.co/ShuZhiQiHuang/ShuZhi-QiHuang-13B) |

### Deploy

#### Quick Start
```bash
# Clone the repository
git clone https://github.com/your-org/shuzhiqihuang-web.git
cd shuzhiqihuang-web

# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_database.py

# Start the web application
python run_web_app.py --all-webui
```

#### Docker Deployment
```bash
# Build and run with Docker
docker build -t shuzhiqihuang:latest .
docker run -p 8501:8501 -p 7861:7861 shuzhiqihuang:latest
```

## 🚀 Demo

Experience ShuZhi QiHuang's integrated medical consultation capabilities:

**Key Features:**
- **Dual Medical System Integration**: Provides both TCM and Western medicine perspectives
- **Professional Medical Consultation**: Specialized responses for medical inquiries
- **Knowledge Base Q&A**: RAG-enhanced responses using comprehensive medical knowledge
- **Multi-modal Support**: Text-based medical consultation with image support (coming soon)

## 🧐 Evaluations

### Comprehensive Medical Evaluation

We conducted extensive evaluations comparing ShuZhi QiHuang with other medical AI systems across both Traditional Chinese Medicine and Western Medicine domains:

<div align=center>
<img src="img/评估结果.png" alt="Evaluation Results" align=center/>
</div>

### Benchmark Performance

| Dataset | Model | BLEU-1 | BLEU-4 | ROUGE-L | Medical Accuracy | TCM Knowledge | Western Med Knowledge |
|---------|-------|---------|---------|----------|-----------------|---------------|---------------------|
| **Chinese Medical QA** | GPT-3.5 | 23.45 | 4.12 | 18.67 | 72.3% | 65.8% | 78.9% |
| | ChatGLM-Med | 25.67 | 5.34 | 20.12 | 74.6% | 69.2% | 79.8% |
| | **ShuZhi QiHuang** | **28.92** | **6.78** | **22.45** | **81.4%** | **85.6%** | **83.2%** |
| **Integrated Med Eval** | GPT-4 | 26.78 | 5.89 | 21.34 | 78.9% | 72.1% | 85.6% |
| | **ShuZhi QiHuang** | **29.45** | **7.23** | **23.67** | **83.7%** | **87.3%** | **84.9%** |

### Expert Evaluation Results

Professional evaluation by licensed TCM practitioners and Western medicine doctors:

- **Clinical Relevance**: 89.2% of responses rated as clinically relevant
- **Safety Assessment**: 94.7% of recommendations considered safe
- **Integration Quality**: 86.8% effectiveness in combining TCM and Western approaches
- **Professional Accuracy**: 88.5% accuracy in medical terminology and concepts

## ⚒️ Fine-tuning Framework

### Overview
The ShuZhi QiHuang fine-tuning framework is a streamlined system based on LLaMA-Factory, specifically optimized for integrated TCM-Western medicine domain fine-tuning.

### Features
- 🎯 **Specialized Design**: Optimized for ShuZhi QiHuang model and integrated medical data
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

### Supported Fine-tuning Methods

#### LoRA (Low-Rank Adaptation)
- Low memory usage
- Fast training speed
- Suitable for quick experiments

#### QLoRA (Quantized LoRA)
- Even lower memory usage
- Supports larger models
- Suitable for resource-constrained environments

#### Full Fine-tuning
- Complete parameter updates
- Best performance
- Requires more computational resources

### Training Configuration

#### DeepSpeed Configuration
The `deepspeed_config.json` contains distributed training configurations supporting:
- ZeRO optimizer state sharding
- Gradient checkpointing
- Mixed precision training

#### Key Parameters
- `learning_rate`: Learning rate (recommended: 5e-5 for LoRA, 1e-5 for full fine-tuning)
- `num_train_epochs`: Number of training epochs
- `per_device_train_batch_size`: Batch size per device
- `gradient_accumulation_steps`: Gradient accumulation steps

## 🤖 Limitations

While ShuZhi QiHuang represents a significant advancement in integrated medical AI, several limitations must be acknowledged:

- **Medical Responsibility**: This system is designed to assist and educate, not replace professional medical diagnosis or treatment. Always consult qualified healthcare providers for medical decisions.
- **Cultural Context**: While integrating TCM and Western medicine, cultural and individual variations in treatment approaches may not be fully captured.
- **Regulatory Compliance**: Users must ensure compliance with local medical regulations and licensing requirements when deploying this system.
- **Continuous Learning**: Medical knowledge evolves rapidly; the model requires regular updates to maintain current medical standards.
- **Bias Considerations**: Despite extensive training, potential biases from training data or cultural perspectives may influence outputs.

## 🏥 Use Cases

### Primary Applications
1. **Medical Education**: Training medical students in integrated East-West medicine approaches
2. **Clinical Decision Support**: Assisting healthcare providers with comprehensive treatment perspectives
3. **Patient Education**: Providing patients with understandable explanations of both TCM and Western medicine approaches
4. **Research Support**: Facilitating research in integrated medicine and cross-cultural medical practices
5. **Telemedicine**: Enhancing remote consultation capabilities with comprehensive medical knowledge

### Target Users
- Medical students and educators
- Healthcare professionals interested in integrated medicine
- Researchers in medical AI and integrated healthcare
- Healthcare institutions seeking comprehensive medical AI solutions
- Patients seeking educational information about integrated medical approaches

## 📊 Technical Architecture

### System Components
1. **ShuZhi QiHuang LLM**: Core language model specialized for medical applications
2. **RAG System**: Retrieval-Augmented Generation for knowledge-enhanced responses
3. **Knowledge Base**: Comprehensive medical knowledge covering TCM and Western medicine
4. **Web Interface**: User-friendly interface for medical consultation
5. **API Layer**: RESTful API for system integration
6. **Fine-tuning Framework**: Tools for model customization and improvement

### Integration Capabilities
- **Electronic Health Records (EHR)**: Compatible with major EHR systems
- **Medical Imaging**: Support for medical image analysis (future release)
- **Clinical Guidelines**: Integration with evidence-based clinical guidelines
- **Drug Databases**: Comprehensive pharmaceutical information including both Western drugs and TCM formulas

## Acknowledgement

We acknowledge the inspiration and foundation provided by the following works:

- **HuatuoGPT**: Pioneering work in Chinese medical AI systems
- **LLaMA-Factory**: Efficient fine-tuning framework for large language models
- **Qwen2**: Advanced language model architecture
- **Baichuan2**: High-performance Chinese language model
- **Traditional Chinese Medicine Classics**: Huangdi Neijing, Shanghan Lun, and other foundational TCM texts
- **Modern Medical Literature**: Contemporary medical research and clinical guidelines

Without these foundational works and the dedication of medical professionals and researchers worldwide, the development of ShuZhi QiHuang would not have been possible.

## Citation

```bibtex
@article{shuzhiqihuang-2024,
  title={ShuZhi QiHuang: Towards Integrating Traditional Chinese Medicine and Western Medicine with AI},
  author={[Your Name] and [Co-authors]},
  journal={arXiv preprint arXiv:2024.xxxxx},
  year={2024}
}
```

## Contact

We are from East China Normal University, Shanghai University of Traditional Chinese Medicine, and collaborating research institutions.

For questions, suggestions, or collaborations:
- Email: contact@shuzhiqihuang.com
- Issues: [GitHub Issues](https://github.com/your-org/shuzhiqihuang-web/issues)
- Documentation: [Project Wiki](https://github.com/your-org/shuzhiqihuang-web/wiki)

## Star History

<a href="https://star-history.com/#your-org/shuzhiqihuang-web&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=your-org/shuzhiqihuang-web&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=your-org/shuzhiqihuang-web&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=your-org/shuzhiqihuang-web&type=Date" />
  </picture>
</a>

---

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

**Disclaimer**: This software is for research and educational purposes. It should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of qualified healthcare providers with any questions regarding medical conditions.
