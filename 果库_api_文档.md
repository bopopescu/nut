# 果库 API 文档 #


**APP_KEY :** 0b19c2b93687347e95c6b6f5cc91bb87 

**APP_Secret :** 47b41864d64bd46


## base url ##
```
http://api.guoku.com/mobile/v4/
```


## 签名算法 ##
* (api_key + 参数 ＋ app_secret) | md5

## 例如

* http://test.guoku.com/mobile/v4/selection/?api_key=0b19c2b93687347e95c6b6f5cc91bb87&count=30&sign=87e59662ec8173df903de9efe078f4f8&timestamp=1428938076.088725
* sign=87e59662ec8173df903de9efe078f4f8 由来
* md5('api_key=0b19c2b93687347e95c6b6f5cc91bb87' ＋ 'count=30' + 'timestamp=1428938076.088725' + app_secret)  = 87e59662ec8173df903de9efe078f4f8 (签名)

**注意：参数先按 key 排序然后加上 app_secret，最后 MD5。 得到 sign**

## API 列表

* 系统参数：

	参数 		 | 类型			  |  是否必须
	------------ | ------------- | ------------
	api_key 	 | string  		  | 必须
	sign 		 | string  		  | 必须
	session 	 | string 		  | 不是必须

* 获取精选列表
	* http://api.guoku.com/mobile/v4/selection/
	* 参数：
		* timestamp 时间戳
		* count     请求的个数
	* 返回:
	
	```
	[
		{
			content: {
				note: {
					creator:{}, // post 用户
				},   // 精选点评
				entity: {}, // 精选商品
			},
			post_time: 1428931440,  // post 时间戳 
			type: "note_selection",
		},
	]
	```
	
* 获取商品详细
	* http://api.guoku.com/mobile/v4/entity/1458215/
	* 参数：
		* entity_id 商品 ID (/mobile/v4/entity/<entity_id>/)
		
	* 返回：	
	
	```
	{
		like_user_list: [], 用户喜欢列表
		note_list: [], 点评列表
		entity: {}, 商品详情
	}
	```
	
* 获取全部分类信息
	* http://api.guoku.com/mobile/v4/category/
	* 返回：
	
	```
	[
		status: 1,
		content: [
			{
				status: 0,
				category_id: 388,
				category_title: "咖啡滤纸",
			}, 
			{
				status: 1,
				category_id: 150,
				category_icon_small: "http://imgcdn.guoku.com/category/small/69b9c24704d8414d33ce44de2603cacb",
				category_title: "牙签筒",
				category_icon_large: "http://imgcdn.guoku.com/category/large/69b9c24704d8414d33ce44de2603cacb"
			}, .....
		],  // 子分类信息
		group_id: 41,
		title: "餐具水具"
	]
	```
		