# Okahu AI Observability preview

This repo includes a demo AI chatbot that is pre-instrumented for observation with Okahu AI Observability cloud. 

Use this demo if you want to try Okahu in docker container
- a self hosted large language model using Nvidia Triton, or 
- a large language model from OpenAI

Check out [Okahu with OpenAI](https://github.com/okahu/okahu-demo-openai) if you want to try Okahu in Github Codespaces. 

## Try Okahu

You'll need 
- An Okahu tenant and API key to [Okahu AI Observability Cloud](https://www.okahu.ai)
- An OpenAI subscription and an API key to [OpenAI developer platform](https://platform.openai.com/overview)
- Setup an Nvidia Triton Inference server. See [instructions](triton-setup/README.md). 
  - Setup Docker on your local machine (Linux, Mac, Windows). See [instructions](https://docs.docker.com)

## Configuring demo environment
- Go to folder config
- Copy config.ini.template to config.ini
- Edit the file and add OpenAI API Key and Okahu API key
- Set the Triton inference server endpoint if you have a Triton inference server configured.

## Chatbot client using OpenAI service
This application uses RAG design pattern to facilitates a coffee chat bot. It's a python program that uses Langchain library. The vector dataset is built using multi-qa-mpnet-base-dot-v1 from Huggingface from a set of Wikipedia articles. The vector data is stored in a local filebased faiss vectorDB. The app uses OpenAI gpt-3.5-turbo model for inference.
### Coffee chatbot app
To run the command line coffee chatbot app use following command from the top level directory
```./coffee_client_openai.sh```
### Coffee chatbot app with Okahu instrumentation
To run the command line coffee chatbot app with Okahu langchain log handler, use following command from the top level
```./coffee_client_openai_with_okahu.sh```

## Chatbot client using NVIDIA Triton inference server
This application uses RAG design pattern to facilitates a coffee chat bot. It's a python program that uses Langchain library. The vector dataset is built using multi-qa-mpnet-base-dot-v1 from Huggingface from a set of Wikipedia articles. The vector data is stored in a local filebased faiss vectorDB. The app uses flan_t5 model for inference that's hosted on a Triton inference server instance.
### Coffee chatbot app
To run the command line coffee chatbot app use following command from the top level directory
```./coffee_client_triton.sh```
### Coffee chatbot app with Okahu instrumentation
To run the command line coffee chatbot app with Okahu langchain log handler, use following command from the top level
```./coffee_client_triton_with_okahu.sh```

## Using Okahu's demo docker with NVIDIA Triton inference server setup
### Download and run Okahu demo container
- Download the container
  ```docker pull okahudocker/okahu_demo:okahu_triton_apps_demo```
- Start container
  ```docker run --rm -p8000:8000 -p8001:8001 -p8002:8002  okahudocker/okahu_demo:okahu_triton_apps_demo <Okahu-API-Key> <OpenAI-API-Key> ```
- Verify the container running
  ``` docker ps ```  
  Note the container ID retured by above command where the Image name is okahudocker/okahu_triton_apps_demo
### Coffee chatbot app with Okahu instrumentation
To run the command line coffee chatbot app with Okahu langchain log handler, use following command from the top level
``` docker exec -it <Container-ID> bash /okahu_demo/coffee_client_triton_with_okahu.sh ``` 
