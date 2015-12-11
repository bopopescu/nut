1. formtools 相关升级文档
    https://docs.djangoproject.com/en/1.8/ref/contrib/formtools/#formtools-how-to-migrate
   
   Actions : 
      a. add django-formtools==1.0 into requirements.txt
      b. pip install django-formtools
      c. in settings.py remove  line 132 ?  # 'django.contrib.sessions',
         and replace it with 
         'formtools'
      d. search whole project for 
         "from django.contrib.formtools.wizard.views"
         replace them with 
         "from formtools.wizard.views"
        
        in nut there is 2 places 
        after the formtools package is installed ,pycharm will resolve the formtools.wizard automaticly 

2. celery 升级

