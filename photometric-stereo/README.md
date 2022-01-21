The objective of this assignment is to recostruct the shape of the object by given images derived under 
the different light directions.
1. To run the project, conda environment is required. 
`conda create --name myenv --file requirements.txt`
command creates environment and installs all necessary dependencies.
2. Computations of the `p` and `q` coordinates of the gradient space of the normal
performed by `photometric_stereo` function imported from `utils.py` file into the `main.py` file. 
3. `utils.py` contains `plot_normal_map` and `plot_surface3d` functions to visualise the results. All output images are saved in the `outputs` folder.
4. For interactive visualization, plotly serves temporarily created html in offline mode. 
