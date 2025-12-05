# 🛰️ Sentinel-2 Super Resolution Web App

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Boost Sentinel-2 satellite imagery resolution from 10m to **1 meter** using Gamma Earth's S2DR3 AI model.
<img width="1917" height="913" alt="image" src="https://github.com/user-attachments/assets/e0328ae8-9adf-4eae-8c61-a5abaa45c9f4" />

## ✨ Features

- 🌍 **Dual Coordinate Input**: Decimal degrees or DMS (Degrees, Minutes, Seconds) format
- 📅 **Date Selection**: Calendar widget for image date selection
- 🧠 **AI Super-Resolution**: Gamma Earth S2DR3 model for enhanced imagery
- 📥 **Easy Downloads**: Individual files or ZIP archive
- 🗺️ **Map Preview**: Interactive location preview
- 📊 **Progress Tracking**: Real-time processing status updates
- 🎯 **All 12 Spectral Bands**: Complete Sentinel-2 spectrum processing

## 🚀 Quick Start

### Prerequisites

- Linux OS (Ubuntu recommended)
- Python 3.12
- GPU with CUDA support (recommended for faster processing)
- Minimum 8GB RAM

### Installation

```bash
# Clone the repository
git clone https://github.com/nitesh4004/sentinel2-super-resolution.git
cd sentinel2-super-resolution

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install S2DR3 package (Linux only)
pip install https://storage.googleapis.com/0x7ff601307fa5/s2dr3-20250905.1-cp312-cp312-linux_x86_64.whl

# Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 📁 Project Structure

```
sentinel2-super-resolution/
├── .streamlit/
│   └── config.toml              # Streamlit configuration
├── utils/
│   ├── __init__.py             # Package initialization
│   └── helpers.py              # Helper functions
├── assets/
│   └── logo.png                # Project logo
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
├── README.md                   # This file
└── LICENSE                     # MIT License
```

## 🔧 Usage

1. **Enter Coordinates**: Use decimal degrees or DMS format in the sidebar
   - Decimal Degrees: Latitude (-90 to 90), Longitude (-180 to 180)
   - DMS Format: Degrees, Minutes, Seconds with direction (N/S/E/W)

2. **Select Date**: Choose a date with likely cloud-free conditions
   - Use the calendar widget to select image date
   - Maximum date is today

3. **Process Image**: Click the 'Process Image' button to run super-resolution
   - Real-time progress bar shows processing status
   - Processing may take several minutes depending on GPU

4. **Download Results**: Download individual files or all files as ZIP
   - All 12 spectral bands available
   - GeoTIFF and PNG formats
   - Complete metadata preserved

## 📊 Technical Specifications

| Parameter | Value |
|-----------|-------|
| Input Resolution | 10m / 20m / 60m |
| Output Resolution | 1 meter |
| Spectral Bands | All 12 bands |
| Model | S2DR3 (Gamma Earth) |
| Input Data Source | ESA Sentinel-2 |
| Processing Type | AI-based Super-Resolution |

## 🔬 How S2DR3 Works

The S2DR3 model uses deep learning to:

- Upscale Sentinel-2 imagery from 10m/20m/60m to 1m resolution
- Preserve all 12 spectral characteristics (coastal, blue, green, red, NIR, SWIR, etc.)
- Reconstruct features down to 3 meter detail
- Maintain spectral fidelity for accurate analysis

## 📋 Application Workflow

```
User Input (Coordinates + Date)
         ↓
Fetch Sentinel-2 Data
         ↓
Initialize S2DR3 AI Model
         ↓
Run Super-Resolution Processing
         ↓
Generate Output Files
         ↓
Provide Download Links
```

## 🌐 Coordinate Format Examples

### Decimal Degrees
```
Location: Ayodhya District, Uttar Pradesh, India
Latitude: 26.314625° N
Longitude: 82.987361° E
```

### DMS Format
```
Latitude: 26°18'52.65" N
Longitude: 82°59'14.50" E
```

## ⚙️ Configuration

Edit `.streamlit/config.toml` to customize:

```toml
[theme]
primaryColor = "#1E88E5"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = true
maxUploadSize = 200
```

## 🐛 Troubleshooting

### S2DR3 Package Not Found

Ensure you're on Linux with Python 3.12:

```bash
python --version  # Should be 3.12.x
uname -s          # Should be Linux
```

### Out of Memory Errors

- Ensure minimum 8GB RAM available
- Close other applications during processing
- Consider GPU with more VRAM (recommended: 8GB+)

### No Cloud-Free Images Available

- Try selecting a different date
- Monsoon season in India typically has more clouds
- Winter months (October-March) usually have clearer skies

## 📚 Resources

- [Gamma Earth S2DR3](https://gamma.earth/) - AI Super-Resolution Model
- [Sentinel-2 Data](https://sentinel.esa.int/web/sentinel/missions/sentinel-2) - ESA Sentinel-2 Mission
- [Streamlit Documentation](https://docs.streamlit.io/) - Streamlit Framework
- [GeoTIFF Format](https://www.ogc.org/standards/geotiff) - GeoTIFF Specification

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Nitesh Kumar** - Geospatial Data Scientist

- GitHub: [@nitesh4004](https://github.com/nitesh4004)
- 
---

Made with ❤️ for geospatial enthusiasts
