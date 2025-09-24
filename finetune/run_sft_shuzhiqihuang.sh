#!/bin/bash

# 数智岐黄大语言模型 SFT 微调脚本
# 适用于中西医领域的监督微调

export WANDB_MODE=offline

# 配置参数
BASE_MODEL_PATH="/path/to/base/model"  # 基础模型路径，如Qwen2.5-14B
OUTPUT_DIR="./outputs/shuzhiqihuang-sft-$(date +%Y%m%d-%H%M%S)"
DATA_DIR="./data/sft"
CACHE_DIR="./cache"

# 训练参数
PER_DEVICE_BATCH_SIZE=4
GRADIENT_ACCUMULATION_STEPS=8
LEARNING_RATE=5e-5
NUM_EPOCHS=3
SAVE_STEPS=500
LOGGING_STEPS=10

# GPU配置 - 根据你的GPU数量调整
export CUDA_VISIBLE_DEVICES=0,1,2,3
NUM_GPUS=4

echo "开始数智岐黄模型SFT微调..."
echo "基础模型: $BASE_MODEL_PATH"
echo "输出目录: $OUTPUT_DIR"
echo "使用GPU: $CUDA_VISIBLE_DEVICES"

deepspeed --num_gpus=$NUM_GPUS --master_port=29500 src/train_bash.py \
    --deepspeed deepspeed_config.json \
    --stage sft \
    --model_name_or_path $BASE_MODEL_PATH \
    --do_train \
    --template qwen \
    --dataset_dir $DATA_DIR \
    --dataset tcm_qa,medical_instruction \
    --finetuning_type lora \
    --lora_target q_proj,v_proj,k_proj,o_proj,gate_proj,up_proj,down_proj \
    --lora_rank 64 \
    --lora_alpha 128 \
    --lora_dropout 0.05 \
    --output_dir $OUTPUT_DIR \
    --cache_dir $CACHE_DIR \
    --per_device_train_batch_size $PER_DEVICE_BATCH_SIZE \
    --gradient_accumulation_steps $GRADIENT_ACCUMULATION_STEPS \
    --lr_scheduler_type cosine \
    --logging_steps $LOGGING_STEPS \
    --preprocessing_num_workers 16 \
    --save_steps $SAVE_STEPS \
    --learning_rate $LEARNING_RATE \
    --num_train_epochs $NUM_EPOCHS \
    --max_samples 100000 \
    --per_device_eval_batch_size 4 \
    --evaluation_strategy steps \
    --eval_steps 500 \
    --max_grad_norm 1.0 \
    --warmup_steps 100 \
    --weight_decay 0.01 \
    --plot_loss \
    --overwrite_output_dir \
    --bf16 \
    --save_safetensors \
    --report_to none

echo "微调完成！模型保存在: $OUTPUT_DIR"
echo "可以使用以下命令合并LoRA权重:"
echo "bash merge_lora.sh $OUTPUT_DIR"
