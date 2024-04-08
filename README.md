# elementaryChatApp

## This is a ChatApp Built on AzureOpenAI. It is created to cater help to elementary students

![Alt text](/images/elementaryChatApp.png)

# Run Locally

## Define below variable in env file

<code> OPENAI_ENDPOINT = ""  </code>
<code> OPENAI_API_KEY = "" </code>
<code> REGION="" </code>
<code> AZ_DEFAULT_DEPLOYMENT=""</code>

## Run on terminal
<code> streamlit run .\mainApp.py </code>

# Deploment to Azure App Service.

## Create App Service in Azure

![Alt text](/images/AppService.png)

## Provide the Github location while deployment

![Alt text](/images/Github-setup.png)

## App Service is created. Validate deployment status from github action or Deployment center in App Service

![Alt text](/images/GithubDeployment.png)

## Update enviornment variables

![Alt text](/images/EnvVariables.png)

## Update Statup Command in Configuration in App Service

![Alt text](/images/updateconfig.png)

## Run it by Selecting Default Domain in App Service.

![Alt text](/images/DeployedApp.png)