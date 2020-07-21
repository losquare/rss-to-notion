## 关于 

本脚本将根据规则采集 RSS 并填充至 notion 指定 Url 中 的 指定格式的 table 内 。



***由于是自用的代码， 难免存在疏漏 ，敬请谅解 。***



## 如何使用

为了使用本脚本,

您首先需要设置正确的 table 格式：

> ​	一个名称为 标题 的 text 或者 title
>
> ​	一个名称为 链接 的 Url
>
> ​	一个名称为 来源 的 text

其他随意

( 当然您也可以修改代码来实现不同的格式 )

附上作者的 table 样式作为参考





![2020-07-18_195203](https://pic.90wish.ru/2020/07/21/5f16d9c56c851.png)



其次您需要在 config.py 中填入您的 token_v2 和 tableUrl 。

token_v2 可以在浏览器 cookie 中获取 。

tableUrl 可以在 notion 界面中 右键 Copylink 获取 。





## 关于规则文件

所有的规则在 ./rules 文件夹下 。 

您可以自己编写规则：

```
来源类型(填写 informationFlow 或者 traditional )
来源名称
RSS 地址
是否开启筛选 (填写 on 或者 off)
筛选关键字(不同的关键字之间请用逗号隔开)
```

注：如果您的来源是 微博，推特等 推荐使用 informationFlow ，传统网站请使用 traditional 。

​		informationFlow : 将会读取 RSS 中的 description 并截取前 90 字 作为标题 。

​		traditional : 将会读取 RSS 中的 title 作为标题 。

​		由于程序将按行号读取规则文件，请严格按行填写规则文件 。

​		请给每个规则文件设置不一样的文件名,否则可能出现不可预料的错误 ! ! !



## 关于 Cache

Cache 目录 存储了 当前规则文件抓取的 Url 历史 以确保不会抓取重复的内容 。

Cache文件的名称与规则名称相同 。

在必要时您可以修改或删除对应的 Cache 文件来达成相关目的 。



## 已知的的问题

当前版本 检查抓取到的数据是否重复 的逻辑并不友好，尽管尚未有该问题影响使用的报告，该问题可能在将来被修正。