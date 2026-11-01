# Comparison: 8681 (Debian) vs build 12020

- **8681 (Debian)**: `2026-10-31_fw13-7840u_b8681-distro`, kernel 7.0.0-42-generic, GTT 24576 MiB, 20.1 GiB available, load 1.19, warnings: system busy (load average > 1)
- **build 12020**: `2026-10-31_fw13-7840u_b12020`, kernel 7.0.0-42-generic, GTT 24576 MiB, 25.2 GiB available, load 2.27, warnings: system busy (load average > 1)

Values are tokens per second (llama-bench mean). pp = prompt processing, tg = generation, d = context already filled.

## Throughput by model

### gemma-4-26B-A4B-it-Q4_0.gguf

| test | 8681 (Debian) | build 12020 | change |
|---|--:|--:|--:|
| GPU pp512 | 366.3 | 493.4 | +35% |
| GPU tg128 | 24.7 | 26.0 | +5% |
| CPU pp512 | 93.1 | 96.2 | +3% |
| CPU tg128 | 19.3 | 19.4 | +0% |
| pp2048 @ 0 | 294.9 | 394.7 | +34% |
| pp2048 @ 8k | 251.4 | 311.3 | +24% |
| pp2048 @ 16k | 210.2 | 259.3 | +23% |
| tg64 @ 0 | 25.0 | 26.1 | +4% |
| tg64 @ 8k | 21.8 | 22.5 | +3% |
| tg64 @ 16k | 20.6 | 21.5 | +5% |

### gpt-oss-20b-MXFP4.gguf

| test | 8681 (Debian) | build 12020 | change |
|---|--:|--:|--:|
| GPU pp512 | 416.0 | 547.3 | +32% |
| GPU tg128 | 26.9 | 29.3 | +9% |
| CPU pp512 | 59.2 | 72.7 | +23% |
| CPU tg128 | 20.4 | 20.3 | -1% |
| pp2048 @ 0 | 328.9 | 464.6 | +41% |
| pp2048 @ 8k | 262.3 | 356.1 | +36% |
| pp2048 @ 16k | 215.2 | 287.5 | +34% |
| tg64 @ 0 | 27.0 | 28.9 | +7% |
| tg64 @ 8k | 24.2 | 26.1 | +8% |
| tg64 @ 16k | 22.2 | 23.8 | +7% |

### Qwen3-0.6B-Q8_0.gguf

| test | 8681 (Debian) | build 12020 | change |
|---|--:|--:|--:|
| GPU pp512 | 2745.1 | 3583.8 | +31% |
| GPU tg128 | 97.8 | 101.1 | +3% |
| CPU pp512 | 295.4 | 699.1 | +137% |
| CPU tg128 | 75.4 | 80.5 | +7% |
| pp2048 @ 0 | 2172.9 | 2590.8 | +19% |
| pp2048 @ 8k | 831.1 | 819.7 | -1% |
| pp2048 @ 16k | 494.4 | 483.0 | -2% |
| tg64 @ 0 | 98.8 | 102.9 | +4% |
| tg64 @ 8k | 42.5 | 43.9 | +3% |
| tg64 @ 16k | 27.3 | 28.2 | +3% |

### Qwen3-1.7B-Q8_0.gguf

| test | 8681 (Debian) | build 12020 | change |
|---|--:|--:|--:|
| GPU pp512 | 1051.8 | 1416.6 | +35% |
| GPU tg128 | 39.2 | 41.0 | +4% |
| CPU pp512 | 117.0 | 247.8 | +112% |
| CPU tg128 | 29.0 | 29.7 | +3% |
| pp2048 @ 0 | 977.9 | 1273.8 | +30% |
| pp2048 @ 8k | 567.8 | 618.4 | +9% |
| pp2048 @ 16k | 397.6 | 407.1 | +2% |
| tg64 @ 0 | 39.9 | 41.2 | +3% |
| tg64 @ 8k | 25.8 | 26.7 | +3% |
| tg64 @ 16k | 19.4 | 19.9 | +2% |

### Qwen3-4B-Q4_K_M.gguf

| test | 8681 (Debian) | build 12020 | change |
|---|--:|--:|--:|
| GPU pp512 | 440.7 | 564.1 | +28% |
| GPU tg128 | 26.4 | 29.4 | +11% |
| CPU pp512 | 88.5 | 133.3 | +51% |
| CPU tg128 | 20.8 | 21.3 | +3% |
| pp2048 @ 0 | 394.8 | 504.1 | +28% |
| pp2048 @ 8k | 224.8 | 257.8 | +15% |
| pp2048 @ 16k | 147.5 | 171.4 | +16% |
| tg64 @ 0 | 26.5 | 29.5 | +11% |
| tg64 @ 8k | 18.2 | 19.7 | +8% |
| tg64 @ 16k | 14.1 | 14.9 | +6% |

### Qwen3-8B-Q4_K_M.gguf

| test | 8681 (Debian) | build 12020 | change |
|---|--:|--:|--:|
| GPU pp512 | 249.1 | 318.6 | +28% |
| GPU tg128 | 15.6 | 16.9 | +8% |
| CPU pp512 | 52.1 | 75.9 | +46% |
| CPU tg128 | 11.5 | 11.7 | +1% |
| pp2048 @ 0 | 232.8 | 298.1 | +28% |
| pp2048 @ 8k | 143.7 | 191.0 | +33% |
| pp2048 @ 16k | 77.0 | 139.7 | +81% |
| tg64 @ 0 | 15.6 | 17.0 | +9% |
| tg64 @ 8k | 12.2 | 12.9 | +6% |
| tg64 @ 16k | 10.1 | 10.6 | +6% |

### Qwen3-30B-A3B-Instruct-2507-UD-Q4_K_XL.gguf

| test | 8681 (Debian) | build 12020 | change |
|---|--:|--:|--:|
| GPU pp512 | 309.7 | 437.4 | +41% |
| GPU tg128 | 31.1 | 36.1 | +16% |
| CPU pp512 | 69.7 | 103.3 | +48% |
| CPU tg128 | 24.6 | 25.8 | +5% |
| pp2048 @ 0 | 239.5 | 328.6 | +37% |
| pp2048 @ 8k | 127.9 | 184.2 | +44% |
| pp2048 @ 16k | 73.9 | 126.5 | +71% |
| tg64 @ 0 | 32.0 | 36.2 | +13% |
| tg64 @ 8k | 23.0 | 25.3 | +10% |
| tg64 @ 16k | 18.1 | 19.6 | +8% |

### gemma-4-E2B-it-Q4_0.gguf

| test | 8681 (Debian) | build 12020 | change |
|---|--:|--:|--:|
| GPU pp512 | fail | 1162.3 |  |
| GPU tg128 | fail | 43.5 |  |
| CPU pp512 | fail | 238.2 |  |
| CPU tg128 | fail | 32.2 |  |
| pp2048 @ 0 | fail | 1084.5 |  |
| pp2048 @ 8k | fail | 747.9 |  |
| pp2048 @ 16k | fail | 558.1 |  |
| tg64 @ 0 | fail | 43.8 |  |
| tg64 @ 8k | fail | 39.7 |  |
| tg64 @ 16k | fail | 37.5 |  |

### gemma-4-E4B-it-Q4_0.gguf

| test | 8681 (Debian) | build 12020 | change |
|---|--:|--:|--:|
| GPU pp512 | fail | 612.2 |  |
| GPU tg128 | fail | 24.3 |  |
| CPU pp512 | fail | 117.9 |  |
| CPU tg128 | fail | 17.0 |  |
| pp2048 @ 0 | fail | 568.8 |  |
| pp2048 @ 8k | fail | 446.7 |  |
| pp2048 @ 16k | fail | 367.6 |  |
| tg64 @ 0 | fail | 24.3 |  |
| tg64 @ 8k | fail | 21.8 |  |
| tg64 @ 16k | fail | 20.4 |  |

## Tuning at 8k context (GPU, pp2048 / tg64)

Micro-batch (ub) and flash attention (fa), then KV cache type with ub 256 and fa on.

### gemma-4-26B-A4B-it-Q4_0.gguf

| setting | 8681 (Debian) | build 12020 |
|---|--:|--:|
| ub 256, fa off | 232.8 / 17.8 | 316.7 / 18.8 |
| ub 256, fa on | 238.9 / 21.6 | 311.4 / 22.7 |
| ub 512, fa off | 270.2 / 17.7 | 351.5 / 18.6 |
| ub 512, fa on | 281.8 / 21.4 | 350.6 / 22.8 |
| KV f16/f16 | 237.6 / 21.4 | 311.4 / 22.7 |
| KV q8_0/q8_0 | 203.3 / 21.6 | 307.9 / 22.7 |
| KV f16/q8_0 | 23.1 / 8.1 | 290.9 / 22.9 |
| KV q8_0/f16 | 30.7 / 8.9 | 250.6 / 21.9 |

### gpt-oss-20b-MXFP4.gguf

| setting | 8681 (Debian) | build 12020 |
|---|--:|--:|
| ub 256, fa off | 187.5 / 20.8 | 226.7 / 22.6 |
| ub 256, fa on | 261.8 / 24.2 | 358.4 / 26.3 |
| ub 512, fa off | 201.9 / 20.5 | 237.3 / 22.7 |
| ub 512, fa on | 310.8 / 24.1 | 403.8 / 26.2 |
| KV f16/f16 | 266.5 / 24.4 | 358.9 / 26.3 |
| KV q8_0/q8_0 | 240.1 / 24.4 | 360.2 / 26.5 |
| KV f16/q8_0 | 21.2 / 7.4 | 329.7 / 26.9 |
| KV q8_0/f16 | 36.2 / 9.1 | 304.0 / 26.4 |

### Qwen3-0.6B-Q8_0.gguf

| setting | 8681 (Debian) | build 12020 |
|---|--:|--:|
| ub 256, fa off | 480.2 / 22.9 | 505.3 / 23.7 |
| ub 256, fa on | 829.7 / 42.2 | 816.4 / 44.0 |
| ub 512, fa off | 523.6 / 23.0 | 549.1 / 23.8 |
| ub 512, fa on | 836.8 / 42.3 | 918.7 / 44.1 |
| KV f16/f16 | 831.0 / 42.4 | 820.2 / 44.0 |
| KV q8_0/q8_0 | 600.6 / 45.1 | 874.8 / 47.5 |
| KV f16/q8_0 | 10.7 / 6.7 | 771.3 / 49.1 |
| KV q8_0/f16 | 19.6 / 9.5 | 640.3 / 44.7 |

### Qwen3-1.7B-Q8_0.gguf

| setting | 8681 (Debian) | build 12020 |
|---|--:|--:|
| ub 256, fa off | 377.9 / 17.6 | 424.2 / 18.1 |
| ub 256, fa on | 569.9 / 25.8 | 619.0 / 26.7 |
| ub 512, fa off | 400.5 / 17.6 | 450.9 / 18.1 |
| ub 512, fa on | 565.7 / 25.8 | 667.3 / 26.7 |
| KV f16/f16 | 569.5 / 25.9 | 615.7 / 26.7 |
| KV q8_0/q8_0 | 451.1 / 26.4 | 649.8 / 27.7 |
| KV f16/q8_0 | 10.6 / 6.1 | 589.2 / 28.5 |
| KV q8_0/f16 | 19.2 / 8.2 | 509.6 / 26.8 |

### Qwen3-4B-Q4_K_M.gguf

| setting | 8681 (Debian) | build 12020 |
|---|--:|--:|
| ub 256, fa off | 158.2 / 11.4 | 175.3 / 12.2 |
| ub 256, fa on | 223.7 / 18.2 | 258.0 / 19.7 |
| ub 512, fa off | 164.8 / 11.4 | 182.5 / 12.2 |
| ub 512, fa on | 202.2 / 18.2 | 270.2 / 19.8 |
| KV f16/f16 | 223.6 / 18.2 | 257.6 / 19.7 |
| KV q8_0/q8_0 | 181.1 / 18.6 | 263.5 / 20.4 |
| KV f16/q8_0 | 4.2 / 3.0 | 235.0 / 21.0 |
| KV q8_0/f16 | 7.6 / 4.3 | 202.8 / 19.9 |

### Qwen3-8B-Q4_K_M.gguf

| setting | 8681 (Debian) | build 12020 |
|---|--:|--:|
| ub 256, fa off | 123.4 / 8.8 | 141.8 / 9.5 |
| ub 256, fa on | 162.2 / 12.4 | 191.3 / 13.1 |
| ub 512, fa off | 128.1 / 8.8 | 146.5 / 9.5 |
| ub 512, fa on | 149.3 / 12.4 | 197.3 / 13.1 |
| KV f16/f16 | 161.8 / 12.4 | 191.5 / 13.1 |
| KV q8_0/q8_0 | 138.4 / 12.5 | 194.0 / 13.4 |
| KV f16/q8_0 | 4.1 / 2.7 | 178.0 / 13.8 |
| KV q8_0/f16 | 7.4 / 3.9 | 158.4 / 13.2 |

### Qwen3-30B-A3B-Instruct-2507-UD-Q4_K_XL.gguf

| setting | 8681 (Debian) | build 12020 |
|---|--:|--:|
| ub 256, fa off | 111.5 / 14.0 | 127.4 / 15.1 |
| ub 256, fa on | 130.1 / 23.1 | 185.2 / 25.3 |
| ub 512, fa off | 124.2 / 14.0 | 138.9 / 15.1 |
| ub 512, fa on | 92.2 / 23.0 | 209.5 / 25.6 |
| KV f16/f16 | 120.3 / 22.8 | 185.6 / 25.3 |
| KV q8_0/q8_0 | 123.6 / 23.6 | 187.3 / 26.1 |
| KV f16/q8_0 | 6.5 / 3.6 | 160.7 / 26.3 |
| KV q8_0/f16 | 9.2 / 4.8 | 139.3 / 25.0 |

### gemma-4-E2B-it-Q4_0.gguf

| setting | 8681 (Debian) | build 12020 |
|---|--:|--:|
| ub 256, fa off | fail / fail | 759.8 / 28.3 |
| ub 256, fa on | fail / fail | 748.8 / 39.5 |
| ub 512, fa off | fail / fail | 765.7 / 28.0 |
| ub 512, fa on | fail / fail | 750.4 / 39.6 |
| KV f16/f16 | fail / fail | 747.5 / 39.7 |
| KV q8_0/q8_0 | fail / fail | 730.8 / 38.9 |
| KV f16/q8_0 | fail / fail | 665.5 / 39.6 |
| KV q8_0/f16 | fail / fail | 533.1 / 37.6 |

### gemma-4-E4B-it-Q4_0.gguf

| setting | 8681 (Debian) | build 12020 |
|---|--:|--:|
| ub 256, fa off | fail / fail | 457.9 / 19.8 |
| ub 256, fa on | fail / fail | 448.5 / 21.9 |
| ub 512, fa off | fail / fail | 469.3 / 19.7 |
| ub 512, fa on | fail / fail | 464.4 / 21.9 |
| KV f16/f16 | fail / fail | 447.1 / 21.8 |
| KV q8_0/q8_0 | fail / fail | 449.1 / 21.6 |
| KV f16/q8_0 | fail / fail | 431.1 / 22.0 |
| KV q8_0/f16 | fail / fail | 369.4 / 21.0 |

## Speculative decoding (server, 256 tokens, temperature 0)

| build | target | draft | type | alone | with draft | speed-up | accepted |
|---|--:|--:|--:|--:|--:|--:|--:|
| 8681 (Debian) | Qwen3-4B-Q4_K_M.gguf | Qwen3-0.6B-Q8_0.gguf | draft-simple | 26.1 | 36.0 | 1.38x | 201 / 244 |
| 8681 (Debian) | Qwen3-8B-Q4_K_M.gguf | Qwen3-0.6B-Q8_0.gguf | draft-simple | 15.3 | 23.0 | 1.50x | 198 / 258 |
| 8681 (Debian) | Qwen3-8B-Q4_K_M.gguf | Qwen3-1.7B-Q8_0.gguf | draft-simple | 15.5 | 18.0 | 1.16x | 218 / 298 |
| 8681 (Debian) | Qwen3-30B-A3B-Instruct-2507-UD-Q4_K_XL.gguf | Qwen3-0.6B-Q8_0.gguf | draft-simple | 31.0 | 23.1 | 0.74x | 197 / 258 |
| build 12020 | Qwen3-4B-Q4_K_M.gguf | Qwen3-0.6B-Q8_0.gguf | draft-simple | 28.6 | 39.9 | 1.40x | 182 / 218 |
| build 12020 | Qwen3-8B-Q4_K_M.gguf | Qwen3-0.6B-Q8_0.gguf | draft-simple | 16.6 | 30.4 | 1.83x | 182 / 217 |
| build 12020 | Qwen3-8B-Q4_K_M.gguf | Qwen3-1.7B-Q8_0.gguf | draft-simple | 16.6 | 20.5 | 1.23x | 183 / 213 |
| build 12020 | Qwen3-30B-A3B-Instruct-2507-UD-Q4_K_XL.gguf | Qwen3-0.6B-Q8_0.gguf | draft-simple | 35.0 | 26.3 | 0.75x | 174 / 242 |
| build 12020 | gemma-4-E4B-it-Q4_0.gguf | mtp-gemma-4-E4B-it-Q4_0.gguf | draft-mtp | 23.6 | 58.4 | 2.47x | 183 / 216 |
| build 12020 | gemma-4-26B-A4B-it-Q4_0.gguf | mtp-gemma-4-26B-A4B-it-Q4_0.gguf | draft-mtp | 25.2 | 40.6 | 1.61x | 186 / 207 |
| build 12020 | gpt-oss-20b-MXFP4.gguf | eagle3-gpt-oss-20b-Q8_0.gguf | draft-eagle3 | 28.6 | 22.0 | 0.77x | 142 / 338 |

