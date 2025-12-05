# 🚀 Deployment Guide - Sentinel-2 Super Resolution Web App

## Overview

The S2DR3 package has specific technical requirements that make deployment challenging. This guide covers different deployment strategies based on your infrastructure.

## System Requirements

### Core Requirements
- **OS**: Linux (Ubuntu 20.04 or later recommended)
- **Python**: 3.12.x (EXACT version - S2DR3 wheel is built for Python 3.12)
- **GPU**: NVIDIA GPU with CUDA support (optional but recommended)
- **RAM**: Minimum 8GB (16GB recommended)
- **Storage**: 20GB+ for Sentinel-2 data processing

### Package Limitations
- S2DR3 is **Linux-only** (no Windows or macOS support)
- Wheel file is platform-specific: `s2dr3-20250905.1-cp312-cp312-linux_x86_64.whl`
- Cannot be installed on Windows directly
- Cannot be installed on Streamlit Cloud (no GPU/wheel support)

---

## Deployment Options

### Option 1: Local Linux Machine (Development)

**Best for**: Testing and development

```bash
# Clone repository
git clone https://github.com/nitesh4004/sentinel2-super-resolution.git
cd sentinel2-super-resolution

# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install S2DR3 package
pip install https://storage.googleapis.com/0x7ff601307fa5/s2dr3-20250905.1-cp312-cp312-linux_x86_64.whl

# Verify installation
python -c "import s2dr3; print('S2DR3 installed successfully')"

# Run the app
streamlit run app.py
```

**Troubleshooting**:
```bash
# Check Python version
python --version  # Should be 3.12.x

# Verify GPU access
python -c "import torch; print(torch.cuda.is_available())"

# Check CUDA version
nvcc --version
```

---

### Option 2: Windows with WSL (Windows Subsystem for Linux)

**Best for**: Windows developers wanting GPU support

#### Step 1: Install WSL
```powershell
# Run PowerShell as Administrator
wsl --install
wsl --update

# Restart your computer
```

#### Step 2: Set up Ubuntu environment
```bash
# Inside WSL Ubuntu terminal
sudo apt update
sudo apt install -y python3.12 python3.12-venv python3.12-dev python3-pip

# Verify
python3.12 --version
```

#### Step 3: Clone and setup project
```bash
# Navigate to project location
cd /mnt/c/Users/YourUsername/path/to/projects

# Clone repository
git clone https://github.com/nitesh4004/sentinel2-super-resolution.git
cd sentinel2-super-resolution

# Create environment
python3.12 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install https://storage.googleapis.com/0x7ff601307fa5/s2dr3-20250905.1-cp312-cp312-linux_x86_64.whl

# Run app
streamlit run app.py
```

**Access from Windows**:
- Open browser: `http://localhost:8501`
- WSL will output the URL automatically

---

### Option 3: Docker (Production-Ready)

**Best for**: Production deployment on Linux servers

#### Using Docker Compose

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  sentinel2-app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8501:8501"
    volumes:
      - ./output_images:/app/output_images
      - ./data:/app/data
    environment:
      - STREAMLIT_SERVER_PORT=8501
      - STREAMLIT_SERVER_ADDRESS=0.0.0.0
      - STREAMLIT_SERVER_HEADLESS=true
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1  # Number of GPUs
              capabilities: [gpu]
    restart: unless-stopped
```

#### Build and run
```bash
# Build image
docker-compose build

# Run container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop container
docker-compose down
```

---

### Option 4: AWS EC2 with GPU

**Best for**: Scalable cloud deployment

#### Launch EC2 Instance
```bash
# Use Deep Learning AMI (Ubuntu)
# Instance type: g4dn.xlarge or better
# Storage: 50GB EBS volume
```

#### Setup
```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-instance-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Verify GPU
nvidia-smi

# Install Python 3.12
sudo apt install -y python3.12 python3.12-venv python3.12-dev

# Clone and setup
git clone https://github.com/nitesh4004/sentinel2-super-resolution.git
cd sentinel2-super-resolution

python3.12 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
pip install https://storage.googleapis.com/0x7ff601307fa5/s2dr3-20250905.1-cp312-cp312-linux_x86_64.whl

# Run with nohup for background execution
nohup streamlit run app.py --server.port 8501 > app.log 2>&1 &
```

#### Access
```
http://your-instance-public-ip:8501
```

---

### Option 5: Google Cloud Run (GPU)

**Best for**: Managed serverless deployment

```bash
# Build and push Docker image
gcloud builds submit --tag gcr.io/PROJECT-ID/sentinel2-app

# Deploy with GPU
gcloud run deploy sentinel2-app \
  --image gcr.io/PROJECT-ID/sentinel2-app \
  --platform managed \
  --region us-central1 \
  --memory 8Gi \
  --cpu 4 \
  --accelerator type=nvidia-tesla-k80,count=1
```

---

### Option 6: Google Colab (Free GPU)

**Best for**: Quick testing without infrastructure costs

#### Run in Colab
1. Open [Google Colab](https://colab.research.google.com)
2. Create new notebook
3. Copy-paste code from `colab_notebook.ipynb`
4. Change runtime to T4 GPU (free tier)
5. Run cells sequentially
6. Results saved to Google Drive

---

## Performance Comparison

| Deployment | Setup Time | Cost | GPU Access | Scalability | Best For |
|---|---|---|---|---|---|
| Local Linux | Minutes | Free | Optional | No | Development |
| WSL | 30 mins | Free | If available | No | Windows Dev |
| Docker | 1 hour | $10-50/mo | Optional | Yes | Production |
| AWS EC2 | 30 mins | $50-200/mo | Yes | Yes | Enterprise |
| Google Cloud | 1 hour | $100-300/mo | Yes | Yes | Cloud-native |
| Colab | 5 mins | Free | Yes | No | Testing |

---

## Troubleshooting

### S2DR3 Installation Fails
```bash
# Check Python version (must be 3.12)
python --version

# Try with verbose output
pip install -vv https://storage.googleapis.com/0x7ff601307fa5/s2dr3-20250905.1-cp312-cp312-linux_x86_64.whl

# Check for conflicting packages
pip list | grep -i gdal
```

### CUDA/GPU Issues
```bash
# Verify CUDA installation
nvcc --version
cuda-smi

# Check PyTorch GPU access
python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"
```

### Streamlit Connection Issues
```bash
# Check port availability
lsof -i :8501

# Run on different port
streamlit run app.py --server.port 8502
```

---

## Security Best Practices

1. **Use secrets for API keys** (if added later)
   - Store in `.streamlit/secrets.toml` (not committed)
   - Use environment variables in production

2. **Configure firewall**
   - Restrict access to trusted IPs
   - Use reverse proxy (nginx/apache)
   - Enable HTTPS with Let's Encrypt

3. **Monitor resources**
   - Set memory limits in Docker
   - Monitor GPU usage
   - Log all processing requests

---

## Monitoring & Logging

### Docker Logs
```bash
docker-compose logs -f --tail=100
```

### System Monitoring
```bash
# CPU, Memory, GPU
watch -n 1 nvidia-smi
top -b
df -h
```

### Application Logs
```bash
tail -f nohup.out  # For EC2/Linux
streamlit run app.py --logger.level=debug
```

---

## Production Checklist

- [ ] Python 3.12 installed and verified
- [ ] S2DR3 package installed successfully
- [ ] GPU detected and accessible
- [ ] Docker image built and tested
- [ ] Environment variables configured
- [ ] Firewall rules configured
- [ ] Monitoring set up
- [ ] Backups scheduled
- [ ] SSL/HTTPS enabled
- [ ] Rate limiting configured

---

## Support & Resources

- [Gamma Earth Documentation](https://gamma.earth)
- [Streamlit Deployment Docs](https://docs.streamlit.io/deploy)
- [Docker Documentation](https://docs.docker.com)
- [AWS EC2 Guide](https://docs.aws.amazon.com/ec2)
- [Google Cloud Documentation](https://cloud.google.com/docs)

---

**Last Updated**: December 5, 2025
**Maintainer**: Nitesh Kumar (nitesh.kumar@swan.co.in)
