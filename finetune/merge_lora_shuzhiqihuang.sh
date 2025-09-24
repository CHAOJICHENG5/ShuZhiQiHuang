#!/bin/bash

# 数智岐黄模型LoRA权重合并脚本

if [ $# -eq 0 ]; then
    echo "用法: $0 <LoRA模型路径> [基础模型路径] [输出路径]"
    echo "示例: $0 ./outputs/shuzhiqihuang-sft-20241201-120000"
    exit 1
fi

LORA_PATH=$1
BASE_MODEL_PATH=${2:-"/path/to/base/model"}  # 默认基础模型路径
OUTPUT_PATH=${3:-"${LORA_PATH}/merged_model"}  # 默认输出路径

echo "开始合并数智岐黄LoRA权重..."
echo "LoRA路径: $LORA_PATH"
echo "基础模型: $BASE_MODEL_PATH"
echo "输出路径: $OUTPUT_PATH"

python src/export_model.py \
    --model_name_or_path $BASE_MODEL_PATH \
    --adapter_name_or_path $LORA_PATH \
    --template qwen \
    --finetuning_type lora \
    --export_dir $OUTPUT_PATH \
    --export_size 2 \
    --export_device cpu \
    --export_legacy_format false

echo "LoRA权重合并完成！"
echo "合并后的模型保存在: $OUTPUT_PATH"
echo ""
echo "现在可以使用VLLM部署合并后的模型："
echo "python -m vllm.entrypoints.openai.api_server \\"
echo "    --model $OUTPUT_PATH \\"
echo "    --host 0.0.0.0 \\"
echo "    --port 7843 \\"
echo "    --served-model-name shuzhiqihuang"
