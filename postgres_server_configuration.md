sudo apt update										--
sudo apt install postgresql postgresql-contrib -y	--
sudo systemctl status postgresql					-- Verify if its running
sudo -i -u postgres 								-- Swith t postgress user
psql												-- Open postgress shell
ALTER USER postgres PASSWORD 'mypassword';          -- Set a new password
\q
exit												-- Logout from postgress

If server needs to be accessed from outside then modify the fiel - postgresql.conf
	sudo nano /etc/postgresql/*/main/postgresql.conf
	listen_addresses = '*' ------------> make it as '*' instead of 'localhost'


Edit Client Auth:
>	sudo nano /etc/postgresql/*/main/pg_hba.conf
Paste this at the end
>	host    all     all     0.0.0.0/0     md5

Restart postgress
>	sudo systemctl restart postgresql


Now open the port:
sudo ufw status verbose
5432/tcp ALLOW Anywhere
5432/tcp ALLOW Anywhere (v6)

Verify the connection from a different machine:
> psql -h <server_ip> -p <port> -U <username> -d <databasename>

============================================================================================

sudo -u postgres psql


#Create new user and password
> CREATE USER username WITH PASSWORD 'password123';

#Create new Database
> CREATE DATABASE mydatabase;

#go inside the DB
\c mydatabase

#Grand Permissions
GRANT ALL PRIVILEGES ON DATABASE mydatabase TO username;
GRANT ALL ON SCHEMA public TO username;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO username;
GRANT USAGE, CREATE ON SCHEMA public TO username;
ALTER SCHEMA public OWNER TO username;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT, INSERT, UPDATE, DELETE, REFERENCES, TRIGGER ON TABLES TO username;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT USAGE, SELECT, UPDATE ON SEQUENCES TO username;

\q



	
	
	





