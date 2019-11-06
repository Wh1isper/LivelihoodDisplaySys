# Usage #

    pip install django
	python manage.py runserver 8000

默认情况下使用localhost:8000 可以修改上述端口

    /login 为登入接口，接收post
	{
		"username":"",
		"password":"",
		"captcha":""
	}
	利用session访问

	/logout 为登出接口，将删除session
	session生存周期为1天
	

	保留/register作为注册接口
	保留/init作为json导入数据库接口
	
	"err":1 未知错误 (请检查API是否正确，数据库参数是否正确)
	"err":2 为权限错误（未登入/用户名或密码错误）
	"err":3 为验证码错误
	"err":101 为注册时错误（用户已存在）
	"err":4 方法错误（POST/GET方法错误等）
	"err":5 数据库读取错误

	"success":1或其他返回表示成功
