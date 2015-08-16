1 .   数据库中加入 两个新字段

 MYSQL  执行 :
  
ALTER TABLE `core`.`core_event_banner` 
ADD COLUMN `background_image` VARCHAR(255) NULL DEFAULT NULL AFTER `updated_time`,
ADD COLUMN `background_color` VARCHAR(14) NULL DEFAULT 'fff' AFTER `background_image`;


2. models  修改  Event_Banner model 定义

加入
 background_image = models.CharField(max_length=255, null=True, blank=True)
 background_color = models.CharField(max_length=14, null=True,blank=True,default='#fff')
  
3. Event_banner 中加入 property 
  
  @property
    def background_image_url(self):
        if self.background_image:
            return "%s%s" %(image_host, self.background_image)
        else:
            return None 
            
4. 