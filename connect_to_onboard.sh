#!/bin/bash

# This script is used to sync time from the ground station to the onboard computer

echo -e "Introduce username@remote_server option... \n"

address_array=("cvar@nx-cvar" "cvar@nx1-cvar" "cvar@px4-cvar" "cvar@xavier-cvar" "cvar@xavier-cvar-1")

echo -e "Possible options: \n"

echo "1: cvar@nx-cvar"
echo "2: cvar@nx1-cvar"
echo "3: cvar@px4-cvar"
echo "4: cvar@xavier-cvar"
echo "5: cvar@xavier-cvar-1"
echo -e "6: custom address\n"

echo "Option: "; read option

# Check if option is a number
if [[ ! $option =~ ^[0-9]+$ ]]; then
    echo -e "Option is not a number\n"
    exit 1
fi

# Check if option is between 1 and 5

if [ "$option" -lt 1 ] || [ "$option" -gt 6 ]; then
    echo -e "Invalid option\n"
    exit 1
fi

if [ "$option" -eq 6 ]; then
    echo -e "Introduce custom address: "; read custom_address
    address=$custom_address
else
    address=${address_array[$option-1]}
fi

echo -e -n "\nIntroduce password for "$address".local in order to sync time: \n"

read -s password

expect -f - <<-EOF
  set timeout 10
  spawn -noecho ssh $address.local "sudo -S date -s '$(date)'"
  expect "*?assword*"
  send -- "$password\r"
  expect "*?assword*"
  send -- "$password\r"
  expect eof
EOF

ssh_exit_status=$?

# Check the exit status
if [ $ssh_exit_status -eq 0 ]; then
    # Check if the output contains an error message indicating a wrong password
    if echo "$ssh_result" | grep -qi "Permission denied"; then
        echo "SSH conection failed: Incorrect password"
    else
        echo -e "\nTime synced with "$address".local\n"
    fi
else
    echo "SSH conection failed: Exit status $ssh_exit_status"
    exit
fi

remote_command="bash -l"

expect -c "
  spawn -noecho ssh -t $address.local \"$remote_command\"
  expect \"*?assword*\"
  send -- \"$password\r\"
  interact
"