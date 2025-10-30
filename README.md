<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->

<a id="readme-top"></a>

<!--
*** DigiSiV - Digital Signal Processing Interactive Exercises
*** Educational repository for "Digitale Signalverarbeitung" course
*** Built with Python, Streamlit, and scientific computing libraries
-->

<!-- PROJECT SHIELDS -->

[![MIT License][license-shield]][license-url]
[![Python][python-shield]][python-url]
[![Streamlit][streamlit-shield]][streamlit-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h1 align="center">🎛️ DigiSiV</h1>
  <h3 align="center">Digitale Signalverarbeitung (Digital Signal Processing)</h3>

  <p align="center">
    Interactive exercises and solutions for Digital Signal Processing concepts
    <br />
    <em>Interaktive Übungen und Lösungen für Konzepte der digitalen Signalverarbeitung</em>
    <br />
    <br />
    <a href="#getting-started"><strong>Get Started / Erste Schritte »</strong></a>
    <br />
    <br />
    <a href="#exercises">View Exercises</a>
    &middot;
    <a href="https://github.com/AGBV/DigiSiV/issues">Report Bug</a>
    &middot;
    <a href="https://github.com/AGBV/DigiSiV/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
        <li><a href="#features">Features</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#exercises">Exercises</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#development">Development</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

This repository contains **interactive solutions and exercises** for the German course **"Digitale Signalverarbeitung"** (Digital Signal Processing). All solutions are implemented in **Python** and made interactive using **Streamlit**, allowing you to explore signal processing concepts directly in your browser.

**🇩🇪 Deutsch:** Dieses Repository enthält **interaktive Lösungen und Übungen** für den Kurs **"Digitale Signalverarbeitung"**. Alle Lösungen sind in **Python** implementiert und mit **Streamlit** interaktiv gestaltet, sodass Sie die Konzepte der Signalverarbeitung direkt im Browser erkunden können.

### Built With

[![Python][Python.org]][Python-url]
[![NumPy][NumPy.org]][NumPy-url]
[![Streamlit][Streamlit.io]][Streamlit-url]
[![Plotly][Plotly.com]][Plotly-url]
[![Numba][Numba.org]][Numba-url]

## Getting Started

To get the interactive exercises running locally, follow these simple steps.

### Prerequisites

- **Python 3.11** or higher
- **uv** (recommended) or **pip** package manager

### Installation

We provide multiple installation methods. **uv is recommended** for faster and more reliable dependency management, but traditional pip methods are also supported.

#### Option 1: Using uv (Recommended) ⚡

**uv** is a fast Python package installer and resolver. If you don't have it installed:

```sh
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh
# or
pip install uv
```

Then install the project:

```sh
# Clone the repository
git clone https://github.com/AGBV/DigiSiV.git
cd DigiSiV

# Install all dependencies
uv install

# Run exercises directly with uv
uv run streamlit run exercise00/app.py
uv run streamlit run exercise01/m1.py
```

#### Option 2: Using pip with Virtual Environment 🐍

```sh
# Clone the repository
git clone https://github.com/AGBV/DigiSiV.git
cd DigiSiV

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install from pyproject.toml (recommended)
pip install -e .

# OR install from requirements.txt
pip install -r requirements.txt

# Run exercises
streamlit run exercise00/app.py
streamlit run exercise01/m1.py
```

#### Option 3: Global pip Installation (Not Recommended)

```sh
# Clone the repository
git clone https://github.com/AGBV/DigiSiV.git
cd DigiSiV

# Install globally from requirements.txt
pip install -r requirements.txt

# Run exercises
streamlit run exercise00/app.py
streamlit run exercise01/m1.py
```

### Quick Start

Once installed, choose your exercise and run it:

**For complex number visualization:**
```sh
# With uv (recommended)
uv run streamlit run exercise00/app.py

# With pip (in activated venv)
streamlit run exercise00/app.py
```

**For audio signal processing:**
```sh
# With uv (recommended) 
uv run streamlit run exercise01/m1.py

# With pip (in activated venv)
streamlit run exercise01/m1.py
```

The application will open in your default web browser at `http://localhost:8501` 🚀

### Development Mode

For development with automatic reloading when files change:

```sh
# With uv
uv run streamlit run --server.runOnSave true exercise00/app.py

# With pip
streamlit run --server.runOnSave true exercise00/app.py
```

_💡 **Tip**: Use the sidebar controls in each application to adjust parameters and explore different scenarios!_

<!-- EXERCISES -->

## Exercises

### 📊 Repository Structure

```
DigiSiV/
├── exercise00/          # 🎨 Introduction: Complex number visualization
│   └── app.py          #    Interactive Mandelbrot Set explorer
├── exercise01/          # 🎵 Audio Signal Processing
│   ├── m1.py           #    Interactive audio analysis app
│   ├── M1.ipynb        #    Jupyter notebook with detailed analysis
│   └── audio01.wav     #    Sample audio file
├── MA2/                # ⚙️  Parameter effects on discretization
│   ├── app.py          #    Main Streamlit application
│   ├── functions.py    #    Signal processing helper functions
│   └── requirements.txt#    Exercise-specific dependencies
├── pyproject.toml      # 📦 Project configuration and dependencies
├── LICENSE             # 📄 MIT License
└── README.md           # 📖 This file
```

### 🎨 Exercise 0: Introduction to Complex Numbers

- **File**: `exercise00/app.py`
- **Topic**: Complex number visualization through fractals
- **Concepts**: Iterative algorithms, complex plane, mathematical visualization
- **Features**:
  - Interactive Mandelbrot Set exploration with customizable parameters
  - Real-time parameter adjustment (max iterations, pixel resolution)
  - High-performance computation with Numba JIT compilation
  - Beautiful fractal visualization using Plotly heatmaps
  - Smooth color gradients and zoom capabilities
- **Run**: `streamlit run exercise00/app.py`

### 🎵 Exercise 1: Audio Signal Processing

- **Files**: `exercise01/m1.py` (Streamlit app), `exercise01/M1.ipynb` (Jupyter notebook)
- **Topic**: Time and frequency domain analysis of audio signals
- **Concepts**: Digital audio processing, FFT, frequency spectrum analysis, sampling
- **Features**:
  - Interactive audio file upload or use default sample
  - Time-domain signal visualization with adjustable time windows
  - Frequency spectrum analysis using Fast Fourier Transform (FFT)
  - Half/full spectrum display options
  - Real-time parameter adjustment for signal analysis
- **Sample Audio**: Includes `audio01.wav` for testing
- **Run**: `streamlit run exercise01/m1.py`

<!-- ### ⚙️ Exercise MA2: Discretization Parameter Effects -->

<!-- - **Topic**: Understanding how discretization parameters affect signal processing systems -->
<!-- - **Concepts**: Continuous vs. discrete systems, transfer functions, impulse responses -->
<!-- - **Features**: -->
  <!-- - Interactive parameter adjustment (τ, ω, damping) -->
  <!-- - Real-time comparison between continuous and discrete systems -->
  <!-- - Multiple system configurations -->
  <!-- - Dynamic plotting and analysis -->
<!-- - **Run**: `streamlit run MA2/app.py` -->
<!-- - **Link**: [Exercise Details](https://github.com/AGBV/DigiSiV/tree/main/MA2) -->


## Usage

### Running Exercises

```sh
# With uv (recommended)
uv run streamlit run exercise00/app.py  # Complex number visualization
uv run streamlit run exercise01/m1.py   # Audio signal processing

# With pip (in activated virtual environment)  
streamlit run exercise00/app.py  # Complex number visualization
streamlit run exercise01/m1.py   # Audio signal processing
```

### Development Mode

For automatic reloading when files change:

```sh
# With uv
uv run streamlit run --server.runOnSave true exercise00/app.py

# With pip  
streamlit run --server.runOnSave true exercise00/app.py
```

_💡 **Tip**: Use the sidebar controls in each application to adjust parameters and explore different scenarios!_

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- DEVELOPMENT -->

## Development

### Adding New Exercises

1. **Create exercise directory**

   ```sh
   mkdir exercise02
   cd exercise02
   ```

2. **Create Streamlit app**

   ```python
   # exercise02/app.py
   import streamlit as st
   import numpy as np

   st.title("Your Exercise Title")
   # Your exercise implementation
   ```

3. **Test your new exercise**

   ```sh
   # With uv
   uv run streamlit run exercise02/app.py
   
   # With pip (in venv)
   streamlit run exercise02/app.py
   ```

4. **Update this README** with exercise description

### Project Setup with devenv (Optional)

This project supports [devenv](https://devenv.sh/) for reproducible development environments:

```sh
# Enter the development environment
direnv allow
```

### Package Management

**Dependencies:**
- **NumPy**: Numerical computations and array operations
- **Plotly**: Interactive plotting and visualization  
- **Streamlit**: Web application framework for Python
- **Numba**: Just-in-time compilation for performance optimization
- **SciPy**: Scientific computing functions

**Configuration files:**
- `pyproject.toml`: Modern Python project configuration (preferred)
- `requirements.txt`: Traditional pip requirements (auto-generated from uv)
- `uv.lock`: Exact dependency versions for reproducible installs

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingExercise`)
3. Commit your Changes (`git commit -m 'Add some AmazingExercise'`)
4. Push to the Branch (`git push origin feature/AmazingExercise`)
5. Open a Pull Request

**Ideas for contributions:**
- 📚 Add new signal processing exercises
- 🐛 Fix bugs or improve existing implementations
- 📖 Enhance documentation or add German translations
- 🎨 Improve visualizations and user interface
- ⚡ Performance optimizations

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgments

Resources and inspiration that made this project possible:

- 📚 **Course**: Digitale Signalverarbeitung (Digital Signal Processing)
- 🐍 [Python](https://python.org) - The foundation of our implementations
- 🚀 [Streamlit](https://streamlit.io) - Making Python apps beautiful and interactive
- 📊 [Plotly](https://plotly.com) - Powerful interactive visualizations
- 🔢 [NumPy](https://numpy.org) - Fundamental package for scientific computing
- ⚡ [Numba](https://numba.pydata.org) - High-performance Python compiler
- 🎨 [Shields.io](https://shields.io) - Beautiful README badges
- 📖 [Best README Template](https://github.com/othneildrew/Best-README-Template) - Inspiration for this README

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[license-shield]: https://img.shields.io/github/license/AGBV/DigiSiV.svg?style=for-the-badge
[license-url]: https://github.com/AGBV/DigiSiV/blob/main/LICENSE
[python-shield]: https://img.shields.io/badge/python-3.11+-blue.svg?style=for-the-badge&logo=python&logoColor=white
[python-url]: https://www.python.org/downloads/
[streamlit-shield]: https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white
[streamlit-url]: https://streamlit.io/
[Python.org]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://python.org/
[NumPy.org]: https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white
[NumPy-url]: https://numpy.org/
[Streamlit.io]: https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white
[Streamlit-url]: https://streamlit.io/
[Plotly.com]: https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white
[Plotly-url]: https://plotly.com/
[Numba.org]: https://img.shields.io/badge/Numba-00A3E0?style=for-the-badge&logo=numba&logoColor=white
[Numba-url]: https://numba.pydata.org/
