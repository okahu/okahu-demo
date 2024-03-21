#!/bin/bash

if [[ $# -lt 1 ]]; then
    echo "Usage <Okahu_key> [OpenAI_Key]"
    exit 1
fi

echo Configuring chatbot apps with local Triton inference server
sed 's/OKAHU_API_KEY=/OKAHU_API_KEY='"$1"'/g ; s/TRITON_LLM_ENDPOINT=/TRITON_LLM_ENDPOINT=http:\/\/127.0.0.1:8000\/v2\/models\/flan_t5\/infer/g' config/config.ini.template > config/config.ini 

if [[ $# -eq 2 ]]; then
    echo Configuring chatbot apps with OpenAI
    sed 's/OPENAI_API_KEY=/OPENAI_API_KEY='"$2"'/g' config/config.ini > config/config.ini.tmp 
    mv config/config.ini.tmp config/config.ini
fi
