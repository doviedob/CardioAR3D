# SimplifiedMONAILabel for 3D Slicer

## Overview

SimplifiedMONAILabel is a streamlined extension for 3D Slicer that integrates MONAI Label functionality, making it easier for users to leverage machine learning models for medical image segmentation focused only on **inference**. This extension simplifies the process of loading, segmenting, and interacting with medical images using pre-trained MONAI Label models using EC2 instances from AWS.

![image](https://github.com/user-attachments/assets/908e6f77-4b3b-4fc9-ad21-79f46786a0b2)


## Features

- User-friendly interface for model selection and image loading
- Seamless integration with remote MONAI Label servers
- Support for various medical image formats (NIFTI, NRRD, etc.)
- Real-time segmentation visualization and editing
- Advanced configuration options for experienced users

## Installation

1. Open 3D Slicer
2. Go to "Extension Wizard" -> "Select Extension" -> "SimplifiedMONAILabel"
3. Click "Add" and select the SimplifiedMONAILabel directory
4. Restart 3D Slicer

## Usage

1. Launch 3D Slicer and load your medical image
2. Open the SimplifiedMONAILabel module. Found it in "Segmentation" 
3. Connect to a MONAI Label server. You can use the following [guides](https://github.com/doviedob/CardioAR3D/blob/6790ebee79949a4466d8ee2db891c6ac7fb14708/Guidelines/README.md)
4. Select a segmentation model
5. Run the segmentation
6. View and edit results as needed

## Requirements

- 3D Slicer (version 5.0 or higher)
- Active internet connection for remote server functionality
- EC2 instances from AWS with MONAI Label installed

## Configuration

Users can adjust various settings through the module's interface, including:
- Server URL
- Model selection
- Segmentation parameters

## Contributing

Contributions to SimplifiedMONAILabel are welcome! Please refer to the CONTRIBUTING.md file for guidelines on how to submit issues, feature requests, and code changes.

## License

This project is licensed under the Apache 2.0 License - see the LICENSE.md file for details.

## Acknowledgments

- MONAI Label team for the original implementation
- 3D Slicer community for their extensive documentation and support

## Contact

For questions or support, please open an issue in this repository.
