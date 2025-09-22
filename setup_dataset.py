#!/usr/bin/env python3
"""
Dataset Setup Helper for ChildGAN on M2 Mac
This script shows you how to organize your MRCD dataset for training.
"""

import os

def create_dataset_structure():
    """
    Creates the expected dataset directory structure for ChildGAN training.
    """
    
    # Base dataset directory
    dataset_root = "data/MRCD"
    
    # Age-gender categories as per README
    categories = {
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
    
    print("🗂️  Creating MRCD dataset directory structure...")
    print(f"📁 Base directory: {dataset_root}/")
    
    # Create directories
    for category_id, description in categories.items():
        category_path = os.path.join(dataset_root, category_id)
        os.makedirs(category_path, exist_ok=True)
        print(f"   📁 {category_id}/ ({description})")
    
    print("\n✅ Dataset structure created!")
    print("\n📋 Next Steps:")
    print("1. Download MRCD dataset from:")
    print("   https://drive.google.com/file/d/1_jOclJy3AFbSHzKsuIh7QD-UOsb5p2RT/view?usp=drive_link")
    print("2. Fill out the agreement form (MRCD Dataset Agreement Form.pdf)")
    print("3. Extract images to appropriate folders above")
    print("4. Images should be named: age_genderId_sequenceID.jpg")
    print("   - age: person's age")
    print("   - genderId: 0 for boys, 1 for girls") 
    print("   - sequenceID: unique identifier")
    
    return dataset_root

def check_dataset_ready(dataset_root):
    """
    Checks if dataset is properly set up for training.
    """
    print(f"\n🔍 Checking dataset at: {dataset_root}")
    
    if not os.path.exists(dataset_root):
        print("❌ Dataset directory not found!")
        return False
    
    categories = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09"]
    total_images = 0
    
    for category in categories:
        category_path = os.path.join(dataset_root, category)
        if os.path.exists(category_path):
            images = [f for f in os.listdir(category_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            total_images += len(images)
            print(f"   📁 {category}/: {len(images)} images")
        else:
            print(f"   ❌ {category}/: Missing!")
    
    print(f"\n📊 Total images found: {total_images}")
    
    if total_images > 0:
        print("✅ Dataset appears ready for training!")
        return True
    else:
        print("❌ No images found. Please add dataset images.")
        return False

def show_training_command(dataset_root):
    """
    Shows the command to run ChildGAN training with proper parameters.
    """
    print(f"\n🚀 To start training with your M2 GPU:")
    print(f"python3 ChildGANTrain.py \\")
    print(f"    --dataroot '{dataset_root}' \\")
    print(f"    --batch_size 4 \\")
    print(f"    --image_size 128 \\")
    print(f"    --niter 25000 \\")
    print(f"    --outf 'output'")
    
    print(f"\n🔬 For testing/inference:")
    print(f"python3 ChildGANTest.py")

if __name__ == "__main__":
    print("🎯 ChildGAN Dataset Setup for M2 Mac")
    print("=" * 50)
    
    # Create dataset structure
    dataset_root = create_dataset_structure()
    
    # Check if images are present
    check_dataset_ready(dataset_root)
    
    # Show training commands
    show_training_command(dataset_root)
    
    print("\n💡 Tips for M2 Mac:")
    print("- Start with small batch_size (4-8) to test memory")
    print("- Monitor Activity Monitor for GPU usage")
    print("- MPS backend is automatically detected and used")
    print("- Training will be much faster than CPU!")