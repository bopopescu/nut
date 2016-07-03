
2. add sku table (model)
1. add sku_attributes field (ListObjectField)
ALTER TABLE `core`.`core_entity` 
ADD COLUMN `sku_attributes` LONGTEXT NULL AFTER `status`;