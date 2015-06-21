Change Log
==========

### Ver 2.2.2


1. **core_buy_link** 表增加 **is_soldout** 字段。
2. 优化 **nickname** 的显示 


### 注：

```
ALTER TABLE core_buy_link ADD COLUMN is_soldout BOOL NOT NULL DEFAULT 0
```



