import os
from pathlib import Path


# -------------------------------------
# FUNCTIONS
# -------------------------------------
def find_files(plan_extension, search_path):
   result = []
   for root, dir, files in os.walk(search_path):
    for file in files:
      if file.endswith(plan_extension):
         result.append(os.path.join(root, file))
   return result

# -------------------------------------
# VARIABLES
# -------------------------------------
environment_dir    = os.getcwd()
terragrunt_dir     = Path(environment_dir).parent
project_dir        = Path(environment_dir).parent.parent
utilities          = "UTILITIES"
utilities_dir      = os.path.join(project_dir, utilities)
checkov_config     = "CHECKOV_CONFIG.yaml"
checkov_output     = "CHECKOV_REPORT.txt"

# -------------------------------------
# CREATE PLANS PER MODULE
# -------------------------------------
# Going through the first level dirs in the environment_dir
for directory in next(os.walk(environment_dir))[1]:
    # Generating the component full path
    component_dir = os.path.join(environment_dir, directory)
    # If the component has a terragrunt.hcl file, we create a plan, the plan will be generated within .terragrunt-cache folder inside every component
    if 'terragrunt.hcl' in os.listdir(component_dir):
        os.chdir(component_dir)
        os.system(f'terragrunt plan --out=PLAN_{directory}.plan')

# -------------------------------------
# RUN CHECKOV
# -------------------------------------
# This variable contains the full paths of the terragrunt generated plans in the .terragrunt-cache dirs
terragrunt_plans = find_files(".plan", project_dir)

for terragrunt_plan_path in terragrunt_plans:
    # CONVERT TO JSON
    # This variable contains the full path of the json plan located in the project_dir
    converted_plan_path = os.path.join(project_dir, os.path.basename(terragrunt_plan_path)[:-5]+".json")
    converted_pretty_plan_path = os.path.join(project_dir, os.path.basename(terragrunt_plan_path)[:-5]+"_PRETTY.json")

    # Change dir to where the terragrunt plan is (To avoid plugins issues)
    os.chdir(os.path.dirname(terragrunt_plan_path))

    # Convert the plan into json and place it in the project_dir
    os.system(f'terraform show -json {terragrunt_plan_path} > {converted_plan_path}')

    # BEAUTIFY JSON
    os.system(f"jq '.' {converted_plan_path} > {converted_pretty_plan_path}")

    # RUN CHECKOV
    # Chdir to the project_dir again and run checkov using he 
    os.chdir(project_dir)
    os.system(
        f'checkov -f {converted_pretty_plan_path} --config-file {os.path.join(utilities_dir, checkov_config)} >> {checkov_output}')
