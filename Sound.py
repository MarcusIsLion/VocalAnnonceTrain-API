import time
from pydub import AudioSegment
import os
from pydub.playback import play
from tkinter import messagebox, Tk, Entry, Label, Button, StringVar, IntVar, OptionMenu, Toplevel, filedialog, Menu
from flask import Flask, Response
import random

def GetStationAudio():
    # je génère un nombre aléatoire en 1 et 10000, si le nombre est égal à 434 je choisis le jingle spécial
    random_number = random.randint(1, 10000)
    if random_number == 435:
        return "Sound/Jingle/StationEasterEgg.mp3"
    else:
        return "Sound/Jingle/Station.mp3"

def Generate_Depart_Annonce(train_name, train_number, plateform_type, plateform_indicator, arrival_station, departure_Hours, departure_Minutes, TypeJingle):
    audio = True

    depart_sidding = plateform_type + plateform_indicator

    # Obtenez les chemins des fichiers audio correspondants
    if os.path.exists(f"Sound/TrainName/{train_name}.mp3"):
        train_name_path = f"Sound/TrainName/{train_name}.mp3"
        train_name_audio = AudioSegment.from_mp3(train_name_path)
    else:
        train_name_audio = AudioSegment.silent(duration=0)
        audio = False

    if os.path.exists(f"Sound/Station/{arrival_station}.mp3"):
        arrival_station_path = f"Sound/Station/{arrival_station}.mp3"
        arrival_station_audio = AudioSegment.from_mp3(arrival_station_path)
    else:
        arrival_station_audio = AudioSegment.silent(duration=0)
        audio = False

    if os.path.exists(f"Sound/Hours/{departure_Hours}.mp3"):
        departure_Hours_path = f"Sound/Hours/{departure_Hours}.mp3"
        departure_Hours_audio = AudioSegment.from_mp3(departure_Hours_path)
    else:
        departure_Hours_audio = AudioSegment.silent(duration=0)
        audio = False

    if os.path.exists(f"Sound/Minutes/{departure_Minutes}.mp3"):
        departure_Minutes_path = f"Sound/Minutes/{departure_Minutes}.mp3"
        departure_Minutes_audio = AudioSegment.from_mp3(departure_Minutes_path)
    else:
        departure_Minutes_audio = AudioSegment.silent(duration=0)
        audio = False

    if os.path.exists(f"Sound/Jingle/{TypeJingle}.mp3"):
        if TypeJingle == "Station":
            jingle_path = GetStationAudio()
        else:
            jingle_path = f"Sound/Jingle/{TypeJingle}.mp3"
        jingle_audio = AudioSegment.from_mp3(jingle_path)
    else:
        jingle_audio = AudioSegment.silent(duration=0)
        audio = False

    # Découpez le numéro de train en milliers, centaines, dizaines et unités
    train_number_str = str(train_number).zfill(4)  # Assurez-vous que la longueur est de 4 chiffres
    thousands_digit = train_number_str[0] + "000"
    hundreds_digit = train_number_str[1] + "00"
    tens_digit = train_number_str[2] + "0"
    units_digit = train_number_str[3]

    if thousands_digit != "0":
        # Obtenez les chemins des fichiers audio pour les milliers, centaines, dizaines et unités
        if os.path.exists(f"Sound/Number/Thousand/{thousands_digit}.mp3"):
            thousands_path = f"Sound/Number/Thousand/{thousands_digit}.mp3"
            thousands_audio = AudioSegment.from_mp3(thousands_path)
        else:
            thousands_audio = AudioSegment.silent(duration=0)
            audio = False
    else:
        thousands_audio = AudioSegment.silent(duration=0)
        audio = False
    if hundreds_digit != "0":
        if os.path.exists(f"Sound/Number/Hundred/{hundreds_digit}.mp3"):
            hundreds_path = f"Sound/Number/Hundred/{hundreds_digit}.mp3"
            hundreds_audio = AudioSegment.from_mp3(hundreds_path)
        else:
            hundreds_audio = AudioSegment.silent(duration=0)
            audio = False
    else:
        hundreds_audio = AudioSegment.silent(duration=0)
        audio = False
    if tens_digit != "0":
        if os.path.exists(f"Sound/Number/Ten/{tens_digit}.mp3"):
            tens_path = f"Sound/Number/Ten/{tens_digit}.mp3"
            tens_audio = AudioSegment.from_mp3(tens_path)
        else:
            tens_audio = AudioSegment.silent(duration=0)
            audio = False
    else:
        tens_audio = AudioSegment.silent(duration=0)
        audio = False
    if units_digit != "0":
        if os.path.exists(f"Sound/Number/Unit/{units_digit}.mp3"):
            units_path = f"Sound/Number/Unit/{units_digit}.mp3"
            units_audio = AudioSegment.from_mp3(units_path)
        else:
            units_audio = AudioSegment.silent(duration=0)
            audio = False
    else:
        units_audio = AudioSegment.silent(duration=0)
        audio = False

    train_number_audio = thousands_audio + hundreds_audio + tens_audio + units_audio

    # je découpe l'entrée de la plateforme qui est composée d'une lettre et d'un chiffre ou d'une lettre et je le stocke dans 2 variables
    if depart_sidding != "":
        depart_sidding = depart_sidding.upper()
        depart_sidding_letter = depart_sidding[0]
        depart_sidding_indicator = depart_sidding[1]

        if depart_sidding_letter != "":
            if os.path.exists(f"Sound/Sidding/SiddingType/{depart_sidding_letter}.mp3"):
                depart_sidding_letter_path = f"Sound/Sidding/SiddingType/{depart_sidding_letter}.mp3"
                depart_sidding_letter_audio = AudioSegment.from_mp3(depart_sidding_letter_path)
            else:
                depart_sidding_letter_audio = AudioSegment.silent(duration=0)
                audio = False
        else:
            depart_sidding_letter_audio = AudioSegment.silent(duration=0)
            audio = False
        if depart_sidding_indicator != "":

            # je vérifie sur l'indicateur est un chiffre ou une lettre :
            if depart_sidding_indicator.isalpha():
                if os.path.exists(f"Sound/Sidding/Alphabet/{depart_sidding_indicator}.mp3"):
                    depart_sidding_indicator_path = f"Sound/Sidding/Alphabet/{depart_sidding_indicator}.mp3"
                    depart_sidding_indicator_audio = AudioSegment.from_mp3(depart_sidding_indicator_path)
                    audio = True
                else:
                    depart_sidding_indicator_audio = AudioSegment.silent(duration=0)
                    audio = False
            else:
                if os.path.exists(f"Sound/Sidding/Number/{depart_sidding_indicator}.mp3"):
                    depart_sidding_indicator_path = f"Sound/Sidding/Number/{depart_sidding_indicator}.mp3"
                    depart_sidding_indicator_audio = AudioSegment.from_mp3(depart_sidding_indicator_path)
                    audio = True
                else:
                    depart_sidding_indicator_audio = AudioSegment.silent(duration=0)
                    audio = False
        else:
            depart_sidding_indicator_audio = AudioSegment.silent(duration=0)
            audio = False
    else:
        depart_sidding_letter_audio = AudioSegment.silent(duration=0)
        depart_sidding_indicator_audio = AudioSegment.silent(duration=0)
        audio = False

    partira_audio = AudioSegment.from_mp3("Sound/Words/Partira.mp3")
    a_audio = AudioSegment.from_mp3("Sound/Words/A.mp3")

    if audio:
        # Concaténez les fichiers audio
        voicemail = jingle_audio + train_name_audio + train_number_audio + arrival_station_audio + partira_audio + depart_sidding_letter_audio + depart_sidding_indicator_audio + a_audio + departure_Hours_audio + departure_Minutes_audio

        # Convertissez le message vocal en bytes
        voicemail_bytes = voicemail.export(format="mp3").read()

        # Renvoyez le son en tant que réponse HTTP
        return Response(voicemail_bytes, mimetype="audio/mpeg")

    else:
        return False

def Generate_Passing_Train(Sidding_type, Sidding_indicator):
    Sidding_type_path = f"Sound/Sidding/SiddingType/{Sidding_type}.mp3"
    Sidding_type_audio = AudioSegment.from_mp3(Sidding_type_path)
    if Sidding_indicator.isalpha():
        Sidding_indicator_path = f"Sound/Sidding/Alphabet/{Sidding_indicator}.mp3"
        Sidding_indicator_audio = AudioSegment.from_mp3(Sidding_indicator_path)
    else:
        Sidding_indicator_path = f"Sound/Sidding/Number/{Sidding_indicator}.mp3"
        Sidding_indicator_audio = AudioSegment.from_mp3(Sidding_indicator_path)

    jingle_audio = AudioSegment.from_mp3(GetStationAudio())
    voicemail = jingle_audio + Sidding_type_audio + Sidding_indicator_audio + AudioSegment.from_mp3("Sound/Sentence/PassingTrain.mp3")

    voicemail_bytes = voicemail.export(format="mp3").read()

    return Response(voicemail_bytes, mimetype="audio/mpeg")

def Generate_Delete_Train(train_name, train_number, train_destination, departure_Hours, departure_Minutes):

    if os.path.exists(f"Sound/TrainName/{train_name}.mp3"):
        train_name_path = f"Sound/TrainName/{train_name}.mp3"
        train_name_audio = AudioSegment.from_mp3(train_name_path)
    else:
        train_name_audio = AudioSegment.silent(duration=0)

    if os.path.exists(f"Sound/Station/{train_destination}.mp3"):
        train_destination_path = f"Sound/Station/{train_destination}.mp3"
        train_destination_audio = AudioSegment.from_mp3(train_destination_path)
    else:
        train_destination_audio = AudioSegment.silent(duration=0)

    if os.path.exists(f"Sound/Hours/{departure_Hours}.mp3"):
        departure_Hours_path = f"Sound/Hours/{departure_Hours}.mp3"
        departure_Hours_audio = AudioSegment.from_mp3(departure_Hours_path)
    else:
        departure_Hours_audio = AudioSegment.silent(duration=0)

    if os.path.exists(f"Sound/Minutes/{departure_Minutes}.mp3"):
        departure_Minutes_path = f"Sound/Minutes/{departure_Minutes}.mp3"
        departure_Minutes_audio = AudioSegment.from_mp3(departure_Minutes_path)
    else:
        departure_Minutes_audio = AudioSegment.silent(duration=0)

    # Découpez le numéro de train en milliers, centaines, dizaines et unités
    train_number_str = str(train_number).zfill(4)  # Assurez-vous que la longueur est de 4 chiffres
    thousands_digit = train_number_str[0] + "000"
    hundreds_digit = train_number_str[1] + "00"
    tens_digit = train_number_str[2] + "0"
    units_digit = train_number_str[3]

    if thousands_digit != "0":
        # Obtenez les chemins des fichiers audio pour les milliers, centaines, dizaines et unités
        if os.path.exists(f"Sound/Number/Thousand/{thousands_digit}.mp3"):
            thousands_path = f"Sound/Number/Thousand/{thousands_digit}.mp3"
            thousands_audio = AudioSegment.from_mp3(thousands_path)
        else:
            thousands_audio = AudioSegment.silent(duration=0)
    else:
        thousands_audio = AudioSegment.silent(duration=0)
    if hundreds_digit != "0":
        if os.path.exists(f"Sound/Number/Hundred/{hundreds_digit}.mp3"):
            hundreds_path = f"Sound/Number/Hundred/{hundreds_digit}.mp3"
            hundreds_audio = AudioSegment.from_mp3(hundreds_path)
        else:
            hundreds_audio = AudioSegment.silent(duration=0)
    else:
        hundreds_audio = AudioSegment.silent(duration=0)
    if tens_digit != "0":
        if os.path.exists(f"Sound/Number/Ten/{tens_digit}.mp3"):
            tens_path = f"Sound/Number/Ten/{tens_digit}.mp3"
            tens_audio = AudioSegment.from_mp3(tens_path)
        else:
            tens_audio = AudioSegment.silent(duration=0)
    else:
        tens_audio = AudioSegment.silent(duration=0)
    if units_digit != "0":
        if os.path.exists(f"Sound/Number/Unit/{units_digit}.mp3"):
            units_path = f"Sound/Number/Unit/{units_digit}.mp3"
            units_audio = AudioSegment.from_mp3(units_path)
        else:
            units_audio = AudioSegment.silent(duration=0)
    else:
        units_audio = AudioSegment.silent(duration=0)

    train_number_audio = thousands_audio + hundreds_audio + tens_audio + units_audio

    jingle_audio = AudioSegment.from_mp3(GetStationAudio())
    voicemail = jingle_audio + AudioSegment.from_mp3("Sound/Sentence/Train Abord/TrainAbord_part1.mp3") + train_name_audio + AudioSegment.from_mp3("Sound/Sentence/Train Abord/TrainAbord_part2.mp3") + train_number_audio + AudioSegment.from_mp3("Sound/Sentence/Train Abord/TrainAbord_part3.mp3") + train_destination_audio + AudioSegment.from_mp3("Sound/Sentence/Train Abord/TrainAbord_part4.mp3") + departure_Hours_audio + departure_Minutes_audio + AudioSegment.from_mp3("Sound/Sentence/Train Abord/TrainAbord_part5.mp3")

    voicemail_bytes = voicemail.export(format="mp3").read()

    return Response(voicemail_bytes, mimetype="audio/mpeg")

def AlarmSignal(train_name):
    alarm_audio = AudioSegment.from_mp3("Sound/Sentence/AlarmSignal.mp3")
    Jingle_audio = AudioSegment.silent(duration=0)
    if train_name == "TGV":
        Jingle_audio += AudioSegment.from_mp3("Sound/Jingle/IBTGV.mp3")
    elif train_name == "TER":
        Jingle_audio += AudioSegment.from_mp3("Sound/Jingle/IBTER.mp3")

    voicemail = Jingle_audio + alarm_audio

    voicemail_bytes = voicemail.export(format="mp3").read()

    return Response(voicemail_bytes, mimetype="audio/mpeg")

def GenerateStrike():
    voicemail = AudioSegment.from_mp3(GetStationAudio()) + AudioSegment.from_mp3("Sound/Sentence/Strike.mp3")

    voicemail_bytes = voicemail.export(format="mp3").read()

    return Response(voicemail_bytes, mimetype="audio/mpeg")

def GenerateDynamicDisplayOff():
    voicemail = AudioSegment.from_mp3(GetStationAudio()) + AudioSegment.from_mp3("Sound/Sentence/DynamicDisplayOff.mp3")

    voicemail_bytes = voicemail.export(format="mp3").read()

    return Response(voicemail_bytes, mimetype="audio/mpeg")