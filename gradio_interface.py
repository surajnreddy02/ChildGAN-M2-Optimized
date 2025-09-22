#!/usr/bin/env python3
"""
ChildGAN Web Interface - Easy-to-use interface for age progression after training
Run this after training is complete to get a web interface for testing your model
"""

import gradio as gr
import torch
import torch.nn as nn
from torch.autograd import Variable
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import os

# Import the model architecture (assuming it's in the same directory)
# You'll need to adjust these imports based on your model files
try:
    from ChildGANTrain import _Encoder, _Decoder
except ImportError:
    print("⚠️  Model architecture files not found. Make sure ChildGANTrain.py is in the same directory.")

class ChildGANInterface:
    def __init__(self, model_path="./training_output"):
        self.device = self.get_device()
        self.model_path = model_path
        self.encoder = None
        self.decoder = None
        self.load_models()
        
        # Image preprocessing
        self.transform = transforms.Compose([
            transforms.Resize((128, 128)),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])
        
        # Denormalization for display
        self.denorm = transforms.Compose([
            transforms.Normalize((-1, -1, -1), (2, 2, 2)),
            transforms.ToPILImage()
        ])
    
    def get_device(self):
        """Detect the best available device"""
        if torch.backends.mps.is_available():
            return torch.device("mps")
        elif torch.cuda.is_available():
            return torch.device("cuda")
        else:
            return torch.device("cpu")
    
    def load_models(self):
        """Load the trained encoder and decoder models"""
        try:
            # Find the latest epoch models
            encoder_files = [f for f in os.listdir(self.model_path) if f.startswith('encoder_epoch_')]
            decoder_files = [f for f in os.listdir(self.model_path) if f.startswith('decoder_epoch_')]
            
            if not encoder_files or not decoder_files:
                print("❌ No trained models found. Please train the model first.")
                return
            
            # Get the latest epoch
            latest_epoch = max([int(f.split('_')[-1].split('.')[0]) for f in encoder_files])
            
            encoder_path = os.path.join(self.model_path, f'encoder_epoch_{latest_epoch}.pth')
            decoder_path = os.path.join(self.model_path, f'decoder_epoch_{latest_epoch}.pth')
            
            print(f"📂 Loading models from epoch {latest_epoch}...")
            
            # Initialize model architecture
            self.encoder = _Encoder(n_channel=3, n_z=50, nef=64, device=self.device)
            self.decoder = _Decoder(n_channel=3, n_z=50, n_l=5, ndf=64, device=self.device)
            
            # Load trained weights
            self.encoder.load_state_dict(torch.load(encoder_path, map_location=self.device))
            self.decoder.load_state_dict(torch.load(decoder_path, map_location=self.device))
            
            # Set to evaluation mode
            self.encoder.eval()
            self.decoder.eval()
            
            # Move to device
            self.encoder.to(self.device)
            self.decoder.to(self.device)
            
            print(f"✅ Models loaded successfully on {self.device}")
            
        except Exception as e:
            print(f"❌ Error loading models: {e}")
            self.encoder = None
            self.decoder = None
    
    def age_progress(self, input_image, current_age, target_age, gender):
        """Perform age progression on the input image"""
        if self.encoder is None or self.decoder is None:
            return "❌ Models not loaded. Please train the model first."
        
        try:
            # Preprocess image
            if isinstance(input_image, str):
                image = Image.open(input_image).convert('RGB')
            else:
                image = input_image.convert('RGB')
            
            # Transform image
            img_tensor = self.transform(image).unsqueeze(0).to(self.device)
            
            # Create age and gender vectors
            current_age_vec = torch.zeros(1, 5).to(self.device)
            current_age_vec[0, current_age] = 1
            
            target_age_vec = torch.zeros(1, 5).to(self.device)
            target_age_vec[0, target_age] = 1
            
            gender_vec = torch.tensor([[2 * gender - 1]], dtype=torch.float).to(self.device)  # -1 for male, 1 for female
            
            # Encode image
            with torch.no_grad():
                z_img = self.encoder(img_tensor)
                
                # Generate aged image
                aged_img = self.decoder(z_img, target_age_vec, gender_vec)
                
                # Convert back to PIL image
                aged_img_pil = self.denorm(aged_img.squeeze().cpu())
                
            return aged_img_pil
            
        except Exception as e:
            return f"❌ Error during age progression: {e}"

def create_interface():
    """Create Gradio interface"""
    interface = ChildGANInterface()
    
    def age_progression_wrapper(image, current_age, target_age, gender):
        age_mapping = {
            "0-5 years": 0,
            "6-10 years": 1, 
            "11-15 years": 2,
            "16-17 years": 3,
            "18+ years": 4
        }
        
        gender_mapping = {"Male": 0, "Female": 1}
        
        current_age_idx = age_mapping[current_age]
        target_age_idx = age_mapping[target_age]
        gender_idx = gender_mapping[gender]
        
        result = interface.age_progress(image, current_age_idx, target_age_idx, gender_idx)
        
        if isinstance(result, str):  # Error message
            return None
        else:
            return result
    
    # Create Gradio interface
    iface = gr.Interface(
        fn=age_progression_wrapper,
        inputs=[
            gr.Image(type="pil", label="📷 Upload Child's Photo"),
            gr.Dropdown(
                choices=["0-5 years", "6-10 years", "11-15 years", "16-17 years", "18+ years"],
                label="👶 Current Age Group",
                value="0-5 years"
            ),
            gr.Dropdown(
                choices=["0-5 years", "6-10 years", "11-15 years", "16-17 years", "18+ years"],
                label="🎯 Target Age Group", 
                value="18+ years"
            ),
            gr.Dropdown(
                choices=["Male", "Female"],
                label="👤 Gender",
                value="Male"
            )
        ],
        outputs=gr.Image(type="pil", label="✨ Age Progressed Result"),
        title="🇮🇳 ChildGAN: Indian Face Age Progression",
        description="""
        Upload a child's photo and see how they might look at different ages!
        
        **Optimized for Indian faces** with Apple M2 Mac training.
        
        **Instructions:**
        1. Upload a clear photo of a child's face
        2. Select their current age group
        3. Choose the target age you want to see
        4. Specify gender for better results
        5. Click Submit to generate the aged face!
        """,
        examples=[
            # You can add example images here
        ],
        theme=gr.themes.Soft()
    )
    
    return iface

if __name__ == "__main__":
    print("🚀 Starting ChildGAN Web Interface...")
    print("🔧 Make sure you have completed training and model files are in ./training_output/")
    
    interface = create_interface()
    
    # Launch the interface
    interface.launch(
        server_name="0.0.0.0",  # Accessible from other devices on network
        server_port=7860,       # Default Gradio port
        share=True,             # Creates public shareable link
        debug=True
    )