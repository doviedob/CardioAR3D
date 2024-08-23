# CardioAR3D

<div style="display: flex; justify-content: center; align-items: center; gap: 10px;">
  <img src="https://github.com/doviedob/CardioAR3D/blob/main/Images/facultad%20de%20ingenieria.png" width="410" height="150" alt="UdeA">
  <img src="https://github.com/doviedob/CardioAR3D/blob/1c0741bccea0d52682b569b8c40b8656d9dd0d7c/Images/ClinicaCardioVID.png" width="410" height="150" alt="CardioVID">
</div>

Internship project from Universidad de Antioquia for developed a 3D reconstruction process in pediatric patients with congenital heart disease. This application is based on the radiology [MONAI sample app](https://github.com/Project-MONAI/MONAILabel/tree/main/sample-apps/radiology) and was modified for the segmentation for main anatomy of heart on CT Scans.


### Table of Contents
- [Problematic](#problematic)
- [Main objective](#main-objective)
- [Specific objectives](#specific-objectives)
- [Workflow](#workflow)
- [Requirements](#requirements)
- [Results](#results)
- [Expected benefits](#expected-benefits)
- [Document](#document)
- [Acknowledgments](#acknowledgments)

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
- CUDA Toolkit
- Dataset
- Stable internet connection

## Results

The performance of the trained model and the complete workflow as designed can be seen with a real case in the following video:

https://github.com/user-attachments/assets/68bf4563-3b9e-4968-aa4f-706311e7e5ad

Additionally, two inference results can be seen below:

<img src="https://github.com/user-attachments/assets/ca0957dc-20a2-4419-92b5-7bfdff1e7293" width="400" height="300" style="float: left;"/> <img src="https://github.com/user-attachments/assets/383b5e8f-a407-4dce-b55d-817a5d2fa881" width="400" height="300" align="right"/>


## Expected benefits

- Better understanding of the anatomy of each individual's heart.
- More accurate procedure planning.
- Better outcomes for patients who have undergone heart surgery.

## Document

The complete formal document of the development of this academic internship project is available in the public repository of the University of Antioquia.

## Acknowledgments

This project uses [MONAI Label](https://github.com/Project-MONAI/MONAILabel), an open source medical image labeling platform. If you use this software in your research, please cite the following article:

*Diaz-Pinto, A., Alle, S., Ihsani, A., et al. (2022). MONAI Label: A framework for AI-assisted Interactive Labeling of 3D Medical Images. arXiv e-prints. [arXiv:2203.12362](https://arxiv.org/pdf/2203.12362.pdf)*

or use the BibTeX below:

```
@article{DiazPinto2022monailabel,
   author = {Diaz-Pinto, Andres and Alle, Sachidanand and Ihsani, Alvin and Asad, Muhammad and
            Nath, Vishwesh and P{\'e}rez-Garc{\'\i}a, Fernando and Mehta, Pritesh and
            Li, Wenqi and Roth, Holger R. and Vercauteren, Tom and Xu, Daguang and
            Dogra, Prerna and Ourselin, Sebastien and Feng, Andrew and Cardoso, M. Jorge},
    title = {{MONAI Label: A framework for AI-assisted Interactive Labeling of 3D Medical Images}},
  journal = {arXiv e-prints},
     year = 2022,
     url  = {https://arxiv.org/pdf/2203.12362.pdf}
}
```
