#  hady ela wdyte data importation de json
import json
import os

#  class absraite 
#  partie 1 : 
from abc import ABC,abstractmethod
class Personne(ABC):
    def __init__(self, cin,nom, prenom,age):
        self.__cin=cin
        self._nom=nom
        self._prenom=prenom
        self._age=age
    # methode abstraite
    @abstractmethod
    def get_role(self):
        pass
    # methode concrete 
    def afficher_infos(self):
        print(f"- CIN : {self.get_cin()}")
        print(f"- Nom : {self._nom}")
        print(f"- Prenom : {self._prenom}")
        print(f"- Age : {self._age} ans")
# partie 2 :encapsulation
    #  getter 
    def get_cin(self):
        return self.__cin
    #  setter 
    def set_cin(self,new_cin):
        if new_cin=="":
            raise Exception("Validation Error!!!! ❌")
        self.__cin=new_cin
        print("votre CIN est Valider 👍")
#  partie 3 : heritage simple

#  classa Medcin
class Medcin(Personne):
    def __init__(self, cin, nom, prenom, age, specialite,salaire):
        super().__init__(cin,nom,prenom,age)
        self.specialite=specialite
        self.__salaire=salaire

    # getter
    @property
    def salaire(self):
        return self.__salaire
    
    # setter
    @salaire.setter
    def salaire(self,new_salaire):
        if new_salaire <= 0:
            raise Exception("Validation de Prix est Error ❌")
        self.__salaire=new_salaire
        print("Votre Salaire est bien!!!!")

        # methode de affichage

    def afficher_infos(self):
        super().afficher_infos()
        print(f"- Specialite : {self.specialite}")
        print(f"- salaire : {self.salaire}","DH")

    #  role methode 
    def get_role(self):
        return "Medcin"

#  class Patient
class Patient(Personne):
    def __init__(self, cin, nom, prenom, age, maladie, num_dossier):
        super().__init__(cin, nom, prenom, age)
        self.__maladie=maladie
        self._num_dossier=num_dossier


    #  methode de cout de consulation
    def couts_consultaion(self,jours):
        return jours * 200
    
    #  methode de role d'une medcin
    def get_role(self):
        return "Patient"
    #  getter 
    @property
    def maladie(self):
        return self.__maladie
    # setter 
    @maladie.setter
    def maladie(self,new_maladie):
        if new_maladie=="":
            raise Exception("Validation Error ❌")
        self.__maladie=new_maladie
        print("Votre maladie est bien Ecrire 👍")


    #  methode de l'affichage
    def afficher_infos(self):
        super().afficher_infos()
        print(f"- maladie : {self.maladie}")
        print(f"- numero de dossier : {self._num_dossier}")
    
# partie : 4 interface Consutable
from abc import ABC,abstractmethod
class Consutable(ABC):

    @abstractmethod
    def consulter(self):
        pass
    @abstractmethod
    def get_tarif(self):
        pass

#  partie 5 : heritage multiple 

#  heritage multiple dans une class MedcinChef

class MedcinChef(Medcin,Consutable):
    def __init__(self, cin, nom, prenom, age, specialite, salaire, departement):
        super().__init__(cin, nom, prenom, age, specialite, salaire)
        self.departement=departement
    
    #  methode de tarife
    def consulter(self):
        print(f"- Dr.Chef{self._nom}")

    #  prix de consultation
    def get_tarif(self):
        return 500
    
    # medcin chef get rol dyalha
    def get_role(self):
        return "MedcinChef"


    #  methode de affichage
    def afficher_infos(self):
        super().afficher_infos()
        print(f"- Departement : {self.departement}")
    

#  partie 6 : super() + redefinition

#  cetter partie pour redefinir des methodes 
#  ya3ni khassni nrj3e nkhdme fkola class aficher infos dyalha fhmty !!!!! mea super()


#  parite 7 :clinique
 

# class clinique
class Clinique:
    #  il ya des attribust de rendez_vous
    def __init__(self,nom):
        self.nom=nom
        #  listes des Rendez_vous 
        self.listRendez_vous=[]
        #  listes des personnes
        self.ListPersonnes=[]


# methode pour ajouter personne 
    def ajouter_personne(self,personne):
        if not isinstance(personne,Personne):
            raise TypeError("❌ Objet invalide ! Doit être une Personne.")
        self.ListPersonnes.append(personne)
        print(f"👍 Le {personne.get_role()} : {personne._nom} {personne._prenom} Ajouter a la clinique.")
    def cout_total_consultations(self,jours):
        if jours <= 0:
            raise ValueError("❌ Le nombre de jours doit être positif !")
        total=0
        for personne in  self.ListPersonnes:
            if isinstance(personne, Patient):
                total+= personne.couts_consultaion(jours)
        return total
    
    #  methode pour recherche d'une personne 
    def recherche_person_by_cin(self,cin):
        for p in self.ListPersonnes:
            if p.get_cin() == cin:
                return p
        return None
    
    # methode pour ajouter un rendez_vous 
    def ajouter_rendez_vous(self,patient ,medcin, date, heure):
        if not isinstance(patient,Patient):
            raise TypeError("❌ Doit être un Patient !")
        if not isinstance(medcin,Medcin):
            raise TypeError("❌ Doit être un Medcin !")
        
        #  dictionary
        rdv = {
            "patient":patient.get_cin(),
            "medcin":medcin.get_cin(),
            "date":date,
            "heure":heure,
        }

        self.listRendez_vous.append(rdv)
        print(f"✅ Rendez-vous ajouté : {patient._nom} avec Dr.{medcin._nom } le {date} à {heure}")




    # mwthode bach n9rawe les info otrj3e t3mere dek lsit persone
    def sauvegarder_json(self, filename="data.json"):
        data = {"personnes": [], "rendez_vous": []}
    
        for p in self.ListPersonnes:
            item = {
                "type": p.get_role(),
                "cin": p.get_cin(),
                "nom": p._nom,
                "prenom": p._prenom,
                "age": p._age
            }
    
            if isinstance(p, Patient):
                item["maladie"] = p.maladie
                item["num_dossier"] = p._num_dossier
            elif isinstance(p, MedcinChef):
                item["specialite"] = p.specialite
                item["salaire"] = p.salaire
                item["departement"] = p.departement
            elif isinstance(p, Medcin):
                item["specialite"] = p.specialite
                item["salaire"] = p.salaire
    
            data["personnes"].append(item)
    
        data["rendez_vous"] = self.listRendez_vous
    
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    #  hady dyal load ewde zema bach n9rawe les infos 
    def load_json(self, filename="data.json"):
        if not os.path.exists(filename):
            return
    
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    
        self.ListPersonnes = []
        self.listRendez_vous = []
    
        for item in data.get("personnes", []):
            t = item.get("type")
    
            if t == "Patient":
                obj = Patient(item["cin"], item["nom"], item["prenom"], item["age"],
                              item.get("maladie", ""), item.get("num_dossier", ""))
            elif t == "MedcinChef":
                obj = MedcinChef(item["cin"], item["nom"], item["prenom"], item["age"],
                                 item.get("specialite", ""), item.get("salaire", 0),
                                 item.get("departement", ""))
            elif t == "Medcin":
                obj = Medcin(item["cin"], item["nom"], item["prenom"], item["age"],
                             item.get("specialite", ""), item.get("salaire", 0))
            else:
                continue
    
            self.ListPersonnes.append(obj)
    
        self.listRendez_vous = data.get("rendez_vous", [])

    #  methode pour l'affichage
    def afficher_rendez_vous(self):
        print("\n======= 📅 RENDEZ-VOUS =========")
        for rdv in self.listRendez_vous:
            pat = self.recherche_person_by_cin(rdv["patient"])
            med = self.recherche_person_by_cin(rdv["medcin"])
    
            pat_name = f"{pat._nom} {pat._prenom}" if pat else rdv["patient_cin"]
            med_name = f"{med._nom} {med._prenom}" if med else rdv["medcin_cin"]
    
            print(f"{pat_name} -> Dr.{med_name} | {rdv['date']} à {rdv['heure']}")

