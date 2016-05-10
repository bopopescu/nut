


SELECT `core_entity_like`.`id`, `core_entity_like`.`entity_id`, `core_entity_like`.`user_id`, `core_entity_like`.`created_time` FROM `core_entity_like` WHERE `core_entity_like`.`user_id` = 412916  ORDER BY `core_entity_like`.`created_time` DESC

SELECT `core_entity_like`.`entity_id` FROM `core_entity_like` INNER JOIN `core_entity` ON ( `core_entity_like`.`entity_id` = `core_entity`.`id` ) WHERE (`core_entity`.`status` >= -1  AND `core_entity_like`.`user_id` = 412916 ) ORDER BY `core_entity_like`.`created_time` DESC

SELECT `core_entity`.`id`, `core_entity`.`user_id`, `core_entity`.`entity_hash`, `core_entity`.`category_id`, `core_entity`.`brand`, `core_entity`.`title`, `core_entity`.`intro`, `core_entity`.`rate`, `core_entity`.`price`, `core_entity`.`mark`, `core_entity`.`images`, `core_entity`.`created_time`, `core_entity`.`updated_time`, `core_entity`.`status` FROM `core_entity` INNER JOIN `core_buy_link` ON ( `core_entity`.`id` = `core_buy_link`.`entity_id` )
WHERE (`core_entity`.`category_id` = 74 AND `core_entity`.`status` >= 0 AND NOT (`core_entity`.`id` = 1588669 ) AND `core_buy_link`.`status` = 2 ) ORDER BY `core_entity`.`created_time` DESC LIMIT 90


1. add entity status to index

alter table core_entity add index entity_status_single_index (status);
alter table core_entity add index entity_id_status_combin_index (id, status)

