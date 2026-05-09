import os

classes = ["dry_waste", "e_waste", "wet_waste", "sanitary_waste"]
splits  = ["train", "val", "test"]

total = 0

for split in splits:
    print(f"\n{split.upper()}")
    split_total = 0
    for cls in classes:
        path = f"data/{split}/{cls}"
        count = len([f for f in os.listdir(path) 
                     if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
        print(f"  {cls}: {count} images")
        split_total += count
        total += count
    print(f"  subtotal: {split_total}")

print(f"\nTOTAL IMAGES: {total}")