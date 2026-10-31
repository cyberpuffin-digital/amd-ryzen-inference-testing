#!/usr/bin/env bash
# Print a JSON description of this machine and its software, for a results
# directory's env.json. Everything here affects performance or is needed to
# reproduce a run; nothing here identifies the machine or its owner.
#
#   bench/capture-env.sh <label> [llama binary or directory]
#
# <label> names the hardware instead of the hostname, e.g. fw13-7840u.
# Read from sysfs and standard tools, without root. Serial numbers, UUIDs,
# MAC/IP addresses, the hostname and the username are never read.
set -uo pipefail

label=${1:?usage: capture-env.sh <label> [llama binary or dir]}
llama=${2:-}

dmi() { cat "/sys/class/dmi/id/$1" 2>/dev/null | xargs; }
first() { for f in "$@"; do [[ -r $f ]] && { cat "$f"; return; }; done; echo unknown; }

# The DRM device of the AMD GPU (vendor 0x1002).
gpu_dev=
for d in /sys/class/drm/card*/device; do
    [[ $(cat "$d/vendor" 2>/dev/null) == 0x1002 ]] && { gpu_dev=$d; break; }
done

# llama.cpp: an upstream build installs one `llama` binary with subcommands;
# Debian and older builds install llama-cli and friends.
if [[ -n $llama && -d $llama ]]; then
    [[ -x $llama/llama ]] && llama=$llama/llama || llama=$llama/llama-cli
fi
llama=${llama:-$(command -v llama-cli)}
if [[ $(basename "$llama") == llama ]]; then
    llama_version=$("$llama" version 2>&1 | grep -m1 version)
    devices=$("$llama" cli --list-devices 2>&1 | grep -E '^\s+[A-Za-z]+[0-9]+:' | sed 's/^ *//')
else
    llama_version=$("$llama" --version 2>&1 | grep -m1 version)
    devices=$("$llama" --list-devices 2>&1 | grep -E '^\s+[A-Za-z]+[0-9]+:' | sed 's/^ *//')
fi

# One line: multiarch systems also list the i386 package.
mesa=$({ dpkg-query -W -f '${Version}\n' mesa-vulkan-drivers 2>/dev/null ||
         rpm -q --qf '%{VERSION}\n' mesa-vulkan-drivers 2>/dev/null || echo unknown; } | head -1)

ac=$(cat /sys/class/power_supply/A*/online 2>/dev/null | head -1)
bat=$(ls -d /sys/class/power_supply/BAT* 2>/dev/null | head -1)
bat_watts=null
if [[ -n $bat && -r $bat/voltage_now && -r $bat/current_now ]]; then
    bat_watts=$(awk -v v="$(cat "$bat/voltage_now")" -v i="$(cat "$bat/current_now")" 'BEGIN {printf "%.1f", v * i / 1e12}')
fi

jq -n \
    --arg label "$label" \
    --arg captured "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
    --arg vendor "$(dmi sys_vendor)" --arg product "$(dmi product_name)" --arg product_version "$(dmi product_version)" \
    --arg bios "$(dmi bios_version)" --arg bios_date "$(dmi bios_date)" \
    --arg cpu "$(grep -m1 'model name' /proc/cpuinfo | cut -d: -f2 | xargs)" \
    --argjson cores "$(lscpu -p=CORE 2>/dev/null | grep -v '^#' | sort -u | wc -l)" \
    --argjson threads "$(nproc --all)" \
    --arg governor "$(first /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor)" \
    --arg epp "$(first /sys/devices/system/cpu/cpu0/cpufreq/energy_performance_preference)" \
    --arg pstate "$(first /sys/devices/system/cpu/amd_pstate/status)" \
    --argjson mem_kib "$(awk '/MemTotal/ {print $2}' /proc/meminfo)" \
    --argjson avail_kib "$(awk '/MemAvailable/ {print $2}' /proc/meminfo)" \
    --arg vram "$(first "$gpu_dev/mem_info_vram_total")" --arg gtt "$(first "$gpu_dev/mem_info_gtt_total")" \
    --arg gpu_pci "$(first "$gpu_dev/device")" --arg gpu_rev "$(first "$gpu_dev/revision")" \
    --arg os "$(. /etc/os-release && echo "$PRETTY_NAME")" --arg kernel "$(uname -r)" \
    --arg mesa "$mesa" --arg llama_version "$llama_version" --arg devices "$devices" \
    --arg ac "$ac" --arg profile "$(first /sys/firmware/acpi/platform_profile)" \
    --arg bat_state "$(first "$bat/status")" --argjson bat_watts "$bat_watts" \
    --arg load "$(cut -d' ' -f1 /proc/loadavg)" \
    '{
      label: $label, captured: $captured,
      system: {vendor: $vendor, product: $product, product_version: $product_version, bios: $bios, bios_date: $bios_date},
      cpu: {model: $cpu, cores: $cores, threads: $threads, governor: $governor, epp: $epp, amd_pstate: $pstate},
      memory: {total_gib: ($mem_kib / 1048576 * 10 | round / 10), available_gib: ($avail_kib / 1048576 * 10 | round / 10)},
      gpu: {pci_device: $gpu_pci, revision: $gpu_rev,
            vram_reserve_mib: (if $vram == "unknown" then null else ($vram | tonumber / 1048576) end),
            gtt_mib: (if $gtt == "unknown" then null else ($gtt | tonumber / 1048576) end)},
      software: {os: $os, kernel: $kernel, mesa_vulkan_drivers: $mesa, llama_cpp: $llama_version,
                 devices: ($devices | split("\n") | map(select(length > 0)))},
      power: {ac_online: ($ac == "1"), platform_profile: $profile, battery: $bat_state, battery_watts: $bat_watts},
      load_average_1m: ($load | tonumber)
    }'
