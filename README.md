# 🔉 Transcribot

A powerful audio and video transcription tool that converts your media files to text using Faster-Whisper models. Built with a user-friendly Streamlit interface for seamless transcription workflows.

**Try it here** 👉 [Transcribot](https://transcribot-muneer.streamlit.app/)

## 🌟 Features

- **Multi-Format Support**: Transcribe audio (MP3, WAV, M4A) and video files (MP4, MOV, AVI, MKV)
- **Advanced AI Models**: Powered by Faster-Whisper with multiple model options for different speed/accuracy needs
- **Interactive GUI**: Clean and intuitive Streamlit web interface
- **Multiple Output Formats**: Get transcriptions as plain text, SRT subtitles, or word-level timestamps
- **Customizable Settings**: Configure transcription models, language settings, and initial prompts
- **Copy & Download**: Easy copy-to-clipboard and download functionality for all outputs

## 🚀 Getting Started

### Prerequisites
- Python 3.10
- Git (for cloning the repository)

### Installation Methods

#### Option 1: Using UV (Recommended)
```bash
# Clone the repository
git clone https://github.com/syedmuneeruddin5/transcribot.git
cd transcribot

# Install UV if you haven't already
pip install uv

# Install dependencies with uv
uv sync
```

#### Option 2: Using pip
```bash
# Clone the repository
git clone https://github.com/syedmuneeruddin5/transcribot.git
cd transcribot

# Create virtual environment
python -m venv .venv

# Activate environment
# Windows:
.\.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r src/requirements.txt
```

## 🎮 Usage

### Launch the Application
```bash
# With uv:
uv run streamlit run src/main.py

# With pip:
streamlit run src/main.py
```

### Using the Interface

1. **Upload Your File**: Choose from supported audio/video formats
2. **Configure Settings** (Optional):
   - Select your preferred Whisper model
   - Add custom initial prompts for better context
3. **Transcribe**: Click the transcribe button and wait for processing
4. **Get Results**: View and download your transcription in multiple formats:
   - **Plain Text**: Clean transcription without timestamps
   - **Segment Timestamps**: SRT format with sentence-level timing
   - **Word Timestamps**: SRT format with word-level precision


## 🔍 Troubleshooting

### Common Issues

**First run is slow**
- This is normal - models are being downloaded
- Subsequent runs will be much faster

## 📄 License

This project is available under the MIT License - see the LICENSE file for details.

## 📝 Acknowledgments

- Built with [Faster-Whisper](https://github.com/SYSTRAN/faster-whisper) for efficient transcription
- Powered by [Streamlit](https://streamlit.io/) for the web interface
