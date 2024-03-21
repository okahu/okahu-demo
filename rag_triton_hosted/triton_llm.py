from langchain_core.language_models.llms import LLM
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from typing import Any, Dict, List, Optional
import os
import uuid
import requests

class TritonLLM(LLM):

    @property
    def _llm_type(self) -> str:
        return "tritonllm"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")
        triton_url: str = os.environ["TRITON_LLM_ENDPOINT"]
        trace_id: str = str(run_manager.parent_run_id)
        span_id: str = str(run_manager.run_id)

        payload = {
            "id": trace_id,
            "inputs": [
                {
                    "name": "text_input",
                    "datatype": "BYTES",
                    "shape": [1],
                    "data": [prompt],
                }
            ]
        }
        uuid_trace_id_hex = uuid.UUID(trace_id).hex
        uuid_span_id_hex = uuid.UUID(span_id).hex

        # eg. 00-80e1afed08e019fc1110464cfa66635c-00085853722dc6d2-00
        # The traceparent header uses the version-trace_id-parent_id-trace_flags format
        header_trace = {"traceparent": f"00-{uuid_trace_id_hex}-00{uuid_span_id_hex[:14]}-00"}

        ret = requests.post(
            triton_url,
            json=payload,
            timeout=10,
            headers= header_trace,
        )
        
        res = ret.json()
        query_response = res["outputs"][0]["data"][0]

        return query_response
