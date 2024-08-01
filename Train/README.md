Among the results found, the first data to be analyzed were the different training sessions to which the model was subjected, varying the number of epochs in each training session, in order to find a value of difference between the training Dice and adequate validation. 

The percentage difference between the "Final Train Mean Dice" and the "Final Val Mean Dice". This will help to quantify possible over-adjustment in each phase of training.


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
