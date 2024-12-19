# Stable Diffusion for User Interfaces

Goal: fine tune a stable diffusion model for use in a user interface generation system as a simple prototyping and requirements-gathering tool.

1. **generate-simple-uis/**: scripts and templates for generating a dataset of UIs and associated labels described using json configurations. A dataset has been uploaded to [Huggingface](https://huggingface.co/datasets/nkyhl/simple-uis) - details below
2. **curated-uis/**: a small set of unlabeled screenshots from professional websites on Moz's list of the [500 most popular websites](https://moz.com/top500)
3. **train/**: scripts for downloading the previously mentioned dataset from Huggingface and fine-tuning an SDXL base model
4. **meeting-notes/**: PDFs of the research updates given every two weeks in Fall 2024

## Generate Simple UIs

In order to create many simple user interface samples for use in the first round of training, jinja templating has been used along with a few python scripts to simultaneously generate a large number of images along with simple labels that describe them.

`generate_grid.py`, `generate_navigation.py` and `generate_element.py` focus on generating UIs with only one type of component. These samples can hopefully train the model to understand basic components.

`generate_complete.py` focuses on generating UIs with many components stitched together, described via a json configuration format that can be iterated over to create thousands of samples. These samples can hopefully train the model to understand the composition of components.

[Huggingface dataset](https://huggingface.co/datasets/nkyhl/simple-uis): This dataset was generated using `generate_complete.py` and uploaded using `prepare_and_upload_dataset.py`. It was created with the following reduced parameters over about an hour, creating 13,034 samples. These options could easily be increased to generate hundreds of thousands to millions of samples if desired:
- row_range = (1,4)
- col_range = (1,4)
- themes = [{'name': 'light','background': '#FFF','shade-1': '#F8F8F8','border': '#c7c7c7','text': '#000',},{'name': 'dark','background': '#000','shade-1': '#1F1F1F','border': '#292929','text': '#E1E1E1',}]
- input_types = {'button': "Button",'checkbox': "Checkbox",'date': '2021-01-01','email': 'johndoe@email.com','file': None,'password': 'password','radio': "Radio",'range': '50','submit': 'Submit','url': 'https://www.example.com'}
- link_configurations = [['Home', 'About']]
- searchbar_configurations = [True, False]
- align_configurations = ['start', 'center', 'end']

## Curated UIs

The UIs generated in the first section are very simplistic and miss out on many of the key elements of a professional-looking user interface.

To improve our model further, a small dataset of professional UI samples has been initiated that can hopefully train the model to create professional user interfaces. This dataset is currently not labeled.

These screenshots were manually taken from 40-50 sites off Moz's list of the [500 most popular websites](https://moz.com/top500). 
News sites were avoided because of the recent election, as every news site had election-themed content that would likely teach the model an unneccessary pattern.
In many cases, multiple screenshots were taken from different pages on a single website, hopefully allowing the model to learn how to create multiple pages in a similar theme.

Many of these images were full-page captures, and could be spliced into smaller sections for use in training.

## Train

The following section describes how the base SDXL model was fine-tuned on the generated UIs. Please see the December 3rd Research Update for more information on the different training approaches used over the course of the semester and their hyperparameters. I have uploaded a few of these fine-tuned models to Huggingface here: [sdxl-simple-ui-generator](https://huggingface.co/nkyhl/sdxl-simple-ui-generator/).

`download_dataset.py` downloads the Huggingface dataset of complete uis (simple uis composed of multiple sections) and saves the individual files to the ./data folder.

**Prerequisites**
1. Please clone [kohya/sd-scripts](https://github.com/kohya-ss/sd-scripts) elsewhere as it includes a few scripts necessary for training. Its location is designated by [sd-scripts] in the following commands. After cloning, make sure to execute `source [sd-scripts]/venv/bin/activate` in order to utilize these scripts.
2. Please download EasyDiffusion or another front-end if you would like to try out your fine-tuned model.
3. Please download the [SDXL base model](https://civitai.com/models/101055/sd-xl) in safetensors format. You may want to download straight to your [easy-diffusion]/models/stable-diffusion/ folder and reference it when training. Its location is designated by [SDXL] in the following commands.

**Example: Fine-Tuning SDXL on the HuggingFace Dataset:**
- `cd train/`
- `python download_dataset.py`
- `python [sd-scripts]/finetune/merge_captions_to_metadata.py . ./data/meta_cap.json`
- `python [sd-scripts]/finetune/prepare_buckets_latents ./data ./data/meta_cap.json ./data/meta_lat.json [SDXL] --batch_size 4 --mixed_precision bf16`
- `accelerate launch --num_cpu_threads_per_process 1 [sd-scripts]/sdxl_train.py —pretrained_model_name_or_path=[SDXL] —in_json ./data/meta_lat.json —train_data_dir=[pwd]/data/ —output_dir=[easy-diffusion]/models/stable-diffusion/ —train_batch_size=4 —learning-rate=1e-6 —max_train_steps=4000 —gradient_checkpointing —mixed_precision=bf16 —save_every_n_steps=400 —save_model_as=safetensors —keep_tokens=255 —optimizer_type=adafactor —optimizer_args scale_parameter=False relative_step=False warmup_init=False —cache_latents —lr_warmup_steps=100 —max_grad_norm=0.0 —max_data_loader_n_workers=1 —persistent_data_loader_workers —full_bf16 —lr_scheduler=constant_with_warmup`

**Notes:**
- Preparing bucket latents for the Huggingface Dataset took around 2 hours on the given hardware,
- Sdxl_train.py requires full file paths rather than relative paths (like ./data) for most command line args for the sdxl_train script. [pwd] designates the full path to this project including train/.
- Labels must have the file extension .caption to prepare bucket latents.
