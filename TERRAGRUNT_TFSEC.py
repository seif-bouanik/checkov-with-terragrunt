import os
from pathlib import Path

# -------------------------------------
# FUNCTIONS
# -------------------------------------
def find_terragrunt_module_dir(components, search_path):
    result = []
    for root, dirs, files in os.walk(search_path):
        for directory in dirs:
            if directory in components:
                full_path = os.path.join(root, directory)
                if full_path.count(directory) > 1:
                    result.append(full_path)
    return result


# -------------------------------------
# VARIABLES
# -------------------------------------
environment_dir = os.getcwd()
terragrunt_dir = Path(environment_dir).parent
project_dir = Path(environment_dir).parent.parent
utilities = "UTILITIES"
utilities_dir = os.path.join(project_dir, utilities)
tfsec_output = "TFSEC_REPORT.md"
components = []


# -------------------------------------
# GET THE TERRAGRUNT-GENERATED TERRAFORM MODULES
# -------------------------------------
# Get the name of all the terraform components:
for directory in next(os.walk(environment_dir))[1]:
    components.append(directory)

# Find all terraform components path in .terragrunt-cache folders
# Logic is to find folders with the following name format: component/*/component
# For instance: /COMPONENT_DATA_STORES/.terragrunt-cache/ziEXqU-89LXliExCBShCCFSL-m4/gGPLzzF_etExkGrpN44aKnIxdPY/COMPONENT_DATA_STORES
# In this folder we can find the terragrunt-generated terraform module
terragrunt_modules = find_terragrunt_module_dir(components, terragrunt_dir)

# We run TFSEC on every terragrunt-generated terraform module
for terragrunt_module in terragrunt_modules:
    os.chdir(terragrunt_module)
    os.system(
        f"tfsec . -f markdown >> {os.path.join(project_dir, tfsec_output)}")
