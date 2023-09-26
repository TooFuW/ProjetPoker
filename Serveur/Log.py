
import datetime

def write_connexion(ip,connection : bool = True):
    current_folder = __file__[:-6]
    log_path = current_folder+"logs/logs.txt"
    blacklist_path =  current_folder+"logs/blacklist.txt"

    current_time = datetime.datetime.utcnow()
    with open(log_path,"+a",encoding="utf-8") as log_file:
        log_file.write(f"{str(ip)} : {'accepted connection at' if connection else 'disconnection at'} {current_time}\n")
        log_file.close()
        return

def is_ip_in_blacklist(ip):
    current_folder = __file__[:-6]
    log_path = current_folder+"logs/logs.txt"
    blacklist_path = current_folder+"logs/blacklist.txt"

    with open(blacklist_path,"r",encoding="utf-8") as blacklist_file:
        banned_ips = blacklist_file.readlines()
        ip_banned = str(ip).strip() in banned_ips
        blacklist_file.close()
        return ip_banned
    
def write_refused_connection(ip):
    current_folder = __file__[:-6]
    log_path = current_folder+"logs/logs.txt"
    blacklist_path = current_folder+"logs/blacklist.txt"

    current_time = datetime.datetime.utcnow()
    with open(log_path,"+a",encoding="utf-8") as log_file:
        log_file.write(f"{str(ip)} : connection refused at {current_time}\n")
        log_file.close()
        return
       
def write_lobby_connexion(ip,lobby_id,connection : bool = True):
    current_folder = __file__[:-6]
    log_path = current_folder+"logs/logs.txt"

    current_time = datetime.datetime.utcnow()
    with open(log_path,"+a",encoding="utf-8") as log_file:
        log_file.write(f"{str(ip)} : connection accepted in lobby {str(lobby_id)} at {current_time}\n")
        log_file.close()
        return
