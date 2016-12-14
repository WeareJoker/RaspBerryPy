#!/bin/bash

## Loop through available interfaces.
while read interface; do                    # While reads a line of the output
    i=$((i+1))                                  # Only God knows what does this (view note 1).
    type=$(cut -f2 -d ' ' <<< ${interface})       # Saves the interface type to check if is wifi.
    status=$(cut -f3 -d ' ' <<< ${interface})     # Saves the status of the current interface.
    interface=$(cut -f1 -d ' ' <<< ${interface})  # Selects the INTERFACE field of the output.
    if [[ "$type" == "802-11-wireless" ]]; then # If is a WiFi interface then:
      interfaces[$i]=${interface}                     # Adds the current interface to an array.
      echo "$interface"               # Prints the name of current interface.
    fi                                          # Ends the if conditional
done < <(nmcli device | tail -n +2)         # Redirects the output of the command nmcli device to the loop.
