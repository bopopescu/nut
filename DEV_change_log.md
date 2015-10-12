8. view optimize : use selected_related , prefetch_related to reduce sql hits.

7. block ISP ad injection

6. 更新 ariticle api , html_unescape article content , before sent to client 

5. 保存文章的时候提取相关商品列表保存

4. Article model 加入related_entities m2m 字段 (需要执行 SQL 语句)
   CREATE TABLE `core_article_related_entities` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `article_id` integer NOT NULL,
    `entity_id` integer NOT NULL,
    UNIQUE (`article_id`, `entity_id`)
    );
    ALTER TABLE `core_article_related_entities` ADD CONSTRAINT `entity_id_refs_id_8f4ed529` FOREIGN KEY (`entity_id`) REFERENCES `core_entity` (`id`);
    ALTER TABLE `core_article_related_entities` ADD CONSTRAINT `article_id_refs_id_c5544a89` FOREIGN KEY (`article_id`) REFERENCES `core_article` (`id`);
    
    详情见 ： 日常开发文档／图文／文章 related entity.MD
    

3. 新增前台，标签 文章列表页
2. 文章列表页顶部加入置顶标签显示
1. 后台标签管理增加 置顶文章标签功能 
    
    (需要手动执行 SQL 语句)
    
    详情见 ： 日常开发文章／tag／实现 文章 tag 置顶 功能.MD

    ALTER TABLE `core`.`tag_tags` 
    ADD COLUMN `isTopArticleTag` TINYINT(1) NOT NULL DEFAULT 0 AFTER `image`;
   
    
=== 2015-10-10 =====  start ===========================