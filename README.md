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

## Step 1 - Create App Service in Azure

![Alt text](/images/AppService.png)


## Step 2 - Provide the Github location while deployment

![Alt text](/images/Github-setup.png)


## Step 3 - App Service is created. Validate deployment status from github action or Deployment center in App Service

![Alt text](/images/GithubDeployment.png)

## Step 4 - Update enviornment variables

![Alt text](/images/EnvVariables.png)

## Step 5 - Update Statup Command in Configuration in App Service

![Alt text](/images/updateconfig.png)

## Step 6 - Run and validate by Selecting Default Domain in App Service.

![Alt text](/images/DeployedApp.png)