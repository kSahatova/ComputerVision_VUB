# computer_vision_VUB

Task 1. Camera calibration and axes reconstruction

All computations take place in the `camera_calibration.py` file where by means of `utils.py` camera parameters are calculated. If the file runs directly, we receive two images in the `output` directory with depicted camera axes for left and right image, respectively. `xy_left.txt` and `xy_right.txt` contain precomputed points on the corresponding images; both files were derived by `get_points.py`. To resolve a remaining part of the task, `Image` class was defined to pass necessary information about the parameters of each camera.  

Task 2. Triangulation

This part of the 3d reconstruction task was elaborated in the `triangulation.py` file. Running the script, we calculate the 3D coordinate for each pair of the corresponding points using the projection matrix of each camera. All estimated points write down to the file `estimatedPoints3D.txt` in the output directory if MSE on the first given points is less that 1. These points are estimations with a depth coordination. 
Finally, all objects of the proposed scene were reconstructed in the `plot3D.ipynb`. 
