kill -9 $(pidof uwsgi)
cd /var/www/vhosts/lovehate.io/lovehate
uwsgi --socket :8001 --module lovehate.wsgi --emperor /etc/uwsgi/vassals --uid root --gid root  --master --processes 6 --threads 3 --stats 127.0.0.1:9191 --daemonize=/var/www/vhosts/lovehate.io/logs/uwsgi.log

