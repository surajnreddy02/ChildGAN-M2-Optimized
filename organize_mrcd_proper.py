#!/usr/bin/env python3
"""
Organize MRCD dataset for PyTorch ImageFolder compatibility
Creates structured folders with class subdirectories for ChildGAN training
"""

import os
import shutil
from pathlib import Path

def organize_mrcd_dataset():
    # Paths
    base_dir = Path(".")
    dataset_dir = base_dir / "MRCD_Asian_Black_White_Dataset"
    output_dir = base_dir / "MRCD_organized"
    
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    
    # Expected subdirectories from the MRCD dataset
    ethnic_dirs = {
        "PR_AsianChildData": "Asian",
        "PR_BlackChildData": "Black", 
        "PR_WhiteChildData_WhiteFinal": "White"
    }
    
    total_files = 0
    
    for source_name, ethnic_label in ethnic_dirs.items():
        source_path = dataset_dir / source_name
        
        if not source_path.exists():
            print(f"❌ Warning: {source_path} not found")
            continue
            
        print(f"📂 Processing {ethnic_label} dataset from {source_name}...")
        
        # Look for age/gender subdirectories
        for age_gender_dir in source_path.iterdir():
            if not age_gender_dir.is_dir():
                continue
                
            # Create class directory (e.g., "Asian_10-19_Female")
            class_name = f"{ethnic_label}_{age_gender_dir.name}"
            class_dir = output_dir / class_name
            class_dir.mkdir(exist_ok=True)
            
            # Copy all images from this category
            file_count = 0
            for img_file in age_gender_dir.iterdir():
                if img_file.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                    dest_file = class_dir / img_file.name
                    shutil.copy2(img_file, dest_file)
                    file_count += 1
            
            print(f"   ✅ {class_name}: {file_count} images")
            total_files += file_count
    
    print(f"\n🎉 Dataset organization complete!")
    print(f"📊 Total images organized: {total_files}")
    print(f"📁 Output directory: {output_dir}")
    
    # List final structure
    print(f"\n📋 Final class structure:")
    for class_dir in sorted(output_dir.iterdir()):
        if class_dir.is_dir():
            img_count = len([f for f in class_dir.iterdir() if f.suffix.lower() in ['.jpg', '.jpeg', '.png']])
            print(f"   {class_dir.name}: {img_count} images")

if __name__ == "__main__":
    organize_mrcd_dataset()