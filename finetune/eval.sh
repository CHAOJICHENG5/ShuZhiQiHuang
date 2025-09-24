#!/bin/bash

# 设置CUDA可见设备
export CUDA_VISIBLE_DEVICES=0

# 运行Python脚本
python evaluate.py \
    --model_name_or_path /path/to/model_path \
    --template vanilla \
    --task ceval \
    --split validation \
    --lang zh \
    --n_shot 5 \
    --batch_size 4