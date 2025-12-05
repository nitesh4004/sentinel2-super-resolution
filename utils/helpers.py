# =============================================================================
# Helper Functions for Sentinel-2 Super Resolution App
# =============================================================================

import os
import glob
import shutil
import zipfile
from io import BytesIO


def dms_to_decimal(degrees: int, minutes: int, seconds: float, direction: str) -> float:
    """Convert DMS (Degrees, Minutes, Seconds) to Decimal Degrees."""
    decimal = float(degrees) + float(minutes) / 60 + float(seconds) / 3600
    if direction in ['S', 'W']:
        decimal *= -1
    return decimal


def decimal_to_dms(decimal_degree: float) -> tuple:
    """Convert Decimal Degrees to DMS format."""
    is_negative = decimal_degree < 0
    decimal_degree = abs(decimal_degree)
    
    degrees = int(decimal_degree)
    minutes_float = (decimal_degree - degrees) * 60
    minutes = int(minutes_float)
    seconds = (minutes_float - minutes) * 60
    
    if is_negative:
        degrees = -degrees
    
    return degrees, minutes, seconds


def create_output_directory(dir_name: str = "output_images") -> str:
    """Create output directory for processed images."""
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    return dir_name


def clear_output_directory(output_dir: str) -> None:
    """Clear all files in the output directory."""
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
        os.makedirs(output_dir)


def get_output_files(output_dir: str) -> list:
    """Get list of generated output files."""
    if os.path.exists(output_dir):
        files = []
        extensions = ['*.tif', '*.tiff', '*.png', '*.jpg', '*.jpeg', '*.geotiff']
        for ext in extensions:
            files.extend(glob.glob(os.path.join(output_dir, ext)))
        return sorted(files)
    return []


def create_zip_of_outputs(output_dir: str) -> BytesIO:
    """Create a ZIP file containing all output files."""
    zip_buffer = BytesIO()
    files = get_output_files(output_dir)
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for file_path in files:
            file_name = os.path.basename(file_path)
            zip_file.write(file_path, file_name)
    
    zip_buffer.seek(0)
    return zip_buffer


def validate_coordinates(lat: float, lon: float) -> bool:
    """Validate latitude and longitude values."""
    return -90 <= lat <= 90 and -180 <= lon <= 180


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} TB"
