import os
import subprocess

def llegeix_noms_arxius(subdirectori):
  try:
    noms_arxius = os.listdir(subdirectori)
    return noms_arxius
  except FileNotFoundError:
    print(f"El subdirectori {subdirectori} no existeix.")

if __name__ == "__main__":

  noms_arxius = llegeix_noms_arxius('./jocs_de_prova')
  if not noms_arxius: exit()
  for nom in noms_arxius:
    nom_sense_extensio = os.path.splitext(nom)[0]
    nom_fitxer_esperat = f'./outputs_esperats/{nom_sense_extensio}.txt'
    
    result = subprocess.run(f'python3 scheme.py ./jocs_de_prova/{nom}', shell=True, capture_output=True, text=True).stdout
    with open(nom_fitxer_esperat, 'r') as esperat:
      expected_output = esperat.read()
      if expected_output == result:
        print(f'OK: Joc de prova {nom} passat correctament.')
      else:
        print(f'FAIL: Joc de prova {nom} NO ha passat.')
        print(f'Output esperat:\n {expected_output}')
        print(f'Output obtingut:\n {result}')