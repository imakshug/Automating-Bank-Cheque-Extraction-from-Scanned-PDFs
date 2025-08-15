# Automating Bank Check Extraction from Scanned PDFs

This project automates the extraction of text and data from bank checks in PDF format using OCR (Optical Character Recognition) technology. It features a modern Streamlit dashboard interface for easy interaction.

## 🌟 Features

- **PDF to Image Conversion**: Converts PDF files containing checks to images
- **Advanced OCR**: Extract text from check images using Tesseract OCR with preprocessing
- **Smart Data Parsing**: Automatically identifies account numbers, dates, amounts, payee information
- **Multiple Export Formats**: Export data to CSV, Excel, and JSON formats
- **Streamlit Dashboard**: Interactive data science dashboard with multi-page navigation
- **Traditional GUI**: Desktop application with file browser
- **Batch Processing**: Process multiple files simultaneously
- **Analytics**: View processing statistics and trends

## 📋 Requirements

- Python 3.7+
- Tesseract OCR (installed and configured)
- Required Python packages (see requirements.txt)

## 🚀 Quick Start

### 1. Installation

1. Clone this repository or download the project files
2. Install Tesseract OCR on your system
3. Create and activate virtual environment:
   ```bash
   python -m venv venv_new
   .\venv_new\Scripts\Activate.ps1  # Windows
   ```
4. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

### 2. Choose Your Interface

#### 📊 **Streamlit Dashboard (Recommended)**
Interactive data science dashboard:
```bash
# Run directly
streamlit run streamlit_app.py

# Or use batch file
run_streamlit.bat
```
Access at: http://localhost:8501

**Features:**
- Multi-page application (Home, Upload, Batch Processing, Analytics)
- Advanced data visualization with charts
- Batch processing capabilities
- Interactive widgets and controls
- Built-in data science tools
- Export options
- Processing analytics

#### 🖥️ **Desktop GUI**
Traditional desktop application:
```bash
# Run directly
python gui.py

# Or use batch file
run_gui.bat
```

#### ⌨️ **Command Line**
Direct script execution:
```bash
# Run directly
python main.py

# Or use batch file
run_main.bat
```

## Project Structure

- `main.py` - Main script with core functionality
- `gui.py` - Tkinter-based GUI application
- `image_methods.py` - Image processing and OCR functions
- `requirements.txt` - Python package dependencies
- `output/` - Directory for processed images
- `cheque.pdf` - Sample PDF file for testing

## Note

Make sure Tesseract OCR is properly installed and the paths in the code match your installation.
