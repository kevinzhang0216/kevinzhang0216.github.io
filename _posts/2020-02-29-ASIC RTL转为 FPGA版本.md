---
layout:     post
title:      FPGA的ASIC原型验证实践002
subtitle:   ASIC RTL转为FPGA版本
date:       2020-02-29
author:     KevinZhang
header-img: img/post-bg-coffee.jpeg
catalog: true
tags:
    - ASIC原型验证
    - FPGA
---

## 1. 前言
最近公司买了两个FPGA原型验证平台：S2C和HAPS，这两个平台均使用Xilinx VU440，在转为FPGA的代码上有一定的区别，但基本思路基本相同，本文介绍一下ASIC RTL转为FPGA版本的注意点。

## 2. ASIC设计转为FGPA设计
### 2.1 ASIC设计转为FPGA设计的准备
在ASIC代码转为FPGA代码前，主要有如下的设计必须被替换或重新编辑。
1. AISC的门控时钟和时钟资源在FPGA中不适用。
2. ASIC的memories
3. Latches和异步延时
4. ASIC的模拟模块
5. IO端口

#### 将ASIC设计转移到FPGA的一般准则
1. ASIC结构不容易转换为FPGA结构
   1. latch
   2. AISC的memory
   3. 门控时钟
   4. 复杂的生成时钟
   5. 时钟多路复用器
   6. 顶层的IO pad
   7. 模拟模块需要连接到外部电路
   8. BIST
2. 避免latch
3. 避免组合逻辑环
4. 为了确保ASIC RTL可移植到FPGA，不要在原始RTL中包含诸如时钟选通、测试插入和低功耗等优化。相反，将优化留给Soc工具，并尽可能保持RTL的纯净
5. 使用'define和'ifdef包括或删除原型设计的代码。使用这些结构来隔离BIST、内存实例化等
6. 在SOC和FPGA间分享make files
7. 使用Wrappers来更改以避免ASIC RTL改变带来的影响，尽量替换文件而不是更改文件

### 2.2 分割设计
ASIC设计比FPGA设计要大得多，通常在多个FPGA上划分为多个分区。专设一章介绍。

### 2.3 处理IO PAD
更改顶层，让工具自己推断。

### 2.4 转换ASIC的Memories
ASIC存储器通常比通常在FPGA中实现的FPGA存储器要大得多、复杂得多。
1. 根据设计需求转化FPGA的BRAM
2. 运行逻辑综合：软件自动从RTL中推断RAMs
3. 检查结果
   1. 是否超出了容量
   2. 查看log文件是否推断正确
   
#### 转化ASIC Memory的几个方法
1. 去掉原型验证不需要的ASIC存储器，以减少空间
2. 尽可能用等效的FPGA模型替换ASIC存储器
3. 用HDL code实例化存储器，软件可以推断出来。使用不同的Wrappers，一个是ASIC，另一个是FPGA
4. 将测试和电源引脚忽视掉或者写为常数
5. 在使用前，充分测试FPGA存储器的行为级模型

#### 容量大的Memory的设计方法
1. 尽可能映射大的存储器到FPGA中
2. 如果复杂的存储器太大了不能放进FPGA中，使用DDR3、DDR4
3. 创建两个RTL Wrapper，一个是FPGA原型，另一个ASIC。

### 2.5 转换AISC的时钟
ASIC时钟通常相当复杂，有许多时钟是平衡的，使用时钟树合成来避免时钟偏移。FPGA具有由软件编程的有限数量的低偏斜全局时钟BUFG，并且具有异步时钟域或为低功耗而选通的域。ASIC的时钟必须转换为适应FPGA架构的方式。
#### ASIC时钟转化的设计方法
1. 简化时钟网络
   1. 避免时钟路径上的扫描和测试逻辑；
   2. 有必要保留mux的复用逻辑，使用BUFGMUX原语替换。
   3. 用MMCM资源替换ASIC的PLL
2. 同步设计复位和MMCM lock信号
   1. 不同MMCM的锁定时间不能保证同时发生。建议轮询设计中所有MMCM的锁定信号以及锁定信号，然后使用此结果为整个设计创建延迟上电主复位
   2. 建议使用单独的复位来控制MMCM。此复位必须与上面讨论的主复位不同，用于将时钟复位电路与设计复位分离


### 2.6 检查资源使用
1. 运行综合
   1. 第一次评估，运行快速综合策略
   2. 对于优化设计，用正常综合策略
2. 检查资源使用量，IO、LUT、FF、Memory、Clock
3. 如果使用量超过，使用register resources替换来实现memories


## 3. 总结
本文主要介绍了ASIC转为FPGA原型验证版本中需要更改的项目(IO、时钟资源、memory)的修改方法以及设计和验证的一般方法，经过验证此方法可以快速将ASIC版本转为FPGA原型验证的版本。

## 4. 参考资料
1. 《protocompiler_user_guide.pdf》
2. [](https://ninghechuan.com/2019/10/03/2019-10-3-%E4%BD%A0%E8%A6%81%E7%9A%84FPGA&%E6%95%B0%E5%AD%97%E5%89%8D%E7%AB%AF%E7%AC%94%E9%9D%A2%E8%AF%95%E9%A2%98%E9%83%BD%E5%9C%A8%E8%BF%99%E5%84%BF%E4%BA%86/)