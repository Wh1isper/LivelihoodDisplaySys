# Usage #

    pip install django
	python manage.py runserver 8000

默认情况下使用localhost:8000 可以修改上述端口

    /login 为登入接口，接收post
	{
		"username":"",
		"password":""
	}
	将setCookie['username']

	/logout 为登出接口，将删除cookie
	

	保留/register作为注册接口
	保留/init作为json导入数据库接口
	
	"err":'0'未知错误（如查找的键不存在）
	"err":'1'为权限错误（未登入）
	"err":'2'为注册时错误（用户已存在）
	"err":'3'方法错误