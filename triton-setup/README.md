##  Trition Server on Kubernetes

This guide assumes that you already have a Kubernetes cluster up and running. 

### NVIDIA GPU operator

NVIDIA GPU operator is required for running containers that host GPU accelerated applications Before running Triton, make sure the GPU Operator is installed and running on the cluster. If you already have installed NVIDIA GPU Operator on the cluster, you can skip this section. 
You can follow the [documentation](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/index.html) for more info. 

To install the GPU Operator you can follow the instructions here: [Installing-the-nvidia-gpu-operator](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/getting-started.html)

In case you face issues do check out the [Common-deployment-scenarios](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/getting-started.html#common-deployment-scenarios) section.

### Triton Infrerencing Server

Examples for deploying Triton Inference Server with Kubernetes and Helm on [GCP](deploy/gcp/README.md),
  [AWS](deploy/aws/README.md), [NVIDIA FleetCommand](deploy/fleetcommand/README.md) and other vendors can be found in Nvidia's guide available [here](https://github.com/triton-inference-server/server/tree/main/deploy)

In case you don't see your vendor listed, you can always follow the [k8s-onprem](https://github.com/triton-inference-server/server/tree/main/deploy/k8s-onprem) helm chart, which should work with any Kubernetes cluster.

Note: Prometheus and Grafana are not necessary for the Trition Installation and can be removed from Chart's dependency. If you wish to remove it, you can edit Chart.yaml and 
remove the prometheus-adapter block from the dependencies list in YAML.

### Deploying Hugging Face Transformer Models in Triton

The [Official tutorial](https://github.com/triton-inference-server/tutorials/tree/main/Quick_Deploy/HuggingFaceTransformers) from Triton can be followed to deploy any Hugging Face model to Triton.

Model used in demo: https://huggingface.co/MBZUAI/LaMini-Flan-T5-783M

Sample Model repository containing the config.pbtxt and model.py files for the model used in demo: [models](models)

Note: Ensure the docker image of Triton is built on same architecture as that of the Triton server (likely x86) otherwise you may see a vague 'exec format error' while running the docker image.