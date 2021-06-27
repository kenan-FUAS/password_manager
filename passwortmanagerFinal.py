#import matplotlib
#matplotlib.use('Agg')
import shutil
from builtins import print
from builtins import print
from getpass import getpass
import os
import time
import os.path
import random
import string
from tkinter import Tk   ## notice lowercase 't' in tkinter here
import threading
import sys

count = 0
passw = ""
options = ["d: Titel löschen", "t: Titel anzeigen", "a: Titel hinzufügen", "c: Master-Passwort ändern", "z: Zeitlimit Anwendung", "e: Programm beenden"]


def getsys():
    if os.name =="nt":
        current_user = os.getlogin()
        os.chdir(r"C:\Users\\"+current_user+"\Desktop")
        return True
    else:
        #current_user= getpass.getuser() #eine Funktion, die den Username übernimmt aber, da der Username bei uns in Ubuntu anders genannt ist, wurde direkt der Benutzername vom eignen System übernommen
        homedir = os.path.expanduser("~")
        os.chdir("/mnt/c/users/Mohammed/pycharmprojects/pythonpassword")
        return False

pfad = os.getcwd()      #Pfad, in dem die Ordner gespeichert werden


#Anzeigen der Optionen:
def optionen():
        print("\nWas möchten Sie tun?\t")
        print("")
        for elem in options:      #Anzeigen der Optionen
            print(elem)

        user_input =input().lower()          #Input-Eingabe des Users

        #Aussuchen der Optionen:

        #Titel löschen
        if user_input == "d":
            delete()        #Aufrufen der Funktion Delete()


        #Alle Titel auflisten:

        elif user_input == "t":
           showTitel()      #Aufrufen der Funktion ShowTitel()

        #Hinzufügen von Titeln:
        elif user_input == "a":
            addTitel()      #Aufrufen der Funktion AddTitel()
            optionen()      #Aufrufen der Funktion optionen()

        #Programm beenden:
        elif user_input == "e":
            print("Das Programm wird beendet.")
            os.execl(sys.executable,*sys.argv)   #Beendigung des Programms
            exit()

        #Ändern des MWP
        elif user_input == "c":
            change_Master_Passwort()     #Aufrufen der Funktion chMPW()

        #Ändern des Zeitlimits:
        elif user_input =="z":
            zeitlimit()     #Aufrufen der Funktion Zeitlimit()
        else:
            print("Eingabe stimmt mit keiner Option überein.")
            time.sleep(2.5)     #Unterbrechung des Programms für 2.5 Sekunden
            optionen()      #Aufrufen der Funktion optionen()



def make_Directory():    #Erstellen von Ordner, in dem die Text-Dateien gespeichert sind

    if getsys():
        os.makedirs("PManager")  # erstellt Ordner 'PManager'
        os.chdir(pfad + "\\PManager")  # ändert Dateien-Pfad
        os.makedirs("MasterPW")  # erstellt Ordner 'MasterPW' in Ordner 'PManager'
        os.makedirs("passwords")  # erstellt Ordner 'passwords' in Ordner 'PManager'
        os.makedirs("Zeitlimit")  # erstellt Ordner 'Zeitlimit' in Ordner 'PManager'
    else:
        os.makedirs("PManager")     #erstellt Ordner 'PManager'
        os.chdir(pfad +"/PManager")    #ändert Dateien-Pfad
        os.makedirs("MasterPW")     #erstellt Ordner 'MasterPW' in Ordner 'PManager'
        os.makedirs("passwords")    #erstellt Ordner 'passwords' in Ordner 'PManager'
        os.makedirs("Zeitlimit")    #erstellt Ordner 'Zeitlimit' in Ordner 'PManager'


def master_passwort_check(user_first_password, count, user_second_password_for_the_check):     #Masterpasswort Abfrage


        if user_first_password==user_second_password_for_the_check:     #wenn das eingegebene Passwort mit dem MasterPW übereinstimmt --> Return value = True
          return True
        else:
            if count < 2 :      #zählt, wie oft schon versucht wurde, sich einzuloggen
                print("Falsches Passwort. Sie haben noch",2 - count,"Versuch(e).")
                user_first_password=getpass("Bitte erneut eingeben:\t")   #erneute Abfrage des MasterPW
                count += 1      #count +1, um die Versuche zu zählen
                if master_passwort_check(user_first_password, count, user_second_password_for_the_check):      #erneuter Aufruf der Funktion
                    return True
            else :
                print("Zu viele Versuche! Das Programm wird beendet.")  #mehr als 3 Versuche --> Programm wird beendet                                                                       #Return value = False
                return False


def countdown():        #Timer für Zwischenablage

        timer = 30      #Timer auf 30 Sekunden festgelegt
        for x in range(30):
            timer -= 1     #for-Schleife, jede Sekunde wird dem Integer timer 1 abgezogen --> nach 30 Sekunden bei 0
            time.sleep(1)
        if timer == 0:
            r = Tk()                    #nach 30 Sekunden wird die Zwischenablage mit einem leeren String aktualisiert,
            r.withdraw()                #sodass das Passwort wieder aus der Zwischenablage gelöscht wird
            r.clipboard_clear()
            r.clipboard_append("")
            r.update()


def countdown2():               #Timer für das automatische Abmelden nach x Minuten
        if getsys():
            open_File = open(pfad + "\\PManager\\Zeitlimit\\Zeitlimit.txt", "r")
            min = open_File.read()  # Minutenanzahl gespeichert ist
            timer = min * 60  # Umwandlung der Minuten in Sekunden
            if min != "":
                mint = int(min)
                timer = mint * 60
            else:
                min = open_File.read()
                timer = int(min * 60)




        else:
            open_File = open(pfad+"/PManager/Zeitlimit/Zeitlimit.txt","r")
            min = open_File.read()  # Minutenanzahl gespeichert ist
            if min !="":
                mint=int(min)
                timer = mint * 60
            else:
                open_File.write("5")
                min = open_File.read()
                mint = int(min)
                timer = mint * 60

        for x in range(int(timer)):  # Analog wie countdown()
            timer -= 1
            time.sleep(1)
        if timer == 0:
            print("\nAutomatisch abgemeldet, da Zeitlimit von " + str(min) + " Minuten erreicht.")
            os.execl(sys.executable, sys.executable, *sys.argv)  # System wird beendet, wenn timer = 0








def zeitlimit():                #Wählen des Zeitlimits, bis automatisch beendet werden soll
    Zeitoptionen=["a: 1 Minute","b: 5 Minuten","c: 10 Minuten","d: 30 Minuten","e: 1 Stunde","f: 2 Stunden"]
    if getsys():
        R = open(pfad + "\\PManager\\Zeitlimit\\Zeitlimit.txt", "r")
    else:
        R = open(pfad+"/PManager/Zeitlimit/Zeitlimit.txt", "r")
       #Aufrufen der Datei, in der das Zeitlimit gespeichert ist
    print("\nAktuelles Zeitlimit: "+R.read()+" Minute(n).")   #Anzeigen des aktuellen Zeitlimits
    R.close()
    benutzer_input = input("Möchten Sie ein neues Zeitlimit festlegen?y/n\t").lower()

    def Limit_return(limit):        #Zeitlimit-Optionen
        if limit == "a":
            return '1'
        elif limit == "b":
            return '5'
        elif limit == "c":
            return '10'
        elif limit == "d":
            return '30'
        elif limit == "e":
            return '60'
        elif limit == "f":
            return '120'
        else:
            print("Eingabe stimmt nicht überein.")
            zeitlimit()     #ernueter Aufruf der Funktion Zeitlimit(), wenn Eingabe nicht mit den Oben angegebenen Optionen übereinstimmt


    if benutzer_input == "y":
        print("")
        for options in Zeitoptionen:            #Anzeigen aller Zeitoptionen
            print(options)

        limit = input("Wählen Sie ein Zeitlimit.\t")        #Wählen des Zeitlimits

        if getsys():
            open_File = open(pfad + "\\PManager\\Zeitlimit\\Zeitlimit.txt", "w+")
            open_File.write(Limit_return(limit))  # Die gewählte Option wird in die Datei geschrieben
            open_File.close()
        else:
            open_File = open(pfad+"/PManager/Zeitlimit/Zeitlimit.txt", "w+")  #öffnen der Datei, in der das Zeitlimit gespeichert wird
            open_File.write(Limit_return(limit))    #Die gewählte Option wird in die Datei geschrieben
            open_File.close()
        if getsys():
            open_File = open(pfad + "\\PManager\\Zeitlimit\\Zeitlimit.txt", "r")
            me = open_File.read()
        else:
            open_File = open(pfad+"/PManager/Zeitlimit/Zeitlimit.txt", "r")  #öffnen der Datei, in der das Zeitlimit gespeichert wird
            me = open_File.read()
        print("Das Zeitlimit beträgt ab dem nächsten Start der Anwendung "+me+" Minute(n).")      #Das aktualisierte Zeitlimit wird angegeben
        open_File.close()
        time.sleep(2.5)   #2.5 Sekunden Verzögerung, damit der User Zeit zum Lesen hat
        optionen()      #Rückkehr zu Optionen
    elif benutzer_input == "n":

        optionen()      #Rückkehr zu Optionen
    else:
        print("Eingabe stimmt nicht überein.")
        zeitlimit()         #erneuter Aufruf der Funktion Zeitlimit(), wenn Eingabe nicht mit den Optionen übereinstimmt




def showTitel():                #Titel anzeigen und Passwort in Zwischenablage speichern
    if getsys():
        path = os.chdir(pfad + "\\PManager\\passwords")  # ändern des Dateipfads in den Ordner 'passwords'
    else:
        path = os.chdir(pfad + "/PManager/passwords") #ändern des Dateipfads in den Ordner 'passwords'
    list = os.listdir(path)
    if list != []:
        print("")
        print("Titel:")
        for titel in os.listdir(path):      #Anzeigen aller Titel
            print(titel)
        print("")
        inp = input("Möchten Sie ein Passwort kopieren?y/n\t").lower()      #Abfrage Passwort kopieren
        if inp == "y":
            name = input("Welcher Titel?\t")
            if check(name):
                Tipa = open(name + ".txt", "r")         #Titel muss ohne '.txt' eingegeben werden
                Tipa = Tipa.read().splitlines()         #Benutzername und Passwort werden Zeilenweise getrennt
                User=Tipa[0]        #Speichern des Benutzernamens in 'User'
                Password=Tipa[1]        #Speichern des Passworts in 'Password
                print("Username: " + User + " | Password copied to clipboard.")     #Ausgeben des Benutzernamens
                if getsys():
                    r = Tk()
                    r.withdraw()
                    r.clipboard_clear()
                    r.clipboard_append(Password)                #Speichern des Passworts in der Zwischenablage
                    r.update()
                    countdown_thread = threading.Thread(target = countdown)
                    countdown_thread.start()                                   #Starten des threads 'countdown' (nach 30 Sekunden wird das Passwort aus
                    Back()   #Rückkehr zu Optionen                             #der Zwischenablage gelöscht
                else:
                    try:
                        r = Tk()
                        r.withdraw()
                        r.clipboard_clear()
                        r.clipboard_append(Password)  # Speichern des Passworts in der Zwischenablage
                        r.update()
                        countdown_thread = threading.Thread(target=countdown)
                        countdown_thread.start()  # Starten des threads 'countdown' (nach 30 Sekunden wird das Passwort aus
                        Back()  # Rückkehr zu Optionen                             #der Zwischenablage gelöscht
                    except Exception:
                        Back()

            else:
                print("der eingegebene Titel ist nicht vorhanden")
                showTitel()
        elif inp == "n":
            optionen()      #Rückkehr zu Optionen
        else:
            print("Eingabe stimmt nicht überein.")
            showTitel()     #erneutes Aufrufen der Funktion 'ShowTitel'
    else:
        print("es sind noch keine Titeln vorhanden\n")
        time.sleep(0.5)
        optionen()




def delete():            #Löschen von Titeln
    if getsys():
        path = os.chdir(pfad + "\\PManager\\passwords")  # ändern des Dateipfads in den Ordner 'passwords'
        os.chdir(pfad + "\\PManager\\passwords")
    else:
        path = os.chdir(pfad + "/PManager/passwords")  # ändern des Dateipfads in den Ordner 'passwords'
        os.chdir(pfad + "/PManager/passwords")

    list = os.listdir(path)
    if list != []:
        print("")
        print("Titel:")                      #--> Listet alle Titel im Ordner 'passwords' auf
        for x in range(len(list)):
            print(list[x])
        print("")
       # os.chdir(pfad+"\\PManager\\passwords") #Ändert Dateizugriff, sodass Titel bearbeitet werden können
        delTitel = input("Welcher Titel soll gelöscht werden?('e' zum zurückkehren)\t")+".txt"    #Auswahl des Titels + sparen des .txt
        if delTitel =="e.txt":   #Zurück ins Menü
            optionen()
        elif os.path.exists(delTitel):              #Überprüft, ob Eingabe existiert
            if input("Sind Sie sicher?y/n\t").lower() == "y":
                os.remove(delTitel)                 #Löscht titel
                print("Titel erfolgreich gelöscht.")
                optionen()
            else:
                optionen()
        else:
            print("Dieser Titel existiert nicht.\n")
            delete()            #erneutes Aufrufen der Funktion 'Delete()'
    else:
        print("Sie haben noch keine Titeln hinzugefügt!\n")
        time.sleep(0.5)
        optionen()


def  addTitel():         #Titel hinzufügen und neues Passwort erstellen
        name = input("Neuer Titel('e' um zurückzukehren.):\t").lower()
        if getsys():
            os.chdir(pfad + "\\PManager\\passwords")        #ändern des Dateipfads in den Ordner 'passwords'
            path = os.getcwd()
        else:
            os.chdir(pfad + "/PManager/passwords")  # ändern des Dateipfads in den Ordner 'passwords'
            path = os.getcwd()


        if name == "e":
            optionen()      #Rückkehr zu Optionen

        elif check(name)==False:

            newTitel = open(name + ".txt", "w+")        #Erstellen der neuen Datei
            newTitel.close()
            newTitel = open(name + ".txt", "a")         #öffnen der Datei
            newTitel.write(input("Geben Sie den Benutzernamen der Anwendung ein:\t"))       #Hinzufügen des Benutzernamens
            newTitel.close()
            addPass(name)       #Hinzufügen eines neuen Passworts durch die Funktion addPass(name)
        else:
            print("Titel schon vorhanden. Bitte anderen Titelnamen hinzufügen.")
            optionen()


def Back():
        print("")
        inp = input("Geben Sie 'e' ein, um zurückzukehren.\t")      #Funktion, um den User zurück zu den Optionen zu bringen
        if inp == "e":                                              #sobald 'e' einegegeben
            optionen()
        else:
            print("Eingabe stimmt nicht überein.")
            Back()


def addPass(name):
        open_pass_File = open(name +".txt", "a")              #Öffnen der Datei, für welche das Passwort erstellt werden soll
        open_pass_File.write("\r"+passwortErstellung())       #Erstellen des Passworts durch die Funktion PasswortErstellung()
        print("Neues Passwort angelegt.")
        time.sleep(1)

def change_Master_Passwort():
        inp = input("Wollen Sie wirklich ihr Master-Passwort ändern?y/n\t").lower() #erneute Bestätigung des Users
        if inp == "y":
            neu = input("Neues Passwort:\t")
            neu2 = input("Neues Passwort wiederholen:\t")       #doppelte Eingabe des neuen Passworts, um Schreibfehler vorzubeugen
            if neu == neu2:     #Überprüfung, ob beide Eingaben identisch sind
                if neu._contains_(" ") or neu =="":
                    print("Passwort darf nicht leer oder nur aus Leerzeichen bestehen!")
                    time.sleep(3)
                    optionen()

                if getsys():
                    os.chdir(pfad+"\\PManager\\MasterPW")   #ändern des Datei-Pfads in den Ordner 'MasterPW'
                    w = open("MasterPW.txt", "w")       #öffnen der Text-Datei, in welcher das MasterPW gespeichert ist
                    w.write(neu)        #Überschreiben des alten MasterPW mit dem neuen MasterPW
                    w.close()
                    print("Master-Passwort erfolgreich geändert.")
                    optionen()      #Rückkehr Optionen
                else:
                    os.chdir(pfad + "/PManager/MasterPW")  # ändern des Datei-Pfads in den Ordner 'MasterPW'
                    w = open("MasterPW.txt", "w")  # öffnen der Text-Datei, in welcher das MasterPW gespeichert ist
                    w.write(neu)  # Überschreiben des alten MasterPW mit dem neuen MasterPW
                    w.close()
                    print("Master-Passwort erfolgreich geändert.")
                    optionen()  # Rückkehr Optionen

            else:
                print("Eingaben stimmen nicht überein.")
                change_Master_Passwort()    #Erneuter Aufruf der Funktion chMWP()


        elif inp == "n":
            optionen()      #Rückkehr Optionen
        else:
            print("Eingabe stimmt nicht überein.")
            change_Master_Passwort()     #Erneuter Aufruf der Funktion chMWP()


def passwortErstellung():
    benutzer_eingabe= input("Möchten Sie das Passwort automatisch generieren lasssen? y/n\t").lower()
    if benutzer_eingabe == "n":
        neues_Password=input("Neues Passwort eingeben:\t ")
        return neues_Password
    elif benutzer_eingabe =="y":

        def scanner_PW_Length():  # um die Länge des Passwords aufzunehmen

            length = 0
            for_ever = True
            try:
                length = int(input("Wie lange soll das Password sein?\t"))
                return length
            except Exception:
                print("Error!\nBitte nur Zahlen eingeben!")
                scanner_PW_Length()

        password_Length = scanner_PW_Length()

        def scanner_Number_Check():  # um zu erfahren ob der Benutzer Zahlen im Password haben möchte
            str = ""
            str = input("Möchten Sie Zahlen im PW haben?y/n\t").lower()
            for_ever = True
            while for_ever:
                if str == 'y':
                    for_ever = False
                    return True
                elif str == 'n':
                    for_ever = False
                    return False
                else:
                    print("Falsche Eingabe!")
                    str = input("Möchten Sie Zahlen im PW haben(Bitte richtige Eingabe)?y/n\t").lower()

        boolean_Number = scanner_Number_Check()

        def scanner_Uppercase_Check():  # um zu erfahren ob der Benutzer große Buchstaben im Password haben möchte
            str = ""
            str = input("Möchten Sie große Buchstaben im PW haben?y/n\t").lower()
            for_ever = True
            while for_ever:
                if str == 'y':
                    for_ever = False
                    return True
                elif str == 'n':
                    for_ever = False
                    return False
                else:
                    print("Falsche Eingabe!")
                    str = input("Möchten Sie große Buchstabe im PW haben(Bitte richtige Eingabe)?y/n\t").lower()

        boolean_GroßLetter = scanner_Uppercase_Check()

        def scanner_Signs_Check():  # um zu erfahren ob der Benutzer Sonderzeichen im Password haben möchte
            str = ""
            str = input("Möchten Sie Sonderzeichen im PW haben?y/n\t").lower()
            for_ever = True
            while for_ever:
                if str == 'y':
                    for_ever = False
                    return True
                elif str == 'n':
                    for_ever = False
                    return False
                else:
                    print("Falsche Eingabe!")
                    str = input("Möchten Sie Sonderzeichen im PW haben(Bitte richtige Eingabe)?y/n\t").lower()

        boolean_Sonderzeichen = scanner_Signs_Check()

        def password(length, boolean_Number, boolean_GroßLetter, boolean_Sonderzeichen):
            str = ""
            if boolean_Number:  # Überprüfung ob der Benutzer zahlen im PW haben möchte
                if boolean_GroßLetter:  # Überprüfung ob der Benutzer große oder kleine Buchstaben im PW haben möchte
                    if boolean_Sonderzeichen:  # Überprüfung ob der Benutzer Sonderzeichen im PW haben möchte
                        for i in range(length):
                            str += random.choice(string.ascii_uppercase + string.digits + string.punctuation)
                    else:
                        for i in range(length):
                            str += random.choice(string.ascii_letters + string.digits)

                else:
                    for i in range(length):
                        str += random.choice(string.ascii_lowercase + string.digits)
            else:  # Überprüfen Falls keine Numbers erwünscht sind__

                if boolean_GroßLetter and boolean_Sonderzeichen:
                    for i in range(length):
                        str += random.choice(string.ascii_uppercase + string.punctuation)

                else:
                    if boolean_GroßLetter and boolean_Sonderzeichen != True:
                        for i in range(length):
                            str += random.choice(string.ascii_letters)

                    elif boolean_Sonderzeichen and boolean_GroßLetter != True:
                        for i in range(length):
                            str += random.choice(string.ascii_lowercase + string.punctuation)
                    else:
                        for i in range(length):
                            str += random.choice(string.ascii_lowercase)

            # print(str)
            return str

        return password(password_Length, boolean_Number, boolean_GroßLetter, boolean_Sonderzeichen)
    else:
        print("Falsche Eingabe!!")
        return passwortErstellung()




def  anmeldung():
    if os.path.exists("PManager") != True:  # Überprüft, ob Ordner PManager existiert. Wenn nicht --> erstmaliges Starten --> Masterpw Eingabe
        print("Willkommen.")
        benutzer_password = input("Geben Sie ihr Masterpasswort ein:\t")  # Eingabe des MasterPW1
        if benutzer_password._contains_(" ") or benutzer_password =="": #U m zu vermeiden, dass das Password nicht aus Leerzeichen oder nichts bestehen
            print("das Passwort darf nicht über leerzeichen verfügen oder aus nichts oder Leerzeichen bestehen!!\nSie müssen ein richtiges Passwort eingeben!!\n")
            time.sleep(0.5)
            anmeldung()
        else:
            make_Directory() # Funktion zur Erstellung von den notwendigen Ordnern und Datei-Pfaden
            if getsys():
                masterPassword_from_file = open(pfad + "\\PManager\\MasterPW\\MasterPW.txt","w+")  # Erstellen der Textdatei, in welcher das MasterPW gespeichert wird
                masterPassword_from_file.write(benutzer_password)  # MasterPW wird in Textdatei gespeichert
                masterPassword_from_file.close()
                default_Zeit_Datei = open(pfad + "\\PManager\\Zeitlimit\\Zeitlimit.txt", "w+")  # default Zeitlimit wird gespeichert
                default_Zeit_Datei.write("5")
                default_Zeit_Datei.close()
            else:
                masterPassword_from_file = open(pfad + "/PManager/MasterPW/MasterPW.txt",
                                                "w+")  # Erstellen der Textdatei, in welcher das MasterPW gespeichert wird
                masterPassword_from_file.write(benutzer_password)  # MasterPW wird in Textdatei gespeichert
                masterPassword_from_file.close()
                default_Zeit_Datei = open(pfad + "/PManager/Zeitlimit/Zeitlimit.txt",
                                          "w+")  # default Zeitlimit wird gespeichert
                default_Zeit_Datei.write("5")
                default_Zeit_Datei.close()

            thread()  # Funktion, welche countdown2() startet --> Zeitlimit
            optionen()  # Rückkehr zu Optionen

    else:  # Normale Anmeldung ab 2. Starten des Programms
        try:
            if getsys():
                open_Master_Password_File = open(pfad + "\\PManager\\MasterPW\\MasterPW.txt", "r")  # öffnet Datei mit Mpw
                masterPassword_from_file = open_Master_Password_File.read()  # Liest das Mpw aus der Datei

                benutzer_passwort = getpass("Bitte geben Sie ihr Passwort ein:\t")

                if master_passwort_check(benutzer_passwort, count, masterPassword_from_file):  # Abfrage des MasterPW
                    print("Willkommen.")
                    thread()  # Funktion, welche countdown2() startet --> Zeitlimit
                    optionen()  # Rückkehr zu Optionen
                else:
                    exit()
            else:
                open_Master_Password_File = open(pfad + "/PManager/MasterPW/MasterPW.txt",
                                                 "r")  # öffnet Datei mit Mpw
                masterPassword_from_file = open_Master_Password_File.read()  # Liest das Mpw aus der Datei

                benutzer_passwort = getpass("Bitte geben Sie ihr Passwort ein:\t")

                if master_passwort_check(benutzer_passwort, count, masterPassword_from_file):  # Abfrage des MasterPW
                    print("Willkommen.")
                    thread()  # Funktion, welche countdown2() startet --> Zeitlimit
                    optionen()  # Rückkehr zu Optionen
                else:
                    exit()

        except Exception as e:
            print(e.args)
            print("\nleider wurde offensichtlich eine für das Programm relevante Datei gelöscht\n")
            time.sleep(1)
            if getsys():
                if os.path.exists(pfad+"\\PManager"+"\\MasterPW"):
                    shutil.rmtree(pfad +"\\PManager"+"\\MasterPW")
                    time.sleep(1)
            else:
                if os.path.exists(pfad + "/PManager" + "/MasterPW"):
                    shutil.rmtree(pfad + "/PManager" + "/MasterPW")
                    time.sleep(1)

            exceptionHandling() #Um Recovery durchführen zu können




def exceptionHandling():
    eingabe = input("Möchten Sie eine Recovery durchführen, indem Sie ein neues Password für das Programm erstellen müssen?y/n\t")
    if eingabe =="y":
        if getsys():
            os.chdir(pfad + "\\PManager")  # ändert Dateien-Pfad
            os.makedirs("MasterPW")  # erstellt Ordner 'MasterPW' in Ordner 'PManager'
            benutzer_passwort = input("Geben Sie ihr Masterpasswort ein:\t")  # Eingabe des MasterPW1
        else:
            os.chdir(pfad + "/PManager")  # ändert Dateien-Pfad
            os.makedirs("MasterPW")  # erstellt Ordner 'MasterPW' in Ordner 'PManager'
            benutzer_passwort = input("Geben Sie ihr Masterpasswort ein:\t")  # Eingabe des MasterPW1
        if benutzer_passwort._contains_(" ") or benutzer_passwort == "":
            print("das geht gar nicht")
            anmeldung()
        else:
            if getsys():
                masterPassword_Datei = open(pfad + "\\PManager\\MasterPW\\MasterPW.txt","w+")  # Erstellen der Textdatei, in welcher das MasterPW gespeichert wird
                masterPassword_Datei.write(benutzer_passwort)  # MasterPW wird in Textdatei gespeichert
                masterPassword_Datei.close()
                #default_Zeit_Datei = open(pfad + "\\PManager\\Zeitlimit\\Zeitlimit.txt",
                #                "w+")  # default Zeitlimit wird gespeichert
                #default_Zeit_Datei.write("5")
                #default_Zeit_Datei.close()
                thread()  # Funktion, welche countdown2() startet --> Zeitlimit
                optionen()  # Rückkehr zu Optionen
            else:
                masterPassword_Datei = open(pfad + "/PManager/MasterPW/MasterPW.txt",
                                            "w+")  # Erstellen der Textdatei, in welcher das MasterPW gespeichert wird
                masterPassword_Datei.write(benutzer_passwort)  # MasterPW wird in Textdatei gespeichert
                masterPassword_Datei.close()
                thread()  # Funktion, welche countdown2() startet --> Zeitlimit
                optionen()  # Rückkehr zu Optionen


    elif eingabe == "n":
        last_question = input("Sind Sie sicher? Alle Ihre Daten werden unwiderruflich gelöscht.y/n\t")
        if last_question=="y":
            print("Alle Daten gelöscht, das Programm wird beendet")
            if getsys():
                shutil.rmtree(pfad + "\\PManager")
                os.execl(sys.executable, sys.executable, *sys.argv)
            else:
                shutil.rmtree(pfad + "/PManager")
                os.execl(sys.executable, sys.executable, *sys.argv)


        elif last_question=="n":
            exceptionHandling()
        else:
            print("Falsche Eingabe!")
            time.sleep(1)
            exceptionHandling()
    else:
        print("Falsche eingabe! bitte richtig eingeben!!")
        time.sleep(2)
        exceptionHandling()

def thread():
        countdown_thread = threading.Thread(target=countdown2)      #starten des threads 'countdown2()'
        countdown_thread.start()


def check(name): #zur Überprüfung, ob der eingegebene Titel schon vorhanden ist oder nicht
    if getsys():

        path = os.chdir(pfad + "\\PManager\\passwords")
    else:
        path = os.chdir(pfad + "/PManager/passwords")

    list = os.listdir(path)
    if list == []:
        return False
    for titel in os.listdir(path):
        if titel == name+".txt":

            time.sleep(1.5)
            return True
        else:
            return False


#Main-Programm

anmeldung()    #Aufrufen der Funktion Anmeldung()
