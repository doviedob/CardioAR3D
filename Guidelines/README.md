# START MONAI LABEL SERVER

## 1. Manual mode

For start a MONAI Label server follow this instructions:


https://github.com/user-attachments/assets/48ac0284-734a-4029-b852-05e94460a6e0




The following commands in the videos was:

```
conda activate monailabel-env
```
Then:
```
monailabel start_server --app apps/radiology --studies datasets/Task02_Heart/imagesTr --conf models segmentation_Heart
```
## 2. Using GUI interface

You can download the [GUI](https://github.com/doviedob/CardioAR3D/tree/93e9a8f3a2c47617000d0fd41ee27f5504a73650/Guidelines/GUI) developed to establish the SSH connection and start MONAI Label server by entering the public EC2 IPv4. For more details, follow the instructions below:

(video)

