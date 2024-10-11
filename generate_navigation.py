import os
from jinja2 import Environment, FileSystemLoader
from selenium import webdriver
from time import sleep

# Set up Jinja2 template environment
env = Environment(loader=FileSystemLoader('templates'))

# Load the template
template = env.get_template('nav.html')

# Selenium setup
driver = webdriver.Chrome()

# Create folders if they don't exist
if not os.path.exists('screenshots'):
    os.makedirs('screenshots')
if not os.path.exists('labels'):
    os.makedirs('labels')

SUBFOLDER = 'navigation'
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

def generate_nav_ui(theme, logo: str, links: list, dropdown: bool, searchbar: bool):
    # Create unique identifier
    tag = f"""{SUBFOLDER}_{f'{len(links)}-links-{"-".join(links)}'}{f'_dropdown' if dropdown else ''}{'_searchbar' if searchbar else ''}_{theme}"""

    # Render the HTML
    rendered_html = template.render(
        logo=logo,
        links=links,
        dropdown=dropdown,
        searchbar=searchbar,
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
    sleep(0.03)
    
    # Take screenshot and save it
    screenshot_path = f'screenshots/{SUBFOLDER}/ui_{tag}.png'
    driver.save_screenshot(screenshot_path)

    # Save description
    label = f"a navbar at the top of the screen{f' with {len(links)} links labeled: {links}' if links else ''}{' with a search bar' if searchbar else ''} with a {theme} theme"
    label_path = f'labels/{SUBFOLDER}/ui_{tag}.caption'
    with open(label_path, 'w') as f:
        f.write(label)

    # Remove HTML
    os.remove(f'./{html_file}')

# Generate and capture multiple UIs
link_configurations = [
    ['Home', 'About'],
    ['Home', 'About', 'Contact'],
    ['Home', 'About', 'Pricing', 'Careers'],
    ['Home', 'About', 'Contact', 'Portfolio', 'Blog'],
    ['Home', 'About', 'Team', 'Services', 'Pricing', 'FAQ'],
]
dropdown_configurations = [True, False]
searchbar_configurations = [True, False]

for theme in THEMES:
    for links in link_configurations:
        for dropdown in dropdown_configurations:
            for searchbar in searchbar_configurations:
                generate_nav_ui(theme, "Logo", links, dropdown, searchbar)

# Close the browser
driver.quit()