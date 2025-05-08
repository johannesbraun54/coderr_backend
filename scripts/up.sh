git add .
git commit -m "$*"
git push
ssh johannesbraun02@34.32.93.121 "cd /home/johannesbraun02/projects/coderr_backend && git pull"