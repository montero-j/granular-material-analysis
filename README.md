## Granular Flow and Clogging

This repository contains code and data for the investigation of clogging in granular materials, using a combination of experimental and computational techniques. The project focuses on understanding the mechanisms leading to the formation of clogs and developing predictive models for this phenomenon.

### Objectives

* **Experimental Analysis:** Study the clogging phenomenon in 3D experiments using high-speed cameras to acquire detailed data on granular material flow.
* **Numerical Simulation:**
    * Analyze the impact of particle mixing on discharge flow in 3D silos using LIGGGHTS simulations.
    * Study avalanche dynamics in 2D and 3D silos using LIGGGHTS, varying particle properties, and applying the Pi theorem for dimensionless avalanche size analysis.
    * Investigate the effect of two fixed particles at the 2D silo orifice on discharge flow, varying the distance between the particles and the orifice.
* **Statistical Analysis:** Apply statistical and dimensional analysis techniques (Pi theorem) to extract relevant information from experimental and simulation data.
* **Model Development:** Create predictive models based on the data and analyses performed to predict the formation of clogs in different scenarios.

### Methodology

The project employs a multidisciplinary methodology that combines:

* **High-Speed Imaging:** Use of high-speed cameras to capture detailed flow dynamics in 3D experiments.
* **Particle Dynamics Simulation:** Use of LIGGGHTS to simulate the behavior of granular materials in silos and other systems, varying parameters such as system geometry, particle properties, and flow conditions.
* **Dimensional Analysis:** Application of the Pi theorem to identify relevant dimensionless parameters and scale simulation and experimental results.
* **Statistical Analysis:** Use of statistical techniques to analyze data and extract significant patterns and relationships.

### Repository Contents

The repository is organized into the following main directories:

* **`data/`**: Contains the experimental and simulation data used in the project.
    * **`experimental/`**: 3D Experimental data, from high speed cameras.
    * **`simulations/`**: 2D and 3D simulations data.
* **`src/`**: Contains the project's source code, including scripts for data acquisition and analysis, as well as configuration and post-processing scripts for LIGGGHTS simulations.
* **`docs/`**: Contains project documentation, including detailed descriptions of experiments and simulations.
