# Ensuring Quality Releases

This project demonstrates the automation of deploying a demo REST API on Microsoft Azure using Azure App Service and executing automated tests against the API. The infrastructure is provisioned using Terraform, and a CI/CD pipeline is set up for seamless integration and testing.

## How to use?
- Fork this repository to your Github account and clone it locally 

### Depencies
For this you'll need to install the following depencies

- Azure CLI
- Terraform
- JMeter
- Postman
- Python
- Selenium
- Chromedriver
- Chrome

### Instructions

You'll need to login in to your azure account before starting in any terminal you have open, it can be in your own cdm

```
az login
```

In this repository we will be using the azure credentials proporcionated by udacity, so, we'll be using the azure resource group that already exists Azuredevops

## Run packer image for the vm

First, you need to update the variable defined in packer-image.json, you''ll need to replace:

```
    "subscription_id": "",
    "tenant_id": "",
    "client_id": "",
    "client_secret": "",   
    "resource_group_name": "",
    "image_name": "",
    "vm_size": ""
```

After that, you just have to run the following code:
```
packer build ./packer-image.json
```
![Alt text](<screenshots/packer_image.png>)

## Configure the storage account and state backend 

- First, run the script create-tf-storage.sh

```
bash create-tf-storage.sh
```
- Then replace the values in terraform/main.tf with the output from running the create-tf-storage.sh

```
terraform {
    backend "azurerm" {
        storage_account_name = ""
        container_name       = "tfstate"
        key                  = "test.terraform.tfstate"
        access_key           = ""
    }
}
```

## Configure terraform

- Update the values in terraform.tfvars
- Generate an SSH keys in azure command shell
```
ssh-keygen -t rsa
cat ~/.ssh/id_rsa.pub
```
- Put the keys in terraform/modules/vm/vm.tf
```
  admin_ssh_key {
    username   = var.vm_admin_username
    public_key = "" 
  }
```

## Executing terraform

- First you'll need to create a new project
- Then create a PAT and copy it to used it later
- Make a new service connection
- Create an agent pool with access to all pipelines, add this agent to a vm
- Create an enviroment and provide it to a different vm that the one used in the previus step
- Finally create a new pipeline, selecting the GitHub repository of this project, and for the yaml select azure-pipelines.yaml

Update the terraform variables with the ones created in those steps:

```
variables:
  python.version: ''
  azureServiceConnectionId: ''
  projectRoot: $(System.DefaultWorkingDirectory)
  environmentName: ''
  tfstatenumber: '' 
  tfrg: ''
  application_type: ''  
```

- Build FakeRestAPI artifact by archiving the entire FakeRestAPI directory into a zip file and publishing the pipeline artifact to the artifact staging directory

- Deploy the FakeRestAPI to the terraform deployed Azure App Service, the url will be
```http://[yourusername]-fakerestapi-appservice.azurewebsites.net/``` 

![Alt text](screenshots/deployed_fakerestapi.png)

### Automated testing

#### Integration testing postman

- Data validation test
![Alt text](screenshots/validation_test.png)
- Regression test
![Alt text](screenshots/regression_test-1.png)

#### Performance testing jmeter

- Stress test
![Alt text](screenshots/stress_test.png)
![Alt text](screenshots/jmeter_stress_html.png)
- Endurance test
![Alt text](screenshots/endurance_test.png)
![Alt text](screenshots/jmeter_endurance_hrml.png)
#### Functional UI testing selenium
![Alt text](screenshots/selenium_test.png)

The pipeline execution should look like this

![Alt text](screenshots/pipeline_successful-1.png)

## Monitoring and Observability

- Go to the Azure Portal and create a new alert in the monitoring group, then execute the pipeline to trigger an alert

Monitor chart
![Alt text](screenshots/monitor_chart.png)

Trigger email alert

![Alt text](screenshots/trigger_email.png)

- Configure azure log analytics by downloading the selenium-test.log artifact from Azure Devops
- Navigate to the Azure Portal and access Azure Log Analytics workspaces. Configure an agent on the virtual machine where the Selenium testing will take place. Ensure the VM is connected to Log Analytics and establish a Data Collection Rule to capture the necessary logs.
- Navigate to the Logs section and initiate the creation of a custom log. Import the file named selenium-test.log. Choose "Timestamp" with the format YYYY-MM-DD HH:MM:SS as the record separator. Specify the path of the selenium-test.log from the VM where the task was executed as the collection path for logs (please note that there might be a delay before the VM can start collecting logs).

#### Querying custom logs

- Then go to logs in general group of your log analytics, select your custom log and run it
![Alt text](screenshots/querying_custom_logs.png)

## Destroy the terraform resources

```
cd terraform
terraform destroy
```