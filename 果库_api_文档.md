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

## 关于图片
* 原图地址:
	* http://imgcdn.guoku.com/images/3dc91064fddd31cdfeecb3a12c26d963.jpg  
	* resize 图片方法：
		* http://imgcdn.guoku.com/images/800/3dc91064fddd31cdfeecb3a12c26d963.jpg   // 800 x 800
		* http://imgcdn.guoku.com/images/310/3dc91064fddd31cdfeecb3a12c26d963.jpg   // 310 x 310
		
## API 列表

* 系统参数：

	参数 		 | 类型			  |  是否必须
	------------ | ------------- | ------------
	api_key 	 | string  		  | 必须
	sign 		 | string  		  | 必须
	session 	 | string 		  | 不是必须

* 获取精选列表
	* http://api.guoku.com/mobile/v4/selection/
	* 方法： GET
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
	* 方法： GET
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
	* 方法： GET
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
	
*  获取分类统计数据
	* http://api.guoku.com/mobile/v4/category/42/stat/
	* 方法 GET
	* 参数：
		* category_id 分类ID (/mobile/v4/category/<category_id>/stat/)
	* 返回:
	
	```
	{
		like_count: 0,  // 传入 session 后会有该值
		entity_count: 95, // 分类下商品数量
		entity_note_count: 232 // 分类下点评数量
	}
	```
	
*  获取商品列表
	* http://api.guoku.com/mobile/v4/category/42/entity/
	* 方法: GET
	* 参数: 
		* category_id 分类ID (/mobile/v4/category/<category_id>/entity/
		* offset 偏移量
		* count  请求的个数
	* 返回：
	
	```
	[
		{
			detail_images: [
				"http://img01.taobaocdn.com/imgextra/i1/101402877/TB2XqncaXXXXXbuXpXXXXXXXXXX_!!101402877.jpg",
				"http://img04.taobaocdn.com/imgextra/i4/101402877/TB2iLPbaXXXXXa0XpXXXXXXXXXX_!!101402877.jpg",
				"http://img01.taobaocdn.com/imgextra/i1/101402877/TB2HmnfaXXXXXbjXXXXXXXXXXXX_!!101402877.jpg",
				"http://img02.taobaocdn.com/imgextra/i2/101402877/TB2cbLdaXXXXXaAXpXXXXXXXXXX_!!101402877.jpg"
			],
			entity_id: 1439745,
			price: "1980.00",
			like_count: 113,
			created_time: 1415776343,
			chief_image: "http://img01.taobaocdn.com/bao/uploaded/i1/TB1dDggFVXXXXXUaXXXXXXXXXXX_!!0-item_pic.jpg", // 商品主图
			entity_hash: "d1e017ea",
			item_list: [  // 商品购买信息
				{
					entity_id: "1439745",
					buy_link: "http://h.guoku.com/mobile/v4/item/40576715722/?type=mobile",
					cid: "50012100",
					default: "True",
					price: 1980,
					origin_source: "taobao.com",
					rank: "0",
					volume: "0",
					origin_id: "40576715722",
					id: "10851"
				}
			],
			title: "球形马达吸尘器",
			mark: "0",
			total_score: 0,
			brand: "DYSON",
			status: "1",
			note_count: 2,
			item_id_list: [
				"54c21867a2128a0711d970da"
			],
			like_already: 0,
			updated_time: 1415776343,
			creator_id: 68310,
			intro: "",
			category_id: "42"
		}, .......
	]
	```


		