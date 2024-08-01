# START MONAI LABEL SERVER

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
