'''
Інструкція для швидкої розгортки.
cd projects
mkdir <project_name> 
cd <project_name>
python3 -m venv venv
source venv/bin/activate

******* 1 варіант
mkdir src 
cd src 
git clone git@github.com:<username>/<project_name> . 
*******

******* 2 варіант
git clone git@github.com:<username>/<project_name> src
*******

cd src 
git clone git@github.com:jurgeon018/boxss 
cp -rp ./box/project_boilerplate/* . 
git add . 
git commit -m 's'
git push origin master 
'''



