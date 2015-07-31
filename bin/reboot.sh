#!/bin/bash

source /appli/conf/relay.conf

echo "Le serveur $( hostname ) a redemarre" |mutt -s "[SPRAYBOT] Le serveur a redemarre" -- root@localhost
/appli/bin/relay.py > /dev/null 2>&1
/usr/local/bin/gpio -g write ${RELAY1} 1 > /dev/null 2>&1
/usr/local/bin/gpio -g write ${RELAY2} 1 > /dev/null 2>&1

cat "${APPDIR}/tmp/relayState.txt" | while read i
do
	RELAY=$( echo $i |awk -F ":" '{print $1}' )
	STATE=$( echo $i |awk -F ":" '{print $2}' )
	/usr/local/bin/gpio -g write ${RELAY} ${STATE}
done
