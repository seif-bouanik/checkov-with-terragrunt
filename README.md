### General  
These scripts should help integrate Checkov, Tflint and Tfsec on Terraform projects running Terragrunt.  

This was tailored to a CI/CD pipeline, alternatively, you can integrate these tools using Terragrunt hooks, with much less overhead.  
  
  
```
terraform {
  before_hook "CHECKOV" {
      commands = ["plan"]
      execute = [
          "checkov",
          "-d",
          ".",
          "--quiet",
          "--skip-download",
          "--skip-fixes",
          "--output-file-path",
          "${get_terragrunt_dir()}"
      ]
  }
}
```
For more, please see [this issue](https://github.com/bridgecrewio/checkov/issues/1284).

### PROJECT STRUCTURE  
The scripts should be placed under the envionrment folder, where you have your root terragrunt.hcl.  

UTILITIES where you should keep your tools config files shoudl be placed on the same level as your root Terragrunt directory, to avoid duplicating these files, if you wish to make custom configs for every environment, then please adjust the utilities path in the scripts.  
  
  

```
. <------------------------------------------------ project_dir
├── MODULES
├── TERRAGRUNT <----------------------------------- terragrunt_dir
│   └── DEV <-------------------------------------- environment_dir
│       ├── MODULE_1
            ...
│       ├── MODULE_N
│       ├── TERRAGRUNT_CHECKOV.py
│       ├── TERRAGRUNT_TFLINT.py
│       ├── TERRAGRUNT_TFSEC.py
│       └── terragrunt.hcl
└── UTILITIES  <----------------------------------- utilities_dir
    ├── CHECKOV_CONFIG.yaml
    └── .tflint.hcl
```



### CONFIG FILES  
All the needed config files are expected in the utilities folder in the project directory.  
  
  
### OUTPUTS  
The expected ouptputs are:
```
# Checkov
# JSON-formatted plan for every module:
. <------------------------------------------------ project_dir
...
├── PLAN_MODULE_1.json
├── PLAN_MODULE_1_PRETTY.json
...
├── PLAN_MODULE_2.json
├── PLAN_MODULE_2_PRETTY.json
# Checkov report:
├── CHECKOV_REPORT.txt
...
```
  

```
# Tflint
...
├── TFLINT_REPORT.txt
...
```
  

```
# Tfsec
...
├── TFSEC_REPORT.md
...
```