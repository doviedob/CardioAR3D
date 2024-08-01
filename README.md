# CardioAR3D
![facultad de ingenieria](https://github.com/doviedob/CardioAR3D/blob/main/Images/facultad%20de%20ingenieria.png)
![CardioVID](https://github.com/doviedob/CardioAR3D/blob/1c0741bccea0d52682b569b8c40b8656d9dd0d7c/Images/ClinicaCardioVID.png)

Internship project from Universidad de Antioquia for developed a 3D reconstruction process in pediatric patients with congenital heart disease.


### Table of Contents
- [Problematic](#problematic)
- [Main objective](#main-objective)
- [Specific objectives](#specific-objectives)
- [Workflow](#workflow)
- [Requirements](#requirements)
- [Results](#results)
- [Expected benefits](#expected-benefits)

## Problematic

- Prior to invasive procedures in interventional cardiology, it is difficult to understand the complex 3D anatomy of the heart from 2D images.
- Need for better visualization and diagnostic tools for the treatment of aortic coarctation.

## Main objective

- To develop a protocol for segmentation and visualization of 3D computed tomography images for diagnostic support of a congenital heart disease of interest to the CardioVID clinic.

## Specific objectives

- To construct a dataset of cardiac computed tomography images of subjects with aortic coarctation heart disease from the CardioVID clinic, considering inclusion and exclusion criteria by age and heart disease of interest.
- To develop a semi-automatic segmentation model for cardiac tomographic images in DICOM format using 3D Slicer software.
- To implement an interactive environment for the visualization and manipulation of cardiac 3D reconstructions.

## Workflow

The next image explain how there was the wrokflow for develop the project.
![flujo de trabajo](https://github.com/doviedob/CardioAR3D/blob/294b87ec044c39f94411f67d43ca546e443fc968/Images/Workflow.png)

## Requirements

- AWS Account
- EC2 instances with GPU. See the differents instances in [AWS page](https://docs.aws.amazon.com/dlami/latest/devguide/gpu.html)
- Conda
- 3D Slicer version 5.0 or later.
- 3D Slicer MONAI Label Plugin. (install step [here](https://docs.monai.io/projects/label/en/latest/quickstart.html#install-monai-label-plugin-in-3d-slicer))
- python 3.9
- Dataset
- Stable internet connection

## Results



https://github.com/user-attachments/assets/20eacfd9-8d51-4657-ab15-105aa07aeb42



## Expected benefits

- Better understanding of the anatomy of each individual's heart.
- More accurate procedure planning.
- Better outcomes for patients who have undergone heart surgery.
