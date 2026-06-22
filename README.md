# Overview

[[_TOC_]]

This repository contains the code for the paper "".

<details> <summary> paper abstract </summary>
Applying control methods to water distribution systems requires suitable system models. 
The elastic water column model, which has been expanded to incorporate dynamic elements like pumps and valves, is a promising model for control applications due to its formulation in state-space form. However, the model has so far only been validated numerically. The presented work implements the elastic water column model with dynamic elements for water distribution systems in Python and applies it to a small-scale physical test rig. The experimental results are compared with the simulation results to show that the EWCM-DE implementation is a suitable tool for real-time control. 
</details>



The implementation of the elastic water column model with dynamic elements is in the directory `test_rig_control_model`. The directory `notebooks` contains jupyter notebooks corresponding to the scenarios introduced in the aforementioned paper:



## Getting Started
### Clone this repository wherever you want to have it
Clone this repository using

:warning: ADJUST THIS LINK
```bash
git clone git@git.rwth-aachen.de:fst-tuda/projects/emergencity/resilince-demonstrator/test-rig-control-model.git
```



### Create a virtual environment and install requirements
#### Microsoft Windows
On Windows, open VS Code and open a terminal. In the terminal, run

```cmd
py -m venv env
```
to create a virtual environment called `env`.


Activate the virtual environment:

```cmd
.\env\Scripts\activate
```

You can confirm you’re in the virtual environment by checking the location of your Python interpreter:

```cmd
# for cmd run
where python
# for powershell run
where.exe python
```
Install the packages in the `requirements.txt` file using the -r flag:

```cmd
py -m pip install -r requirements.txt
```

Note for jupyter notebooks: To use the created virtual environment `env` , you will need to select it as the kernel. VS Code sometimes has trouble finding newly created virtual environments. To solve this issue, open Command Palette in VS Code and execute `Developer: Reload Window`. After that, the `env` should be listed in the list of kernels. 

#### GNU/Linux and Apple macOS
On Linux distributions (Ubuntu, Raspberry Pi OS, etc.), run

```cmd
python3 -m venv env
```
To create the virtual environment.

```cmd
source ./env/bin/activate
```
To activate a virtual environment.

```cmd
which python3
```
To check the location of your Python interpreter.

```cmd
python3 -m pip install -r requirements.txt
```
To install the packages in the `requirements.txt`.
