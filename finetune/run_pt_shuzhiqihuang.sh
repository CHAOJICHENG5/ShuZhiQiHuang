#!/bin/bash

# 数智岐黄大语言模型预训练脚本
# 适用于中西医领域的大规模语料预训练

export WANDB_MODE=offline

# 配置参数
BASE_MODEL_PATH="/path/to/base/model"  # 基础模型路径
OUTPUT_DIR="./outputs/shuzhiqihuang-pt-$(date +%Y%m%d-%H%M%S)"
DATA_DIR="./data"
CACHE_DIR="./cache"

# 训练参数
PER_DEVICE_BATCH_SIZE=8
GRADIENT_ACCUMULATION_STEPS=4
LEARNING_RATE=1e-4
NUM_EPOCHS=1
SAVE_STEPS=1000
LOGGING_STEPS=10

# GPU配置 - 根据你的GPU数量调整
export CUDA_VISIBLE_DEVICES=0,1,2,3
NUM_GPUS=4

echo "开始数智岐黄模型预训练..."
echo "基础模型: $BASE_MODEL_PATH"
echo "输出目录: $OUTPUT_DIR"
echo "使用GPU: $CUDA_VISIBLE_DEVICES"

deepspeed --num_gpus=$NUM_GPUS --master_port=29501 src/train_bash.py \
    --deepspeed deepspeed_config.json \
    --stage pt \
    --model_name_or_path $BASE_MODEL_PATH \
    --do_train \
    --template qwen \
    --dataset_dir $DATA_DIR \
    --dataset tcm_corpus,medical_textbook,clinical_notes \
    --finetuning_type lora \
    --lora_target q_proj,v_proj,k_proj,o_proj,gate_proj,up_proj,down_proj \
    --lora_rank 128 \
    --lora_alpha 256 \
    --lora_dropout 0.1 \
    --output_dir $OUTPUT_DIR \
    --cache_dir $CACHE_DIR \
    --per_device_train_batch_size $PER_DEVICE_BATCH_SIZE \
    --gradient_accumulation_steps $GRADIENT_ACCUMULATION_STEPS \
    --lr_scheduler_type cosine \
    --logging_steps $LOGGING_STEPS \
    --preprocessing_num_workers 24 \
    --save_steps $SAVE_STEPS \
    --learning_rate $LEARNING_RATE \
    --num_train_epochs $NUM_EPOCHS \
    --max_samples 1000000 \
    --max_seq_length 2048 \
    --max_grad_norm 1.0 \
    --warmup_steps 500 \
    --weight_decay 0.01 \
    --plot_loss \
    --overwrite_output_dir \
    --bf16 \
    --save_safetensors \
    --report_to none

echo "预训练完成！模型保存在: $OUTPUT_DIR"
echo "可以使用以下命令合并LoRA权重:"
echo "bash merge_lora.sh $OUTPUT_DIR"
