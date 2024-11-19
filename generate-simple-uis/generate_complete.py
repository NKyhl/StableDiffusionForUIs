import json
import os
from jinja2 import Environment, FileSystemLoader
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep, time
from itertools import product

# Set up Jinja2 template environment
env = Environment(loader=FileSystemLoader('templates'))

# Load the template
template = env.get_template('complete.html')

# Selenium setup
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome()

# Create folders if they don't exist
if not os.path.exists('screenshots'):
    os.makedirs('screenshots')
if not os.path.exists('labels'):
    os.makedirs('labels')

SUBFOLDER = 'complete'
if not os.path.exists(f'screenshots/{SUBFOLDER}'):
    os.makedirs(f'screenshots/{SUBFOLDER}')
if not os.path.exists(f'labels/{SUBFOLDER}'):
    os.makedirs(f'labels/{SUBFOLDER}')

def generate_complete_ui(config):
    # Create unique identifier
    tag = f"""{SUBFOLDER}_{time()}"""

    # Render the HTML
    rendered_html = template.render(
        config=config
    )
    
    # Save the HTML file
    html_file = f'generated_ui_{tag}.html'
    with open(f'{html_file}', 'w') as f:
        f.write(rendered_html)
    
    # Load the generated HTML in the browser
    file_path = f'file://{os.getcwd()}/{html_file}'
    driver.get(file_path)
    
    # Wait for the page to fully load
    sleep(0.005)
    
    # Take screenshot and save it
    screenshot_path = f'screenshots/{SUBFOLDER}/ui_{tag}.png'
    driver.save_screenshot(screenshot_path)

    # Generate description
    label = f"a user interface with a {config['theme']['name']} theme"
    if config['navbar']:
        label += f" with a navbar with a 'Logo' logo in the top left with {len(config['navbar']['links'])} links labeled: {', '.join(config['navbar']['links'])}"
        if config['navbar']['searchbar']:
            label += " and a search bar on the right"
    if config['grid']['rows'] > 1 or config['grid']['columns'] > 1:
        label += f". The main content of the page is a grid with {config['grid']['rows']} rows and {config['grid']['columns']} columns"
    if config['input']:
        r, c = config['input']['location']
        label += f". The page also contains an input of type {config['input']['input_type']} at location ({r}, {c}) in the grid"
        if config['input']['default_value']:
            label += f" with the default value '{config['input']['default_value']}'"
        horizontal_align_translations = {
            'start': 'left',
            'center': 'center',
            'end': 'right',
        }
        vertical_align_translations = {
            'start': 'top',
            'center': 'center',
            'end': 'bottom',
        }
        label += f". The input is aligned {horizontal_align_translations[config['input']['horizontal_align']]} horizontally and {vertical_align_translations[config['input']['vertical_align']]} vertically"

    # Save English description
    label_path = f'labels/{SUBFOLDER}/ui_{tag}.caption'
    with open(label_path, 'w') as f:
        f.write(label)

    # Save json configuration 
    config_path = f'labels/{SUBFOLDER}/ui_{tag}.config'
    with open(config_path, 'w') as f:
        json.dump(config, f)

    # Remove HTML
    os.remove(f'./{html_file}')

# Generate and capture multiple UIs
THEMES = [
    {
        'name': 'light',
        'background': '#FFF',
        'shade-1': '#F8F8F8',
        'border': '#c7c7c7',
        'text': '#000',
    },
    {
        'name': 'dark',
        'background': '#000',
        'shade-1': '#1F1F1F',
        'border': '#292929',
        'text': '#E1E1E1',
    },
]

input_types = { # Map input types to their default values
    'button': "Button",
    'checkbox': "Checkbox",
    'date': '2021-01-01',
    # 'datetime-local': '2021-01-01T00:00',
    'email': 'johndoe@email.com',
    'file': None,
    # 'month': '2021-01',
    # 'number': '42',
    'password': 'password',
    'radio': "Radio",
    'range': '50',
    # 'reset': 'Reset',
    # 'search': 'Search',
    'submit': 'Submit',
    # 'tel': '123-456-7890',
    # 'text': 'Text',
    # 'time': '1:00',
    'url': 'https://www.example.com',
    # 'week': '2021-W01',
}

link_configurations = [
    ['Home', 'About'],
]
searchbar_configurations = [True, False]
align_configurations = ['start', 'center', 'end']

for theme in THEMES:
    for iRow in range(3, 4):
        for iCol in range(1, 4):
            print(f"Generating {theme['name']} theme with {iRow} rows and {iCol} columns - {time()}")

            for links in link_configurations:
                for searchbar in searchbar_configurations:

                    for input_type, default_value in input_types.items():
                        for location in product(range(iRow), range(iCol)):
                            for horizontal_align in align_configurations:
                                for vertical_align in align_configurations:

                                    config = {
                                        'theme': theme,
                                        'navbar': {
                                            'logo': 'Logo',
                                            'links': links,
                                            'searchbar': searchbar,
                                        },
                                        'grid': {
                                            'rows': iRow,
                                            'columns': iCol,
                                        },
                                        'input': {
                                            'input_type': input_type,
                                            'default_value': default_value,
                                            'location': location,
                                            'horizontal_align': horizontal_align,
                                            'vertical_align': vertical_align,
                                        }
                                    }

                                    generate_complete_ui(config)

# Close the browser
driver.quit()