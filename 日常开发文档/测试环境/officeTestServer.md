1. ip 
    initial : 10.0.9.136
    
2. user / pass
    root / guoku!@#

3. mysql (install mysql )
    user / pass
    root / mypass
    
4. copy requirements to /opt/script/requirements

    brew install pip 
    brew install freetype imagemagick
    pip install -r requirements
    pip install qrcode 
    
    
    
 
5. brew install redis
    bash > redis-server &
    
6. start redis 
    redis-server 
   
### can use file cache instead of redis cache 
 
   
7. start mysql  , 
 
  sudo /usr/local/mysql/support-files/mysql.server start
  
  make sure your mysql server has user/pass same as the office.py settings file 
  
  
  
  
 
 