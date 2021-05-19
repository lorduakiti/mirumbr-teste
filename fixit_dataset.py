import os
import sys
import shutil
from itertools import (takewhile, repeat)

path = 'E:\\GitHub\\mirumbr-teste\\'
dataset = 'dataset_original.csv'
path_file = os.path.join(path, dataset)
path_ds_folder = 'datasets\\'
path_ds_file = path + path_ds_folder + dataset
filename = 'dataset.sql'
path_ds_file_new = path + path_ds_folder + filename


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def raw_in_count(filename):
    f = open(filename, 'rb')
    bufgen = takewhile(lambda x: x, (f.raw.read(1024 * 1024) for _ in repeat(None)))
    return sum(buf.count(b'\n') for buf in bufgen)


def delete_last_line(filename):
    with open(filename, 'r+', encoding="utf-8") as file:

        # Move o ponteiro (similar a um cursor de um editor de textos) para o fim do arquivo.
        file.seek(0, os.SEEK_END)

        # Pula o ultimo caractere do arquivo
        # No caso de a ultima linha ser null, deletamos a ultima linha e a penúltima
        pos = file.tell() - 1

        # Lê cada caractere no arquivo, um por vez, a partir do penúltimo
        # caractere indo para trás, buscando por um caractere de nova linha
        # Se encontrarmos um nova linha, sai da busca
        while pos > 0 and file.read(1) != "\n":
            pos -= 1
            file.seek(pos, os.SEEK_SET)

        # Enquanto não estivermos no começo do arquivo, deleta todos os caracteres para frente desta posição
        if pos > 0:
            file.seek(pos, os.SEEK_SET)
            file.truncate()
    file.close()


def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    # print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    sys.stdout.write(f'{bcolors.OKGREEN}\r{prefix} |{bar}| {percent}% {suffix}{bcolors.ENDC}')
    sys.stdout.flush()
    # Print New Line on Complete
    if iteration == total:
        print(printEnd)


def fixit_line(ln, step=1):

    if step == -3:
        # Ajusta texto com caracteres de escape
        ln = ln.replace('\'', '`') \
            .replace('("', '(~').replace('")', '~)') \
            .replace('(\'', '(`').replace('\')', '`)')
        # Ajusta textos específicos com erro
        ln = ln.replace('""Introduction"","" Bibliography""', '""Introduction"", "" Bibliography""') \
            .replace('""Persians"", ""Prometheus Bound"", ""Women of Trachis"",""Philoctetes"",""Trojan"","" Women"", ""Bacchae""', '""Persians"", ""Prometheus Bound"", ""Women of Trachis"", ""Philoctetes"", ""Trojan"", "" Women"", ""Bacchae""')

    elif step == -2:
        # Retira as quebras de linha
        ln = ln.rstrip('\n').replace('\n', ' ', 10)

    elif step == -1:
        # Ajusta linhas com erro
        ln = fixit_line(ln.replace('\'),', ''), -2)

    elif step == 0:
        # Ajuste da linha de cabeçalho
        ln = ln.replace('-', '_') \
            .replace('","', '"|"') \
            .replace('"', '\'') \
            .replace('\'|\'', ',')
        ln = ln.rstrip('\n').replace('\n', '').replace('\'', '')
        ln = ln.rstrip('\n').replace('\n', '').replace('(\'', '(')

    elif step == 1:
        # Ajusta texto com caracteres de escape
        ln = fixit_line(ln, -3)
        # Ajusta formato dos campos do tipo array
        ln = ln.replace('"[', '"{').replace(']"', '}"')
        # Aplica separador temporário
        ln = ln.replace('","', '"|"')
        # Subistitui campos vazios por NULL
        ln = ln.replace('|""|', '|NULL|') \
            .replace('(""|', '(NULL|') \
            .replace('|""),', '|NULL),')
        # Retira quebras de linha
        ln = fixit_line(ln, -2)

    elif step == 2:
        # Ajuste das aspas
        ln = ln.replace('("', '(\'').replace('"),', '\'),').replace('"|"', '\',\'')
        ln = ln.replace('"|NULL|"', '\',NULL,\'') \
            .replace('(NULL|",', '(NULL,\'') \
            .replace('"|NULL),', '\',NULL),')
        ln = ln.replace(',\'\',', ',NULL,') \
            .replace(',\'\'),', ',NULL),')
        ln = ln.replace('(~', '("').replace('~)', '")')

    elif step == 3:
        # Ajuste da linha final do comando de INSERT
        ln = ln.replace('),', ');') + '\n'

    elif step == 4:
        # Incluindo fechamento de linha para linhas normais
        ln = '(' + ln.rstrip('\n') + '),'

    elif step == 5:
        # Prepara linha para gravação
        ln = fixit_line(ln, 4)
        ln = fixit_line(ln, 2)
        ln = ln + '\n'

    return ln


def fixit_file():
    # Ajustando cabeçalho do arquivo "dataset.csv"
    try:
        ln = ''
        ln_aux = ''
        last_line = ''
        final_line = ''

        # Fazendo cópia do arquivo original
        shutil.copy(path_ds_file, path_ds_file_new)

        # Alerando informações do cabeçalho
        head_line = 1
        total_lines = raw_in_count(path_ds_file_new)
        print('Total de linhas: ', total_lines)
        with open(path_ds_file_new, 'rt', encoding='utf-8-sig') as file:
            text = file.readlines()
            firstline = text[0]
            new_firstline = fixit_line(firstline, 0) \
                .replace('authors', 'author') \
                .replace('categories', 'categorie')
            new_firstline = 'insert into public.dataset \n (' + new_firstline + ') \n values \n'
            # print(firstline)
            # print(new_firstline)
        file.close()

        # Ajustando erros de caractéres especiais nas linhas do arquivo
        with open(path_ds_file_new, 'w', encoding='utf-8-sig') as f:
            i = 1
            last_error_line = False
            for ln in text:
                ln = ln.strip()

                ln_aux = ''
                num_chars = len(ln)
                first_char = '' if (num_chars == 0) else ln[0]
                last_char = '' if (num_chars == 0) else ln[(num_chars - 1)]
                error_line = False
                flag_write = 0

                if i <= head_line:
                    f.write(new_firstline)
                elif ln == '':
                    error_line = True
                    ln = fixit_line(last_line, -1) + ' ' + fixit_line(ln, -2)
                else:
                    # Define linhas com erro devido a quebra de linha adicional
                    if first_char != '"':
                        error_line = True
                        flag_write = -1

                    ln = fixit_line(ln, 1)

                    # if error_line:
                    #     print(f"{bcolors.UNDERLINE}\n{last_error_line} >>> {last_line}{bcolors.ENDC}")
                    #     print(f"{bcolors.UNDERLINE}\n{error_line} >>> {ln}{bcolors.ENDC}")

                    # Escreve no arquivo somente a linha anterior sem erro caso a linha atual não contenha erros
                    if error_line and (not last_error_line) and (i > (head_line + 1)):
                        # Está na primeira linha com erro
                        # Não deve gravar a linha no arquivo
                        ln = fixit_line(last_line, -1) + ' ' + ln
                        # print(f"{bcolors.FAIL}\n{error_line} >> {last_error_line} >> {ln}{bcolors.ENDC}")

                    elif error_line and last_error_line and (i > (head_line + 1)):
                        # Está nas próximas linhas com erro
                        # Não deve gravar a linha no arquivo
                        ln = fixit_line(last_line, -1) + ' ' + ln
                        # print(f"{bcolors.FAIL}\n{error_line} > {last_error_line} > {ln}{bcolors.ENDC}")

                    elif (not error_line) and last_error_line and (i > (head_line + 1)):
                        # Está na próxima linha sem erro, depois de passar nas linhas com erro
                        last_line = fixit_line(last_line, 5)
                        ln_aux = last_line
                        flag_write = 2

                    elif (not error_line) and (not last_error_line) and (i > (head_line + 1)):
                        # Está em uma linha sem erro
                        # Grava linha anterior avaliada como normal (sem erro)
                        last_line = fixit_line(last_line, 5)
                        ln_aux = last_line
                        flag_write = 1

                    # # Ajusta úlima linha
                    # if (i == total_lines) and (flag_write == 0):
                    #     ln = fixit_line(ln, 5)
                    #     ln = fixit_line(ln, 3)
                    #     ln_aux = ln

                    # Grava linha
                    if (ln_aux != '') and (flag_write != -1):
                        f.write(ln_aux)

                last_line = ln
                last_line_all = last_line + ln
                last_error_line = error_line
                last_flag_write = flag_write

                msg = f'{i}|{total_lines}->{flag_write}'
                if flag_write == -1:
                    print(f"{bcolors.FAIL}\nLinha com Erro: {msg}{bcolors.ENDC}")
                elif flag_write == 2:
                    print(f"{bcolors.FAIL}\n{ln_aux}{bcolors.ENDC}")
                else:
                    print_progress_bar(i, total_lines, prefix='Progress:', suffix=msg, length=100)
                i += 1

            # Ajusta úlima linha
            if ln != '':
                final_line = fixit_line(fixit_line(ln, 5), 3)
                f.write(final_line)

        f.close()

        delete_last_line(path_ds_file_new)

        print(f"{bcolors.OKBLUE}\nAjustado cabeçalho e linhas do arquivo: {bcolors.ENDC}", filename)

    except Exception as err:
        print(f"{bcolors.WARNING}\nErro ao corrigir cabeçalho e nome de colunas dos arquivos.{bcolors.ENDC}")
        print(ln, '\n')
        print(err)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


if __name__ == '__main__':
    fixit_file()
