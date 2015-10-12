BEGIN;
CREATE TABLE `core_gkuser_groups` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `gkuser_id` integer NOT NULL,
    `group_id` integer NOT NULL,
    UNIQUE (`gkuser_id`, `group_id`)
)
;
ALTER TABLE `core_gkuser_groups` ADD CONSTRAINT `group_id_refs_id_a8c0eb2d` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);
CREATE TABLE `core_gkuser_user_permissions` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `gkuser_id` integer NOT NULL,
    `permission_id` integer NOT NULL,
    UNIQUE (`gkuser_id`, `permission_id`)
)
;
ALTER TABLE `core_gkuser_user_permissions` ADD CONSTRAINT `permission_id_refs_id_079bfc3a` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`);
CREATE TABLE `core_gkuser` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `password` varchar(128) NOT NULL,
    `last_login` datetime NOT NULL,
    `is_superuser` bool NOT NULL,
    `email` varchar(255) NOT NULL UNIQUE,
    `is_active` integer NOT NULL,
    `is_admin` bool NOT NULL,
    `date_joined` datetime NOT NULL
)
;
ALTER TABLE `core_gkuser_groups` ADD CONSTRAINT `gkuser_id_refs_id_6fa84be8` FOREIGN KEY (`gkuser_id`) REFERENCES `core_gkuser` (`id`);
ALTER TABLE `core_gkuser_user_permissions` ADD CONSTRAINT `gkuser_id_refs_id_b4c68d59` FOREIGN KEY (`gkuser_id`) REFERENCES `core_gkuser` (`id`);
CREATE TABLE `core_user_profile` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` integer NOT NULL UNIQUE,
    `nickname` varchar(64) NOT NULL,
    `location` varchar(32),
    `city` varchar(32),
    `gender` varchar(2) NOT NULL,
    `bio` varchar(1024),
    `website` varchar(1024),
    `avatar` varchar(255) NOT NULL,
    `email_verified` bool NOT NULL
)
;
ALTER TABLE `core_user_profile` ADD CONSTRAINT `user_id_refs_id_2d69357d` FOREIGN KEY (`user_id`) REFERENCES `core_gkuser` (`id`);
CREATE TABLE `core_user_follow` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `follower_id` integer NOT NULL,
    `followee_id` integer NOT NULL,
    `followed_time` datetime NOT NULL,
    UNIQUE (`follower_id`, `followee_id`)
)
;
ALTER TABLE `core_user_follow` ADD CONSTRAINT `follower_id_refs_id_179b1a63` FOREIGN KEY (`follower_id`) REFERENCES `core_gkuser` (`id`);
ALTER TABLE `core_user_follow` ADD CONSTRAINT `followee_id_refs_id_179b1a63` FOREIGN KEY (`followee_id`) REFERENCES `core_gkuser` (`id`);
CREATE TABLE `core_banner` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `content_type` varchar(64) NOT NULL,
    `key` varchar(1024) NOT NULL,
    `image` varchar(64) NOT NULL,
    `created_time` datetime NOT NULL,
    `updated_time` datetime NOT NULL
)
;
CREATE TABLE `core_show_banner` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `banner_id` integer NOT NULL UNIQUE,
    `created_time` datetime NOT NULL
)
;
ALTER TABLE `core_show_banner` ADD CONSTRAINT `banner_id_refs_id_d8073954` FOREIGN KEY (`banner_id`) REFERENCES `core_banner` (`id`);
CREATE TABLE `core_sidebar_banner` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `image` varchar(255) NOT NULL,
    `created_time` datetime NOT NULL,
    `updated_time` datetime NOT NULL,
    `link` varchar(255) NOT NULL,
    `position` integer NOT NULL,
    `status` integer NOT NULL
)
;
CREATE TABLE `core_category` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `title` varchar(128) NOT NULL,
    `cover` varchar(255) NOT NULL,
    `status` bool NOT NULL
)
;
CREATE TABLE `core_sub_category` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `group_id` integer NOT NULL,
    `title` varchar(128) NOT NULL,
    `alias` varchar(128) NOT NULL,
    `icon` varchar(64),
    `status` bool NOT NULL
)
;
ALTER TABLE `core_sub_category` ADD CONSTRAINT `group_id_refs_id_97180265` FOREIGN KEY (`group_id`) REFERENCES `core_category` (`id`);
CREATE TABLE `core_brand` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(100) NOT NULL UNIQUE,
    `alias` varchar(100),
    `icon` varchar(255),
    `company` varchar(100),
    `website` varchar(255),
    `tmall_link` varchar(255),
    `national` varchar(100),
    `intro` longtext NOT NULL,
    `status` integer NOT NULL,
    `created_date` datetime NOT NULL
)
;
CREATE TABLE `core_entity` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` integer,
    `entity_hash` varchar(32) NOT NULL UNIQUE,
    `category_id` integer NOT NULL,
    `brand` varchar(256) NOT NULL,
    `title` varchar(256) NOT NULL,
    `intro` longtext NOT NULL,
    `rate` numeric(3, 2) NOT NULL,
    `price` numeric(20, 2) NOT NULL,
    `mark` integer NOT NULL,
    `images` longtext NOT NULL,
    `created_time` datetime NOT NULL,
    `updated_time` datetime NOT NULL,
    `status` integer NOT NULL
)
;
ALTER TABLE `core_entity` ADD CONSTRAINT `category_id_refs_id_782af7be` FOREIGN KEY (`category_id`) REFERENCES `core_sub_category` (`id`);
ALTER TABLE `core_entity` ADD CONSTRAINT `user_id_refs_id_81348919` FOREIGN KEY (`user_id`) REFERENCES `core_gkuser` (`id`);
CREATE TABLE `core_selection_entity` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `entity_id` integer NOT NULL UNIQUE,
    `is_published` bool NOT NULL,
    `pub_time` datetime NOT NULL
)
;
ALTER TABLE `core_selection_entity` ADD CONSTRAINT `entity_id_refs_id_d0aa8b2e` FOREIGN KEY (`entity_id`) REFERENCES `core_entity` (`id`);
CREATE TABLE `core_buy_link` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `entity_id` integer NOT NULL,
    `origin_id` varchar(100) NOT NULL,
    `origin_source` varchar(255) NOT NULL,
    `cid` varchar(255),
    `link` varchar(255) NOT NULL,
    `price` numeric(20, 2) NOT NULL,
    `foreign_price` numeric(20, 2) NOT NULL,
    `volume` integer NOT NULL,
    `rank` integer NOT NULL,
    `default` bool NOT NULL,
    `shop_link` varchar(255),
    `seller` varchar(255),
    `status` integer UNSIGNED NOT NULL
)
;
ALTER TABLE `core_buy_link` ADD CONSTRAINT `entity_id_refs_id_73f6b4fa` FOREIGN KEY (`entity_id`) REFERENCES `core_entity` (`id`);
CREATE TABLE `core_entity_like` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `entity_id` integer NOT NULL,
    `user_id` integer NOT NULL,
    `created_time` datetime NOT NULL,
    UNIQUE (`entity_id`, `user_id`)
)
;
ALTER TABLE `core_entity_like` ADD CONSTRAINT `user_id_refs_id_80516781` FOREIGN KEY (`user_id`) REFERENCES `core_gkuser` (`id`);
ALTER TABLE `core_entity_like` ADD CONSTRAINT `entity_id_refs_id_0f8a96e5` FOREIGN KEY (`entity_id`) REFERENCES `core_entity` (`id`);
CREATE TABLE `core_note` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` integer NOT NULL,
    `entity_id` integer NOT NULL,
    `note` longtext,
    `post_time` datetime NOT NULL,
    `updated_time` datetime NOT NULL,
    `status` integer NOT NULL
)
;
ALTER TABLE `core_note` ADD CONSTRAINT `user_id_refs_id_8449289d` FOREIGN KEY (`user_id`) REFERENCES `core_gkuser` (`id`);
ALTER TABLE `core_note` ADD CONSTRAINT `entity_id_refs_id_a30c4b02` FOREIGN KEY (`entity_id`) REFERENCES `core_entity` (`id`);
CREATE TABLE `core_note_comment` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `note_id` integer NOT NULL,
    `user_id` integer NOT NULL,
    `content` longtext NOT NULL,
    `replied_comment_id` integer,
    `replied_user_id` integer,
    `post_time` datetime NOT NULL
)
;
ALTER TABLE `core_note_comment` ADD CONSTRAINT `user_id_refs_id_b2384386` FOREIGN KEY (`user_id`) REFERENCES `core_gkuser` (`id`);
ALTER TABLE `core_note_comment` ADD CONSTRAINT `note_id_refs_id_626e3de7` FOREIGN KEY (`note_id`) REFERENCES `core_note` (`id`);
CREATE TABLE `core_note_poke` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `note_id` integer NOT NULL,
    `user_id` integer NOT NULL,
    `created_time` datetime NOT NULL,
    UNIQUE (`note_id`, `user_id`)
)
;
ALTER TABLE `core_note_poke` ADD CONSTRAINT `user_id_refs_id_dc55d470` FOREIGN KEY (`user_id`) REFERENCES `core_gkuser` (`id`);
ALTER TABLE `core_note_poke` ADD CONSTRAINT `note_id_refs_id_17f499d9` FOREIGN KEY (`note_id`) REFERENCES `core_note` (`id`);
CREATE TABLE `core_sina_token` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` integer NOT NULL UNIQUE,
    `sina_id` varchar(64),
    `screen_name` varchar(64),
    `access_token` varchar(255),
    `create_time` datetime NOT NULL,
    `expires_in` integer UNSIGNED NOT NULL,
    `updated_time` datetime
)
;
ALTER TABLE `core_sina_token` ADD CONSTRAINT `user_id_refs_id_d4318613` FOREIGN KEY (`user_id`) REFERENCES `core_gkuser` (`id`);
CREATE TABLE `core_taobao_token` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` integer NOT NULL UNIQUE,
    `taobao_id` varchar(64),
    `screen_name` varchar(64),
    `access_token` varchar(255),
    `refresh_token` varchar(255),
    `open_uid` varchar(64),
    `isv_uid` varchar(64),
    `create_time` datetime NOT NULL,
    `expires_in` integer UNSIGNED NOT NULL,
    `re_expires_in` integer UNSIGNED NOT NULL,
    `updated_time` datetime
)
;
ALTER TABLE `core_taobao_token` ADD CONSTRAINT `user_id_refs_id_7a3a4fc6` FOREIGN KEY (`user_id`) REFERENCES `core_gkuser` (`id`);
CREATE TABLE `core_wechat_token` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` integer NOT NULL UNIQUE,
    `unionid` varchar(255) NOT NULL,
    `nickname` varchar(255) NOT NULL,
    `updated_time` datetime
)
;
ALTER TABLE `core_wechat_token` ADD CONSTRAINT `user_id_refs_id_ee5d502d` FOREIGN KEY (`user_id`) REFERENCES `core_gkuser` (`id`);
CREATE TABLE `core_article_related_entities` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `article_id` integer NOT NULL,
    `entity_id` integer NOT NULL,
    UNIQUE (`article_id`, `entity_id`)
)
;
ALTER TABLE `core_article_related_entities` ADD CONSTRAINT `entity_id_refs_id_8f4ed529` FOREIGN KEY (`entity_id`) REFERENCES `core_entity` (`id`);
CREATE TABLE `core_article` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `creator_id` integer NOT NULL,
    `title` varchar(64) NOT NULL,
    `cover` varchar(255) NOT NULL,
    `content` longtext NOT NULL,
    `publish` integer NOT NULL,
    `created_datetime` datetime,
    `updated_datetime` datetime NOT NULL,
    `showcover` bool NOT NULL,
    `read_count` integer NOT NULL
)
;
ALTER TABLE `core_article` ADD CONSTRAINT `creator_id_refs_id_da1c21b1` FOREIGN KEY (`creator_id`) REFERENCES `core_gkuser` (`id`);
ALTER TABLE `core_article_related_entities` ADD CONSTRAINT `article_id_refs_id_c5544a89` FOREIGN KEY (`article_id`) REFERENCES `core_article` (`id`);
CREATE TABLE `core_selection_article` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `article_id` integer NOT NULL,
    `is_published` bool NOT NULL,
    `pub_time` datetime,
    `create_time` datetime NOT NULL
)
;
ALTER TABLE `core_selection_article` ADD CONSTRAINT `article_id_refs_id_6fa6871c` FOREIGN KEY (`article_id`) REFERENCES `core_article` (`id`);
CREATE TABLE `core_media` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `creator_id` integer NOT NULL,
    `file_path` varchar(200) NOT NULL,
    `content_type` varchar(30) NOT NULL,
    `upload_datetime` datetime
)
;
ALTER TABLE `core_media` ADD CONSTRAINT `creator_id_refs_id_01e9904f` FOREIGN KEY (`creator_id`) REFERENCES `core_gkuser` (`id`);
CREATE TABLE `core_event` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `title` varchar(30) NOT NULL,
    `tag` varchar(30) NOT NULL,
    `slug` varchar(100) NOT NULL UNIQUE,
    `status` bool NOT NULL,
    `created_datetime` datetime NOT NULL
)
;
CREATE TABLE `core_event_status` (
    `event_id` integer NOT NULL PRIMARY KEY,
    `is_published` bool NOT NULL,
    `is_top` bool NOT NULL
)
;
ALTER TABLE `core_event_status` ADD CONSTRAINT `event_id_refs_id_99e1bafe` FOREIGN KEY (`event_id`) REFERENCES `core_event` (`id`);
CREATE TABLE `core_event_banner` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `image` varchar(255) NOT NULL,
    `banner_type` integer NOT NULL,
    `user_id` varchar(30),
    `link` varchar(255),
    `background_image` varchar(255),
    `background_color` varchar(14),
    `created_time` datetime NOT NULL,
    `updated_time` datetime NOT NULL
)
;
CREATE TABLE `core_show_event_banner` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `banner_id` integer NOT NULL UNIQUE,
    `event_id` integer,
    `position` integer NOT NULL,
    `created_time` datetime NOT NULL
)
;
ALTER TABLE `core_show_event_banner` ADD CONSTRAINT `event_id_refs_id_5e7397f8` FOREIGN KEY (`event_id`) REFERENCES `core_event` (`id`);
ALTER TABLE `core_show_event_banner` ADD CONSTRAINT `banner_id_refs_id_6cdb57c5` FOREIGN KEY (`banner_id`) REFERENCES `core_event_banner` (`id`);
CREATE TABLE `core_editor_recommendation` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `image` varchar(255) NOT NULL,
    `link` varchar(255) NOT NULL,
    `created_time` datetime NOT NULL,
    `updated_time` datetime NOT NULL
)
;
CREATE TABLE `core_show_editor_recommendation` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `recommendation_id` integer NOT NULL UNIQUE,
    `event_id` integer,
    `position` integer NOT NULL,
    `created_time` datetime NOT NULL
)
;
ALTER TABLE `core_show_editor_recommendation` ADD CONSTRAINT `event_id_refs_id_93ae143b` FOREIGN KEY (`event_id`) REFERENCES `core_event` (`id`);
ALTER TABLE `core_show_editor_recommendation` ADD CONSTRAINT `recommendation_id_refs_id_7f23c766` FOREIGN KEY (`recommendation_id`) REFERENCES `core_editor_recommendation` (`id`);
CREATE TABLE `core_friendly_link` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(64) NOT NULL,
    `link` varchar(255) NOT NULL,
    `link_category` varchar(64) NOT NULL,
    `position` integer,
    `logo` varchar(255),
    `status` integer NOT NULL
)
;
CREATE INDEX `core_gkuser_groups_436776e0` ON `core_gkuser_groups` (`gkuser_id`);
CREATE INDEX `core_gkuser_groups_5f412f9a` ON `core_gkuser_groups` (`group_id`);
CREATE INDEX `core_gkuser_user_permissions_436776e0` ON `core_gkuser_user_permissions` (`gkuser_id`);
CREATE INDEX `core_gkuser_user_permissions_83d7f98b` ON `core_gkuser_user_permissions` (`permission_id`);
CREATE INDEX `core_user_profile_f8168153` ON `core_user_profile` (`nickname`);
CREATE INDEX `core_user_follow_c5e64013` ON `core_user_follow` (`follower_id`);
CREATE INDEX `core_user_follow_9683117f` ON `core_user_follow` (`followee_id`);
CREATE INDEX `core_user_follow_c51cfd3b` ON `core_user_follow` (`followed_time`);
CREATE INDEX `core_banner_41e5f0d8` ON `core_banner` (`created_time`);
CREATE INDEX `core_banner_b7cc06d7` ON `core_banner` (`updated_time`);
CREATE INDEX `core_show_banner_41e5f0d8` ON `core_show_banner` (`created_time`);
CREATE INDEX `core_sidebar_banner_41e5f0d8` ON `core_sidebar_banner` (`created_time`);
CREATE INDEX `core_sidebar_banner_b7cc06d7` ON `core_sidebar_banner` (`updated_time`);
CREATE INDEX `core_category_9246ed76` ON `core_category` (`title`);
CREATE INDEX `core_category_48fb58bb` ON `core_category` (`status`);
CREATE INDEX `core_sub_category_5f412f9a` ON `core_sub_category` (`group_id`);
CREATE INDEX `core_sub_category_9246ed76` ON `core_sub_category` (`title`);
CREATE INDEX `core_sub_category_5a09fd37` ON `core_sub_category` (`alias`);
CREATE INDEX `core_sub_category_48fb58bb` ON `core_sub_category` (`status`);
CREATE INDEX `core_brand_b6c1f530` ON `core_brand` (`created_date`);
CREATE INDEX `core_entity_6340c63c` ON `core_entity` (`user_id`);
CREATE INDEX `core_entity_6f33f001` ON `core_entity` (`category_id`);
CREATE INDEX `core_entity_5a5255da` ON `core_entity` (`price`);
CREATE INDEX `core_entity_31f1de87` ON `core_entity` (`mark`);
CREATE INDEX `core_entity_41e5f0d8` ON `core_entity` (`created_time`);
CREATE INDEX `core_entity_b7cc06d7` ON `core_entity` (`updated_time`);
CREATE INDEX `core_selection_entity_abff12bc` ON `core_selection_entity` (`pub_time`);
CREATE INDEX `core_buy_link_c096cf48` ON `core_buy_link` (`entity_id`);
CREATE INDEX `core_buy_link_7c86b947` ON `core_buy_link` (`origin_id`);
CREATE INDEX `core_entity_like_c096cf48` ON `core_entity_like` (`entity_id`);
CREATE INDEX `core_entity_like_6340c63c` ON `core_entity_like` (`user_id`);
CREATE INDEX `core_entity_like_41e5f0d8` ON `core_entity_like` (`created_time`);
CREATE INDEX `core_note_6340c63c` ON `core_note` (`user_id`);
CREATE INDEX `core_note_c096cf48` ON `core_note` (`entity_id`);
CREATE INDEX `core_note_fdd15200` ON `core_note` (`post_time`);
CREATE INDEX `core_note_b7cc06d7` ON `core_note` (`updated_time`);
CREATE INDEX `core_note_comment_f6e610e1` ON `core_note_comment` (`note_id`);
CREATE INDEX `core_note_comment_6340c63c` ON `core_note_comment` (`user_id`);
CREATE INDEX `core_note_comment_fdd15200` ON `core_note_comment` (`post_time`);
CREATE INDEX `core_note_poke_f6e610e1` ON `core_note_poke` (`note_id`);
CREATE INDEX `core_note_poke_6340c63c` ON `core_note_poke` (`user_id`);
CREATE INDEX `core_note_poke_41e5f0d8` ON `core_note_poke` (`created_time`);
CREATE INDEX `core_sina_token_f856f082` ON `core_sina_token` (`sina_id`);
CREATE INDEX `core_sina_token_be6d63dc` ON `core_sina_token` (`screen_name`);
CREATE INDEX `core_sina_token_2acf0efe` ON `core_sina_token` (`access_token`);
CREATE INDEX `core_taobao_token_cef6c694` ON `core_taobao_token` (`taobao_id`);
CREATE INDEX `core_taobao_token_be6d63dc` ON `core_taobao_token` (`screen_name`);
CREATE INDEX `core_taobao_token_2acf0efe` ON `core_taobao_token` (`access_token`);
CREATE INDEX `core_taobao_token_06503ec5` ON `core_taobao_token` (`refresh_token`);
CREATE INDEX `core_taobao_token_a4e99593` ON `core_taobao_token` (`open_uid`);
CREATE INDEX `core_taobao_token_93e60f21` ON `core_taobao_token` (`isv_uid`);
CREATE INDEX `core_wechat_token_9f934cc8` ON `core_wechat_token` (`unionid`);
CREATE INDEX `core_article_related_entities_e669cc35` ON `core_article_related_entities` (`article_id`);
CREATE INDEX `core_article_related_entities_c096cf48` ON `core_article_related_entities` (`entity_id`);
CREATE INDEX `core_article_ad376f8d` ON `core_article` (`creator_id`);
CREATE INDEX `core_article_6dcc8a5c` ON `core_article` (`created_datetime`);
CREATE INDEX `core_selection_article_e669cc35` ON `core_selection_article` (`article_id`);
CREATE INDEX `core_selection_article_abff12bc` ON `core_selection_article` (`pub_time`);
CREATE INDEX `core_selection_article_7952171b` ON `core_selection_article` (`create_time`);
CREATE INDEX `core_media_ad376f8d` ON `core_media` (`creator_id`);
CREATE INDEX `core_media_b460d505` ON `core_media` (`upload_datetime`);
CREATE INDEX `core_event_6dcc8a5c` ON `core_event` (`created_datetime`);
CREATE INDEX `core_event_banner_41e5f0d8` ON `core_event_banner` (`created_time`);
CREATE INDEX `core_event_banner_b7cc06d7` ON `core_event_banner` (`updated_time`);
CREATE INDEX `core_show_event_banner_a41e20fe` ON `core_show_event_banner` (`event_id`);
CREATE INDEX `core_show_event_banner_41e5f0d8` ON `core_show_event_banner` (`created_time`);
CREATE INDEX `core_editor_recommendation_41e5f0d8` ON `core_editor_recommendation` (`created_time`);
CREATE INDEX `core_editor_recommendation_b7cc06d7` ON `core_editor_recommendation` (`updated_time`);
CREATE INDEX `core_show_editor_recommendation_a41e20fe` ON `core_show_editor_recommendation` (`event_id`);
CREATE INDEX `core_show_editor_recommendation_41e5f0d8` ON `core_show_editor_recommendation` (`created_time`);

COMMIT;
