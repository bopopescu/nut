1.  测试环境中 Entity_Like 数量比较少
    日期靠前。 popular_random method中, 样本数量太少
    random.sample()出现样本小于取样数的错误。

2.  本地测试解决方案
    a.) 倒入500000个 entity_like
    b.) 判断是否测试环境   method isTestEnv
    c.) 如果是， 设置筛选时间范围为 70天
    d.) 如果样本数仍然小于 取样数 ， 直接返回所有样本
    
//TODO
3. 仍然需要确认， 生产环境，不受影响。

  