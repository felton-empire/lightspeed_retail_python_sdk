## lightspeed Retail Python SDK ##

An easy to use python SDK for use with the lightspeed Retail API

#### Setting up Python ####

This SDK runs on python 3.6.2. This is done most easily with pyenv. On Mac:

1. Install Homebrew if you don't already have it https://brew.sh/
1. ```brew install pyenv pyenv-virtualenv sqlite openssl zlib sqlite```
1. ```CFLAGS="-I/usr/local/opt/sqlite/include -I/usr/local/opt/zlib/include"```
```LDFLAGS="-L/usr/local/opt/zlib/lib -L/usr/local/opt/sqlite/lib" pyenv```
```install 3.6.2```
1. ```pyenv virtualenv 3.6.2 ls_sdk```
1. You will automatically have the correct version of python when you switch
into the project directory
