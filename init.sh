
#sudo apt-get install python3

#sudo pip3 install -r requirements.txt

python3 -c "import os; print ('\nSECRET_KEY = ' + str(repr(os.urandom(24))));" >> app/settings.py