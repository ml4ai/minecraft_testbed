#!/bin/bash


i=1
while [ $i -eq 1 ];do    

    sleep 10  
    # every 10 seconds, reset the permissions for any map that may have been written to Local directory
    chmod 777 -R .
    
done


