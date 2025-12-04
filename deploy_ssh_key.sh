#!/usr/bin/expect -f

set timeout 30
set password "9-Sportsdataio"
set host "root@72.60.43.168"

# Copy SSH key to server
spawn ssh-copy-id -i ~/.ssh/hostinger_vps.pub -o StrictHostKeyChecking=no $host

expect {
    "password:" {
        send "$password\r"
        expect eof
    }
    "Are you sure you want to continue connecting" {
        send "yes\r"
        expect "password:"
        send "$password\r"
        expect eof
    }
}
