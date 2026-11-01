# fw13-7840u: version: 8681 (Debian)

- **Machine:** Framework Laptop 13 (AMD Ryzen 7040Series) (A7), BIOS 03.20 (06/23/2026)
- **CPU:** AMD Ryzen 7 7840U w/ Radeon 780M Graphics, 8 cores / 16 threads, governor performance, EPP performance
- **Memory:** 30.2 GiB visible, 20.1 GiB available at start; GPU reserve 512 MiB, GTT 24576 MiB
- **Software:** Ubuntu 26.04.1 LTS, kernel 7.0.0-42-generic, Mesa 26.0.8-1ubuntu0.3
- **Devices:** ROCm0: AMD Radeon 780M Graphics (24576 MiB, 20492 MiB free); Vulkan0: AMD Radeon 780M Graphics (RADV PHOENIX) (25088 MiB, 24445 MiB free)
- **Power:** AC yes, profile performance, battery Not charging; load average 1.19
- **Captured:** 2026-10-31T18:06:58Z

> ⚠️ system busy (load average > 1)

## gemma-4-26B-A4B-it-Q4_0.gguf

gemma4 ?B Q4_0, 13.60 GiB, 25.23 B params

### GPU (Vulkan) vs CPU, empty context

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 512 | True | f16 | pp512 | 366.3 ± 12.5 |
| Vulkan0 | 8 | 512 | True | f16 | tg128 | 24.7 ± 0.0 |
| CPU | 8 | 512 | False | f16 | pp512 | 93.1 ± 0.8 |
| CPU | 8 | 512 | False | f16 | tg128 | 19.3 ± 0.0 |

### GPU as the context fills (-ub 256)

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 256 | True | f16 | pp2048 | 294.9 ± 0.9 |
| Vulkan0 | 8 | 256 | True | f16 | tg64 | 25.0 ± 0.2 |
| Vulkan0 | 8 | 256 | True | f16 | pp2048 @ d8192 | 251.4 ± 0.3 |
| Vulkan0 | 8 | 256 | True | f16 | tg64 @ d8192 | 21.8 ± 0.1 |
| Vulkan0 | 8 | 256 | True | f16 | pp2048 @ d16384 | 210.2 ± 0.2 |
| Vulkan0 | 8 | 256 | True | f16 | tg64 @ d16384 | 20.6 ± 0.1 |

### GPU tuning at 8k context: micro-batch and flash attention

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 256 | False | f16 | pp2048 @ d8192 | 232.8 ± 0.6 |
| Vulkan0 | 8 | 256 | False | f16 | tg64 @ d8192 | 17.8 ± 0.1 |
| Vulkan0 | 8 | 256 | True | f16 | pp2048 @ d8192 | 238.9 ± 0.7 |
| Vulkan0 | 8 | 256 | True | f16 | tg64 @ d8192 | 21.6 ± 0.1 |
| Vulkan0 | 8 | 512 | False | f16 | pp2048 @ d8192 | 270.2 ± 1.2 |
| Vulkan0 | 8 | 512 | False | f16 | tg64 @ d8192 | 17.7 ± 0.1 |
| Vulkan0 | 8 | 512 | True | f16 | pp2048 @ d8192 | 281.8 ± 0.3 |
| Vulkan0 | 8 | 512 | True | f16 | tg64 @ d8192 | 21.4 ± 0.1 |

### GPU tuning at 8k context: KV cache type

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 256 | True | f16 | pp2048 @ d8192 | 237.6 ± 1.0 |
| Vulkan0 | 8 | 256 | True | f16 | tg64 @ d8192 | 21.4 ± 0.2 |
| Vulkan0 | 8 | 256 | True | f16/q8_0 | pp2048 @ d8192 | 23.1 ± 0.0 |
| Vulkan0 | 8 | 256 | True | f16/q8_0 | tg64 @ d8192 | 8.1 ± 0.0 |
| Vulkan0 | 8 | 256 | True | q8_0/f16 | pp2048 @ d8192 | 30.7 ± 0.2 |
| Vulkan0 | 8 | 256 | True | q8_0/f16 | tg64 @ d8192 | 8.9 ± 0.0 |
| Vulkan0 | 8 | 256 | True | q8_0 | pp2048 @ d8192 | 203.3 ± 0.6 |
| Vulkan0 | 8 | 256 | True | q8_0 | tg64 @ d8192 | 21.6 ± 0.1 |

## gpt-oss-20b-MXFP4.gguf

gpt-oss 20B MXFP4 MoE, 11.27 GiB, 20.91 B params

### GPU (Vulkan) vs CPU, empty context

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 512 | True | f16 | pp512 | 416.0 ± 3.0 |
| Vulkan0 | 8 | 512 | True | f16 | tg128 | 26.9 ± 0.1 |
| CPU | 8 | 512 | False | f16 | pp512 | 59.2 ± 0.0 |
| CPU | 8 | 512 | False | f16 | tg128 | 20.4 ± 0.0 |

### GPU as the context fills (-ub 256)

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 256 | True | f16 | pp2048 | 328.9 ± 0.5 |
| Vulkan0 | 8 | 256 | True | f16 | tg64 | 27.0 ± 0.2 |
| Vulkan0 | 8 | 256 | True | f16 | pp2048 @ d8192 | 262.3 ± 0.5 |
| Vulkan0 | 8 | 256 | True | f16 | tg64 @ d8192 | 24.2 ± 0.1 |
| Vulkan0 | 8 | 256 | True | f16 | pp2048 @ d16384 | 215.2 ± 2.0 |
| Vulkan0 | 8 | 256 | True | f16 | tg64 @ d16384 | 22.2 ± 0.1 |

### GPU tuning at 8k context: micro-batch and flash attention

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 256 | False | f16 | pp2048 @ d8192 | 187.5 ± 0.4 |
| Vulkan0 | 8 | 256 | False | f16 | tg64 @ d8192 | 20.8 ± 0.1 |
| Vulkan0 | 8 | 256 | True | f16 | pp2048 @ d8192 | 261.8 ± 0.3 |
| Vulkan0 | 8 | 256 | True | f16 | tg64 @ d8192 | 24.2 ± 0.1 |
| Vulkan0 | 8 | 512 | False | f16 | pp2048 @ d8192 | 201.9 ± 0.2 |
| Vulkan0 | 8 | 512 | False | f16 | tg64 @ d8192 | 20.5 ± 0.2 |
| Vulkan0 | 8 | 512 | True | f16 | pp2048 @ d8192 | 310.8 ± 0.7 |
| Vulkan0 | 8 | 512 | True | f16 | tg64 @ d8192 | 24.1 ± 0.0 |

### GPU tuning at 8k context: KV cache type

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 256 | True | f16 | pp2048 @ d8192 | 266.5 ± 0.6 |
| Vulkan0 | 8 | 256 | True | f16 | tg64 @ d8192 | 24.4 ± 0.1 |
| Vulkan0 | 8 | 256 | True | f16/q8_0 | pp2048 @ d8192 | 21.2 ± 0.0 |
| Vulkan0 | 8 | 256 | True | f16/q8_0 | tg64 @ d8192 | 7.4 ± 0.0 |
| Vulkan0 | 8 | 256 | True | q8_0/f16 | pp2048 @ d8192 | 36.2 ± 0.1 |
| Vulkan0 | 8 | 256 | True | q8_0/f16 | tg64 @ d8192 | 9.1 ± 0.0 |
| Vulkan0 | 8 | 256 | True | q8_0 | pp2048 @ d8192 | 240.1 ± 0.4 |
| Vulkan0 | 8 | 256 | True | q8_0 | tg64 @ d8192 | 24.4 ± 0.1 |

## Qwen3-0.6B-Q8_0.gguf

qwen3 0.6B Q8_0, 0.59 GiB, 0.60 B params

### GPU (Vulkan) vs CPU, empty context

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 512 | True | f16 | pp512 | 2745.1 ± 108.0 |
| Vulkan0 | 8 | 512 | True | f16 | tg128 | 97.8 ± 0.1 |
| CPU | 8 | 512 | False | f16 | pp512 | 295.4 ± 0.5 |
| CPU | 8 | 512 | False | f16 | tg128 | 75.4 ± 0.1 |

### GPU as the context fills (-ub 256)

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 256 | True | f16 | pp2048 | 2172.9 ± 3.2 |
| Vulkan0 | 8 | 256 | True | f16 | tg64 | 98.8 ± 0.2 |
| Vulkan0 | 8 | 256 | True | f16 | pp2048 @ d8192 | 831.1 ± 2.3 |
| Vulkan0 | 8 | 256 | True | f16 | tg64 @ d8192 | 42.5 ± 0.1 |
| Vulkan0 | 8 | 256 | True | f16 | pp2048 @ d16384 | 494.4 ± 1.0 |
| Vulkan0 | 8 | 256 | True | f16 | tg64 @ d16384 | 27.3 ± 0.1 |

### GPU tuning at 8k context: micro-batch and flash attention

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 256 | False | f16 | pp2048 @ d8192 | 480.2 ± 0.5 |
| Vulkan0 | 8 | 256 | False | f16 | tg64 @ d8192 | 22.9 ± 0.1 |
| Vulkan0 | 8 | 256 | True | f16 | pp2048 @ d8192 | 829.7 ± 0.8 |
| Vulkan0 | 8 | 256 | True | f16 | tg64 @ d8192 | 42.2 ± 0.4 |
| Vulkan0 | 8 | 512 | False | f16 | pp2048 @ d8192 | 523.6 ± 0.1 |
| Vulkan0 | 8 | 512 | False | f16 | tg64 @ d8192 | 23.0 ± 0.1 |
| Vulkan0 | 8 | 512 | True | f16 | pp2048 @ d8192 | 836.8 ± 3.5 |
| Vulkan0 | 8 | 512 | True | f16 | tg64 @ d8192 | 42.3 ± 0.1 |

### GPU tuning at 8k context: KV cache type

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 256 | True | f16 | pp2048 @ d8192 | 831.0 ± 3.0 |
| Vulkan0 | 8 | 256 | True | f16 | tg64 @ d8192 | 42.4 ± 0.1 |
| Vulkan0 | 8 | 256 | True | f16/q8_0 | pp2048 @ d8192 | 10.7 ± 0.0 |
| Vulkan0 | 8 | 256 | True | f16/q8_0 | tg64 @ d8192 | 6.7 ± 0.1 |
| Vulkan0 | 8 | 256 | True | q8_0/f16 | pp2048 @ d8192 | 19.6 ± 0.0 |
| Vulkan0 | 8 | 256 | True | q8_0/f16 | tg64 @ d8192 | 9.5 ± 0.0 |
| Vulkan0 | 8 | 256 | True | q8_0 | pp2048 @ d8192 | 600.6 ± 1.7 |
| Vulkan0 | 8 | 256 | True | q8_0 | tg64 @ d8192 | 45.1 ± 0.3 |

## Qwen3-1.7B-Q8_0.gguf

qwen3 1.7B Q8_0, 1.70 GiB, 1.72 B params

### GPU (Vulkan) vs CPU, empty context

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 512 | True | f16 | pp512 | 1051.8 ± 11.2 |
| Vulkan0 | 8 | 512 | True | f16 | tg128 | 39.2 ± 0.2 |
| CPU | 8 | 512 | False | f16 | pp512 | 117.0 ± 0.0 |
| CPU | 8 | 512 | False | f16 | tg128 | 29.0 ± 0.0 |

### GPU as the context fills (-ub 256)

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 256 | True | f16 | pp2048 | 977.9 ± 1.1 |
| Vulkan0 | 8 | 256 | True | f16 | tg64 | 39.9 ± 0.0 |
| Vulkan0 | 8 | 256 | True | f16 | pp2048 @ d8192 | 567.8 ± 1.4 |
| Vulkan0 | 8 | 256 | True | f16 | tg64 @ d8192 | 25.8 ± 0.2 |
| Vulkan0 | 8 | 256 | True | f16 | pp2048 @ d16384 | 397.6 ± 0.9 |
| Vulkan0 | 8 | 256 | True | f16 | tg64 @ d16384 | 19.4 ± 0.1 |

### GPU tuning at 8k context: micro-batch and flash attention

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 256 | False | f16 | pp2048 @ d8192 | 377.9 ± 0.1 |
| Vulkan0 | 8 | 256 | False | f16 | tg64 @ d8192 | 17.6 ± 0.0 |
| Vulkan0 | 8 | 256 | True | f16 | pp2048 @ d8192 | 569.9 ± 1.1 |
| Vulkan0 | 8 | 256 | True | f16 | tg64 @ d8192 | 25.8 ± 0.1 |
| Vulkan0 | 8 | 512 | False | f16 | pp2048 @ d8192 | 400.5 ± 0.5 |
| Vulkan0 | 8 | 512 | False | f16 | tg64 @ d8192 | 17.6 ± 0.0 |
| Vulkan0 | 8 | 512 | True | f16 | pp2048 @ d8192 | 565.7 ± 0.8 |
| Vulkan0 | 8 | 512 | True | f16 | tg64 @ d8192 | 25.8 ± 0.1 |

### GPU tuning at 8k context: KV cache type

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 256 | True | f16 | pp2048 @ d8192 | 569.5 ± 1.4 |
| Vulkan0 | 8 | 256 | True | f16 | tg64 @ d8192 | 25.9 ± 0.1 |
| Vulkan0 | 8 | 256 | True | f16/q8_0 | pp2048 @ d8192 | 10.6 ± 0.0 |
| Vulkan0 | 8 | 256 | True | f16/q8_0 | tg64 @ d8192 | 6.1 ± 0.0 |
| Vulkan0 | 8 | 256 | True | q8_0/f16 | pp2048 @ d8192 | 19.2 ± 0.1 |
| Vulkan0 | 8 | 256 | True | q8_0/f16 | tg64 @ d8192 | 8.2 ± 0.0 |
| Vulkan0 | 8 | 256 | True | q8_0 | pp2048 @ d8192 | 451.1 ± 1.0 |
| Vulkan0 | 8 | 256 | True | q8_0 | tg64 @ d8192 | 26.4 ± 0.0 |

## Qwen3-4B-Q4_K_M.gguf

qwen3 4B Q4_K - Medium, 2.32 GiB, 4.02 B params

### GPU (Vulkan) vs CPU, empty context

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 512 | True | f16 | pp512 | 440.7 ± 2.8 |
| Vulkan0 | 8 | 512 | True | f16 | tg128 | 26.4 ± 0.1 |
| CPU | 8 | 512 | False | f16 | pp512 | 88.5 ± 0.1 |
| CPU | 8 | 512 | False | f16 | tg128 | 20.8 ± 0.0 |

### GPU as the context fills (-ub 256)

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 256 | True | f16 | pp2048 | 394.8 ± 0.8 |
| Vulkan0 | 8 | 256 | True | f16 | tg64 | 26.5 ± 0.0 |
| Vulkan0 | 8 | 256 | True | f16 | pp2048 @ d8192 | 224.8 ± 0.7 |
| Vulkan0 | 8 | 256 | True | f16 | tg64 @ d8192 | 18.2 ± 0.0 |
| Vulkan0 | 8 | 256 | True | f16 | pp2048 @ d16384 | 147.5 ± 1.3 |
| Vulkan0 | 8 | 256 | True | f16 | tg64 @ d16384 | 14.1 ± 0.0 |

### GPU tuning at 8k context: micro-batch and flash attention

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 256 | False | f16 | pp2048 @ d8192 | 158.2 ± 0.1 |
| Vulkan0 | 8 | 256 | False | f16 | tg64 @ d8192 | 11.4 ± 0.0 |
| Vulkan0 | 8 | 256 | True | f16 | pp2048 @ d8192 | 223.7 ± 0.4 |
| Vulkan0 | 8 | 256 | True | f16 | tg64 @ d8192 | 18.2 ± 0.0 |
| Vulkan0 | 8 | 512 | False | f16 | pp2048 @ d8192 | 164.8 ± 0.1 |
| Vulkan0 | 8 | 512 | False | f16 | tg64 @ d8192 | 11.4 ± 0.0 |
| Vulkan0 | 8 | 512 | True | f16 | pp2048 @ d8192 | 202.2 ± 2.0 |
| Vulkan0 | 8 | 512 | True | f16 | tg64 @ d8192 | 18.2 ± 0.0 |

### GPU tuning at 8k context: KV cache type

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 256 | True | f16 | pp2048 @ d8192 | 223.6 ± 0.4 |
| Vulkan0 | 8 | 256 | True | f16 | tg64 @ d8192 | 18.2 ± 0.0 |
| Vulkan0 | 8 | 256 | True | f16/q8_0 | pp2048 @ d8192 | 4.2 ± 0.0 |
| Vulkan0 | 8 | 256 | True | f16/q8_0 | tg64 @ d8192 | 3.0 ± 0.0 |
| Vulkan0 | 8 | 256 | True | q8_0/f16 | pp2048 @ d8192 | 7.6 ± 0.0 |
| Vulkan0 | 8 | 256 | True | q8_0/f16 | tg64 @ d8192 | 4.3 ± 0.0 |
| Vulkan0 | 8 | 256 | True | q8_0 | pp2048 @ d8192 | 181.1 ± 0.2 |
| Vulkan0 | 8 | 256 | True | q8_0 | tg64 @ d8192 | 18.6 ± 0.0 |

## Qwen3-8B-Q4_K_M.gguf

qwen3 8B Q4_K - Medium, 4.68 GiB, 8.19 B params

### GPU (Vulkan) vs CPU, empty context

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 512 | True | f16 | pp512 | 249.1 ± 0.3 |
| Vulkan0 | 8 | 512 | True | f16 | tg128 | 15.6 ± 0.0 |
| CPU | 8 | 512 | False | f16 | pp512 | 52.1 ± 0.0 |
| CPU | 8 | 512 | False | f16 | tg128 | 11.5 ± 0.0 |

### GPU as the context fills (-ub 256)

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 256 | True | f16 | pp2048 | 232.8 ± 0.3 |
| Vulkan0 | 8 | 256 | True | f16 | tg64 | 15.6 ± 0.0 |
| Vulkan0 | 8 | 256 | True | f16 | pp2048 @ d8192 | 143.7 ± 1.9 |
| Vulkan0 | 8 | 256 | True | f16 | tg64 @ d8192 | 12.2 ± 0.0 |
| Vulkan0 | 8 | 256 | True | f16 | pp2048 @ d16384 | 77.0 ± 1.6 |
| Vulkan0 | 8 | 256 | True | f16 | tg64 @ d16384 | 10.1 ± 0.0 |

### GPU tuning at 8k context: micro-batch and flash attention

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 256 | False | f16 | pp2048 @ d8192 | 123.4 ± 0.0 |
| Vulkan0 | 8 | 256 | False | f16 | tg64 @ d8192 | 8.8 ± 0.0 |
| Vulkan0 | 8 | 256 | True | f16 | pp2048 @ d8192 | 162.2 ± 0.2 |
| Vulkan0 | 8 | 256 | True | f16 | tg64 @ d8192 | 12.4 ± 0.0 |
| Vulkan0 | 8 | 512 | False | f16 | pp2048 @ d8192 | 128.1 ± 0.2 |
| Vulkan0 | 8 | 512 | False | f16 | tg64 @ d8192 | 8.8 ± 0.0 |
| Vulkan0 | 8 | 512 | True | f16 | pp2048 @ d8192 | 149.3 ± 5.1 |
| Vulkan0 | 8 | 512 | True | f16 | tg64 @ d8192 | 12.4 ± 0.0 |

### GPU tuning at 8k context: KV cache type

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 256 | True | f16 | pp2048 @ d8192 | 161.8 ± 0.1 |
| Vulkan0 | 8 | 256 | True | f16 | tg64 @ d8192 | 12.4 ± 0.0 |
| Vulkan0 | 8 | 256 | True | f16/q8_0 | pp2048 @ d8192 | 4.1 ± 0.0 |
| Vulkan0 | 8 | 256 | True | f16/q8_0 | tg64 @ d8192 | 2.7 ± 0.0 |
| Vulkan0 | 8 | 256 | True | q8_0/f16 | pp2048 @ d8192 | 7.4 ± 0.0 |
| Vulkan0 | 8 | 256 | True | q8_0/f16 | tg64 @ d8192 | 3.9 ± 0.0 |
| Vulkan0 | 8 | 256 | True | q8_0 | pp2048 @ d8192 | 138.4 ± 0.1 |
| Vulkan0 | 8 | 256 | True | q8_0 | tg64 @ d8192 | 12.5 ± 0.0 |

## Qwen3-30B-A3B-Instruct-2507-UD-Q4_K_XL.gguf

qwen3moe 30B.A3B Q4_K - Medium, 16.47 GiB, 30.53 B params

### GPU (Vulkan) vs CPU, empty context

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 512 | True | f16 | pp512 | 309.7 ± 4.7 |
| Vulkan0 | 8 | 512 | True | f16 | tg128 | 31.1 ± 0.1 |
| CPU | 8 | 512 | False | f16 | pp512 | 69.7 ± 1.9 |
| CPU | 8 | 512 | False | f16 | tg128 | 24.6 ± 0.2 |

### GPU as the context fills (-ub 256)

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 256 | True | f16 | pp2048 | 239.5 ± 1.2 |
| Vulkan0 | 8 | 256 | True | f16 | tg64 | 32.0 ± 0.0 |
| Vulkan0 | 8 | 256 | True | f16 | pp2048 @ d8192 | 127.9 ± 0.4 |
| Vulkan0 | 8 | 256 | True | f16 | tg64 @ d8192 | 23.0 ± 0.1 |
| Vulkan0 | 8 | 256 | True | f16 | pp2048 @ d16384 | 73.9 ± 1.0 |
| Vulkan0 | 8 | 256 | True | f16 | tg64 @ d16384 | 18.1 ± 0.0 |

### GPU tuning at 8k context: micro-batch and flash attention

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 256 | False | f16 | pp2048 @ d8192 | 111.5 ± 1.1 |
| Vulkan0 | 8 | 256 | False | f16 | tg64 @ d8192 | 14.0 ± 0.0 |
| Vulkan0 | 8 | 256 | True | f16 | pp2048 @ d8192 | 130.1 ± 0.9 |
| Vulkan0 | 8 | 256 | True | f16 | tg64 @ d8192 | 23.1 ± 0.1 |
| Vulkan0 | 8 | 512 | False | f16 | pp2048 @ d8192 | 124.2 ± 1.3 |
| Vulkan0 | 8 | 512 | False | f16 | tg64 @ d8192 | 14.0 ± 0.0 |
| Vulkan0 | 8 | 512 | True | f16 | pp2048 @ d8192 | 92.2 ± 2.5 |
| Vulkan0 | 8 | 512 | True | f16 | tg64 @ d8192 | 23.0 ± 0.2 |

### GPU tuning at 8k context: KV cache type

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 256 | True | f16 | pp2048 @ d8192 | 120.3 ± 0.7 |
| Vulkan0 | 8 | 256 | True | f16 | tg64 @ d8192 | 22.8 ± 0.1 |
| Vulkan0 | 8 | 256 | True | f16/q8_0 | pp2048 @ d8192 | 6.5 ± 0.0 |
| Vulkan0 | 8 | 256 | True | f16/q8_0 | tg64 @ d8192 | 3.6 ± 0.0 |
| Vulkan0 | 8 | 256 | True | q8_0/f16 | pp2048 @ d8192 | 9.2 ± 0.0 |
| Vulkan0 | 8 | 256 | True | q8_0/f16 | tg64 @ d8192 | 4.8 ± 0.3 |
| Vulkan0 | 8 | 256 | True | q8_0 | pp2048 @ d8192 | 123.6 ± 0.2 |
| Vulkan0 | 8 | 256 | True | q8_0 | tg64 @ d8192 | 23.6 ± 0.1 |

## Speculative decoding (server, 256 tokens, temperature 0)

| target | draft | type | alone t/s | with draft t/s | speed-up | accepted |
|---|---|---|--:|--:|--:|--:|
| Qwen3-4B-Q4_K_M.gguf | Qwen3-0.6B-Q8_0.gguf | draft-simple | 26.1 | 36.0 | 1.38x | 201 / 244 |
| Qwen3-8B-Q4_K_M.gguf | Qwen3-0.6B-Q8_0.gguf | draft-simple | 15.3 | 23.0 | 1.50x | 198 / 258 |
| Qwen3-8B-Q4_K_M.gguf | Qwen3-1.7B-Q8_0.gguf | draft-simple | 15.5 | 18.0 | 1.16x | 218 / 298 |
| Qwen3-30B-A3B-Instruct-2507-UD-Q4_K_XL.gguf | Qwen3-0.6B-Q8_0.gguf | draft-simple | 31.0 | 23.1 | 0.74x | 197 / 258 |

## Errors

```
[gpu-vs-cpu] failed: -m ~/models/ggml-org/gemma-4-E2B-it-GGUF/gemma-4-E2B-it-Q4_0.gguf -dev Vulkan0 -ngl 99 -fa 1 -p 512 -n 128
[gpu-vs-cpu] failed: -m ~/models/ggml-org/gemma-4-E2B-it-GGUF/gemma-4-E2B-it-Q4_0.gguf -dev none -ngl 0 -t 8 -p 512 -n 128
[depth] failed: -m ~/models/ggml-org/gemma-4-E2B-it-GGUF/gemma-4-E2B-it-Q4_0.gguf -dev Vulkan0 -ngl 99 -fa 1 -ub 256 -p 2048 -n 64 -d 0,8192,16384
[tuning] failed: -m ~/models/ggml-org/gemma-4-E2B-it-GGUF/gemma-4-E2B-it-Q4_0.gguf -dev Vulkan0 -ngl 99 -ub 256,512 -fa 0,1 -p 2048 -n 64 -d 8192
[kv-type] failed: -m ~/models/ggml-org/gemma-4-E2B-it-GGUF/gemma-4-E2B-it-Q4_0.gguf -dev Vulkan0 -ngl 99 -ub 256 -fa 1 -ctk f16,q8_0 -ctv f16,q8_0 -p 2048 -n 64 -d 8192
[gpu-vs-cpu] failed: -m ~/models/ggml-org/gemma-4-E4B-it-GGUF/gemma-4-E4B-it-Q4_0.gguf -dev Vulkan0 -ngl 99 -fa 1 -p 512 -n 128
[gpu-vs-cpu] failed: -m ~/models/ggml-org/gemma-4-E4B-it-GGUF/gemma-4-E4B-it-Q4_0.gguf -dev none -ngl 0 -t 8 -p 512 -n 128
[depth] failed: -m ~/models/ggml-org/gemma-4-E4B-it-GGUF/gemma-4-E4B-it-Q4_0.gguf -dev Vulkan0 -ngl 99 -fa 1 -ub 256 -p 2048 -n 64 -d 0,8192,16384
[tuning] failed: -m ~/models/ggml-org/gemma-4-E4B-it-GGUF/gemma-4-E4B-it-Q4_0.gguf -dev Vulkan0 -ngl 99 -ub 256,512 -fa 0,1 -p 2048 -n 64 -d 8192
[kv-type] failed: -m ~/models/ggml-org/gemma-4-E4B-it-GGUF/gemma-4-E4B-it-Q4_0.gguf -dev Vulkan0 -ngl 99 -ub 256 -fa 1 -ctk f16,q8_0 -ctv f16,q8_0 -p 2048 -n 64 -d 8192
```
