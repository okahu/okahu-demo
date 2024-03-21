### Endpoint Deployment
This directory contains the code and the deployment files for the langchain RAG application which uses self hosted Triton APIs.

Use the following az cli command to deploy this code to a endpoint:

```az ml online-deployment create --file ./rag_triton_hosted/endpoint-deployment.yml --workspace-name okahu-demo-wsp-eastus --resource-group okahu_rg```

