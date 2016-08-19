#!/bin/bash
curl -s "http://10.1.1.1:49000/upnp/control/WANCommonIFC1" -H "Content-Type: text/xml; charset="utf-8"" -H "SoapAction:urn:schemas-upnp-org:service:WANCommonInterfaceConfig:1#GetAddonInfos" -d "@/home/pi/upnp/linkspeed.xml" 
