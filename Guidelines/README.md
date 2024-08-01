# START MONAI LABEL SERVER

For start a MONAI Label server follow this instructions:

(video)

The following commands in the videos was:

```
conda activate monailabel-env
```
Then:
```
monailabel start_server --app apps/radiology --studies datasets/Task02_Heart/imagesTr --conf models segmentation_Heart
```
