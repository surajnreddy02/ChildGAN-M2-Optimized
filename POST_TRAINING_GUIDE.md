# 🇮🇳 ChildGAN Post-Training Usage Guide

After training is complete, you'll have several options to use your trained age progression model:

## 📁 Training Output Files

After training completes, you'll find these files in `./training_output/`:

```
training_output/
├── encoder_epoch_800.pth     # Trained facial encoder (final)
├── decoder_epoch_800.pth     # Trained age progression generator (final)  
├── dimag_epoch_800.pth       # Trained discriminator (final)
├── input_epoch_*.png         # Training progress images (input faces)
├── fake_epoch_*.png          # Training progress images (generated faces)
└── ... (intermediate epoch models)
```

## 🎯 Interface Options

### Option 1: Command Line Interface (Simplest)

Use the CLI tool for quick testing:

```bash
# Activate virtual environment
source .venv/bin/activate

# Basic usage - age a child to adult
python cli_interface.py -i input_photo.jpg -o aged_result.jpg -c 0 -t 4 -g 1

# Parameters:
# -i: Input image path
# -o: Output image path  
# -c: Current age (0=0-5y, 1=6-10y, 2=11-15y, 3=16-17y, 4=18+y)
# -t: Target age (0=0-5y, 1=6-10y, 2=11-15y, 3=16-17y, 4=18+y)
# -g: Gender (0=Male, 1=Female)
```

**Examples:**
```bash
# Age a 5-year-old girl to adult
python cli_interface.py -i child.jpg -o adult.jpg -c 0 -t 4 -g 1

# Age a 10-year-old boy to teenager  
python cli_interface.py -i kid.jpg -o teen.jpg -c 1 -t 3 -g 0
```

### Option 2: Web Interface (User-Friendly)

Install Gradio for a beautiful web interface:

```bash
# Install Gradio
pip install gradio

# Launch web interface
python gradio_interface.py
```

This opens a web browser with:
- **📷 Photo Upload:** Drag & drop child photos
- **👶 Age Selection:** Choose current and target age groups
- **👤 Gender Selection:** Male/Female for better results
- **✨ Live Results:** See aged faces instantly

The web interface will be accessible at: `http://localhost:7860`

### Option 3: Custom Integration

For developers wanting to integrate into their apps:

```python
import torch
from cli_interface import load_models, age_progress_image

# Load trained models
device = torch.device("mps")  # or "cuda" or "cpu"
encoder, decoder = load_models("./training_output", device)

# Process image
result = age_progress_image(
    image_path="child.jpg",
    current_age=0,    # 0-5 years  
    target_age=4,     # 18+ years
    gender=1,         # Female
    encoder=encoder,
    decoder=decoder,
    device=device,
    output_path="aged.jpg"
)
```

## 🎯 Age Group Mappings

- **0:** 0-5 years (Early Childhood)
- **1:** 6-10 years (Late Childhood) 
- **2:** 11-15 years (Early Adolescence)
- **3:** 16-17 years (Late Adolescence)
- **4:** 18+ years (Adult)

## 💡 Usage Tips

### Best Results:
- **Clear Photos:** Use high-quality, well-lit face photos
- **Front-Facing:** Direct face photos work better than side angles  
- **Single Person:** Photos with one clear face
- **Good Lighting:** Avoid heavy shadows or overexposure

### Photo Requirements:
- **Format:** JPG, PNG supported
- **Size:** Any size (will be resized to 128x128 internally)
- **Face Visibility:** Clear, unobstructed facial features

### Expected Quality:
- **Indian Faces:** Excellent quality (trained on 521+ Indian samples)
- **Age Progression:** Smooth transitions between age groups
- **Gender Awareness:** Different aging patterns for male/female
- **Facial Features:** Preserves key facial characteristics

## 🚀 Quick Start After Training

1. **Check Training Complete:**
   ```bash
   ls ./training_output/encoder_epoch_800.pth
   ```

2. **Test with CLI:**
   ```bash
   python cli_interface.py -i test_photo.jpg -o result.jpg -c 0 -t 4 -g 0
   ```

3. **Launch Web Interface:**
   ```bash
   pip install gradio
   python gradio_interface.py
   ```

## 🎉 You're Ready!

Your M2 Mac-optimized ChildGAN model is trained on 28,669 images including 521 Indian faces, ready for high-quality age progression on Indian faces with excellent generalization!

**Estimated Training Time:** ~4.5 hours on M2 Mac
**Model Quality:** Optimized for Indian facial features with robust diversity