import os
from jinja2 import Environment, FileSystemLoader
from selenium import webdriver
from time import sleep

# Set up Jinja2 template environment
env = Environment(loader=FileSystemLoader('templates'))

# Load the template
template = env.get_template('input.html')

# Selenium setup
driver = webdriver.Chrome()

# Create folders if they don't exist
if not os.path.exists('screenshots'):
    os.makedirs('screenshots')
if not os.path.exists('labels'):
    os.makedirs('labels')

SUBFOLDER = 'input'
if not os.path.exists(f'screenshots/{SUBFOLDER}'):
    os.makedirs(f'screenshots/{SUBFOLDER}')
if not os.path.exists(f'labels/{SUBFOLDER}'):
    os.makedirs(f'labels/{SUBFOLDER}')

THEMES = {
    'light': {
        'background': '#FFF',
        'shade-1': '#F8F8F8',
        'border': '#c7c7c7',
        'text': '#000',
    },
    'dark': {
        'background': '#000',
        'shade-1': '#1F1F1F',
        'border': '#292929',
        'text': '#E1E1E1',
    },
}

def generate_input_ui(theme, input_type, default_value, location, location_description):
    # Create unique identifier
    tag = f'{SUBFOLDER}_{input_type}_{location_description}_{theme}'

    # Render the HTML
    rendered_html = template.render(
        input_type=input_type,
        default_value=default_value,
        row=location[0],
        col=location[1],
        theme=THEMES[theme]
    )
    
    # Save the HTML file
    html_file = f'generated_ui_{tag}.html'
    with open(f'{html_file}', 'w') as f:
        f.write(rendered_html)
    
    # Load the generated HTML in the browser
    file_path = f'file://{os.getcwd()}/{html_file}'
    driver.get(file_path)
    
    # Wait for the page to fully load
    sleep(0.05)
    
    # Take screenshot and save it
    screenshot_path = f'screenshots/{SUBFOLDER}/ui_{tag}.png'
    driver.save_screenshot(screenshot_path)

    # Save description
    label = f'a user interface with a {input_type} input field in the {location_description} with a {theme} theme'
    label_path = f'labels/{SUBFOLDER}/ui_{tag}.caption'
    with open(label_path, 'w') as f:
        f.write(label)

    # Remove HTML
    os.remove(f'./{html_file}')

# Generate and capture multiple UIs
locations = {
    'top-left': (1, -1),
    'top-center': (1, 0),
    'top-right': (1, 1),
    'left': (0, -1),
    'center': (0, 0),
    'right': (0, 1),
    'bottom-left': (-1, -1),
    'bottom-center': (-1, 0),
    'bottom-right': (-1, 1),
}
input_types = { # Map input types to their default values
    'button': "Button",
    'checkbox': "Checkbox",
    'date': '2021-01-01',
    'datetime-local': '2021-01-01T00:00',
    'email': 'johndoe@email.com',
    'file': None,
    'month': '2021-01',
    'number': '42',
    'password': 'password',
    'radio': "Radio",
    'range': '50',
    'reset': 'Reset',
    'search': 'Search',
    'submit': 'Submit',
    'tel': '123-456-7890',
    'text': 'Text',
    'time': '1:00',
    'url': 'https://www.example.com',
    'week': '2021-W01',
}

for theme in THEMES:
    for input_type, default_value in input_types.items():
        for location_description, location in locations.items():
            generate_input_ui(theme, input_type, default_value, location, location_description)

# Close the browser
driver.quit()