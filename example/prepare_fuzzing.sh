#!/bin/bash

### use root permission if necessary

echo core >/proc/sys/kernel/core_pattern
cd /sys/devices/system/cpu
echo performance | tee cpu*/cpufreq/scaling_governor

# disable ASLR
echo 0 | tee /proc/sys/kernel/randomize_va_space
