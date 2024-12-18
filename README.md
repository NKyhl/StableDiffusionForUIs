# UI Stable Diffusion

Goal: fine tune a stable diffusion model for use in a user interface generation system as a requirements-gathering and simple prototyping tool.

1. **generate-simple-uis/**: scripts and templates for generating a large number of basic UIs and associated labels described using json configurations. A dataset has been uploaded to [Huggingface](https://huggingface.co/datasets/nkyhl/simple-uis) - details below
2. **curated-uis/**: a small set of screenshots from professional websites on Moz's list of the [500 most popular websites](https://moz.com/top500)
3. **train/**: scripts for downloading the previously mentioned dataset from Huggingface and fine-tuning an SDXL base model

**General Setup:**
- `python -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`

## Generate Simple UIs

In order to create many simple user interface samples for use in the first round of training, jinja templating has been used along with a few python scripts to simultaneously generate a large number of images along with simple labels that describe them.

`generate_grid.py`, `generate_navigation.py` and `generate_element.py` focus on generating UIs with only one type of component. These samples can hopefully train the model to understand basic components.

`generate_complete.py` focuses on generating UIs with many components stitched together, described via a json configuration format that can be iterated over to create thousands of samples. These samples can hopefully train the model to understand the composition of components.

[Huggingface dataset](https://huggingface.co/datasets/nkyhl/simple-uis): This dataset was generated using `generate_complete.py` using the following reduced parameters over about an hour, creating 13,034 samples. These options could easily be increased to generate hundreds of thousands to millions of samples if desired:
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