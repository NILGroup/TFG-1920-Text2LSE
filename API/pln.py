import es_core_news_md
nlp = es_core_news_md.load()
from spacy import displacy

#---------------------------------------------------------#
# Listas con diccionarios divididos por tipo de palabras
#---------------------------------------------------------#

# Si se añade en la oración -> True / Si se elimina de la oración -> False
preposiciones = {"a": False, "al": False, "ante": True, "bajo": True, "cabe": False, "con": True, "contra": True, "de": False, "del": False, "desde": True, "en": False, "entre": True, "hacia": True, "hasta": True, "para": True, "por": True, "según": True, "sin": True, "so": False, "sobre": True, "tras": True, "mediante": False, "durante": True, "versus": False, "vía": False}

palabrasTiempo = {"segundo", "minuto", "hora", "día", "semana", "mes", "año", "mañana"}

posesivos = {
    "mi":["yo","yo"],"tu":["tu","tu"],"su":["él","ella"],
    "mis":["yo","yo"],"tus":["tu","tu"],
    "nuestro":["nosotros","nosotras"],"vuestro":["vosotros","vosotras"],"sus": ["ellos","ellas"],
    "nuestra":["nosotros","nosotras"],"vuestra":["vosotros","vosotras"],
    "nuestros":["nosotros","nosotras"],"vuestros":["vosotros","vosotras"],
    "nuestras":["nosotros","nosotras"],"vuestras":["vosotros","vosotras"]
}

reflexivos = {"me","te","se","nos","os"}

adverbios = {
    "tiempo": ["antes", "después", "luego", "pronto", "tarde", "temprano", "todavía", "aún", "ya", "ayer", "hoy", "mañana", "anteayer", 
              "siempre", "nunca", "jamás", "próximamente", "prontamente", "anoche", "enseguida", "ahora", "mientras", "anteriormente", "semana pasada"
              "antes de ayer", "año pasado", "próxima semana", "próximo año"],

    "cantidad": ["muy", "poco", "mucho", "bastante", "más", "menos", "algo", "demasiado", "casi", "solo", "solamente", "tan", "tanto", 
                "todo", "nada", "aproximadamente"],

    "negacion": ["no","nunca","jamás","tampoco"]
}
#---------------------------------------------------------#
# Función que convierte en JSON los tags de un token de spacy
#---------------------------------------------------------#
def splitTags(string):
    dic = dict()

    pos = string[0:string.find("_")]
    tags = string[string.rfind("_")+1:len(string)]

    if (len(tags) > 0) and ("|" in string):
        tags = tags.split("|")
    else:
        tags = tags.split(" ")

    #Inserta en el diccionario los datos de la lista en forma Key:Value
    if len(pos) > 0:
        dic.setdefault("Pos",pos)
    if len(tags) > 1:
        for tag in tags:
            dic.setdefault(tag.split("=")[0],tag.split("=")[1])

    return dic

#---------------------------------------------------------#
# Función devuelve si un token contiene un tag específico
#---------------------------------------------------------#
def keyexits(key,diccionario):
    if key in diccionario:
        return True
    return False

#---------------------------------------------------------#
# Función devuelve el valor de un tag de un token específico
#---------------------------------------------------------#
def getKeyValue(key,dic):
    if(keyexits(key,dic)):
        return dic[key]

#---------------------------------------------------------#
#Función que devuelve el PronPers asociado al DetPos
#---------------------------------------------------------#
def detPosToPronPers(child):
    if child.text.lower() in posesivos:
        return posesivos.get(child.text.lower(),False)

#---------------------------------------------------------#
# Función que devuelve si se añade o no una preposición a la oración final en LSE
#---------------------------------------------------------#
def getIfAddPreposition (child):
  return preposiciones[child.text]
      
#---------------------------------------------------------#
# Función que devuelve si se añade o no un determinante a la oración final en LSE
#---------------------------------------------------------#
def getIfAddDeterminant(word):
 
  determinantType = getKeyValue('PronType',splitTags(word.tag_))
  # artículo determinado -> no lo añadimos
  if (determinantType == 'Art'):
    return False
 
  return True
 
 # -------------------------------------------

#---------------------------------------------------------#
# Función que devuelve el diccionario con toda la información de la oración
#---------------------------------------------------------#
def getDiccionarioOracion():
  return diccionario

#---------------------------------------------------------#
# Variables globales
#---------------------------------------------------------#

tiempo = []
sujeto = []
predicado = []
oracion = []
verbo = None
prep = None
diccionario = {}

# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------- MORFOLOGIA -------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
def analisismorfologico(diccionario):

    frase = diccionario["oracion"]
    nueva_frase = []

    hayAdvTiempo = False
    global verbo
    
    for word in frase:
        #-------Si es DET POSESIVO lo sustituyo por el PRONOMBRE PERSONAL correspondiente.----------
        if ((word.pos_ == "DET" or word.pos_ == "PROPN")  and getKeyValue('PronType',splitTags(word.tag_)) == "Prs"):
            new_word = detPosToPronPers(word)
            if (new_word != None):
                  nueva_frase.append(new_word[0]) 

             
            else:
               nueva_frase.append(word.text)
       
        elif(word.pos_=="ADJ"):
          nueva_frase.append(word.lemma_)


        elif(word.pos_ == "ADV" and word.text.lower() in adverbios['tiempo']):
          hayAdvTiempo = True
          nueva_frase.append(word.text)

        elif (word == verbo):
          if(hayAdvTiempo == False and len(tiempo) == 0):
            if(getKeyValue('Tense',diccionario[word.text]) == "Past"):
                nueva_frase.insert(0,'pasado')

            elif(getKeyValue('Tense',diccionario[word.text]) == "Fut"):
              nueva_frase.insert(0,'futuro')
              
          if(verbo.lemma_ != 'ser' and verbo.lemma_ != 'estar' and verbo.lemma_ != 'parecer'):
            nueva_frase.append(word.lemma_)
        else:
          nueva_frase.append(word.text)
        
    return nueva_frase
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------- FUNCIÓN RECURSIVA ROOT -------------------------------------------
# --------------------------------------------------------------------------------------------------------------------

# Función a la que le llega la palabra de la que hay que sacar el árbol y si es parte del sujeto o no esa palabra.
# Define el orden de las pablabras en LSE en función de sus tipos
def subtrees (word, esSujeto, tipoPadre):

  global tiempo
  global sujeto
  global predicado
  global oracion
  global verbo
  global prep
  global diccionario

  añadir = True

  tipoActual = ""
 

  # Si es verbo no lo tratamos ahora -> lo añadimos al final del tratamiento de la oración
  if ((word.dep_ == "ROOT" and word.pos_ == 'VERB') or (word.dep_ == "ROOT" and word.pos_ == 'AUX')):
    verbo = word
    añadir = False

  else:

    if (word.pos_ == 'PRON' and word.text.lower() in reflexivos):
      añadir = False

    # Comprobamos si hay un verbo en la oración -> guardamos su lemma_ si no es ser o estar
    if ((word.dep_ == "cop" and word.pos_ == 'AUX') or word.pos_ == "VERB"):
        verbo = word
        añadir = False

    # ---------------------- CONJUNCIONES O SIGNOS DE PUNTUACIÓN -------------------------- 
    if (word.pos_ == 'CONJ' or word.dep_ == 'punct'):
      añadir = False

    #---------------------- PREPOSICIONES -------------------------- 
    if (word.pos_ == 'ADP'):
      añadir = getIfAddPreposition(word)

    # ---------------------- DETERMINANTES --------------------------
    # Se mira si se añade o no y en la parte de morfología se cambian las palabras, por ejemplo(por pasos) : (oración inicial) mi casa -> (en este paso) casa mi -> (paso morfología) casa mía
    if (word.pos_ == 'DET'): 
      añadir = getIfAddDeterminant(word)
      

   # ------------------------ SUSTANTIVOS ----------------------------
    #  PALABRAS DE TEMPORALIDAD
    # Si hallamos una palabra de temporalidad (semana, año, mes, etc) cogemos todo lo que herede de esta palabra, lo tratamos y lo que quede lo ponemos al principio de la oración
    if (word.pos_ == 'NOUN'):
      if (word.text.lower() in palabrasTiempo):
        tipoActual = "tiempo"

  # ---------------------------------------------------------------------
  # ---------------------------------------------------------------------

  if (tipoActual == ""):
    tipoActual = tipoPadre

  # --------------------- TIEMPO--------------------------

  if (tipoActual == "tiempo"):
    if (añadir == True):  
      tiempo.insert(0, word)
    for child in word.children:
      subtrees(child, True, tipoActual)

  # --------------------- SUJETO--------------------------
  elif (word.dep_ == 'nsubj' or esSujeto):
    if (añadir == True):  
      sujeto.append(word)
    for child in word.children:
      subtrees(child, True, tipoActual)

  # -------------------- PREDICADO ------------------------
  else: 
    if (añadir == True): 
      predicado.append(word)
    for child in word.children:
      subtrees(child, False, tipoActual)


# --------------------------------------------------------------------------------------------------------------------
# ------------------------------------------- FUNCIÓN PRINCIPAL -> LLAMADA A FUNCIÓN RECURSIVA -----------------------
# --------------------------------------------------------------------------------------------------------------------

def TranslateSentence(initSentence):
  
  global tiempo
  global sujeto
  global predicado
  global oracion
  global verbo
  global prep
  global diccionario

  tiempo = []
  sujeto = []
  predicado = []
  oracion = []
  verbo = None
  prep = None
  diccionario = {}

  root = ""
  modificador = None

  doc = nlp(initSentence)

  for token in doc:
    if (token.dep_ == "ROOT"):
      root = token
    
  subtrees(root, False,'root')

  # Vamos añadiendo el sujeto ordenado a la oración
  for suj in sujeto:
    if (suj.dep_ == 'nsubj'):
      oracion.append(suj)
      diccionario["sujeto"] = splitTags(suj.tag_)
    
    elif(suj.dep_ == 'nmod' and suj.pos_ == 'NOUN'):
        modificador = suj
        oracion.append(suj)

    #Si PronType (tag) es Personal(prs) entonces va antes que el sujeto
    elif(getKeyValue('PronType',splitTags(suj.tag_)) == "Prs"):
        if(modificador == None):
          ind = len(oracion)-1
          oracion.insert(ind, suj)
        else:
          oracion.insert(1, suj)

    else:
      oracion.append(suj)

    diccionario[suj.text] = splitTags(suj.tag_)
    diccionario[suj.text].setdefault("lemma", suj.lemma_)
  # Vamos añadiendo el predicado ordenado a la oración
  for pred in predicado:
    if pred.pos_ == "ADV":
      if pred.text.lower() in adverbios['tiempo']:
          oracion.insert(0,pred)
      else:
        oracion.append(pred)
      
    else:
      oracion.append(pred)

    diccionario[pred.text] = splitTags(pred.tag_)
    diccionario[pred.text].setdefault("lemma", pred.lemma_)
  # Vamos añadiendo palabras de tiempo
  for palabra in tiempo:
    oracion.insert(0,palabra)
    diccionario[palabra.text] = splitTags(palabra.tag_)
    diccionario[palabra.text].setdefault("lemma", palabra.lemma_)

  # Añadimos el verbo
  if (verbo != None):
    oracion.append(verbo)
    diccionario[verbo.text] = splitTags(verbo.tag_)
    diccionario[verbo.text].setdefault("lemma", verbo.lemma_)

  diccionario["oracion"] = oracion

  return analisismorfologico(diccionario)
