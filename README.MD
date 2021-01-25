### Story Time
DL based interactive Alexa skill. You create a story with Alexa by taking turns and saying three words on each turn.

### Run API locally
After you have cloned the repository, install the dependencies with pip

`pip install -r requirements.txt`

Run application with

`uvicorn api.main:app`

### Run API on Digital Ocean
1. Install terraform 
2. Go to the terraform directory in the project
3. Create `terraform.tfvars` file and initialize all the variables present in the `variables.tf` (`terraform.tfvars.example` included)
4. Run `terraform init` 
5. To see what changes the script will make to the cloud run `terraform plan`
6. To execute the script run `terraform apply`
7. To remove all the resources which where created run `terraform destroy`

### Authors:
* Nino Basilaia ninucabas@gmail.com
* Somesh Khandelia  someshkhandelia@gmail.com
