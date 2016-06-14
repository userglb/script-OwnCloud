#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Anna Golub"
__date__ = "01/06/2016"

try:
    import sys
    import owncloud
    import os
    import time
    import getpass
    import logging
    import logging.handlers
    import unicodedata

except ImportError:
    print((os.linesep * 2).join(["Error en importar els moduls:",
    str(sys.exc_info()[1]), "Es necesitan instalarse ", "Tancant..."]))
    sys.exit(-2)

def upload(oc, dir_a_enviar, dir_a_controlar, fitxer, modif, log):
    """Pujar fitxer al cloud"""
    if os.path.isfile(dir_a_controlar + fitxer) == True:
        oc.put_file(dir_a_enviar + modif, dir_a_controlar + fitxer)
        log.info("> S'ha copiat el fitxer: " + dir_a_enviar + modif)
    #else:
        #asser oc.put_directory(dir_a_enviar, dir_a_controlar + fitxer)
        #log.info("> S'ha copiat la carpeta: " + dir_a_enviar + fitxer + '/')

def elimina_tildes(cadena):
    """Eliminar les lletras que tinguin tildes"""
    s = ''.join((c for c in unicodedata.normalize('NFD',unicode(cadena)) if unicodedata.category(c) != 'Mn'))
    return s.decode() 
        
def elimina_caract(fitxer):
    """Eliminar caracters prohibits"""
    caracters_elim = ['!', '?', '~', '"', '#', '%', '&', '*', ':', '<', '>', '?', '/', '\\', '{', '|', '}', ' ']
    fitxer = fitxer.translate(None, ''.join(caracters_elim))
    fitxer = fitxer.replace('ñ', "n")
    fitxer = fitxer.replace('Ñ', "N")
    fitxer = fitxer.replace('ç', "c")
    fitxer = fitxer.replace('Ç', "C")
    fitxer = fitxer.decode('utf-8')
    fitxer = elimina_tildes(fitxer)
    return fitxer
       
        
def logs(id):
    """Guardem els logs """
    log=logging.getLogger('Usuari: ' + id)
    log.setLevel(logging.DEBUG)
    nom_log = logging.handlers.RotatingFileHandler(filename='logs_monitor.log', mode='a', maxBytes=1024, backupCount=5)
    format_log = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',datefmt='%y-%m-%d %H:%M:%S')
    nom_log.setFormatter(format_log)
    log.addHandler(nom_log)
    return log
    
    
def main():
    """Monitorització d'una carpeta """              
    oc = owncloud.Client('https://***********')
    id = 'username'
    log = logs(id)
    #clau = getpass.getpass(prompt='Introdueix la clau: ')
    clau = 'passwd'
    oc.login(id, clau)
    print "Connexió creada amb èxit!"
    log.info("> S'ha establert connexió amb l'usuari: " + id )
    #oc.mkdir('testdir2')
    dir_a_enviar = "testdir2/"
    dir_a_controlar = "/home/anna/test/"
    abans = dict ([(f, None) for f in os.listdir (dir_a_controlar)])
    while True:
      time.sleep (300) #cambiar a 10 per fer proves petites
      despres = dict ([(f, None) for f in os.listdir (dir_a_controlar)])
      nou = [f for f in despres if not f in abans]
      eliminat = [f for f in abans if not f in despres]
      if nou: 
          print "> Nou: ", ", ".join (nou)
          i=0
          any = (time.strftime("%Y"))
          llista = str(oc.list(dir_a_enviar))
          llista_any = str(dir_a_enviar) + str(any) + '/'
          if llista_any not in llista: 
              oc.mkdir(llista_any)
          while i<len(nou):
              if os.path.getsize ( dir_a_controlar + nou[i]) > 0:
                  modif = elimina_caract(nou[i])
                  upload(oc, llista_any, dir_a_controlar, nou[i], modif, log)
              i=i+1
          
      if eliminat: print "> Eliminat: ", ", ".join (eliminat)
      abans = despres


if __name__ == "__main__":
    main()
