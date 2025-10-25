# Stable Diffusion - Text to Image

A sleek, self-contained web interface for experimenting with the Stability AI SD3.5-Flash model. This app provides a user-friendly UI to control key generation parameters and includes features like style presets, dark/light mode, and a random prompt generator.

![Project Screenshot](static/asset/screenshot.png)

---

## 🌟 Features

* **SD3.5-Flash Engine:** Directly connects to the high-speed `sd3.5-flash` model via the Stability AI API.
* **Full Parameter Control:**
    * **Prompt & Negative Prompt:** Full text support.
    * **Style Presets:** A dropdown of all 17 supported styles (Cinematic, Anime, etc.).
    * **Aspect Ratio:** All 9 supported aspect ratios (1:1, 16:9, etc.).
    * **CFG Scale:** An interactive slider to control prompt adherence.
    * **Seed:** Set a specific seed for reproducible images or use `0` for random.
* **Sleek User Interface:**
    * **Dark / Light Mode:** A theme toggle that saves your preference.
    * **Random Prompt:** A "dice" button to cycle through pre-defined creative prompts.
    * **Helpful Tooltips:** Hover-to-see descriptions for technical parameters.
* **Resilient Backend:**
    * **API Key Rotation:** Automatically cycles through a list of API keys in your `.env` file if one hits its billing limit.

---

## 🛠️ Project Structure

Here is an overview of the project's file structure:

stable_diffusion_text2image/  
├── .venv/  
├── .env  
├── .gitignore  
├── app.py  
├── pyproject.toml  
├── uv.lock  
├── README.md  
├── static/  
│     └── style.css  
└── templates/  
      └── index.html  

---

## 🚀 Getting Started

Follow these instructions to get the project running on your local machine.

### 1. Prerequisites

* **Python 3.10+**
* **`uv`**: This project uses `uv` for package management. You can install it [here](https://github.com/astral-sh/uv).
* **Stability AI Account**: You will need one or more API keys from [Stability AI](https://platform.stability.ai/).

### 2. Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/pranavsahu99s/stable_diffusion_text2image.git
    cd stable_diffusion_text2image
    ```

2.  **Create the virtual environment and install dependencies:**
    `uv` will read the `pyproject.toml` and `uv.lock` files to create a consistent environment.
    ```bash
    uv sync
    ```

3.  **Create your Environment File:**
    Create a file named `.env` in the main project folder. This is where you'll store your API keys.
    ```bash
    touch .env
    ```

4.  **Add Your API Keys:**
    Open the `.env` file and add your Stability AI keys as a single, comma-separated string. The app will automatically rotate through them.

    **.env**
    ```ini
    STABILITY_KEYS="sk-key1-goes-here,sk-key2-goes-here,sk-key3-goes-here"
    ```

### 3. Running the Application

1.  **Activate the virtual environment:**
    ```bash
    source .venv/bin/activate
    ```
    *(On Windows, use `.venv\Scripts\activate`)*

2.  **Run the Flask server:**
    ```bash
    python app.py
    ```

3.  **Open the app:**
    Open your web browser and go to **http://127.0.0.1:5000**. You should see the web interface, ready to go!

---

## 💻 Tech Stack

* **Backend:** **Python** with **Flask** (as the webserver) & **Requests** (for API calls).
* **Frontend:** **HTML5**, **CSS3** (with CSS Variables for theming), and vanilla **JavaScript** (using `fetch` for API communication).
* **Environment:** **`uv`** for high-speed package management and dependency locking.

---
