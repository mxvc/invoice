# 说明

电子发票解析工具，标准发票pdf格式

https://fp.zzutil.com/
解析结果

![截图](doc/img.png)

# 开发笔记

## 原理

主要是解析发票二维码，得到大部分信息，但缺少总金额

总金额的获取：查找和价税合计同一行的数字

## 乱码

有些pdf使用了内嵌字体，使用 PyMuPDF 时出现乱码，查了下没有很好的解决方法。换成 pdfplumber解决问题

## 发票版式

https://inv-veri.chinatax.gov.cn/fpcs/fpbs.html

## 发票编码

https://zhuanlan.zhihu.com/p/633025591

第2个属性值，表示发票种类代码，不同类型发票值如下。

- 01增值税专用发票
- 04增值税普通发票
- 10增值税普通发票（电子）
- 08增值税专用发票（电子）