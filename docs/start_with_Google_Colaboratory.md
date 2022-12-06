# How to start PE with Google Colaboratory

## Prepation

### Create Your project
1. Go to [Google Cloud Platform](https://console.cloud.google.com/).
1. Create your project.
1. Enable "Places API".

### Restrict Your API Key
1. Go to [Credential](https://console.cloud.google.com/google/maps-apis/credentials).
2. Click your API name.
3. Set key restrictions. Be sure to read [Google's Official document for key restriction](https://cloud.google.com/docs/authentication/api-keys?hl=en_US&_ga=2.22971646.-472611623.1669725235&_gac=1.89610601.1669726477.Cj0KCQiA-JacBhC0ARIsAIxybyMaLd8m16G73pFt7nddHkzexDaFyzTNlFoUgyEOYRtX839nPn1C864aAojmEALw_wcB#securing_an_api_key). An example setting for Google Colaboratory is as follows.

![Setting_key_restriction](https://user-images.githubusercontent.com/108068990/205912332-266803f5-b46e-451c-8e7e-9e4751debf0d.png)

### Create budgets and budget alerts
1. Go to [Budget and Alert](https://console.cloud.google.com/billing/).
2. Creat your budget.
3. Select your project.
4. Set your budget amount. An example setting is as follows.

![Setting_budget_amount](https://user-images.githubusercontent.com/108068990/205912721-ea280837-82cf-4310-9a65-a8cf4e72d264.png)

### Set maximum API usage
1. Go to [Quotas](https://console.cloud.google.com/google/maps-apis/quotas).
2. Expand "Requests".
3. Set your limit of requests. An example setting is as follows.

![Setting_quota](https://user-images.githubusercontent.com/108068990/205912840-cffc78d9-9c37-44d0-bd04-f091c93c27b0.png)
