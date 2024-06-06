# Opti'Find

Opti'Find is a school project produced by a group of 5 students from CESI engineering school. The goal of this project is to create a service to find a good solution to the Vehicle Routing Problem (VRP) using a our algorithm.

The project is composed of a Frontend part and a Backend part. The Frontend is a web application that allows the user to create a VRP instance and to visualize the solution. The Backend is ... that receives the VRP instance and returns the solution. There is also tools to generate VRP instances, to test the algorithm and to compare the results with other algorithms.

## Outline

- [Features](#features)
- [Folder organization](#folder-organization)
- [Installation](#installation)
  - [Requirements](#requirements)
  - [Installing](#installing)
- [Usage](#usage)
- [Contributors](#contributors)
- [License](#license)

## Features

## Folder organization

The project is organized in several folders:

- [`assets`](assets/): Contains the assets of the project (images, data, etc.).
- [`OptiFind_app`](OptiFind_app/): Contains the flask application of the project.
- [`reports`](reports/): Contains all the reports that we have to submit to our school in Jupyter Notebook format.
- [`src`](src/): Contains the backend part of the project.
- [`tests`](tests/): Contains the unit tests of the project.
- [`tools`](tools/): Contains the tools to generate VRP instances, to test the algorithm and to compare the results with other algorithms.

## Installation

### Installing

To install the project, you need to follow these steps:

1. Clone the repository:

```bash
git clone https://github.com/CESI-A3-Projet-AlgoAvan-C-Group/OptiFind.git
```

### Requirements

To install the project, you need to have the following tools installed on your machine:

- [Python](https://www.python.org/downloads/)
- [Pip](https://pypi.org/project/pip/)
- [Flask](https://flask.palletsprojects.com/en/2.0.x/)

You can install the required packages by running the following command:

```bash
pip install -r requirements.txt
```

## Usage

To use the project, you need to follow these steps:

1. Go to the `OptiFind_app` folder:

```bash
cd OptiFind_app
```

2. Run the Flask application:

```bash
flask --app views.py run
```

3. Open your browser and go to the following URL:

```
http://127.0.0.1:5000/
```

4. You can now use the web application to create a VRP instance and to visualize the solution.

## Contributors

- **[El Massi Imad](https://github.com/Imad-54)**
- **[Houille Lukas](https://github.com/lukas-houille)**
- **[Morel Romain](https://github.com/Roooomain)**
- **[Ritter Antoine](https://github.com/RitterAntoine)**
- **[Rouas Léo](https://github.com/Okamizz)**

## License

This software is the collective property of El Massi Imad, Houille Lukas, Morel Romain, Ritter Antoine, and Rouas Léo. It is strictly prohibited to copy, modify, distribute, or use this software without the explicit permission of all members of the group.

All rights reserved.