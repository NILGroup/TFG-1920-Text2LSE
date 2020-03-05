# Preparamos Spacy
import es_core_news_md
nlp = es_core_news_md.load()
from spacy import displacy

# Si se añade en la oración -> True / Si se elimina de la oración -> False
preposiciones = {"a": False, "al": False, "ante": True, "bajo": True, "cabe": False, "con": True, "contra": True, "de": False, "del": False, "desde": True, "en": False, "entre": True, "hacia": True, "hasta": True, "para": True, "por": True, "según": True, "sin": True, "so": False, "sobre": True, "tras": True, "mediante": False, "durante": True, "versus": False, "vía": False}
# mediante yo creo que sí se muestra pero ARASAAC no tiene video

palabrasTiempo = {"segundo", "minuto", "hora", "día", "semana", "mes", "año", "ayer", "anteayer", "mañana"}

posesivos = {
    "mi":["yo","yo"],"tu":["tu","tu"],"su":["él","ella"],
    "nuestro":["nosotros","nosotras"],"vuestro":["vosotros","vosotras"],"sus": ["ellos","ellas"]
}


adverbios = {
    "tiempo": ["antes", "después", "luego", "pronto", "tarde", "temprano", "todavía", "aún", "ya", "ayer", "hoy", "mañana", "anteayer", 
              "siempre", "nunca", "jamás", "próximamente", "prontamente", "anoche", "enseguida", "ahora", "mientras", "anteriormente", "semana pasada"
              "antes de ayer", "año pasado", "próxima semana", "próximo año"],

    "cantidad": ["muy", "poco", "mucho", "bastante", "más", "menos", "algo", "demasiado", "casi", "solo", "solamente", "tan", "tanto", 
                "todo", "nada", "aproximadamente"],

    "negacion": ["no","nunca","jamás","tampoco"]

}

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


def getAdverbType (child):
  tags = splitTags(child)
  # Me da que vamos a tener que hacer un diccionario de adverbios

def keyexits(key,diccionario):
    if key in diccionario:
        return True
    return False

def getKeyValue(key,dic):
    if(keyexits(key,dic)):
        return dic[key]

# Completar con el resto de tipos
# def getDeterminantType(chidl):
#     splittags(child.tag_)
#     if(keyexits('PronType',dic)):
#         return dic['PronType']
  
# def getGender(dic):  
#     if(keyexits('Gender',dic)):
#         return dic['Gender']

# def getTense(dic):
#     if(keyexits('Tense',dic)):
#         return dic['Tense']

#---------------------------------------------------------#
#Función que devuelve el PronPers asociado al DetPos
#---------------------------------------------------------#
def detPosToPronPers(child):
    if child.text.lower() in posesivos:
        return posesivos.get(child.text.lower(),False)


# -------------------------------------------
# Función que devuelve si se añade o no una preposición a la oración final en LSE
def getIfAddPreposition (child):
  return preposiciones[child.text]
      
# -------------------------------------------

# Función que devuelve si se añade o no un determinante a la oración final en LSE
def getIfAddDeterminant(word):
 
  determinantType = getKeyValue('PronType',splitTags(word.tag_))
  # artículo determinado -> no lo añadimos
  if (determinantType == 'Art'):
    return False
 
  return True
 


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
    
    #print(diccionario)

    for word in frase:
        #-------Si es DET POSESIVO lo sustituyo por el PRONOMBRE PERSONAL correspondiente.----------
        if (word.pos_ == "DET" and getKeyValue('PronType',splitTags(word.tag_)) == "Prs"):
            new_word = detPosToPronPers(word)

            if (getKeyValue('Gender',diccionario["sujeto"]) == "Masc"):
                nueva_frase.append(new_word[0]) 
            else:
                nueva_frase.append(new_word[1])
        
        elif(word.pos == "ADV" and word.text.lower() in adverbios['tiempo']):
          hayAdvTiempo = True

        elif (word == verbo):
          if(hayAdvTiempo == False):
            if(getKeyValue('Tense',diccionario[word]) == "Past"):
                nueva_frase.insert(0,'ayer')

            elif(getKeyValue('Tense',diccionario[word]) == "Fut"):
              nueva_frase.insert(0,'mañana')
              
          
          nueva_frase.append(word.lemma_)
        else:
          nueva_frase.append(word.text)
        
    #print(frase)
    return nueva_frase
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------- FUNCIÓN RECURSIVA ROOT -------------------------------------------
# --------------------------------------------------------------------------------------------------------------------

# Función a la que le llega la palabra de la que hay que sacar el árbol y si es parte del sujeto o no esa palabra.
# Define el orden de las pablabras en LSE en función de sus tipos
def subtrees (word, esSujeto):

  añadir = True
  global verbo

  # Si es verbo no lo tratamos ahora -> lo añadimos al final del tratamiento de la oración
  if ((word.dep_ == "ROOT" and word.pos_ == 'VERB') and (word.dep_ == "ROOT" and word.pos_ == 'AUX')):
    #if(word.lemma_ != "ser" and word.lemma_ != "estar"):
    verbo = word
    añadir = False

  else:

    # Comprobamos si hay un verbo en la oración -> guardamos su lemma_ si no es ser o estar
    if ((word.dep_ == "cop" and word.pos_ == 'AUX') or word.pos_ == "VERB"):
        #if(word.lemma_ != "ser" and word.lemma_ != "estar"):
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
      

    # ------------------------ ADVERBIOS ----------------------------
    # Ver de que tipo son y colocar en la oración según corresponda

    # Tiempo
    # Lugar
    # Modo
    # Cantidad
    # Interrogativos / Excalamtivos
    # Afirmación
    # Negación
    # Duda

   # ------------------------ SUSTANTIVOS ----------------------------
    #  PALABRAS DE TEMPORALIDAD
    # Si hallamos una palabra de temporalidad (semana, año, mes, etc) cogemos todo lo que herede de esta palabra, lo tratamos y lo que quede lo ponemos al principio de la oración
    if (word.pos_ == 'NOUN'):
      if (word.text.lower() in palabrasTiempo):
        alPrincipio = True
    # Por ejemplo: La semana pasada -> De semana heredan LA y PASADA -> se trataría así -> semana pasada -> quedaría colocarlo al inicio de la oración 

  # ---------------------------------------------------------------------
  # ---------------------------------------------------------------------

  # --------------------- SUJETO--------------------------
  if (word.dep_ == 'nsubj' or esSujeto):
    if (añadir == True):    
      sujeto.append(word)
    for child in word.children:
      subtrees(child, True)

  # -------------------- PREDICADO ------------------------
  else: 
    if (añadir == True): 
      predicado.append(word)
    for child in word.children:
      subtrees(child, False)


# --------------------------------------------------------------------------------------------------------------------
# ------------------------------------------- FUNCIÓN PRINCIPAL -> LLAMADA A FUNCIÓN RECURSIVA -----------------------
# --------------------------------------------------------------------------------------------------------------------

def TranslateSentence(initSentence):
  
  root = ""
  isVerbRoot = False
  verbAux = ""
  modificador = None

  doc = nlp(initSentence)

  for token in doc:

    print (token.text + " -> " + token.dep_ + " -> " + token.tag_ + " -> " + token.pos_+ " -> " + token.lemma_)
    if (token.dep_ == "ROOT"):
      root = token
    
  subtrees(root, False)

  # Vamos añadiendo el sujeto ordenado a la oración
  for suj in sujeto:
    if (suj.dep_ == 'nsubj'):
      oracion.insert(0, suj)
      diccionario["sujeto"] = splitTags(suj.tag_)
    
    elif(suj.dep_ == 'nmod' and suj.pos_ == 'NOUN'):
        modificador = suj
        oracion.append(suj)

    #Si PronType (tag) es Personal(prs) entonces va antes que el sujeto
    elif(getKeyValue('PronType',splitTags(suj.tag_)) == "Prs"):
        if(modificador == None):
            oracion.insert(0, suj)
        else:
            oracion.insert(1, suj)

    else:
      oracion.append(suj)

    diccionario[suj] = splitTags(suj.tag_)
  # Vamos añadiendo el predicado ordenado a la oración
  for pred in predicado:
    posibleAdvTim = None

    if pred.pos_ == "ADV":
      if pred.text.lower() in adverbios['tiempo']:
          oracion.insert(0,pred)
      else:
        oracion.append(pred)
      
    # elif pred.dep_ == 'obl':
    #   for p in pred.children:
    #     if p.dep_ == 'det':
    #       if getIfAddDeterminant(p):
    #          posibleAdvTim = p.text + " " + pred.text
    #       else:
    #         posibleAdvTim = posibleAdvTim + pred.text

    #     elif p.pos_ == 'ADJ':
    #       posibleAdvTim = posibleAdvTim + " " + p.text

    #     if posibleAdvTim in adverbios['tiempo']:
    #       oracion.insert(0,posibleAdvTim)

    #   #oracion.append(pred)
    #   break
    #   # if(predicado.index(pred) < len(predicado)-1):
    #   #   posibleAdvTim = pred.text + " " + predicado[predicado.index(pred) + 1].text
    #   #   if posibleAdvTim in adverbios['tiempo']:
    #   #     oracion.insert(0,pred)

    else:
      oracion.append(pred)

    diccionario[pred] = splitTags(pred.tag_)

  if (verbo != None):
    oracion.append(verbo)
    diccionario[verbo] = splitTags(verbo.tag_)

  diccionario["oracion"] = oracion
  
  # AQUÍ HABRÁ QUE LLAMAR A LA PARTE DE MORFOLOGÍA PARA CAMBIAR PALABRAS, COMO POR EJEMPLO,  
    # MI -> YO 
    # VERBO EN PASADO -> AÑADIR AYER SI NO HAY YA ALGUNA PALABRA INDICANDO TIEMPO
    # FEMENINOS -> PASAR A MASCULINOS
    # ETC

  print ("---------------------------------------------------------------------------------- ")
  print ("------------------------------------ SUJETO -------------------------------------- ")
  print (sujeto)
  print ("----------------------------------- PREDICADO ------------------------------------ ")
  print (predicado)
  print ("------------------------------------ ORACIÓN ------------------------------------ ")
  print (oracion)
  print ("----------------------------------- DICCIONARIO --------------------------------- ")
  print(diccionario)
  print ("------------------------------------- MORFOLOGIA ------------------------------------ ")
  print(analisismorfologico(diccionario))

# Llamada a la función principal
sentence =  "Los niños comen chocolate con leche hoy"
TranslateSentence(sentence)


# FALLA
  # 4. Mi tía fue al supermercado en coche. -> tía mi supermercado coche -> DEBERÍA SER -> yo tía ayer supermercado coche
  # 5. Los problemas de la empresa aumentaron este año -> problemas empresa año este aumentar -> DEBERÍA SER -> este año empresa problemas aumentar
  # 6. Mi hermana y mi tía están de vacaciones -> tía hermana mi mi vacaciones -> DEBERÍA SER -> yo hermana yo tía vacaciones
  # 7. Se rompió el teclado de mi ordenador -> teclado ordenador mi se romper .> DEBERÍA SER -> yo ordenador teclado romper
  # 8. Los niños comen chocolate con leche hoy -> niós chocolate leche con comer hoy -> DEBERÍA SER -> hoy niños chocolate leche con comer
  # 9. Mi hermana acudió a la policía a denunciar un robo -> hermana mi policia robo un denunciar -> DEBERÍA SER -> yo hermana ayer policía ir. Robo denunciar

# FUNCIONA
  # 1. Él bebe agua -> Él agua beber
  # 2. El niño bebe agua -> niño agua beber
  # 3. La niña bebe agua con limón -> niña agua limón con beber

# PENDIENTE
  # 1. Determinantes 
      # posesivos -> mi casa -> yo casa
      # demostrativos "este", "esta", "estos", "estas", "ese", "esa", "esos", "esas", "aquel", "aquella", "aquellos" y "aquellas" -> qué se hace? 
  # 2. Palabras temporales -> añadir el conjunto de las palabras temporales al principio de la oración
  # 3. Adverbios -> añadirlos donde correscponda según el tipo
  # 4. Sujetos compuestos (mi hermana y mi tía -> yo hermana yo tía)
  # 5. Quitar me te se
  # 6. Verbos compuestos -> convertir en un verbo solo -> he comido -> pasado comer (quitando el he)
  # 7. Temporalidad verbos -> añadir ayer, presente o futuro si no hay temporalidad indicada
  # 8. Femeninos -> pasar a masculinos (bonita -> bonito)
  # 9. Frases compuestas -> dividir en distintas frases