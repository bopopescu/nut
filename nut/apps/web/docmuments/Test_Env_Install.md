Mac : 
 
 

 
Basicly the main document is allright , except you may meet some trouble in
getting PIL and amqp RUNNING  

--------------install PIL 1.1.7-------------------
   
curl -O -L http://effbot.org/media/downloads/Imaging-1.1.7.tar.gz
# extract
tar -xzf Imaging-1.1.7.tar.gz
cd Imaging-1.1.7
# build and install
python setup.py build
sudo python setup.py install

------------ handle 'freetype/fterrors.h' file not found error ------------

ln -s /usr/local/include/freetype2 /usr/local/include/freetype

http://stackoverflow.com/questions/20325473/error-installing-python-image-library-using-pip-on-mac-os-x-10-9


------------- AMQP ------------
$ wget http://pypi.python.org/packages/source/l/librabbitmq/librabbitmq-1.0.1.tar.gz
$ tar xvfz librabbitmq-1.0.1.tar.gz
$ cd librabbitmq-1.0.1
$ python setup.py install


You may want use your own project setting file for testing , 
setup the DJANGO_SETTINGS_MODULE env in test configuration interface .

