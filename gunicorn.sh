# Define variables:
PORT=$1
APPNAME=DjangoStates
NAME=django-states
GUNICORN=gunicorn
DBDIR=$HOME/db/$NAME
ACCESS_LOG=$DBDIR/access.log
GUNICORN_LOG=$DBDIR/gunicorn.log

if [[ "x$1" == "x" ]]; then
    PORT=8081
fi

# Monitor log on screen:
tail -n 0 -f $ACCESS_LOG &
tail -n 0 -f $GUNICORN_LOG &

# Start Gunicorn server:
echo Starting Gunicorn...
exec $GUNICORN $APPNAME.wsgi:application \
    --name $NAME \
    --bind 0.0.0.0:$PORT \
    --workers 3 \
    --log-level=info \
    --log-file=$GUNICORN_LOG \
    --access-logfile=$ACCESS_LOG
