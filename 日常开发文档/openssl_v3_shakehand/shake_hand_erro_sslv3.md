1. first 


brew update
brew install openssl
brew link --force openssl

openssl version -a

Replace with a symlink to /usr/local/Cellar/openssl/1.0.1g/bin/openssl

e.g. in my case openssl was located in /usr/bin

mv /usr/bin/openssl /usr/bin/openssl_OLD
ln -s /usr/local/Cellar/openssl/1.0.1g/bin/openssl /usr/bin/openssl

Finally 

install pyopenssl pyasn1 ndg-httpsclient

http://apple.stackexchange.com/questions/126830/how-to-upgrade-openssl-in-os-x
http://stackoverflow.com/questions/15185661/openssl-version-macosx-homebrew
http://stackoverflow.com/questions/31649390/python-requests-ssl-handshake-failure