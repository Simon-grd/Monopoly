from typing import List

try:
    import mysql.connector  # type: ignore
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False

from models.case import Propriete
from models.gare import Gare
from models.compagnie import Compagnie

class DB:
    @classmethod
    def connexionBase(cls):
        if not MYSQL_AVAILABLE:
            return None
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="aDHp8P6?2/6]",
            database="monopoly"
        )
        return mydb
    
    def __init__(self, host="localhost", user="root", password="aDHp8P6?2/6]", database="monopoly"):
        if not MYSQL_AVAILABLE:
            print("⚠️ mysql-connector-python n'est pas installé")
            print("   Installez-le avec: pip install mysql-connector-python")
        self.config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database
        }
        self.connection = None
    
    def connect(self):
        if not MYSQL_AVAILABLE:
            return False
        try:
            self.connection = mysql.connector.connect(**self.config)
            return True
        except Exception as e:
            print(f"Erreur de connexion à la base de données: {e}")
            return False
    
    def disconnect(self):
        if MYSQL_AVAILABLE and self.connection and self.connection.is_connected():
            self.connection.close()
    
    def charger_proprietes(self) -> List:
        if not MYSQL_AVAILABLE:
            return []
        if not self.connection or not self.connection.is_connected():
            if not self.connect():
                return []
        
        proprietes = []
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM v_proprietes ORDER BY position")
            
            for row in cursor.fetchall():
                type_prop = row['type_propriete']
                
                if type_prop == 'gare':
                    prop = Gare(row['nom'], row['position'])
                elif type_prop == 'compagnie':
                    prop = Compagnie(row['nom'], row['position'])
                else:
                    prop = Propriete(
                        row['nom'],
                        row['position'],
                        row['prix'],
                        row['loyer_base'],
                        row['couleur']
                    )
                proprietes.append(prop)
            
            cursor.close()
        except Exception as e:
            print(f"Erreur lors du chargement des propriétés: {e}")
        
        return proprietes