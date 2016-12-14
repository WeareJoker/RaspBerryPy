
ifconfig $1 down
ip link set name $2 dev $1
ifconfig $2 up
