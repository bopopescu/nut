## Mobile Apps
```
+--------------+-------------+------+-----+---------+----------------+
| Field        | Type        | Null | Key | Default | Extra          |
+--------------+-------------+------+-----+---------+----------------+
| id           | int(11)     | NO   | PRI | NULL    | auto_increment |
| user_id      | int(11)     | NO   | MUL | NULL    |                |
| app_name     | varchar(30) | NO   | UNI | NULL    |                |
| desc         | longtext    | NO   |     | NULL    |                |
| api_key      | varchar(64) | NO   |     | NULL    |                |
| api_secret   | varchar(32) | NO   |     | NULL    |                |
| created_time | datetime    | NO   |     | NULL    |                |
+--------------+-------------+------+-----+---------+----------------+
```

```
insert into mobile_apps select * from guoku.mobile_apps;
update mobile_apps set user_id = 1;;
```

## Mobile Session Key
```
+-------------+-------------+------+-----+---------+----------------+
| Field       | Type        | Null | Key | Default | Extra          |
+-------------+-------------+------+-----+---------+----------------+
| id          | int(11)     | NO   | PRI | NULL    | auto_increment |
| user_id     | int(11)     | NO   | MUL | NULL    |                |
| app_id      | int(11)     | NO   | MUL | NULL    |                |
| session_key | varchar(64) | NO   | UNI | NULL    |                |
| create_time | datetime    | NO   |     | NULL    |                |
+-------------+-------------+------+-----+---------+----------------+
```
```
insert into mobile_session_key 
	select * from guoku.mobile_session_key 
		where user_id in (select id from core_gkuser);
```