from datasets import load_dataset
from tqdm import tqdm
import os

'''Download dataset of composed UIs from HuggingFace'''

dataset = load_dataset("nkyhl/simple-uis")

output_dir = "data"
os.makedirs(output_dir, exist_ok=True)

# Iterate through the dataset and save images and metadata
for row in tqdm(dataset['train'], desc="Downloading dataset"):
    tag = row['name']

    # Save image at lower quality
    image = row['image']
    image.save(os.path.join(output_dir, f"{tag}.jpg"), "JPEG", quality=85)

    # Save caption (label)
    with open(os.path.join(output_dir, f"{tag}.caption"), "w") as f:
        f.write(row['caption'])
    
    # Save JSON configuration used to generate the UI (Optional)
    # with open(os.path.join(output_dir, f"{tag}.config"), "w") as f:
    #     f.write(row['config'])
