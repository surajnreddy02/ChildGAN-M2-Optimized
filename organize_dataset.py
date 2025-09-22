#!/usr/bin/env python3
"""
MRCD Dataset Organization Script
Combines Asian, Black, and White datasets into unified structure
"""

import os
import shutil
from pathlib import Path

def organize_mrcd_dataset():
    """
    Organizes the MRCD dataset by combining all ethnic groups into unified folders
    """
    base_path = Path(".")
    source_path = base_path / "MRCD_Asian_Black_White_Dataset"
    target_path = base_path / "data" / "MRCD"
    
    print("🔄 Organizing MRCD Dataset...")
    
    # Create target structure
    target_path.mkdir(parents=True, exist_ok=True)
    
    # Categories: 00-09 (age/gender combinations)
    categories = [f"{i:02d}" for i in range(10)]
    
    for category in categories:
        category_path = target_path / category
        category_path.mkdir(exist_ok=True)
    
    # Source datasets
    datasets = [
        "PR_AsianChildData",
        "PR_BlackChildData", 
        "PR_WhiteChildData_WhiteFinal"
    ]
    
    total_copied = 0
    
    for dataset in datasets:
        dataset_path = source_path / dataset
        if not dataset_path.exists():
            print(f"⚠️  {dataset} not found, skipping...")
            continue
            
        print(f"📁 Processing {dataset}...")
        
        for category in categories:
            source_cat_path = dataset_path / category
            target_cat_path = target_path / category
            
            if source_cat_path.exists():
                # Get all image files
                image_files = list(source_cat_path.glob("*.jpg")) + list(source_cat_path.glob("*.png"))
                
                for img_file in image_files:
                    # Create unique filename to avoid conflicts
                    prefix = dataset.split("_")[1].lower()  # asian, black, white
                    new_name = f"{prefix}_{img_file.name}"
                    target_file = target_cat_path / new_name
                    
                    # Copy file
                    shutil.copy2(img_file, target_file)
                    total_copied += 1
                
                print(f"   📂 {category}/: {len(image_files)} images")
    
    print(f"\n✅ Dataset organization complete!")
    print(f"📊 Total images copied: {total_copied}")
    
    # Verify the organization
    verify_dataset_structure(target_path)
    
    return target_path

def verify_dataset_structure(dataset_path):
    """
    Verifies the dataset structure and counts images
    """
    print(f"\n🔍 Verifying dataset at: {dataset_path}")
    
    categories = [f"{i:02d}" for i in range(10)]
    category_names = {
        "00": "0-3 Years Boys",
        "01": "0-3 Years Girls", 
        "02": "4-8 Years Boys",
        "03": "4-8 Years Girls",
        "04": "9-12 Years Boys", 
        "05": "9-12 Years Girls",
        "06": "13-16 Years Boys",
        "07": "13-16 Years Girls",
        "08": "17-20 Years Boys",
        "09": "17-20 Years Girls"
    }
    
    total_images = 0
    
    for category in categories:
        category_path = dataset_path / category
        if category_path.exists():
            images = list(category_path.glob("*.jpg")) + list(category_path.glob("*.png"))
            total_images += len(images)
            print(f"   📁 {category}/ ({category_names[category]}): {len(images)} images")
        else:
            print(f"   ❌ {category}/: Missing!")
    
    print(f"\n📊 Total images: {total_images}")
    
    if total_images > 0:
        print("✅ Dataset ready for training!")
        return True
    else:
        print("❌ No images found!")
        return False

if __name__ == "__main__":
    print("🎯 MRCD Dataset Organization")
    print("=" * 50)
    
    dataset_path = organize_mrcd_dataset()
    
    print(f"\n🚀 Ready to train! Use this command:")
    print(f"python3 ChildGANTrain.py --dataroot '{dataset_path}' --batch_size 4 --niter 1000")