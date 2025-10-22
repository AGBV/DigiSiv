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

### Why This Project? / Warum dieses Projekt?

- 🎓 **Educational Focus**: Learn digital signal processing through hands-on, interactive examples
- 🌐 **Browser-Based**: No complex setup - everything runs in your web browser
- 🔬 **Real-Time Exploration**: Adjust parameters and see immediate visual feedback
- 📊 **Rich Visualizations**: Understanding complex concepts through clear plots and animations
- 🚀 **Performance Optimized**: Fast computations using scientific Python libraries

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

This project leverages powerful Python libraries for scientific computing and web applications:

[![Python][Python.org]][Python-url]
[![NumPy][NumPy.org]][NumPy-url]
[![Streamlit][Streamlit.io]][Streamlit-url]
[![Plotly][Plotly.com]][Plotly-url]
[![Numba][Numba.org]][Numba-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Features

- 🎯 **Interactive Exercises**: Hands-on signal processing exercises with real-time parameter adjustment
- 📊 **Visual Learning**: Rich visualizations using Plotly for better understanding
- 🚀 **Performance Optimized**: Uses Numba for fast numerical computations
- 🌐 **Browser-based**: No local setup required - run everything in your web browser
- 📚 **Educational**: Step-by-step solutions with explanations
- 🔄 **Real-time Updates**: See changes instantly as you adjust parameters
- 📱 **Responsive Design**: Works on desktop and mobile devices

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

<!-- GETTING STARTED -->

## Getting Started

To get the interactive exercises running locally, follow these simple steps.

### Prerequisites

- **Python 3.11** or higher
- **pip** or **uv** package manager (uv recommended for faster installations)

### Installation

1. **Clone the repository**

   ```sh
   git clone https://github.com/AGBV/DigiSiV.git
   cd DigiSiV
   ```

2. **Install dependencies**

   Using uv (recommended):

   ```sh
   uv install
   ```

   Or using pip:

   ```sh
   pip install -e .
   ```

3. **Run your first exercise**
   ```sh
   streamlit run exercise00/app.py
   ```

The application will open in your default web browser at `http://localhost:8501` 🚀

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- EXERCISES -->

## Exercises

### 📊 Repository Structure

```
DigiSiV/
├── exercise00/          # 🎨 Introduction: Complex number visualization
│   └── app.py          #    Interactive Mandelbrot Set explorer
├── MA2/                # ⚙️  Parameter effects on discretization
│   ├── app.py          #    Main Streamlit application
│   ├── functions.py    #    Signal processing helper functions
│   └── requirements.txt#    Exercise-specific dependencies
├── pyproject.toml      # 📦 Project configuration and dependencies
├── LICENSE             # 📄 MIT License
└── README.md           # 📖 This file
```

### 🎨 Exercise 0: Introduction to Complex Numbers

- **Topic**: Complex number visualization through fractals
- **Concepts**: Iterative algorithms, complex plane, mathematical visualization
- **Features**:
  - Interactive Mandelbrot Set exploration
  - Real-time parameter adjustment
  - High-performance computation with Numba
- **Run**: `streamlit run exercise00/app.py`

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

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->

## Usage

Each exercise is a standalone Streamlit application. Here's how to explore the different signal processing concepts:

### 🎨 Mandelbrot Set Visualization (Exercise 0)

```sh
streamlit run exercise00/app.py
```

- Explore complex number mathematics through beautiful fractal visualizations
- Adjust iteration parameters and zoom levels
- Learn about mathematical convergence and divergence

<!-- ### ⚙️ Discretization Analysis (Exercise MA2) -->
<!-- ```sh -->
<!-- streamlit run MA2/app.py -->
<!-- ``` -->
<!-- - Compare continuous and discrete signal processing systems -->
<!-- - Adjust system parameters (τ, ω, damping) and see real-time effects -->
<!-- - Visualize transfer functions and impulse responses -->
<!-- - Understand the implications of different discretization approaches -->

### 🛠️ Development Mode

For development with automatic reloading:

```sh
streamlit run --server.runOnSave true exercise00/app.py
```

_💡 **Tip**: Use the sidebar controls in each application to adjust parameters and explore different scenarios!_

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- DEVELOPMENT -->

## Development

### Adding New Exercises

1. **Create exercise directory**

   ```sh
   mkdir exercise01
   cd exercise01
   ```

2. **Create Streamlit app**

   ```python
   # exercise01/app.py
   import streamlit as st
   import numpy as np

   st.title("Your Exercise Title")
   # Your exercise implementation
   ```

3. **Update this README** with exercise description

### Project Setup with devenv (Optional)

This project supports [devenv](https://devenv.sh/) for reproducible development environments:

```sh
# Enter the development environment
direnv allow
```

### Dependencies

The project uses these core libraries:

- **NumPy**: Numerical computations and array operations
- **Plotly**: Interactive plotting and visualization
- **Streamlit**: Web application framework for Python
- **Numba**: Just-in-time compilation for performance optimization

See `pyproject.toml` for the complete dependency list.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

### English

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingExercise`)
3. Commit your Changes (`git commit -m 'Add some AmazingExercise'`)
4. Push to the Branch (`git push origin feature/AmazingExercise`)
5. Open a Pull Request

### Deutsch

Wenn Sie einen Vorschlag haben, der dies verbessern würde, forken Sie bitte das Repository und erstellen Sie einen Pull Request. Sie können auch einfach ein Issue mit dem Tag "Enhancement" öffnen.

**Ideas for contributions / Ideen für Beiträge:**

- 📚 Add new signal processing exercises
- 🐛 Fix bugs or improve existing implementations
- 📖 Enhance documentation or add German translations
- 🎨 Improve visualizations and user interface
- ⚡ Performance optimizations

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->

## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->

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

<p align="right">(<a href="#readme-top">back to top</a>)</p>

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
