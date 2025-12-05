# =============================================================================
# Sentinel-2 Super Resolution Web App
# Boost Sentinel-2 imagery to 1m resolution using Gamma Earth AI (S2DR3)
# Author: Nitesh Kumar
# =============================================================================

import streamlit as st
import os
import glob
import shutil
import zipfile
from datetime import datetime, timedelta
from io import BytesIO
from utils.helpers import (
    dms_to_decimal,
    create_output_directory,
    get_output_files,
    create_zip_of_outputs,
    clear_output_directory,
)

# =============================================================================
# Page Configuration
# =============================================================================
st.set_page_config(
    page_title="Sentinel-2 Super Resolution",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/nitesh4004/sentinel2-super-resolution/issues',
        'Report a bug': 'https://github.com/nitesh4004/sentinel2-super-resolution/issues',
        'About': "# Sentinel-2 Super Resolution\nBoost imagery to 1m using Gamma Earth AI"
    }
)

# =============================================================================
# Custom CSS
# =============================================================================
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .info-box {
        background-color: #E3F2FD;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #1E88E5;
    }
    </style>
""", unsafe_allow_html=True)

# =============================================================================
# Initialize Session State
# =============================================================================
if 'processing_complete' not in st.session_state:
    st.session_state['processing_complete'] = False
if 'output_dir' not in st.session_state:
    st.session_state['output_dir'] = 'output_images'

# =============================================================================
# Sidebar - Input Parameters
# =============================================================================
with st.sidebar:
    st.header("📍 Input Parameters")
    
    # Coordinate input method
    coord_method = st.radio(
        "Coordinate Input Method:",
        ["Decimal Degrees", "DMS (Degrees, Minutes, Seconds)"],
        index=0,
        help="Choose how you want to enter coordinates"
    )
    
    st.markdown("---")
    
    if coord_method == "Decimal Degrees":
        st.subheader("🌍 Coordinates")
        latitude = st.number_input(
            "Latitude (°N/S)",
            min_value=-90.0,
            max_value=90.0,
            value=26.314625,
            format="%.6f",
            help="Positive for North, Negative for South"
        )
        longitude = st.number_input(
            "Longitude (°E/W)",
            min_value=-180.0,
            max_value=180.0,
            value=82.987361,
            format="%.6f",
            help="Positive for East, Negative for West"
        )
    else:
        st.subheader("🌍 Latitude (DMS)")
        col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
        with col1:
            lat_deg = st.number_input("Deg", min_value=0, max_value=90, value=26, key="lat_deg")
        with col2:
            lat_min = st.number_input("Min", min_value=0, max_value=59, value=18, key="lat_min")
        with col3:
            lat_sec = st.number_input("Sec", min_value=0.0, max_value=59.99, value=52.65, key="lat_sec", format="%.2f")
        with col4:
            lat_dir = st.selectbox("", ["N", "S"], key="lat_dir")
        
        st.subheader("🌍 Longitude (DMS)")
        col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
        with col1:
            lon_deg = st.number_input("Deg", min_value=0, max_value=180, value=82, key="lon_deg")
        with col2:
            lon_min = st.number_input("Min", min_value=0, max_value=59, value=59, key="lon_min")
        with col3:
            lon_sec = st.number_input("Sec", min_value=0.0, max_value=59.99, value=14.50, key="lon_sec", format="%.2f")
        with col4:
            lon_dir = st.selectbox("", ["E", "W"], key="lon_dir")
        
        latitude = dms_to_decimal(lat_deg, lat_min, lat_sec, lat_dir)
        longitude = dms_to_decimal(lon_deg, lon_min, lon_sec, lon_dir)
    
    st.markdown("---")
    
    # Date input
    st.subheader("📅 Image Date")
    default_date = datetime.now() - timedelta(days=20)
    selected_date = st.date_input(
        "Select Date",
        value=default_date,
        max_value=datetime.now(),
        help="Select a date for cloud-free Sentinel-2 imagery"
    )
    date_str = selected_date.strftime("%Y-%m-%d")
    
    st.markdown("---")
    
    # Coordinates summary
    st.subheader("📌 Summary")
    st.code(f"Lat: {latitude:.6f}°\nLon: {longitude:.6f}°\nDate: {date_str}")

# =============================================================================
# Main Content
# =============================================================================
st.markdown('<div class="main-header">🛰️ Sentinel-2 Super Resolution</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Boost Sentinel-2 Image Resolution to 1 Meter using Gamma Earth AI (S2DR3)</div>', unsafe_allow_html=True)

# Create tabs
tab1, tab2, tab3 = st.tabs(["🔧 Process", "📥 Downloads", "ℹ️ About"])

# =============================================================================
# Tab 1: Processing
# =============================================================================
with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
            #### 🧠 About S2DR3 Super Resolution
            This application uses **Gamma Earth's S2DR3** deep learning model to enhance
            Sentinel-2 imagery from 10m/20m/60m to **1 meter resolution**.
            
            - All 12 spectral bands are upscaled
            - Preserves spectral characteristics
            - Reconstructs features down to 3m detail
        """)
        
        process_btn = st.button("🚀 Process Image", type="primary", use_container_width=True)
        
        if process_btn:
            output_dir = create_output_directory()
            clear_output_directory(output_dir)
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                status_text.text("📡 Initializing S2DR3 module...")
                progress_bar.progress(10)
                
                import s2dr3.inferutils
                
                status_text.text("🔍 Fetching Sentinel-2 data...")
                progress_bar.progress(30)
                
                lonlat = (longitude, latitude)
                
                status_text.text("🧠 Running AI Super-Resolution model...")
                progress_bar.progress(50)
                
                original_dir = os.getcwd()
                os.chdir(output_dir)
                s2dr3.inferutils.test(lonlat, date_str)
                os.chdir(original_dir)
                
                progress_bar.progress(90)
                status_text.text("✅ Processing complete!")
                progress_bar.progress(100)
                
                st.session_state['processing_complete'] = True
                st.session_state['output_dir'] = output_dir
                st.success("🎉 Image processing completed successfully!")
                st.balloons()
                
            except ImportError:
                progress_bar.empty()
                st.error("""⚠️ **S2DR3 Package Not Installed**
                
Install the package using:
```
pip install https://storage.googleapis.com/0x7ff601307fa5/s2dr3-20250905.1-cp312-cp312-linux_x86_64.whl
```
**Requirements:** Linux, Python 3.12, GPU with CUDA (recommended)""")
            except Exception as e:
                progress_bar.empty()
                st.error(f"❌ Error: {str(e)}")
        
        # Map preview
        st.subheader("📍 Location Preview")
        map_data = {"lat": [latitude], "lon": [longitude]}
        st.map(map_data, zoom=10)
    
    with col2:
        st.markdown("""
            #### ⚠️ Requirements
            - Linux OS (Ubuntu)
            - Python 3.12
            - GPU with CUDA
            - Min 8GB RAM
        """)

# =============================================================================
# Tab 2: Downloads
# =============================================================================
with tab2:
    if st.session_state.get('processing_complete', False):
        output_dir = st.session_state.get('output_dir', 'output_images')
        output_files = get_output_files(output_dir)
        
        if output_files:
            st.markdown("#### ✅ Files Ready for Download")
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📄 Individual Files")
                for file_path in output_files:
                    file_name = os.path.basename(file_path)
                    file_size = os.path.getsize(file_path) / (1024 * 1024)
                    
                    with open(file_path, 'rb') as f:
                        st.download_button(
                            label=f"📄 {file_name} ({file_size:.2f} MB)",
                            data=f.read(),
                            file_name=file_name,
                            mime="image/tiff" if file_name.endswith(('.tif', '.tiff')) else "image/png",
                            key=f"dl_{file_name}"
                        )
            
            with col2:
                st.subheader("📦 Download All")
                zip_buffer = create_zip_of_outputs(output_dir)
                st.download_button(
                    label="📦 Download All as ZIP",
                    data=zip_buffer,
                    file_name=f"sentinel2_superres_{date_str}.zip",
                    mime="application/zip",
                    type="primary",
                    use_container_width=True
                )
            
            st.info(f"Total files: {len(output_files)}")
        else:
            st.warning("No output files found.")
    else:
        st.info("👈 Configure parameters in the sidebar and click 'Process Image' to generate outputs.")

# =============================================================================
# Tab 3: About
# =============================================================================
with tab3:
    st.markdown("""
    ## 📋 How to Use
    
    1. **Enter Coordinates**: Use decimal degrees or DMS format in the sidebar
    2. **Select Date**: Choose a date with likely cloud-free conditions
    3. **Process**: Click 'Process Image' to run super-resolution
    4. **Download**: Download individual files or all files as ZIP
    
    ## 🔬 Technical Details
    
    | Parameter | Value |
    |-----------|-------|
    | Input Resolution | 10m / 20m / 60m |
    | Output Resolution | 1 meter |
    | Spectral Bands | All 12 bands |
    | Model | S2DR3 (Gamma Earth) |
    
    ## 🔗 Resources
    
    - [Gamma Earth](https://gamma.earth)
    - [Sentinel-2 Data](https://sentinel.esa.int/web/sentinel/missions/sentinel-2)
    - [GitHub Repository](https://github.com/nitesh4004/sentinel2-super-resolution)
    
    ## 👨‍💻 Author
    
    **Nitesh Kumar** - Geospatial Data Scientist
    """)

# =============================================================================
# Footer
# =============================================================================
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit | Powered by Gamma Earth S2DR3", unsafe_allow_html=True)
