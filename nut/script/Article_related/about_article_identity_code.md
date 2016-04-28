1. 查重系统更新
	1.   抓取系统生成新图文前， 要做查重检查
        2.   检查重复算法，参见 Article model , caculate_identity_code  方法
	3.   只有从外站抓取的文章，入库的时候查重， 参见 guoku_crawler 项目
        4.   需要对原有图文数据做一次性处理，重新计算所有文章的 identity_code （参见 2 ）
        5.   之后进来的微信文章，可以保证不重复了 （即使编辑了题目，因为identity_code 保存了原始文章的题目信息的hash）
        

2. 图文原有数据处理，计算identity_code 操作步骤
        0.  停止文章编辑工作
	1.  备份 core_article 表
	2.  执行 script/Article_related/generate_article_identity_code.py ， 注意 script 中的 settings 指向正确的配置文件
        3.  检查数据库 core_article 表， 如果出问题， 从备份恢复， 调试 2 ， 重新执行
	4.  记录文章库中最新的 article id , 下次执行计算identity_code 可能会用到
         
         

3. 后续工作

	1. 编辑添加的文章，不会有identity_code 
        2. 如果之后编辑修改抓取文章题目， 当再次运行 （重新计算 identity_code 的时候），不用计算之前计算过的文章，否则，修改过题目的文章（来自微信）， 会生成新的identity_code , 下次抓取过来这篇文章，就会重复入库
        3. 所以， 下次执行 计算identity_code 只需要从上次，计算过的地方计算， 并且， 如果一篇文章已经有了 identity_code ， 就不要覆盖！！！！！！

