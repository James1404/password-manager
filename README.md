<a id="readme-top"></a>


<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

# Password Manager

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project

A password manager for CS1032, by James Barnfather.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

* Python 3.12

### Installation

#### Linux
Use:
```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Or:
```sh
make init
```

#### Windows
```sh
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
```

<!-- USAGE -->
## Usage

```sh
python main.py
```

or

```sh
make run
```

<!-- ROADMAP -->
## Roadmap

- [ ] Add a GUI using QT6
- [ ] Improve encryption safety

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/James1404/password-manager.svg?style=for-the-badge
[contributors-url]: https://github.com/James1404/password-manager/graphs/contributors
[stars-shield]: https://img.shields.io/github/stars/James1404/password-manager.svg?style=for-the-badge
[stars-url]: https://github.com/James1404/password-manager/stargazers
[issues-shield]: https://img.shields.io/github/issues/James1404/password-manager.svg?style=for-the-badge
[issues-url]: https://github.com/James1404/password-manager/issues
[license-shield]: https://img.shields.io/github/license/James1404/password-manager.svg?style=for-the-badge
[license-url]: https://github.com/James1404/password-manager/blob/master/LICENSE.txt
