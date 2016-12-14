#!/bin/bash

## Restores the screen when the program exits.
trap "tput rmcup; exit"  SIGHUP SIGINT SIGTERM

## Saves the screen contents.
tput smcup

## Clears the screen.
clear

## Loop through available interfaces.
while read interface; do                    # While reads a line of the output
    i=$((i+1))                                  # Only God knows what does this (view note 1).
    type=$(cut -f2 -d ' ' <<< ${interface})       # Saves the interface type to check if is wifi.
    status=$(cut -f3 -d ' ' <<< ${interface})     # Saves the status of the current interface.
    interface=$(cut -f1 -d ' ' <<< ${interface})  # Selects the INTERFACE field of the output.
    if [[ "$type" == "802-11-wireless" ]]; then # If is a WiFi interface then:
      interfaces[$i]=${interface}                     # Adds the current interface to an array.
      #echo "$i: $interface ($status)"               # Prints the name of current interface.
    fi                                          # Ends the if conditional
done < <(nmcli device | tail -n +2)         # Redirects the output of the command nmcli device to the loop.

## If there is only one interface
if [[ "$i" == "2" ]]; then
    iface=1 # Selected interface is the only one
    clear   # Quick and dirty workaround for make disappear the interface list.
else
    ## Prompts the user for the interface to use.
    #read -p "Select the interface: " iface
    iface=1 # Just use first interface
fi

## If the entered number is valid then...
if [[ "$iface" -le ${i} ]]; then
    #read -p "Enter the SSID or BSSID: " b_ssid # Prompts the user for the ESSID/BSSID
    #read -p "Enter the password: " pass # Prompts the user for the password
    output=$(nmcli device wifi connect $1 password $2 iface $3 --timeout 10) # Tries to connect
    wget -q --tries=5 --timeout=5 --spider http://google.com &> /dev/null # Is connected to Internet?
    if [[ $? -eq 0 ]]; then
            echo "You're connected." # Is connected to Internet
            exit 0
    else
            echo "Error. $output" # Anything goes wrong
            exit 1
    fi
else
    echo "Invalid interface entered. Exiting..."
    exit 2
fi

## Note 1: this line increments $i
