import os
from jinja2 import Environment, FileSystemLoader
from selenium import webdriver
from time import sleep

# Set up Jinja2 template environment
env = Environment(loader=FileSystemLoader('templates'))

# Load the template
template = env.get_template('grid.html')

# Selenium setup
driver = webdriver.Chrome()

# Create folders if they don't exist
if not os.path.exists('screenshots'):
    os.makedirs('screenshots')
if not os.path.exists('labels'):
    os.makedirs('labels')

SUBFOLDER = 'grid'
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

def generate_grid_ui(theme, rows, columns):
    # Create unique identifier
    tag = f'{SUBFOLDER}_{rows}_{columns}_{theme}'

    # Render the HTML with x columns
    rendered_html = template.render(
        rows=rows,
        cols=columns,
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
    label = f'{rows} rows of {columns} columns with a {theme} theme'
    label_path = f'labels/{SUBFOLDER}/ui_{tag}.caption'
    with open(label_path, 'w') as f:
        f.write(label)

    # Remove HTML
    os.remove(f'./{html_file}')

# Generate and capture multiple UIs
for theme in THEMES:
    for iRow in range(1, 4):
        for iCol in range(1, 6):
            # Skip unecessary grid
            if iRow == 1 and iCol == 1:
                continue

            generate_grid_ui(theme, iRow, iCol)

# Close the browser
driver.quit()