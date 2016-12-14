# total
TOTAL

# How to autorun when booting  
cp ./shell_scripts/booting_autorun.sh /etc/init.d/
chmod +x /etc/init.d/booting_autorun.sh  
update-rc.d booting_autorun.sh defaults  


