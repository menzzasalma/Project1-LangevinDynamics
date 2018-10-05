=============================
Project 1 - Langevin Dynamics
=============================


.. image:: https://img.shields.io/pypi/v/menzzasalma_langevin.svg
        :target: https://pypi.python.org/pypi/menzzasalma_langevin

.. image:: https://img.shields.io/travis/menzzasalma/menzzasalma_langevin.svg
        :target: https://travis-ci.org/menzzasalma/menzzasalma_langevin

.. image:: https://readthedocs.org/projects/menzzasalma-langevin/badge/?version=latest
        :target: https://menzzasalma-langevin.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




CHE 477 - Project 1 - Langevin Dynamics model


* Free software: MIT license

Description
--------
This is a function that attempts to model the motion of a particle undergoing one-dimensional Brownian motion. Given a set of initial conditions and positional boundaries, it will calculate the drag and random forces on a particle, then log and visualize this data. 

Features
--------
- Accepts all the following inputs from the command line:
        - temperature
        - total_time
        - time_step
        - initial_position
        - initial_velocity
        - damping_coefficient
- Returns the final position and velocity of the particle to the command line
- Returns a text file with the instantaneous velocity and instantaneous position of a particle at every specified time step.
- Returns a histogram with the number of trials that ended in a particle hitting the wall in each one second time interval
- Returns a .png file with the trajectory of a particle that collides with the opposite wall

How to Install
--------
To install this program, perform a git clone on this repository. 

``
git clone git@github.com:menzzasalma/Project1-LangevinDynamics
``

How to Use
--------
To use the program, navigate to the folder titled "Project1-LangevinDynamics" Using your command line. It should contain the program file, menzzasalma_langevin.py.

Then, run 
``
python menzzasalma_langevin.py
``
This can be followed by using any of the accepted inputs, which can be seen in the "Features" section. This will update these values in the program. Any or all of them can be used at once, just initialize them with two hyphens. For example:
``
python menzzasalma_langevin.py --temperature 500 --total_time 1000 --initial_velocity 2
``

These inputs must be numbers (floats or integers); strings will return an error. 



Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
