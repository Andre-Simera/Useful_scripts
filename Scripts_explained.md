# Stereo Vision

## Calibration

-The *Calibration.py* script takes in the calibration images as input and use then to get the intrinsic parameters of each camera i.e. the camera matrix and the distortion coefficients. It then use these intrinsic parameters to determine the extrinsic parameters of the stereo camera system.

-These intrinsic and extrinsic parameters are then save into a *.npz* file for use in the rectification process.

-Only the *Intrinsic_&_Extrinsic_parameters.npz* file has been uploaded and not the calibration images.

## Rectification

The *Rectification.py* script reads in the paramters from the *Intrinsic_&_Extrinsic_parameters.npz* file.



## Disparity Map
