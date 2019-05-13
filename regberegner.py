#Definer custom errors som en række classes. Tro mig, det bliver mere overskueligt sådan her.

class ElbilError (Exception):
  def __init__(self):
    print("Desværre understøtter min janky-ass beregner ikke el- og brintbiler. Sorry mang.")
    quit()
class AfgiftsError (Exception):
  def __init__(self):
    print("Skriv venligst kun y eller n på prisen er afgiftspligtig.")
    quit()
class DataError (Exception):
  def __init__(self):
    print("Der er noget galt med dine data. Prøv igen.")
class GenError(DataError):
  def __init__(self):
    DataError().__init__
    print("Fejlkode #1, generisk datafejl. Programmet fik noget andet, end det regnede med - typisk bogstaver i stedet for tal eller omvendt.")
    quit()
class NegError(DataError):
  def __init__(self):
    DataError().__init__
    print("Fejlkode #2, negative tal. Du kan ikke bruge negative tal.")
    quit()
class MomsError(DataError):
  def __init__(self):
    DataError().__init__
    print("Du kan kun svare Y eller N på, om prisen er inkl. moms")
    quit()

#Gather user inputs. Lots and lots of inputs.
try:
  vaerdi = int(input("Hvad er bilens værdi i hele kr? "))
  moms = str(input("Er det inkl. moms? Hvis ja, skriv Y. Ellers, skriv N.").lower())
  afgiftspligtig = input ("Er den værdi allerede den afgiftspligtige værdi? Skriv y eller n. ".lower())
  barnesaede = int(input("Hvor mange integrerede barnesæder har bilen? Hvis der er ingen, så skriv 0 "))
  airbags = int(input("Hvor mange airbags har bilen? "))
  NCAP = int(input("Hvor mange Euro NCAP-stjerner har bilen? "))
  fuel = str(input("Kører bilen på benzin eller diesel? ").lower())
  mpg = float(input("Hvor mange km pr. liter (rundet ned)"))
  selealarmer = int(input("Hvor mange selealarmer har bilen? "))
except:
  raise GenError

#tilføj moms til bilens pris, hvis det ikke er der. Raise MomsError, hvis svaret er mærkeligt.
if moms == "y":
  vaerdi = vaerdi
elif moms == "n":
  vaerdi = vaerdi * 1.25
else:
  raise MomsError

#verdens længste logic check der lige sikrer sig, at data ikke er super whack.
if vaerdi < 0 or barnesaede < 0 or airbags <0 or NCAP < 0 or NCAP > 5 or mpg < 0 or selealarmer < 0:
  raise NegError
else:
  pass

#fastsæt minimumsafgift og definer afgiften
minimumsafgift = 20000
Regafg = 0
#kæmpestor IF-blok, som springer værdijusteringer over, hvis de allerede er lavet. Svares der andet end y eller n (saneret), bliver AfgiftsError raised
if afgiftspligtig == "n":

  #begynd beregninger. Starter med barnesæde
  if barnesaede > 0:
    print("Bilens værdi justeres med " + str(6000 * barnesaede) + " kr på grund af indbyggede barnesæder")
    vaerdi = vaerdi - (6000 * barnesaede)
  else:
    pass

  #beregn airbags
  if airbags == 0:
    vaerdi = vaerdi + 7450
    print ("Bilens værdi justeres med " + "\+ 7450 kr på grund af ingen airbags.")
  elif airbags == 1:
    vaerdi = vaerdi + 3725
    print("Bilens værdi justeres med " + "\+ 3725 kr på grund af kun en airbag")
  elif airbags > 3 and airbags < 6:
    vaerdi = vaerdi - (airbags*1280)
    print("Bilens værdi justeres ned med " + str(airbags*1280) + (" kr på grund af airbags"))
  elif airbags > 6:
    vaerdi = vaerdi - (4*1280)
    print("Bilens værdi justeres ned med 5120 kr pga. airbags")
  else:
    pass

  #beregn EuroNCAP
  if NCAP >= 5:
    vaerdi = vaerdi - 8000
    print("Bilens værdi reduceres med 8000 kr på grund af 5 EuroNCAP stjerner")
elif afgiftspligtig == "y":
  pass
else:
  raise AfgiftsError
  
#første reg.afgift beregning 
if vaerdi < 189200:
  Regafg = vaerdi*0.85
  print("Bilens umiddelbare registeringsafgift er " + str(Regafg) + " beregnet som 0.85 gange bilens værdi")
elif vaerdi >= 189201:
  Regafg = vaerdi*1.5
  print("Bilens umiddelbare registeringsafgift er " + str(Regafg) + " beregnet som 1.5 gange bilens værdi")

#så skal der leges med benzinøkonomi!
if fuel == "benzin":
  if mpg >= 20:
    Regafg = Regafg - (4000*(mpg-20))
    print("Registreringsafgiften reduceres med " + str(4000*(mpg-20)) + " på grund af benzinøkonomi")
  elif mpg < 20:
    Regafg = Regafg + (6000*(20-mpg))
    print("Registreringsafgiften hæves med " + str(6000*(20-mpg)) + " på grund af benzinøkonomi")
elif fuel == "diesel":
  if mpg >= 22:
    regafg = Regafg - (4000*(mpg-22))
    print("Registreringsafgiften reduceres med " + str(4000*(mpg-22)) + " på grund af brændstoføkonomi")
  elif mpg < 22:
    regafg = regafg + (6000*(22-mpg))
    print("Registreringsafgiften hæves med " + str(6000*(22-mpg)) + " på grund af brændstoføkonomi")
else:
  raise ElbilError

#ryk afgiften op på minimumsafgiften, hvis den er for lav
if Regafg < minimumsafgift:
  Regafg = minimumsafgift
  print("Registreringsafgiften er lige nu lavere ned minimumsafgiften på 20.000 kr. Den er derfor sat til 20.000 kr ")
else:
  pass

#selealarmer!
if selealarmer >= 3:
  Regafg = Regafg - (3000)
  print("Registreringsafgiften er blevet reduceret med 3000 på grund af selealarmer")
else:
  Regafg = Regafg - (1000*selealarmer)
  print("Registreringsafgiften er blevet reduceret med " + str(1000*selealarmer) + " kr på grund af selealarmer.")

#print resultatet
print("Bilens afgiftspligtige værdi er " + str(vaerdi) + " og dertil er der " + str(int(Regafg)) + " i registreringsafgift. Den totale pris er derfor " + str(int(Regafg + vaerdi)))
