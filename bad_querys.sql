


SELECT `core_entity_like`.`id`, `core_entity_like`.`entity_id`, `core_entity_like`.`user_id`, `core_entity_like`.`created_time` FROM `core_entity_like` WHERE `core_entity_like`.`user_id` = 412916  ORDER BY `core_entity_like`.`created_time` DESC

SELECT `core_entity_like`.`entity_id` FROM `core_entity_like` INNER JOIN `core_entity` ON ( `core_entity_like`.`entity_id` = `core_entity`.`id` ) WHERE (`core_entity`.`status` >= -1  AND `core_entity_like`.`user_id` = 412916 ) ORDER BY `core_entity_like`.`created_time` DESC