#!/usr/bin/env python3
"""
Integrate Indian CRFW dataset with MRCD dataset for optimal Indian face training
"""

import os
import shutil
from pathlib import Path

def integrate_indian_dataset():
    # Paths
    base_dir = Path(".")
    indian_source = base_dir / "CRFW" / "Indian"
    mrcd_dataset = base_dir / "MRCD_childgan_format"
    output_dir = base_dir / "MRCD_Indian_Combined"
    
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    
    # First, copy existing MRCD structure
    print("📂 Copying existing MRCD dataset structure...")
    for class_dir in mrcd_dataset.iterdir():
        if class_dir.is_dir():
            target_class = output_dir / class_dir.name
            target_class.mkdir(exist_ok=True)
            
            # Copy existing images
            for img_file in class_dir.iterdir():
                if img_file.suffix.lower() in ['.jpg', '.png', '.jpeg']:
                    shutil.copy2(img_file, target_class / img_file.name)
    
    # Now integrate Indian dataset
    print("🇮🇳 Integrating Indian CRFW dataset...")
    
    indian_count = 0
    for img_file in indian_source.iterdir():
        if not img_file.suffix.lower() in ['.jpg', '.png', '.jpeg']:
            continue
            
        # Parse filename: age_gender_...
        filename = img_file.name
        parts = filename.split('_')
        
        if len(parts) >= 2:
            try:
                age_group = int(parts[0])
                gender = int(parts[1])
                
                # Map to ChildGAN class system (age_group * 2 + gender)
                if age_group <= 4 and gender <= 1:  # Valid range
                    class_id = age_group * 2 + gender
                    target_class = output_dir / str(class_id)
                    
                    # Create unique filename to avoid conflicts
                    new_name = f"Indian_CRFW_{indian_count}_{img_file.name}"
                    target_file = target_class / new_name
                    
                    shutil.copy2(img_file, target_file)
                    indian_count += 1
                    
            except ValueError:
                continue  # Skip invalid filenames
    
    print(f"✅ Integrated {indian_count} Indian faces")
    
    # Final statistics
    print(f"\n📊 Final Combined Dataset Statistics:")
    total_images = 0
    for class_dir in sorted(output_dir.iterdir()):
        if class_dir.is_dir():
            img_count = len([f for f in class_dir.iterdir() if f.suffix.lower() in ['.jpg', '.png', '.jpeg']])
            indian_count_class = len([f for f in class_dir.iterdir() if f.name.startswith('Indian_CRFW')])
            total_images += img_count
            
            age_group = int(class_dir.name) // 2
            gender = "Male" if int(class_dir.name) % 2 == 0 else "Female"
            
            print(f"   Class {class_dir.name} (Age{age_group}_{gender}): {img_count} total ({indian_count_class} Indian)")
    
    print(f"\n🎯 Total combined dataset: {total_images} images")
    print(f"📁 Output directory: {output_dir}")
    
    return output_dir

if __name__ == "__main__":
    integrate_indian_dataset()