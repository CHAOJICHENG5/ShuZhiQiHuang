"""
数智岐黄微调框架安装脚本
"""

import os
import re
from setuptools import find_packages, setup


def get_version():
    """获取版本号"""
    try:
        with open(os.path.join("src", "llmtuner", "__init__.py"), "r", encoding="utf-8") as f:
            file_content = f.read()
            pattern = r"{0}\W*=\W*\"([^\"]+)\"".format("__version__")
            version_match = re.search(pattern, file_content)
            if version_match:
                return version_match.group(1)
    except FileNotFoundError:
        pass
    return "1.0.0"  # 默认版本


def get_requires():
    """获取依赖包列表"""
    with open("requirements.txt", "r", encoding="utf-8") as f:
        file_content = f.read()
        lines = [line.strip() for line in file_content.strip().split("\n") 
                if line.strip() and not line.startswith("#")]
        return lines


# 数智岐黄专用的额外依赖
extra_require = {
    "deepspeed": ["deepspeed>=0.13.1"],
    "metrics": ["nltk", "jieba", "rouge-chinese"],
    "vllm": ["vllm>=0.3.0"],
    "bitsandbytes": ["bitsandbytes>=0.39.0"],
    "gptq": ["optimum>=1.16.0", "auto-gptq>=0.5.0"],
    "awq": ["autoawq"],
    "qwen": ["tiktoken", "transformers_stream_generator"],
    "medical": ["medicalai", "tcm-tools"],  # 中医药专用工具
    "quality": ["ruff", "black"],
}


def main():
    setup(
        name="shuzhiqihuang-finetune",
        version=get_version(),
        author="ShuZhi QiHuang Team",
        author_email="team@shuzhiqihuang.com",
        description="数智岐黄大语言模型微调框架",
        long_description=open("README.md", "r", encoding="utf-8").read(),
        long_description_content_type="text/markdown",
        keywords=["数智岐黄", "中西医融合", "医药", "大语言模型", "微调", "TCM", "Western Medicine", "LLM", "Fine-tuning"],
        license="Apache 2.0 License",
        url="https://github.com/shuzhiqihuang/shuzhiqihuang-web",
        package_dir={"": "src"},
        packages=find_packages("src"),
        python_requires=">=3.8.0",
        install_requires=get_requires(),
        extras_require=extra_require,
        classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "Intended Audience :: Education",
            "Intended Audience :: Science/Research",
            "Intended Audience :: Healthcare Industry",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Topic :: Scientific/Engineering :: Artificial Intelligence",
            "Topic :: Scientific/Engineering :: Medical Science Apps",
        ],
        entry_points={
            "console_scripts": [
                "shuzhiqihuang-train=llmtuner.train.tuner:main",
                "shuzhiqihuang-eval=llmtuner.eval.evaluator:main",
                "shuzhiqihuang-export=llmtuner.extras.export:main",
            ],
        },
    )


if __name__ == "__main__":
    main()
