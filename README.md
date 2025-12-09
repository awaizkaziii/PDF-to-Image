# 🖼️ PDF Image Extractor Pro

A powerful and user-friendly Streamlit web application for extracting images from PDF files with advanced features like format conversion, preview gallery, and batch downloads.

## ✨ Features

- **📄 PDF Upload**: Support for PDF files of any size
- **🔍 Smart Extraction**: Automatically extracts all images from all pages
- **📸 Image Preview**: Visual gallery with adjustable grid layout (1-5 images per row)
- **🎨 Format Conversion**: Convert images to PNG, JPG, or WEBP formats
- **⚙️ Quality Control**: Adjustable quality settings for compressed formats (JPG/WEBP)
- **📊 Detailed Statistics**: Comprehensive image information and analytics
- **⬇️ Flexible Downloads**:
  - Batch download as ZIP file
  - Individual image downloads
- **📈 Progress Tracking**: Real-time extraction progress for large PDFs
- **🛡️ Error Handling**: Robust error handling with informative messages
- **📱 Responsive Design**: Modern, professional UI with sidebar settings

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Start

1. **Clone or download** this repository

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

4. **Open your browser** and navigate to the URL shown (usually `http://localhost:8501`)

## 📖 Usage

### Basic Workflow

1. **Upload PDF**: Click the file uploader and select your PDF file
2. **Extract Images**: Click the "🔍 Extract Images" button
3. **Preview**: Browse extracted images in the Preview tab
4. **Review Details**: Check image statistics in the Details tab
5. **Download**: Choose your preferred download option in the Download tab

### Advanced Options

- **Format Conversion**: Use the sidebar to convert images to different formats
- **Quality Settings**: Adjust compression quality for JPG/WEBP outputs
- **Grid Layout**: Customize the number of images displayed per row in the preview

## 📋 Requirements

- `streamlit>=1.28.0` - Web application framework
- `PyMuPDF>=1.23.0` - PDF processing library
- `Pillow>=10.0.0` - Image processing library

## 🏗️ Project Structure

```
pdf-image-extractor/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🎯 Key Components

### `extract_images()` Function
- Opens PDF using PyMuPDF
- Iterates through all pages
- Extracts images with metadata (page number, index, format)
- Returns structured data for processing

### Image Processing
- Format conversion using PIL/Pillow
- Quality control for compressed formats
- Memory-efficient processing

### UI Features
- **Preview Tab**: Visual gallery with thumbnails
- **Details Tab**: DataFrame with image statistics
- **Download Tab**: Multiple download options

## 🔧 Configuration

### Sidebar Settings
- **Output Format**: Choose between Original, PNG, JPG, or WEBP
- **Image Quality**: Slider for JPG/WEBP compression (50-100%)

### Display Options
- **Images per Row**: Adjustable grid layout (1-5 columns)

## 📊 Statistics Provided

- Total number of images extracted
- Total file size of all images
- Number of pages containing images
- Individual image details (filename, page, format, size)

## 🐛 Troubleshooting

### Common Issues

1. **No images found**: The PDF might not contain embedded images
2. **Format conversion fails**: Some images might be in unsupported formats
3. **Large PDFs**: Processing might take time - watch the progress bar

### Error Messages
The app provides detailed error messages for:
- PDF reading errors
- Image extraction failures
- Format conversion issues

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

1. Fork the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Linux/Mac)
4. Install dependencies: `pip install -r requirements.txt`
5. Make your changes
6. Test thoroughly
7. Submit a PR

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- PDF processing powered by [PyMuPDF](https://pymupdf.readthedocs.io/)
- Image handling by [Pillow](https://python-pillow.org/)

## 📞 Support

If you encounter any issues or have suggestions for improvements, please:

1. Check the troubleshooting section above
2. Open an issue on GitHub
3. Provide details about your PDF file and the error encountered

---

**Happy PDF Image Extracting! 🎉**
