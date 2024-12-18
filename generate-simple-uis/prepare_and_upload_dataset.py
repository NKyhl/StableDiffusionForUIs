import os
import json
from datasets import Dataset, Features, Image, Value, DatasetDict
from huggingface_hub import login
from ast import literal_eval

'''Upload dataset to HuggingFace as a .parquet file'''

login()
image_dir = 'screenshots/complete'
label_dir = 'labels/complete'

data = []
for image_name in os.listdir(image_dir):
    base = os.path.splitext(image_name)[0]
    image_path = os.path.join(image_dir, image_name)
    caption_path = os.path.join(label_dir, f'{base}.caption')
    config_path = os.path.join(label_dir, f'{base}.config')

    with open(caption_path, 'r') as f:
        caption = f.read().strip()

    with open(config_path, 'r') as f:
        d = f.read().strip()
        config = literal_eval(d)
        config = json.dumps(config)

    data.append({"image": image_path, "name": base, "caption": caption, "config": config})

features = Features({
    'image': Image(),
    'name': Value('string'),
    'caption': Value('string'),
    'config': Value('string')
})

dataset = Dataset.from_list(data, features=features)
dataset.push_to_hub("nkyhl/simple-uis")