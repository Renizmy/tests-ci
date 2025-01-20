import os
import jinja2
import yaml

# Define the top-level directories
TOP_LEVEL_DIRS = [
    "external-import",
    "stream",
]

# Collect subdirectories for each top-level directory
dirs = {}
for top_dir in TOP_LEVEL_DIRS:
    if os.path.exists(top_dir):
        dirs[top_dir] = [
            sub_dir for sub_dir in os.listdir(top_dir) if os.path.isdir(os.path.join(top_dir, sub_dir))
        ]

# Load the Jinja template
template_path = ".circleci/templates/dynamic.yml.j2"

with open(".circleci/vars.yml", "r") as yaml_file:
    images = yaml.safe_load(yaml_file)

with open(template_path, "r") as file:
    template = jinja2.Template(file.read())

# Render the template with collected directories
config = template.render(dirs=dirs, version="6.4.2",images=images)

# Write the generated config to a CircleCI configuration file
output_path = "dynamic.yml"
os.makedirs(".circleci", exist_ok=True)
with open(output_path, "w") as file:
    file.write(config)

print(f"Generated CircleCI config at {output_path}")
