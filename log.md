# 此文档用于记录进度 #

## 9月20日 ##

1. 讨论前后端实现方案，确定使用前后端分离方式，其中
	1. 后端使用json返回数据，前端采用url方式提供参数
	2. 前端通过轮询方式进行滚动展示
	3. 后端采用django+SQLite驱动，大部分运算采用数据库运算
	4. html跳转由前端实现
2. json已全部导入数据库

--TODO：

1. 按讨论逻辑编写api
2. 创建git页面进行代码管理和分享
3. 测试login/logout/register功能
	1. 利用login后logout，检查cookie和response情况




editor：Wh1isper


## 10月28日 ##

创建了dev分支进行版本控制，准备第一次迭代

editor：Wh1isper


## 11月6日 ##

login,count,item测试通过

filter存在after/before错误，正在定位

报警API搭建完成，思考报警的项目

验证码模块搭建完成，等待中文验证码api(@wcz)

editor：Wh1isper