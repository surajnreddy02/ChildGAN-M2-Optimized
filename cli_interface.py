#!/usr/bin/env python3
"""
ChildGAN Command Line Interface - Simple CLI for age progression testing
Use this after training to test your model from command line
"""

import torch
import torchvision.transforms as transforms
from PIL import Image
import argparse
import os
import sys

def get_device():
    """Detect the best available device"""
    if torch.backends.mps.is_available():
        print("🚀 Using MPS (Apple M2 GPU)")
        return torch.device("mps")
    elif torch.cuda.is_available():
        print("🚀 Using CUDA GPU")
        return torch.device("cuda")
    else:
        print("💻 Using CPU")
        return torch.device("cpu")

def load_models(model_path, device):
    """Load trained encoder and decoder models"""
    try:
        # Import model architectures
        sys.path.append('.')
        from ChildGANTrain import _Encoder, _Decoder
        
        # Find latest epoch
        encoder_files = [f for f in os.listdir(model_path) if f.startswith('encoder_epoch_')]
        if not encoder_files:
            raise FileNotFoundError("No encoder models found in training_output")
        
        latest_epoch = max([int(f.split('_')[-1].split('.')[0]) for f in encoder_files])
        
        print(f"📂 Loading models from epoch {latest_epoch}...")
        
        # Initialize models
        encoder = _Encoder(n_channel=3, n_z=50, nef=64, device=device)
        decoder = _Decoder(n_channel=3, n_z=50, n_l=5, ndf=64, device=device)
        
        # Load weights
        encoder_path = os.path.join(model_path, f'encoder_epoch_{latest_epoch}.pth')
        decoder_path = os.path.join(model_path, f'decoder_epoch_{latest_epoch}.pth')
        
        encoder.load_state_dict(torch.load(encoder_path, map_location=device))
        decoder.load_state_dict(torch.load(decoder_path, map_location=device))
        
        encoder.eval()
        decoder.eval()
        encoder.to(device)
        decoder.to(device)
        
        print("✅ Models loaded successfully!")
        return encoder, decoder
        
    except Exception as e:
        print(f"❌ Error loading models: {e}")
        return None, None

def age_progress_image(image_path, current_age, target_age, gender, encoder, decoder, device, output_path):
    """Perform age progression on a single image"""
    try:
        # Age group mapping
        age_names = ["0-5 years", "6-10 years", "11-15 years", "16-17 years", "18+ years"]
        
        # Load and preprocess image
        image = Image.open(image_path).convert('RGB')
        
        transform = transforms.Compose([
            transforms.Resize((128, 128)),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])
        
        img_tensor = transform(image).unsqueeze(0).to(device)
        
        # Create age and gender vectors
        target_age_vec = torch.zeros(1, 5).to(device)
        target_age_vec[0, target_age] = 1
        
        gender_vec = torch.tensor([[2 * gender - 1]], dtype=torch.float).to(device)  # -1 male, 1 female
        
        # Generate aged image
        with torch.no_grad():
            z_img = encoder(img_tensor)
            aged_img = decoder(z_img, target_age_vec, gender_vec)
        
        # Denormalize and save
        denorm = transforms.Compose([
            transforms.Normalize((-1, -1, -1), (2, 2, 2)),
            transforms.ToPILImage()
        ])
        
        aged_img_pil = denorm(aged_img.squeeze().cpu())
        aged_img_pil.save(output_path)
        
        print(f"✅ Age progression complete!")
        print(f"📷 Input: {os.path.basename(image_path)} ({age_names[current_age]})")
        print(f"🎯 Output: {os.path.basename(output_path)} ({age_names[target_age]})")
        print(f"👤 Gender: {'Female' if gender == 1 else 'Male'}")
        
        return aged_img_pil
        
    except Exception as e:
        print(f"❌ Error during age progression: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='ChildGAN Age Progression CLI')
    parser.add_argument('--input', '-i', required=True, help='Input image path')
    parser.add_argument('--output', '-o', default='aged_output.jpg', help='Output image path')
    parser.add_argument('--current_age', '-c', type=int, default=0, 
                       help='Current age group (0-4): 0=0-5y, 1=6-10y, 2=11-15y, 3=16-17y, 4=18+y')
    parser.add_argument('--target_age', '-t', type=int, default=4,
                       help='Target age group (0-4): 0=0-5y, 1=6-10y, 2=11-15y, 3=16-17y, 4=18+y') 
    parser.add_argument('--gender', '-g', type=int, default=0,
                       help='Gender: 0=Male, 1=Female')
    parser.add_argument('--model_path', '-m', default='./training_output',
                       help='Path to trained models directory')
    
    args = parser.parse_args()
    
    print("🇮🇳 ChildGAN Indian Face Age Progression")
    print("=" * 50)
    
    # Validate inputs
    if not os.path.exists(args.input):
        print(f"❌ Input image not found: {args.input}")
        return
    
    if not os.path.exists(args.model_path):
        print(f"❌ Model directory not found: {args.model_path}")
        print("💡 Make sure to complete training first!")
        return
    
    if args.current_age < 0 or args.current_age > 4:
        print("❌ Current age must be 0-4")
        return
        
    if args.target_age < 0 or args.target_age > 4:
        print("❌ Target age must be 0-4")
        return
    
    if args.gender < 0 or args.gender > 1:
        print("❌ Gender must be 0 (Male) or 1 (Female)")
        return
    
    # Initialize
    device = get_device()
    encoder, decoder = load_models(args.model_path, device)
    
    if encoder is None or decoder is None:
        return
    
    # Perform age progression
    result = age_progress_image(
        args.input, 
        args.current_age, 
        args.target_age, 
        args.gender, 
        encoder, 
        decoder, 
        device, 
        args.output
    )
    
    if result:
        print(f"\n🎉 Success! Aged image saved to: {args.output}")

if __name__ == "__main__":
    main()