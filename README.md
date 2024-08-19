# PDF to Audio Converter

This project provides a Python script that converts PDF documents into audio files. The script extracts text from a PDF, cleans the text, converts it to speech, and saves it as an audio file in MP3 format.

## Features

- Extracts text from large PDF files.
- Cleans unnecessary characters from the extracted text.
- Converts text to speech using `pyttsx3`.
- Splits the text into chunks and processes them to avoid memory overload.
- Combines the generated audio chunks into a single MP3 file.

## Requirements

### Python Dependencies

This project uses [Poetry](https://python-poetry.org/) for dependency management. The required Python libraries are:

- PyPDF2
- pyttsx3
- pydub

### System Dependencies

**macOS (using Homebrew)**

You need to install ffmpeg to handle audio processing. This can be installed via Homebrew:

```bash
brew install ffmpeg
```

**Windows**

For Windows, you will need to download and install FFmpeg manually:

1. Download the latest build of FFmpeg from the [official website](https://ffmpeg.org/download.html).
2. Extract the files and add the bin directory to your system's PATH.

**Linux**

On Linux, FFmpeg can usually be installed via the package manager.

For Debian-based distributions (like Ubuntu):

```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

For Red Hat-based distributions (like Fedora or CentOS):

```bash
sudo dnf install ffmpeg
```

### Installation

1. Clone the repository:
    - `git clone https://github.com/sairoko12/pdf-2-audio.git`
    - `cd pdf-2-audio`
2. Install Python dependencies using Poetry:
    - Ensure you have Poetry installed. If not, you can install it via pip:
        - `pip install poetry`
    - Then, install the project dependencies:
        - `poetry install`
3. Install System Dependencies:
    - Follow the instructions in the “System Dependencies” section to install FFmpeg on your system.

## Usage

To convert a PDF file to an audio file, run the following command:

```bash
poetry run python script.py
```

This will convert the specified PDF file to an MP3 audio file.

### Cleaning up

Temporary audio files generated during the conversion process are automatically removed after the final audio file is created.

## Contributing

If you encounter any issues or have suggestions for improvements, please feel free to submit an issue or a pull request.

## License

This project is licensed under the MIT License. See the [MIT License](https://opensource.org/licenses/MIT) for more details.
