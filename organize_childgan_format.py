#!/usr/bin/env python3
"""
Organize MRCD dataset to match ChildGAN's expected structure:
- 5 age groups (0-4) 
- 2 genders (0-1)
- Total 10 classes: 0,1,2,3,4,5,6,7,8,9
- Class mapping: age*2 + gender
"""

import os
import shutil
from pathlib import Path
import random

def organize_for_childgan():
    # Paths
    base_dir = Path(".")
    source_dir = base_dir / "MRCD_organized" 
    output_dir = base_dir / "MRCD_childgan_format"
    
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    
    # Create 10 class directories (0-9)
    # Class mapping: age_group * 2 + gender
    # age_group: 0-4, gender: 0(even numbers) or 1(odd numbers)
    class_names = {}
    for age_group in range(5):
        for gender in [0, 1]:
            class_id = age_group * 2 + gender
            gender_name = "Male" if gender == 0 else "Female"
            class_names[class_id] = f"Age{age_group}_{gender_name}"
            (output_dir / str(class_id)).mkdir(exist_ok=True)
    
    print("🎯 ChildGAN Class Mapping:")
    for class_id, name in class_names.items():
        print(f"   Class {class_id}: {name}")
    
    # Map original classes to ChildGAN classes
    # We'll sample from each ethnic/age category and distribute to age groups
    ethnic_age_mapping = {}
    
    # Process each source class
    total_copied = 0
    for source_class_dir in source_dir.iterdir():
        if not source_class_dir.is_dir():
            continue
            
        class_name = source_class_dir.name
        parts = class_name.split('_')
        if len(parts) != 2:
            continue
            
        ethnic = parts[0]  # Asian, Black, White
        age_code = parts[1]  # 00, 01, 02, etc.
        
        # Map age codes to age groups (0-4)
        # Original has 00-09, we'll group them into 5 groups
        age_num = int(age_code)
        age_group = age_num // 2  # 00-01->0, 02-03->1, 04-05->2, 06-07->3, 08-09->4
        
        # Assume even age codes are one gender, odd are another
        # This is arbitrary since we don't have gender info in the class names
        gender = age_num % 2
        
        target_class = age_group * 2 + gender
        target_dir = output_dir / str(target_class)
        
        # Copy images (sample up to 1000 per original class to keep dataset manageable)
        images = list(source_class_dir.glob("*.jpg")) + list(source_class_dir.glob("*.png"))
        random.shuffle(images)
        
        copy_count = 0
        for img_file in images[:1000]:  # Limit to prevent huge dataset
            dest_name = f"{ethnic}_{age_code}_{img_file.name}"
            dest_path = target_dir / dest_name
            shutil.copy2(img_file, dest_path)
            copy_count += 1
            
        print(f"📁 {class_name} -> Class {target_class} ({class_names[target_class]}): {copy_count} images")
        total_copied += copy_count
    
    print(f"\n🎉 Dataset organized for ChildGAN!")
    print(f"📊 Total images: {total_copied}")
    print(f"📁 Output directory: {output_dir}")
    
    # Final summary
    print(f"\n📋 Final class distribution:")
    for class_id in range(10):
        class_dir = output_dir / str(class_id)
        img_count = len(list(class_dir.glob("*.jpg")) + list(class_dir.glob("*.png")))
        print(f"   Class {class_id} ({class_names[class_id]}): {img_count} images")

if __name__ == "__main__":
    # Set random seed for reproducibility
    random.seed(42)
    organize_for_childgan()