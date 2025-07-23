from ..models import *
from ..connection import init_db

def filter_ia(phone:str) -> IA:
    db = init_db()
    
    if not db:
        raise (Exception("Não consegue conectar com data base"))
    
    try:
        ia = db.query(IA).filter(IA.phone_number == phone.first())
        if not ia:
            print(f"Nenhuma IA cadastrada com esse número de telefone {phone}")
            return None
        
        #adicionar as FKS
        ia.ia_config
        ia.prompts
             
    except Exception as ex:
        print(f"error : {ex}")
        
    finally:
        if db:
            db.close()