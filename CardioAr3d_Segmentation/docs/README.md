# Model Overview
The model was trained from scratch for seven segments following the instruction from [MONAI Label tutorial](https://www.youtube.com/watch?v=3HTh2dqZqew)

### MONAI Label Showcase

### Data
The data was provided from internar using only

### Preprocessing

## Training Configuration

## Evaluation Configuration

### Memory Consumption

### Memory Consumption Warning

### Input

1 channel:
1. CT

### Output

7 channels:
1. Aorta
2. Miocardium
3. LA
4. LV
5. RA
6. RV
7. Pulmonar artery

## Resource Requirements and Latency Benchmarks

### GPU Consumption Warning

The model is trained with 104 classes in single instance, for predicting 104 structures, the GPU consumption can be large.

For inference pipeline, please refer to the following section for benchmarking results. Normally, a CT scans with 300 slices will take about 27G memory, if your CT is larger, please prepare larger GPU memory or use CPU for inference.

## Performance

#### TensorRT speedup
This bundle supports acceleration with TensorRT. The table below displays the speedup ratios observed on an A100 80G GPU.


## MONAI Bundle Commands
In addition to the Pythonic APIs, a few command line interfaces (CLI) are provided to interact with the bundle. The CLI supports flexible use cases, such as overriding configs at runtime and predefining arguments in a file.

For more details usage instructions, visit the [MONAI Bundle Configuration Page](https://docs.monai.io/en/latest/config_syntax.html).

#### Execute training:

```
python -m monai.bundle run --config_file configs/train.json
```

Please note that if the default dataset path is not modified with the actual path in the bundle config files, you can also override it by using `--dataset_dir`:

```
python -m monai.bundle run --config_file configs/train.json --dataset_dir <actual dataset path>
```

#### Override the `train` config to execute multi-GPU training:

```
torchrun --standalone --nnodes=1 --nproc_per_node=2 -m monai.bundle run --config_file "['configs/train.json','configs/multi_gpu_train.json']"
```

Please note that the distributed training-related options depend on the actual running environment; thus, users may need to remove `--standalone`, modify `--nnodes`, or do some other necessary changes according to the machine used. For more details, please refer to [pytorch's official tutorial](https://pytorch.org/tutorials/intermediate/ddp_tutorial.html).

#### Override the `train` config to execute evaluation with the trained model:

```
python -m monai.bundle run --config_file "['configs/train.json','configs/evaluate.json']"
```

#### Override the `train` config and `evaluate` config to execute multi-GPU evaluation:

```
torchrun --standalone --nnodes=1 --nproc_per_node=2 -m monai.bundle run --config_file "['configs/train.json','configs/evaluate.json','configs/multi_gpu_evaluate.json']"
```

#### Execute inference:

```
python -m monai.bundle run --config_file configs/inference.json
```
#### Execute inference with Data Samples:

```
python -m monai.bundle run --config_file configs/inference.json --datalist "['sampledata/imagesTr/s0037.nii.gz','sampledata/imagesTr/s0038.nii.gz']"
```

#### Export checkpoint to TensorRT based models with fp32 or fp16 precision:

```
python -m monai.bundle trt_export --net_id network_def --filepath models/model_trt.ts --ckpt_file models/model.pt --meta_file configs/metadata.json --config_file configs/inference.json --precision <fp32/fp16> --use_trace "True"
```

#### Execute inference with the TensorRT model:

```
python -m monai.bundle run --config_file "['configs/inference.json', 'configs/inference_trt.json']"
```


# References
