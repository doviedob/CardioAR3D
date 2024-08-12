# TRAIN MODEL

The model was trained from scratch for seven segments following the instruction from [MONAI Label tutorial](https://www.youtube.com/watch?v=3HTh2dqZqew)

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

## Training configuration

The training as performed with the following:

* GPU: At least 32GB of GPU memory
* Actual Model Input: 96 x 96 x 96
* AMP: True
* Optimizer: Adam
* Learning Rate: 2e-4
### Memory Consumption
* Dataset Manager: CacheDataset
* Data Size: 20 samples
* Cache Rate: 1.0
* Single GPU - System RAM Usage: 5.8G


## Proccess

Among the results found, the first data to be analyzed were the different training sessions to which the model was subjected, varying the number of epochs in each training session, in order to find a value of difference between the training Dice and adequate validation. 

The percentage difference between the "Final Train Mean Dice" and the "Final Val Mean Dice". This will help to quantify possible over-adjustment in each phase of training.

The [stats](https://github.com/doviedob/CardioAR3D/tree/40111595c041a0acef9993db7efbe8b76ade23d6/Train/Stats) resume was present in the table below:

| Epochs | Training Time | Best Val Epoch | Best Val Mean Dice | Final Train Mean Dice | Final Val Mean Dice | Train-Val Difference (%) |
|:------:|:---------:|:----:|:----------------:|:------:|:------:|:------:|
| 50 | 00:11:47 | 44 | 0.4239 | 0.2654 | 0.4099 | -54.45% | 
| 200 | 00:23:40 | 200 | 0.1589 | 0.0393 | 0.1589 | -304.33% | 
| 500 | 00:57:45 | 438 | 0.6066 | 0.5934 | 0.5430 | 8.49% | 
| 800 | 01:31:25 | 763 | 0.6420 | 0.7098 | 0.5718 | 19.44% | 
| 1200 | 02:18:16 | 1183 | 0.6711 | 0.8567 | 0.5584 | 34.82% | 

***Note: Training times were calculated by running on NVIDIA A10g graphics on an EC2 instance of AWS.***

From 500 epochs onwards, positive percentages begin to be observed, indicating that training performance exceeds validation performance. This is more typical and may suggest the onset of overfitting. The difference between training and validation performance grows steadily from 500 to 1200 epochs:
- At 500 epochs: 8.49% difference.
- At 800 epochs: 19.44% difference
- At 1200 epochs: 34.82% difference

The increase in percentage difference suggests that the overfitting is more pronounced as training progresses. At 1200 epochs, the training performance is 34.82% better than the validation performance, which is a significant difference.

For this reason, it was decided to choose the model trained on **800 epochs** as the most optimal among the experiments performed.

## Performance

The model's performance was assessed using a dice score. The mean dice score achieved by this model is 0.66.

### Training Mean Dice
![image](https://github.com/user-attachments/assets/d513c11d-6fe2-44b6-a05d-9c3f00530be2)

### Training Loss
![image](https://github.com/user-attachments/assets/33ef1a3b-6479-4662-85e7-d16c5f151d1d)

### Validation Mean Dice
![image](https://github.com/user-attachments/assets/34542050-5e18-43c6-87cb-1b33e55206e9)
![image](https://github.com/user-attachments/assets/c2680a19-d9de-4da8-8fbe-011fbc2e68a9)


## References

aa

## License

bb
