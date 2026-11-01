# fw13-7840u: version: 0.8.0-dev (build 12020, commit 0ec4027a2)

- **Machine:** Framework Laptop 13 (AMD Ryzen 7040Series) (A7), BIOS 03.20 (06/23/2026)
- **CPU:** AMD Ryzen 7 7840U w/ Radeon 780M Graphics, 8 cores / 16 threads, governor performance, EPP performance
- **Memory:** 30.2 GiB visible, 25.2 GiB available at start; GPU reserve 512 MiB, GTT 24576 MiB
- **Software:** Ubuntu 26.04.1 LTS, kernel 7.0.0-42-generic, Mesa 26.0.8-1ubuntu0.3
- **Devices:** Vulkan0: AMD Radeon 780M Graphics (RADV PHOENIX) (25088 MiB, 24425 MiB free)
- **Power:** AC yes, profile performance, battery Not charging; load average 2.27
- **Captured:** 2026-10-31T23:39:47Z

> ⚠️ system busy (load average > 1)

## gemma-4-26B-A4B-it-Q4_0.gguf

gemma4 26B.A4B Q4_0, 13.60 GiB, 25.23 B params

### GPU (Vulkan) vs CPU, empty context

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 512 | 1 | f16 | pp512 | 493.4 ± 2.9 |
| Vulkan0 | 8 | 512 | 1 | f16 | tg128 | 26.0 ± 0.0 |
| CPU | 8 | 512 | -1 | f16 | pp512 | 96.2 ± 0.9 |
| CPU | 8 | 512 | -1 | f16 | tg128 | 19.4 ± 0.2 |

### GPU as the context fills (-ub 256)

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 256 | 1 | f16 | pp2048 | 394.7 ± 0.5 |
| Vulkan0 | 8 | 256 | 1 | f16 | tg64 | 26.1 ± 0.0 |
| Vulkan0 | 8 | 256 | 1 | f16 | pp2048 @ d8192 | 311.3 ± 1.5 |
| Vulkan0 | 8 | 256 | 1 | f16 | tg64 @ d8192 | 22.5 ± 0.1 |
| Vulkan0 | 8 | 256 | 1 | f16 | pp2048 @ d16384 | 259.3 ± 1.5 |
| Vulkan0 | 8 | 256 | 1 | f16 | tg64 @ d16384 | 21.5 ± 0.1 |

### GPU tuning at 8k context: micro-batch and flash attention

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 256 | 0 | f16 | pp2048 @ d8192 | 316.7 ± 1.8 |
| Vulkan0 | 8 | 256 | 0 | f16 | tg64 @ d8192 | 18.8 ± 0.1 |
| Vulkan0 | 8 | 256 | 1 | f16 | pp2048 @ d8192 | 311.4 ± 2.0 |
| Vulkan0 | 8 | 256 | 1 | f16 | tg64 @ d8192 | 22.7 ± 0.1 |
| Vulkan0 | 8 | 512 | 0 | f16 | pp2048 @ d8192 | 351.5 ± 0.6 |
| Vulkan0 | 8 | 512 | 0 | f16 | tg64 @ d8192 | 18.6 ± 0.1 |
| Vulkan0 | 8 | 512 | 1 | f16 | pp2048 @ d8192 | 350.6 ± 1.0 |
| Vulkan0 | 8 | 512 | 1 | f16 | tg64 @ d8192 | 22.8 ± 0.1 |

### GPU tuning at 8k context: KV cache type

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 256 | 1 | f16 | pp2048 @ d8192 | 311.4 ± 1.8 |
| Vulkan0 | 8 | 256 | 1 | f16 | tg64 @ d8192 | 22.7 ± 0.1 |
| Vulkan0 | 8 | 256 | 1 | f16/q8_0 | pp2048 @ d8192 | 290.9 ± 5.4 |
| Vulkan0 | 8 | 256 | 1 | f16/q8_0 | tg64 @ d8192 | 22.9 ± 0.1 |
| Vulkan0 | 8 | 256 | 1 | q8_0/f16 | pp2048 @ d8192 | 250.6 ± 0.6 |
| Vulkan0 | 8 | 256 | 1 | q8_0/f16 | tg64 @ d8192 | 21.9 ± 0.1 |
| Vulkan0 | 8 | 256 | 1 | q8_0 | pp2048 @ d8192 | 307.9 ± 1.5 |
| Vulkan0 | 8 | 256 | 1 | q8_0 | tg64 @ d8192 | 22.7 ± 0.1 |

## gemma-4-E2B-it-Q4_0.gguf

gemma4 E2B Q4_0, 2.63 GiB, 4.63 B params

### GPU (Vulkan) vs CPU, empty context

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 512 | 1 | f16 | pp512 | 1162.3 ± 5.4 |
| Vulkan0 | 8 | 512 | 1 | f16 | tg128 | 43.5 ± 0.0 |
| CPU | 8 | 512 | -1 | f16 | pp512 | 238.2 ± 0.2 |
| CPU | 8 | 512 | -1 | f16 | tg128 | 32.2 ± 0.0 |

### GPU as the context fills (-ub 256)

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 256 | 1 | f16 | pp2048 | 1084.5 ± 0.8 |
| Vulkan0 | 8 | 256 | 1 | f16 | tg64 | 43.8 ± 0.0 |
| Vulkan0 | 8 | 256 | 1 | f16 | pp2048 @ d8192 | 747.9 ± 0.9 |
| Vulkan0 | 8 | 256 | 1 | f16 | tg64 @ d8192 | 39.7 ± 0.0 |
| Vulkan0 | 8 | 256 | 1 | f16 | pp2048 @ d16384 | 558.1 ± 1.3 |
| Vulkan0 | 8 | 256 | 1 | f16 | tg64 @ d16384 | 37.5 ± 0.1 |

### GPU tuning at 8k context: micro-batch and flash attention

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 256 | 0 | f16 | pp2048 @ d8192 | 759.8 ± 6.7 |
| Vulkan0 | 8 | 256 | 0 | f16 | tg64 @ d8192 | 28.3 ± 0.0 |
| Vulkan0 | 8 | 256 | 1 | f16 | pp2048 @ d8192 | 748.8 ± 1.0 |
| Vulkan0 | 8 | 256 | 1 | f16 | tg64 @ d8192 | 39.5 ± 0.0 |
| Vulkan0 | 8 | 512 | 0 | f16 | pp2048 @ d8192 | 765.7 ± 5.6 |
| Vulkan0 | 8 | 512 | 0 | f16 | tg64 @ d8192 | 28.0 ± 0.1 |
| Vulkan0 | 8 | 512 | 1 | f16 | pp2048 @ d8192 | 750.4 ± 1.2 |
| Vulkan0 | 8 | 512 | 1 | f16 | tg64 @ d8192 | 39.6 ± 0.0 |

### GPU tuning at 8k context: KV cache type

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 256 | 1 | f16 | pp2048 @ d8192 | 747.5 ± 0.7 |
| Vulkan0 | 8 | 256 | 1 | f16 | tg64 @ d8192 | 39.7 ± 0.1 |
| Vulkan0 | 8 | 256 | 1 | f16/q8_0 | pp2048 @ d8192 | 665.5 ± 0.5 |
| Vulkan0 | 8 | 256 | 1 | f16/q8_0 | tg64 @ d8192 | 39.6 ± 0.0 |
| Vulkan0 | 8 | 256 | 1 | q8_0/f16 | pp2048 @ d8192 | 533.1 ± 0.5 |
| Vulkan0 | 8 | 256 | 1 | q8_0/f16 | tg64 @ d8192 | 37.6 ± 0.0 |
| Vulkan0 | 8 | 256 | 1 | q8_0 | pp2048 @ d8192 | 730.8 ± 2.1 |
| Vulkan0 | 8 | 256 | 1 | q8_0 | tg64 @ d8192 | 38.9 ± 0.0 |

## gemma-4-E4B-it-Q4_0.gguf

gemma4 E4B Q4_0, 4.26 GiB, 7.46 B params

### GPU (Vulkan) vs CPU, empty context

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 512 | 1 | f16 | pp512 | 612.2 ± 0.9 |
| Vulkan0 | 8 | 512 | 1 | f16 | tg128 | 24.3 ± 0.0 |
| CPU | 8 | 512 | -1 | f16 | pp512 | 117.9 ± 0.3 |
| CPU | 8 | 512 | -1 | f16 | tg128 | 17.0 ± 0.0 |

### GPU as the context fills (-ub 256)

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 256 | 1 | f16 | pp2048 | 568.8 ± 0.4 |
| Vulkan0 | 8 | 256 | 1 | f16 | tg64 | 24.3 ± 0.0 |
| Vulkan0 | 8 | 256 | 1 | f16 | pp2048 @ d8192 | 446.7 ± 3.8 |
| Vulkan0 | 8 | 256 | 1 | f16 | tg64 @ d8192 | 21.8 ± 0.0 |
| Vulkan0 | 8 | 256 | 1 | f16 | pp2048 @ d16384 | 367.6 ± 1.3 |
| Vulkan0 | 8 | 256 | 1 | f16 | tg64 @ d16384 | 20.4 ± 0.1 |

### GPU tuning at 8k context: micro-batch and flash attention

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 256 | 0 | f16 | pp2048 @ d8192 | 457.9 ± 3.3 |
| Vulkan0 | 8 | 256 | 0 | f16 | tg64 @ d8192 | 19.8 ± 0.0 |
| Vulkan0 | 8 | 256 | 1 | f16 | pp2048 @ d8192 | 448.5 ± 2.2 |
| Vulkan0 | 8 | 256 | 1 | f16 | tg64 @ d8192 | 21.9 ± 0.0 |
| Vulkan0 | 8 | 512 | 0 | f16 | pp2048 @ d8192 | 469.3 ± 0.6 |
| Vulkan0 | 8 | 512 | 0 | f16 | tg64 @ d8192 | 19.7 ± 0.0 |
| Vulkan0 | 8 | 512 | 1 | f16 | pp2048 @ d8192 | 464.4 ± 2.0 |
| Vulkan0 | 8 | 512 | 1 | f16 | tg64 @ d8192 | 21.9 ± 0.0 |

### GPU tuning at 8k context: KV cache type

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 256 | 1 | f16 | pp2048 @ d8192 | 447.1 ± 2.7 |
| Vulkan0 | 8 | 256 | 1 | f16 | tg64 @ d8192 | 21.8 ± 0.0 |
| Vulkan0 | 8 | 256 | 1 | f16/q8_0 | pp2048 @ d8192 | 431.1 ± 0.2 |
| Vulkan0 | 8 | 256 | 1 | f16/q8_0 | tg64 @ d8192 | 22.0 ± 0.0 |
| Vulkan0 | 8 | 256 | 1 | q8_0/f16 | pp2048 @ d8192 | 369.4 ± 0.2 |
| Vulkan0 | 8 | 256 | 1 | q8_0/f16 | tg64 @ d8192 | 21.0 ± 0.0 |
| Vulkan0 | 8 | 256 | 1 | q8_0 | pp2048 @ d8192 | 449.1 ± 1.6 |
| Vulkan0 | 8 | 256 | 1 | q8_0 | tg64 @ d8192 | 21.6 ± 0.0 |

## gpt-oss-20b-MXFP4.gguf

gpt-oss 20B MXFP4 MoE, 11.27 GiB, 20.91 B params

### GPU (Vulkan) vs CPU, empty context

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 512 | 1 | f16 | pp512 | 547.3 ± 3.4 |
| Vulkan0 | 8 | 512 | 1 | f16 | tg128 | 29.3 ± 0.0 |
| CPU | 8 | 512 | -1 | f16 | pp512 | 72.7 ± 2.4 |
| CPU | 8 | 512 | -1 | f16 | tg128 | 20.3 ± 0.0 |

### GPU as the context fills (-ub 256)

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 256 | 1 | f16 | pp2048 | 464.6 ± 1.0 |
| Vulkan0 | 8 | 256 | 1 | f16 | tg64 | 28.9 ± 0.0 |
| Vulkan0 | 8 | 256 | 1 | f16 | pp2048 @ d8192 | 356.1 ± 0.8 |
| Vulkan0 | 8 | 256 | 1 | f16 | tg64 @ d8192 | 26.1 ± 0.0 |
| Vulkan0 | 8 | 256 | 1 | f16 | pp2048 @ d16384 | 287.5 ± 1.0 |
| Vulkan0 | 8 | 256 | 1 | f16 | tg64 @ d16384 | 23.8 ± 0.1 |

### GPU tuning at 8k context: micro-batch and flash attention

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 256 | 0 | f16 | pp2048 @ d8192 | 226.7 ± 0.5 |
| Vulkan0 | 8 | 256 | 0 | f16 | tg64 @ d8192 | 22.6 ± 0.1 |
| Vulkan0 | 8 | 256 | 1 | f16 | pp2048 @ d8192 | 358.4 ± 0.8 |
| Vulkan0 | 8 | 256 | 1 | f16 | tg64 @ d8192 | 26.3 ± 0.1 |
| Vulkan0 | 8 | 512 | 0 | f16 | pp2048 @ d8192 | 237.3 ± 0.6 |
| Vulkan0 | 8 | 512 | 0 | f16 | tg64 @ d8192 | 22.7 ± 0.1 |
| Vulkan0 | 8 | 512 | 1 | f16 | pp2048 @ d8192 | 403.8 ± 0.9 |
| Vulkan0 | 8 | 512 | 1 | f16 | tg64 @ d8192 | 26.2 ± 0.1 |

### GPU tuning at 8k context: KV cache type

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 256 | 1 | f16 | pp2048 @ d8192 | 358.9 ± 1.5 |
| Vulkan0 | 8 | 256 | 1 | f16 | tg64 @ d8192 | 26.3 ± 0.1 |
| Vulkan0 | 8 | 256 | 1 | f16/q8_0 | pp2048 @ d8192 | 329.7 ± 0.3 |
| Vulkan0 | 8 | 256 | 1 | f16/q8_0 | tg64 @ d8192 | 26.9 ± 0.1 |
| Vulkan0 | 8 | 256 | 1 | q8_0/f16 | pp2048 @ d8192 | 304.0 ± 0.6 |
| Vulkan0 | 8 | 256 | 1 | q8_0/f16 | tg64 @ d8192 | 26.4 ± 0.1 |
| Vulkan0 | 8 | 256 | 1 | q8_0 | pp2048 @ d8192 | 360.2 ± 0.3 |
| Vulkan0 | 8 | 256 | 1 | q8_0 | tg64 @ d8192 | 26.5 ± 0.1 |

## Qwen3-0.6B-Q8_0.gguf

qwen3 0.6B Q8_0, 0.59 GiB, 0.60 B params

### GPU (Vulkan) vs CPU, empty context

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 512 | 1 | f16 | pp512 | 3583.8 ± 110.4 |
| Vulkan0 | 8 | 512 | 1 | f16 | tg128 | 101.1 ± 0.3 |
| CPU | 8 | 512 | -1 | f16 | pp512 | 699.1 ± 1.1 |
| CPU | 8 | 512 | -1 | f16 | tg128 | 80.5 ± 0.1 |

### GPU as the context fills (-ub 256)

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 256 | 1 | f16 | pp2048 | 2590.8 ± 5.1 |
| Vulkan0 | 8 | 256 | 1 | f16 | tg64 | 102.9 ± 1.4 |
| Vulkan0 | 8 | 256 | 1 | f16 | pp2048 @ d8192 | 819.7 ± 4.1 |
| Vulkan0 | 8 | 256 | 1 | f16 | tg64 @ d8192 | 43.9 ± 0.1 |
| Vulkan0 | 8 | 256 | 1 | f16 | pp2048 @ d16384 | 483.0 ± 3.0 |
| Vulkan0 | 8 | 256 | 1 | f16 | tg64 @ d16384 | 28.2 ± 0.0 |

### GPU tuning at 8k context: micro-batch and flash attention

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 256 | 0 | f16 | pp2048 @ d8192 | 505.3 ± 0.5 |
| Vulkan0 | 8 | 256 | 0 | f16 | tg64 @ d8192 | 23.7 ± 0.0 |
| Vulkan0 | 8 | 256 | 1 | f16 | pp2048 @ d8192 | 816.4 ± 4.2 |
| Vulkan0 | 8 | 256 | 1 | f16 | tg64 @ d8192 | 44.0 ± 0.1 |
| Vulkan0 | 8 | 512 | 0 | f16 | pp2048 @ d8192 | 549.1 ± 0.4 |
| Vulkan0 | 8 | 512 | 0 | f16 | tg64 @ d8192 | 23.8 ± 0.0 |
| Vulkan0 | 8 | 512 | 1 | f16 | pp2048 @ d8192 | 918.7 ± 1.4 |
| Vulkan0 | 8 | 512 | 1 | f16 | tg64 @ d8192 | 44.1 ± 0.1 |

### GPU tuning at 8k context: KV cache type

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 256 | 1 | f16 | pp2048 @ d8192 | 820.2 ± 2.2 |
| Vulkan0 | 8 | 256 | 1 | f16 | tg64 @ d8192 | 44.0 ± 0.1 |
| Vulkan0 | 8 | 256 | 1 | f16/q8_0 | pp2048 @ d8192 | 771.3 ± 2.8 |
| Vulkan0 | 8 | 256 | 1 | f16/q8_0 | tg64 @ d8192 | 49.1 ± 0.4 |
| Vulkan0 | 8 | 256 | 1 | q8_0/f16 | pp2048 @ d8192 | 640.3 ± 1.4 |
| Vulkan0 | 8 | 256 | 1 | q8_0/f16 | tg64 @ d8192 | 44.7 ± 0.4 |
| Vulkan0 | 8 | 256 | 1 | q8_0 | pp2048 @ d8192 | 874.8 ± 2.7 |
| Vulkan0 | 8 | 256 | 1 | q8_0 | tg64 @ d8192 | 47.5 ± 0.6 |

## Qwen3-1.7B-Q8_0.gguf

qwen3 1.7B Q8_0, 1.70 GiB, 1.72 B params

### GPU (Vulkan) vs CPU, empty context

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 512 | 1 | f16 | pp512 | 1416.6 ± 6.4 |
| Vulkan0 | 8 | 512 | 1 | f16 | tg128 | 41.0 ± 0.0 |
| CPU | 8 | 512 | -1 | f16 | pp512 | 247.8 ± 0.5 |
| CPU | 8 | 512 | -1 | f16 | tg128 | 29.7 ± 0.0 |

### GPU as the context fills (-ub 256)

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 256 | 1 | f16 | pp2048 | 1273.8 ± 0.8 |
| Vulkan0 | 8 | 256 | 1 | f16 | tg64 | 41.2 ± 0.0 |
| Vulkan0 | 8 | 256 | 1 | f16 | pp2048 @ d8192 | 618.4 ± 2.5 |
| Vulkan0 | 8 | 256 | 1 | f16 | tg64 @ d8192 | 26.7 ± 0.0 |
| Vulkan0 | 8 | 256 | 1 | f16 | pp2048 @ d16384 | 407.1 ± 1.0 |
| Vulkan0 | 8 | 256 | 1 | f16 | tg64 @ d16384 | 19.9 ± 0.0 |

### GPU tuning at 8k context: micro-batch and flash attention

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 256 | 0 | f16 | pp2048 @ d8192 | 424.2 ± 0.4 |
| Vulkan0 | 8 | 256 | 0 | f16 | tg64 @ d8192 | 18.1 ± 0.0 |
| Vulkan0 | 8 | 256 | 1 | f16 | pp2048 @ d8192 | 619.0 ± 0.4 |
| Vulkan0 | 8 | 256 | 1 | f16 | tg64 @ d8192 | 26.7 ± 0.0 |
| Vulkan0 | 8 | 512 | 0 | f16 | pp2048 @ d8192 | 450.9 ± 0.8 |
| Vulkan0 | 8 | 512 | 0 | f16 | tg64 @ d8192 | 18.1 ± 0.0 |
| Vulkan0 | 8 | 512 | 1 | f16 | pp2048 @ d8192 | 667.3 ± 3.0 |
| Vulkan0 | 8 | 512 | 1 | f16 | tg64 @ d8192 | 26.7 ± 0.0 |

### GPU tuning at 8k context: KV cache type

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 256 | 1 | f16 | pp2048 @ d8192 | 615.7 ± 5.0 |
| Vulkan0 | 8 | 256 | 1 | f16 | tg64 @ d8192 | 26.7 ± 0.0 |
| Vulkan0 | 8 | 256 | 1 | f16/q8_0 | pp2048 @ d8192 | 589.2 ± 1.4 |
| Vulkan0 | 8 | 256 | 1 | f16/q8_0 | tg64 @ d8192 | 28.5 ± 0.1 |
| Vulkan0 | 8 | 256 | 1 | q8_0/f16 | pp2048 @ d8192 | 509.6 ± 0.3 |
| Vulkan0 | 8 | 256 | 1 | q8_0/f16 | tg64 @ d8192 | 26.8 ± 0.1 |
| Vulkan0 | 8 | 256 | 1 | q8_0 | pp2048 @ d8192 | 649.8 ± 0.9 |
| Vulkan0 | 8 | 256 | 1 | q8_0 | tg64 @ d8192 | 27.7 ± 0.1 |

## Qwen3-4B-Q4_K_M.gguf

qwen3 4B Q4_K - Medium, 2.32 GiB, 4.02 B params

### GPU (Vulkan) vs CPU, empty context

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 512 | 1 | f16 | pp512 | 564.1 ± 2.9 |
| Vulkan0 | 8 | 512 | 1 | f16 | tg128 | 29.4 ± 0.0 |
| CPU | 8 | 512 | -1 | f16 | pp512 | 133.3 ± 0.2 |
| CPU | 8 | 512 | -1 | f16 | tg128 | 21.3 ± 0.0 |

### GPU as the context fills (-ub 256)

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 256 | 1 | f16 | pp2048 | 504.1 ± 0.9 |
| Vulkan0 | 8 | 256 | 1 | f16 | tg64 | 29.5 ± 0.0 |
| Vulkan0 | 8 | 256 | 1 | f16 | pp2048 @ d8192 | 257.8 ± 0.8 |
| Vulkan0 | 8 | 256 | 1 | f16 | tg64 @ d8192 | 19.7 ± 0.0 |
| Vulkan0 | 8 | 256 | 1 | f16 | pp2048 @ d16384 | 171.4 ± 1.0 |
| Vulkan0 | 8 | 256 | 1 | f16 | tg64 @ d16384 | 14.9 ± 0.0 |

### GPU tuning at 8k context: micro-batch and flash attention

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 256 | 0 | f16 | pp2048 @ d8192 | 175.3 ± 0.2 |
| Vulkan0 | 8 | 256 | 0 | f16 | tg64 @ d8192 | 12.2 ± 0.0 |
| Vulkan0 | 8 | 256 | 1 | f16 | pp2048 @ d8192 | 258.0 ± 1.0 |
| Vulkan0 | 8 | 256 | 1 | f16 | tg64 @ d8192 | 19.7 ± 0.0 |
| Vulkan0 | 8 | 512 | 0 | f16 | pp2048 @ d8192 | 182.5 ± 0.1 |
| Vulkan0 | 8 | 512 | 0 | f16 | tg64 @ d8192 | 12.2 ± 0.0 |
| Vulkan0 | 8 | 512 | 1 | f16 | pp2048 @ d8192 | 270.2 ± 0.1 |
| Vulkan0 | 8 | 512 | 1 | f16 | tg64 @ d8192 | 19.8 ± 0.0 |

### GPU tuning at 8k context: KV cache type

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 256 | 1 | f16 | pp2048 @ d8192 | 257.6 ± 1.3 |
| Vulkan0 | 8 | 256 | 1 | f16 | tg64 @ d8192 | 19.7 ± 0.0 |
| Vulkan0 | 8 | 256 | 1 | f16/q8_0 | pp2048 @ d8192 | 235.0 ± 0.3 |
| Vulkan0 | 8 | 256 | 1 | f16/q8_0 | tg64 @ d8192 | 21.0 ± 0.0 |
| Vulkan0 | 8 | 256 | 1 | q8_0/f16 | pp2048 @ d8192 | 202.8 ± 0.4 |
| Vulkan0 | 8 | 256 | 1 | q8_0/f16 | tg64 @ d8192 | 19.9 ± 0.0 |
| Vulkan0 | 8 | 256 | 1 | q8_0 | pp2048 @ d8192 | 263.5 ± 0.6 |
| Vulkan0 | 8 | 256 | 1 | q8_0 | tg64 @ d8192 | 20.4 ± 0.1 |

## Qwen3-8B-Q4_K_M.gguf

qwen3 8B Q4_K - Medium, 4.68 GiB, 8.19 B params

### GPU (Vulkan) vs CPU, empty context

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 512 | 1 | f16 | pp512 | 318.6 ± 1.4 |
| Vulkan0 | 8 | 512 | 1 | f16 | tg128 | 16.9 ± 0.0 |
| CPU | 8 | 512 | -1 | f16 | pp512 | 75.9 ± 0.1 |
| CPU | 8 | 512 | -1 | f16 | tg128 | 11.7 ± 0.0 |

### GPU as the context fills (-ub 256)

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 256 | 1 | f16 | pp2048 | 298.1 ± 0.6 |
| Vulkan0 | 8 | 256 | 1 | f16 | tg64 | 17.0 ± 0.0 |
| Vulkan0 | 8 | 256 | 1 | f16 | pp2048 @ d8192 | 191.0 ± 0.5 |
| Vulkan0 | 8 | 256 | 1 | f16 | tg64 @ d8192 | 12.9 ± 0.0 |
| Vulkan0 | 8 | 256 | 1 | f16 | pp2048 @ d16384 | 139.7 ± 0.2 |
| Vulkan0 | 8 | 256 | 1 | f16 | tg64 @ d16384 | 10.6 ± 0.0 |

### GPU tuning at 8k context: micro-batch and flash attention

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 256 | 0 | f16 | pp2048 @ d8192 | 141.8 ± 0.1 |
| Vulkan0 | 8 | 256 | 0 | f16 | tg64 @ d8192 | 9.5 ± 0.0 |
| Vulkan0 | 8 | 256 | 1 | f16 | pp2048 @ d8192 | 191.3 ± 0.3 |
| Vulkan0 | 8 | 256 | 1 | f16 | tg64 @ d8192 | 13.1 ± 0.0 |
| Vulkan0 | 8 | 512 | 0 | f16 | pp2048 @ d8192 | 146.5 ± 0.1 |
| Vulkan0 | 8 | 512 | 0 | f16 | tg64 @ d8192 | 9.5 ± 0.0 |
| Vulkan0 | 8 | 512 | 1 | f16 | pp2048 @ d8192 | 197.3 ± 0.5 |
| Vulkan0 | 8 | 512 | 1 | f16 | tg64 @ d8192 | 13.1 ± 0.0 |

### GPU tuning at 8k context: KV cache type

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 256 | 1 | f16 | pp2048 @ d8192 | 191.5 ± 0.6 |
| Vulkan0 | 8 | 256 | 1 | f16 | tg64 @ d8192 | 13.1 ± 0.0 |
| Vulkan0 | 8 | 256 | 1 | f16/q8_0 | pp2048 @ d8192 | 178.0 ± 0.1 |
| Vulkan0 | 8 | 256 | 1 | f16/q8_0 | tg64 @ d8192 | 13.8 ± 0.0 |
| Vulkan0 | 8 | 256 | 1 | q8_0/f16 | pp2048 @ d8192 | 158.4 ± 0.5 |
| Vulkan0 | 8 | 256 | 1 | q8_0/f16 | tg64 @ d8192 | 13.2 ± 0.0 |
| Vulkan0 | 8 | 256 | 1 | q8_0 | pp2048 @ d8192 | 194.0 ± 0.3 |
| Vulkan0 | 8 | 256 | 1 | q8_0 | tg64 @ d8192 | 13.4 ± 0.0 |

## Qwen3-30B-A3B-Instruct-2507-UD-Q4_K_XL.gguf

qwen3moe 30B.A3B Q4_K - Medium, 16.47 GiB, 30.53 B params

### GPU (Vulkan) vs CPU, empty context

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 512 | 1 | f16 | pp512 | 437.4 ± 1.5 |
| Vulkan0 | 8 | 512 | 1 | f16 | tg128 | 36.1 ± 0.0 |
| CPU | 8 | 512 | -1 | f16 | pp512 | 103.3 ± 2.1 |
| CPU | 8 | 512 | -1 | f16 | tg128 | 25.8 ± 0.1 |

### GPU as the context fills (-ub 256)

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 256 | 1 | f16 | pp2048 | 328.6 ± 0.7 |
| Vulkan0 | 8 | 256 | 1 | f16 | tg64 | 36.2 ± 0.2 |
| Vulkan0 | 8 | 256 | 1 | f16 | pp2048 @ d8192 | 184.2 ± 0.5 |
| Vulkan0 | 8 | 256 | 1 | f16 | tg64 @ d8192 | 25.3 ± 0.1 |
| Vulkan0 | 8 | 256 | 1 | f16 | pp2048 @ d16384 | 126.5 ± 0.3 |
| Vulkan0 | 8 | 256 | 1 | f16 | tg64 @ d16384 | 19.6 ± 0.0 |

### GPU tuning at 8k context: micro-batch and flash attention

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 256 | 0 | f16 | pp2048 @ d8192 | 127.4 ± 0.1 |
| Vulkan0 | 8 | 256 | 0 | f16 | tg64 @ d8192 | 15.1 ± 0.0 |
| Vulkan0 | 8 | 256 | 1 | f16 | pp2048 @ d8192 | 185.2 ± 0.6 |
| Vulkan0 | 8 | 256 | 1 | f16 | tg64 @ d8192 | 25.3 ± 0.1 |
| Vulkan0 | 8 | 512 | 0 | f16 | pp2048 @ d8192 | 138.9 ± 0.1 |
| Vulkan0 | 8 | 512 | 0 | f16 | tg64 @ d8192 | 15.1 ± 0.1 |
| Vulkan0 | 8 | 512 | 1 | f16 | pp2048 @ d8192 | 209.5 ± 0.2 |
| Vulkan0 | 8 | 512 | 1 | f16 | tg64 @ d8192 | 25.6 ± 0.2 |

### GPU tuning at 8k context: KV cache type

| device | threads | ubatch | flash attn | KV | test | t/s |
|---|--:|--:|---|---|---|--:|
| Vulkan0 | 8 | 256 | 1 | f16 | pp2048 @ d8192 | 185.6 ± 0.5 |
| Vulkan0 | 8 | 256 | 1 | f16 | tg64 @ d8192 | 25.3 ± 0.1 |
| Vulkan0 | 8 | 256 | 1 | f16/q8_0 | pp2048 @ d8192 | 160.7 ± 0.4 |
| Vulkan0 | 8 | 256 | 1 | f16/q8_0 | tg64 @ d8192 | 26.3 ± 0.1 |
| Vulkan0 | 8 | 256 | 1 | q8_0/f16 | pp2048 @ d8192 | 139.3 ± 0.1 |
| Vulkan0 | 8 | 256 | 1 | q8_0/f16 | tg64 @ d8192 | 25.0 ± 0.1 |
| Vulkan0 | 8 | 256 | 1 | q8_0 | pp2048 @ d8192 | 187.3 ± 0.6 |
| Vulkan0 | 8 | 256 | 1 | q8_0 | tg64 @ d8192 | 26.1 ± 0.2 |

## Speculative decoding (server, 256 tokens, temperature 0)

| target | draft | type | alone t/s | with draft t/s | speed-up | accepted |
|---|---|---|--:|--:|--:|--:|
| Qwen3-4B-Q4_K_M.gguf | Qwen3-0.6B-Q8_0.gguf | draft-simple | 28.6 | 39.9 | 1.40x | 182 / 218 |
| Qwen3-8B-Q4_K_M.gguf | Qwen3-0.6B-Q8_0.gguf | draft-simple | 16.6 | 30.4 | 1.83x | 182 / 217 |
| Qwen3-8B-Q4_K_M.gguf | Qwen3-1.7B-Q8_0.gguf | draft-simple | 16.6 | 20.5 | 1.23x | 183 / 213 |
| Qwen3-30B-A3B-Instruct-2507-UD-Q4_K_XL.gguf | Qwen3-0.6B-Q8_0.gguf | draft-simple | 35.0 | 26.3 | 0.75x | 174 / 242 |
| gemma-4-E4B-it-Q4_0.gguf | mtp-gemma-4-E4B-it-Q4_0.gguf | draft-mtp | 23.6 | 58.4 | 2.47x | 183 / 216 |
| gemma-4-26B-A4B-it-Q4_0.gguf | mtp-gemma-4-26B-A4B-it-Q4_0.gguf | draft-mtp | 25.2 | 40.6 | 1.61x | 186 / 207 |
| gpt-oss-20b-MXFP4.gguf | eagle3-gpt-oss-20b-Q8_0.gguf | draft-eagle3 | 28.6 | 22.0 | 0.77x | 142 / 338 |
