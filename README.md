0. sudo apt-get install sqlite3
1. sudo pip3 install -r requirements.txt
2. sudo adduser telegram_user
3. touch /var/log/telegram-loyalty.log
4. sudo chown telegram_user:telegram_user /var/log/telegram-loyalty.log
5. Fill environment variables in the systemd/telegram-loyalty.service file.
6. sudo cp systemd/telegram-loyalty.service /etc/systemd/system/telegram-loyalty.service
7. sudo systemctl enable telegram-loyalty
8. sudo systemctl start telegram-loyalty
9. Repeat 5-8 steps if you need the second bot for the second brand (the first
   bot for vivat, the second - for librarium).

