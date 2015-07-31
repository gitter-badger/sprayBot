#!/bin/bash

TEMP=$( /opt/vc/bin/vcgencmd measure_temp |awk -F '=' '{print $2}' )

echo "Temperature CPU de spraybot: ${TEMP}"
echo "Temperature CPU de spraybot: ${TEMP}" | mutt -s "[SPRAYBOT] Temperature" -- root@localhost
