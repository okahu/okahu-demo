# Use original NVIDIA Triton image
#from nvcr.io/nvidia/tritonserver:24.02-py3
#from okahudocker/okahu_demo:okahu_triton_demo
from okahudocker/okahu_demo:okahu_triton_demo

# Upload models
RUN mkdir /okahu_demo
COPY ./ /okahu_demo/
RUN chmod +x /okahu_demo/*.sh
RUN ls -l /okahu_demo
WORKDIR /okahu_demo

#Install dependant packages
RUN pip install --ignore-installed --no-cache-dir -r requirements.txt 
##
#RUN pip install --ignore-installed credential_utilties/ embeddings/ okahu-handlers
#--ignore-installed 

EXPOSE 8000/tcp
EXPOSE 8001/tcp
EXPOSE 8002/tcp

ENTRYPOINT ["/okahu_demo/setup_okahu_demo_docker.sh"]
