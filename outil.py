print("le fichier outil est entrain de s'executer")
print("la valeur de __name__ est : ",__name__)

def dire_bonjour():
    print("bonjour depuis outils.py")

if __name__=="__main__":
    print("outil.py est execute directement")