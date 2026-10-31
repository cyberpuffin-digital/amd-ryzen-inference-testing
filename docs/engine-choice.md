# Why llama.cpp with Vulkan

Checked 2026-10-31 for the Radeon 780M (gfx1103) on Linux. Revisit as the
options change; a finding here that stops being true should be corrected in
place, with the date.

| Option | Verdict on the 780M | Why |
|---|---|---|
| **llama.cpp, Vulkan (RADV)** | **Used** | Works with stock Mesa, no vendor runtime; supports every model family here, MoE, quantized KV cache and speculative decoding (draft models, MTP, EAGLE3 in upstream builds). |
| llama.cpp, ROCm/HIP | To test | gfx1103 isn't on ROCm's supported list; community reports use `HSA_OVERRIDE_GFX_VERSION=11.0.0`. Anecdotally better at prompt processing, worse at generation. Phoronix found ROCm lower-latency than Vulkan on a Radeon AI PRO R9700 and Strix Halo, not on this GPU.[^phoronix] |
| Lemonade (AMD) | Not needed | For Ryzen 7000/8000 its GPU path *is* llama.cpp with Vulkan; it adds model management and a server.[^lemonade] Its ROCm list names discrete GPUs only. |
| Ollama | Not used | Its Linux AMD path is ROCm, so the 780M needs the same override or falls back to CPU. Its model files do load in llama.cpp when the architecture is supported. |
| vLLM | Not applicable | AMD's ROCm builds target Instinct data-center GPUs.[^vllm] |
| MLC-LLM | Not tested | Has a Vulkan backend, but its published AMD results are from 2023 and on discrete GPUs.[^mlc] |
| NPU (XDNA1) | Not usable | FastFlowLM runs only on XDNA2 (Strix and later).[^flm] No Linux LLM runtime for XDNA1 was found. |

No published MoE prompt-processing numbers for the 780M were found
([llama.cpp discussion #27519](https://github.com/ggml-org/llama.cpp/discussions/27519));
that is one of the gaps this repository's results fill.

[^phoronix]: [Phoronix: AMD ROCm vs. Vulkan performance for Lemonade with llama.cpp](https://www.phoronix.com/review/lemonade-vulkan-rocm/3)
[^lemonade]: [Lemonade FAQ](https://lemonade-server.ai/docs/guide/faq/)
[^vllm]: [ROCm vLLM inference performance testing](https://rocm.docs.amd.com/en/docs-7.2.2/how-to/rocm-for-ai/inference/benchmark-docker/previous-versions/vllm-0.11.1-20251103.html)
[^mlc]: [MLC: Making AMD GPUs competitive for LLM inference (2023)](https://blog.mlc.ai/2023/08/09/Making-AMD-GPUs-competitive-for-LLM-inference)
[^flm]: [FastFlowLM](https://github.com/shdu-amd/FastFlowLM)
