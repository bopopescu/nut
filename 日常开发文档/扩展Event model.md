1. 问题描述
   因为要写一个专题列表页，现在的专题 Event model 中，status 字段负责 描述该 Event 是否是 唯一 活跃的Event
   但是， 列表页要求，有一个字段 ， 描述该Event是否被发布。 
   只能扩展该Model， 用一个 one to one relation 来达到上述要求
   
   
2. 扩展步骤
    2.0.  备份数据库.......
    
    2.1. 在 apps/core/models.py 中 建立一个 新的model
        
    class Event_Status(models.Model):
        event = models.OneToOneField(Event, primary_key=True)
        is_published = models.BooleanField(default=False)
        is_top = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s status : is_published : %s , is_top : %s" %(self.event.slug, self.is_published, self.is_top)

    2.2. 在Django的项目目录下执行
        ./manage.py syncdb
        
        出现如下 output
        
        Creating tables ...
        Creating table core_event_status
        Installing custom SQL ...
        Installing indexes ...
        Installed 0 object(s) from 0 fixture(s)
        
    2.3. 在Django的项目目录下执行
        ./manage.py shell
        在python的提示符下输入 ：
            from apps.core.models import Event, Event_Status
evs = Event.objects.all()
for ev in evs : 
    es = Event_Status(is_published=False, is_top=ev.status)
    es.event = ev 
    es.save()
                
        以上语句会把所有现有的event 的 event_status 设置为 is_published＝False， is_top＝event.status
        
        
    2.4 在浏览器中进入管理后台，进入专题管理
        将会出现在专题列表中的EVENT 的 “专题是否发布” 设置为 "true"
        这些专题会出现在列表中。
        
        
        
        
