import os
import random
import shutil

classes = ["dry_waste", "e_waste", "wet_waste", "sanitary_waste"]

for class_name in classes:

    # Here we will read all the images.
    folder = f"data/raw/{class_name}"
    images = [f for f in os.listdir(folder) if f.lower().endswith(('.jpg' , '.jpeg' , '.png'))]

    # shuffle randomly
    random.shuffle(images)

    images = images[:1000]

    # calculate split positions
    total     = len(images)
    train_end = int(total * 0.70)
    val_end   = int(total * 0.85)

    train = images[0:train_end]
    val   = images[train_end:val_end]
    test  = images[val_end:]

    # create destination folders
    os.makedirs(f"data/train/{class_name}", exist_ok=True)
    os.makedirs(f"data/val/{class_name}",   exist_ok=True)
    os.makedirs(f"data/test/{class_name}",  exist_ok=True)

    # copy files
    for image in train:
        shutil.copy(f"data/raw/{class_name}/{image}",
                    f"data/train/{class_name}/{image}")

    for image in val:
        shutil.copy(f"data/raw/{class_name}/{image}",
                    f"data/val/{class_name}/{image}")

    for image in test:
        shutil.copy(f"data/raw/{class_name}/{image}",
                    f"data/test/{class_name}/{image}")

    print(f"{class_name} done — train:{len(train)} val:{len(val)} test:{len(test)}")