# Copyright 2023, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#  * Neither the name of NVIDIA CORPORATION nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import os

os.environ[
    "TRANSFORMERS_CACHE"
] = "/tmp/flan_t5/hf_cache"
import json

import numpy as np
import torch
import transformers
import triton_python_backend_utils as pb_utils


class TritonPythonModel:
    def initialize(self, args):
        self.logger = pb_utils.Logger
        self.model_config = json.loads(args["model_config"])
        self.model_params = self.model_config.get("parameters", {})
        default_hf_model = "MBZUAI/LaMini-Flan-T5-783M"
        default_max_gen_length = "15"
        # Check for user-specified model name in model config parameters
        hf_model = self.model_params.get("huggingface_model", {}).get(
            "string_value", default_hf_model
        )
        # Check for user-specified max length in model config parameters
        self.max_output_length = int(
            self.model_params.get("max_output_length", {}).get(
                "string_value", default_max_gen_length
            )
        )

        self.logger.log_info(f"Max sequence length: {self.max_output_length}")
        self.logger.log_info(f"Loading HuggingFace model: {hf_model}...")
        # Assume tokenizer available for same model
        self.pipeline = transformers.pipeline(
            "text2text-generation",
            model=hf_model,
            torch_dtype=torch.float16,
            device_map="auto",
        )

    def execute(self, requests):
        prompts = []
        for request in requests:
            input_tensor = pb_utils.get_input_tensor_by_name(request, "text_input")
            multi_dim = input_tensor.as_numpy().ndim > 1
            if not multi_dim:
                prompt = input_tensor.as_numpy()[0].decode("utf-8")
                self.logger.log_info(f"Generating sequences for text_input: {prompt}")
                prompts.append(prompt)
            else:
                # Implementation to accept dynamically batched inputs
                num_prompts = input_tensor.as_numpy().shape[0]
                for prompt_index in range(0, num_prompts):
                    prompt = input_tensor.as_numpy()[prompt_index][0].decode("utf-8")
                    self.logger.log_info(f"Generating sequences for text_input 's: {prompt}")
                    prompts.append(prompt)

        batch_size = len(prompts)
        return self.generate(prompts, batch_size)

    def generate(self, prompts, batch_size):
        sequences = self.pipeline(
            prompts,
            max_length = self.max_output_length,
            batch_size = batch_size,
            do_sample = True,
        )
        
        responses = []
        texts = []
        for i, seq in enumerate(sequences):
            output_tensors = []
            text = seq["generated_text"]
            texts.append(text)
            tensor = pb_utils.Tensor("text_output", np.array(texts, dtype=np.object_))
            output_tensors.append(tensor)
            responses.append(pb_utils.InferenceResponse(output_tensors=output_tensors))

        return responses

    def finalize(self):
        print("Cleaning up...")
