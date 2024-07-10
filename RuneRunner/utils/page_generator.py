import os
from jinja2 import Environment, FileSystemLoader

def generate_index_page(base_dir):
    template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('index.html')

    links = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.html'):
                rel_path = os.path.relpath(os.path.join(root, file), base_dir)
                links.append({'name': rel_path, 'path': rel_path})

    output = template.render(links=links)
    with open(os.path.join(base_dir, 'index.html'), 'w') as f:
        f.write(output)