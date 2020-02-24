cd /home/jurgeon/dev/margo/src

git remote remove origin 
git remote add origin git@github.com:jurgeon018/margo.git
git pull origin master --strategy-option theirs

python3 manage.py makemigrations 
python3 manage.py migrate 
sudo rm -rf static_root 
python3 manage.py collectstatic --noinput

python3 manage.py loaddata categories content 
python3 manage.py c_items prices.csv

# python3 manage.py loaddata initial content 

python3 manage.py shell -c "from django.contrib.auth import get_user_model; User=get_user_model();User.objects.create_superuser('admin', 'admin@gmail.com', 'admin')"


sudo chown :www-data db.sqlite3
sudo chmod 664 db.sqlite3
sudo chown -R :www-data media/
sudo chmod -R 775 media/
sudo chown :www-data .
sudo ufw allow http/tcp
sudo ufw allow https/tcp
sudo ufw allow https
sudo ufw allow 8000
sudo ufw allow 'Nginx Full'
sudo nginx -t
sudo systemctl enable nginx
sudo systemctl enable uwsgi
sudo systemctl start nginx
sudo systemctl restart nginx
sudo systemctl start uwsgi
sudo systemctl restart uwsgi
sudo systemctl daemon-reload

cd /home/jurgeon/dev/snippets/vps/
