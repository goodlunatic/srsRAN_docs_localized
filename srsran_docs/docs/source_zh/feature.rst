.. _feature_list:

srsRAN 功能特性
---------------

srsUE
*****

srsUE 是一个完全以软件实现的 4G LTE 和 5G NR UE modem。它作为标准 Linux-based operating system 上的应用运行，可连接任意 LTE 或 5G NR network，并提供标准 network interface 以及高速移动连接能力。

SRS UE 包含以下特性：

- LTE Release 10，并兼容直到 Release 15 的特性
- 支持 5G NSA 和 SA
- 支持 TDD 和 FDD 配置
- 已测试带宽：1.4、3、5、10、15 和 20 MHz
- Transmission mode 1（single antenna）、2（transmit diversity）、3（CCD）和 4（closed-loop spatial multiplexing）
- 可手动配置的 DL/UL carrier frequency
- 支持 XOR/Milenage authentication 的 Soft USIM
- 通过 PC/SC 支持 Hard USIM
- 支持 Snow3G 和 AES integrity/ciphering
- 集成 Linux OS 的 TUN virtual network kernel interface
- 细粒度 log system，支持逐层 log level 和 hex dump
- MAC 和 NAS layer 的 Wireshark packet capture
- 命令行 trace metrics
- 详细的输入配置文件
- 支持 Evolved Multimedia Broadcast and Multicast Service (eMBMS)
- 基于频域的 ZF 和 MMSE equalizer
- 高度优化的 Turbo Decoder，可用于 Intel SSE4.1/AVX2（+150 Mbps）
- 面向 EPA、EVA 和 ETU 3GPP channel 的 channel simulator
- 支持 QoS
- 在 20 MHz MIMO TM3/TM4 或 2xCA 配置下支持 150 Mbps DL（QAM256 下可达 195 Mbps）
- 在 20 MHz SISO 配置下支持 75 Mbps DL（QAM256 下可达 98 Mbps）
- 在 10 MHz SISO 配置下支持 36 Mbps DL
- 支持 Ettus USRP B2x0/X3x0 family、BladeRF、LimeSDR
