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
	session生存周期为12小时
	

	保留/register作为注册接口
	保留/init作为json导入数据库接口
	
	"err":1 未知错误 (请检查API是否正确，数据库参数是否正确)
	"err":2 为权限错误（未登入/用户名或密码错误）
	"err":3 为验证码错误
	"err":101 为注册时错误（用户已存在）
	"err":4 方法错误（POST/GET方法错误等）
	"err":5 数据库读取错误

	"success":1或其他返回表示成功

##以下为接口
	
	用户登入功能API接口：用于普通用户登入与鉴权
	路由：/login
	方法：POST
	提交参数：
	parameters:
	    username:
	        用户名
	    password:
	        密码
	    captcha:
	        验证码
	返回参数：
	responses:
	    HTTP返回：200
	    登录成功:
	        json:{“success”: “0”}
	        并在响应头中Set-Cookie
	
	验证码获取API：用于前端获取验证码
	路由：login/check_code
	方法：GET
	responses:
		HTTP返回：200
		返回验证码图片流
	
	分类计数功能API接口：将数据按一定方法进行分类、过滤后返回各个分类下的计数
	路由：/query/count
	方法：GET
	提交参数：
	parameters:
	    first_category:
	        可选值: none(默认),STREET,COMMUNITY,EVENT_TYPE,etc.
	        将要查询的的数据按first_category中指定的分类方法分至不同的类中
	        为none时不进行分类
	    first_category_filter_id:
	        可选值: all(默认) 或 id1,id2
	        对first_category进行过滤，只返回id为id1,id2的数据
	        多个id值以逗号分隔
	        all表示返回此分类下的所有id(即不进行过滤)
	    second_category:
	        可选值: none(默认),STREET,COMMUNITY,EVENT_TYPE,etc.
	        将first_category分类后数据按second_category中指定的分类方法进行二次分类
	        为none时不进行二次分类
	    second_category_filter_id:
	        可选值: all(默认) 或 id1,id2
	        对second_category进行过滤，只返回id为id1,id2的数据
	        多个id值以逗号分隔
	        all表示返回此分类下的所有id(即不进行过滤)
	    time_after:
	        值为形如yyyy-mm-dd的字符串
	        默认值为1970-01-01
	        对数据进行过滤，只返回此日之后(含此日)的数据
	    time_before:
	        值为形如yyyy-mm-dd-hh-mm-ss的字符串
	        默认值为2999-12-31
	        对数据进行过滤，只返回此日之前(不含此日)的数据
		即：[time_after,time_before)的数据
	返回参数：
	responses:
	    HTTP返回：200
	    成功:
	        按分类返回ID与对应数量的键值对，见example
	example:
	/query/count?first_category=STREET
	返回如下：
	        {"100": 123, "101": 456, "102": 789, ...}
	/query/count?first_category=STREET&first_category_filter_id=100,101
	返回如下：
	{"100": 123, "101": 456}
	/query/count?first_category=STREET&second_category=EVENT_PROPERTY
	返回如下：
	        {
	            "100":{
	                "1": 10,
	                "2": 20,
	                "3": 30,
	                "4": 40,
	                "5": 12,
	                "6": 11,
	                "all": 123
	            },
	            "101": { ... },
	            "102": { ... },
	            ...
	        }
	/query/count?first_category=STREET&second_category=EVENT_PROPERTY&second_category_filter_id=1,2,3
	返回如下：
			{
	            "100":{
	                "1": 10,
	                "2": 20,
	                "3": 30,
	                "all": 60
	            },
	            "101": { ... },
	            "102": { ... },
	            ...
	        }
	
	指定事件查询API: 返回某一主键对应事件的详细信息
	路由：/query/item
	方法：GET
	提交参数：
	parameters:
	    REC_ID:
	        整数
	返回参数：
	responses:
	    HTTP返回：200
	    成功:
	        {"REC_ID": 72687, "EVENT_PROPERTY_ID": 5, ...}
	
	
	
	事件过滤API：按一定规则进行过滤后返回所有符合条件的结果，排序后输出
	路由：/query/filter
	方法：GET
	提交参数：
	parameters:
	    sort:
	        time_inc, time_dec, id_inc, id_dec(默认), ...
	    time_after:
	        值为形如yyyy-mm-dd的字符串
	        默认值为1970-01-01
	        对数据进行过滤，只返回此日之后(含此日)的数据
	    time_before:
	        值为形如yyyy-mm-dd-hh-mm-ss的字符串
	        默认值为2999-12-31
	        对数据进行过滤，只返回此日之前(不含此日)的数据
		即：[time_after,time_before)
	    id_after:
	        对主键进行过滤，默认值为-INF
	        只返回主键值为id_after之后(不含id_after)的数据
	    id_before:
	        对主键进行过滤，默认值为+INF
	        只返回主键值为id_before之前(不含id_before)的数据
	    count:
	        返回数据的个数，默认值为20，最大值为100
	    offset:
	        对于排序后的结果，找到id为offset的元素，返回它之后(不含它)count个数据
	        缺省这从第一个开始返回
	返回参数：
	responses:
	    HTTP返回：200
	成功:
		返回符合要求的事件的详细信息
	    
	
	事件报警API：用于出现紧急事件报警
	路由：/warning
	方法：GET
	parameters:
	    time_after:
	        值为形如yyyy-mm-dd的字符串
	        默认值为1970-01-01
	        对数据进行过滤，只返回此日之后(含此日)的数据
	    time_before:
	        值为形如yyyy-mm-dd-hh-mm-ss的字符串
	        默认值为2999-12-31
	        对数据进行过滤，只返回此日之前(不含此日)的数据
		即：[time_after,time_before)的数据
	    id_after:
	        对主键进行过滤，默认值为-INF
	        只返回主键值为id_after之后(不含id_after)的数据
	    id_before:
	        对主键进行过滤，默认值为+INF
	        只返回主键值为id_before之前(不含id_before)的数据
		begin:
			整型，指示从多少条开始，默认值是0
		count:
			整型，指示返回的最多条数，默认值是20
	responses:
	成功：
		返回紧急事件的详细信息
	



