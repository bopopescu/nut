1. 文章内容(table.field : core_article.content )中存在商品卡片info ，每张卡片的 HTML 如下：

    <div guoku_ele="True" class="guoku-card container-fluid hover-light" data_entity_hash="b4bad50b"> 
    ==================
    guoku_entity_hash 对应单件商品的  hash

2. 每次文章保存时需要 提取 文章中的 所有卡片， 建立商品和文章的 M2M 关系


3. add field to Article Model 

4.  syncdb will not create new related tabel , we must add it by hand
    so add table by hand 
    
    
CREATE TABLE `core_article_related_entities` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `article_id` integer NOT NULL,
    `entity_id` integer NOT NULL,
    UNIQUE (`article_id`, `entity_id`)
);
ALTER TABLE `core_article_related_entities` ADD CONSTRAINT `entity_id_refs_id_8f4ed529` FOREIGN KEY (`entity_id`) REFERENCES `core_entity` (`id`);
ALTER TABLE `core_article_related_entities` ADD CONSTRAINT `article_id_refs_id_c5544a89` FOREIGN KEY (`article_id`) REFERENCES `core_article` (`id`);


5. change Article save method 

