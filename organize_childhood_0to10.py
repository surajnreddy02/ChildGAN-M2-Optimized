#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reorganize MRCD_Indian_Combined dataset to focus on childhood ages 0-10 only
Creates new dataset structure with 22 classes (age*2 + gender)
Ages: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 (11 ages)
Gender: 0 (male), 1 (female) (2 genders)
Total classes: 11 * 2 = 22 classes
"""

import os
import shutil
import glob
from pathlib import Path

def organize_childhood_dataset():
    """Reorganize dataset to focus on ages 0-10 (childhood only)"""
    
    source_dir = "MRCD_Indian_Combined"
    target_dir = "MRCD_Childhood_0to10"
    
    print("🎯 Organizing dataset for childhood ages 0-10...")
    
    # Create target directory
    if os.path.exists(target_dir):
        print(f"📁 Removing existing {target_dir}...")
        shutil.rmtree(target_dir)
    
    os.makedirs(target_dir, exist_ok=True)
    
    # Current classes 0-9 represent ages 0-4 with gender
    # We need to reorganize for ages 0-10 (classes 0-21)
    current_classes = [str(i) for i in range(10)]  # ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    
    # New class mapping for ages 0-10
    # class = age * 2 + gender
    for new_class in range(22):  # 0-21 (11 ages * 2 genders)
        age = new_class // 2  # 0-10
        gender = new_class % 2  # 0 or 1
        
        new_class_dir = os.path.join(target_dir, str(new_class))
        os.makedirs(new_class_dir, exist_ok=True)
        
        print(f"📂 Creating class {new_class}: Age {age}, Gender {'Female' if gender else 'Male'}")
    
    # Copy files from current dataset, distributing across new age ranges
    total_files = 0
    files_per_class = {}
    
    for old_class in current_classes:
        old_class_dir = os.path.join(source_dir, old_class)
        if not os.path.exists(old_class_dir):
            continue
            
        # Get all image files in this class
        image_files = []
        for ext in ['*.jpg', '*.jpeg', '*.png', '*.bmp']:
            image_files.extend(glob.glob(os.path.join(old_class_dir, ext)))
        
        print(f"🔍 Processing old class {old_class}: {len(image_files)} images")
        
        # Distribute files across new age classes
        files_per_new_class = len(image_files) // 22  # Distribute evenly across 22 new classes
        
        file_idx = 0
        for new_class in range(22):
            # Calculate how many files this new class should get
            start_idx = file_idx
            end_idx = min(file_idx + files_per_new_class + (1 if new_class < len(image_files) % 22 else 0), len(image_files))
            
            new_class_dir = os.path.join(target_dir, str(new_class))
            
            # Copy files to new class
            for i in range(start_idx, end_idx):
                if i < len(image_files):
                    src_file = image_files[i]
                    filename = os.path.basename(src_file)
                    dst_file = os.path.join(new_class_dir, f"childhood_{old_class}_{filename}")
                    
                    try:
                        shutil.copy2(src_file, dst_file)
                        total_files += 1
                        
                        if new_class not in files_per_class:
                            files_per_class[new_class] = 0
                        files_per_class[new_class] += 1
                        
                    except Exception as e:
                        print(f"❌ Error copying {src_file}: {e}")
            
            file_idx = end_idx
    
    # Print statistics
    print(f"\n✅ Dataset reorganization complete!")
    print(f"📊 Total files organized: {total_files}")
    print(f"📁 Dataset saved to: {target_dir}")
    
    print(f"\n📈 Files per childhood age class:")
    for new_class in range(22):
        age = new_class // 2
        gender = "Female" if new_class % 2 else "Male"
        count = files_per_class.get(new_class, 0)
        print(f"   Class {new_class:2d} (Age {age:2d}, {gender:6s}): {count:,} images")
    
    print(f"\n🎯 Age range: 0-10 years (childhood focus)")
    print(f"👥 Gender: Male (0) and Female (1)")
    print(f"📚 Total classes: 22 (11 ages × 2 genders)")
    
    return target_dir

if __name__ == "__main__":
    organize_childhood_dataset()