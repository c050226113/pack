import shlex
import subprocess
import sys
import os
import datetime


path = os.path.dirname(sys.argv[0]) + '/'
os.chdir(path)
for i in range(1, len(path.split('/')) - 2):
    sys.path.append(path + '../' * i)


def get_log_file_path(exec_file, _type):
    out_dir = os.path.dirname(exec_file) + '/info'
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    if _type == 'hour':
        log_file = 'hour' + str(1)
    elif _type == 'day':
        log_file = 'day-' + str(datetime.date.today())
    else:
        log_file = 'month-' + str(datetime.date.today())[:-3]
    return out_dir + '/' + log_file


def get_log_fp(log_file):
    if os.path.exists(log_file):
        log_fp = open(log_file, 'a')
    else:
        log_fp = open(log_file, 'w')
    return log_fp


if __name__ == '__main__':
    def main():
        argv = sys.argv
        exec_file = argv[1]
        _type = argv[2]

        log_file = get_log_file_path(exec_file, _type)
        log_fp = get_log_fp(log_file)

        f = open(log_file, 'r')
        f.seek(0, 2)
        now = f.tell()
        if now > 10:
            f.seek(now - 3)
            word = f.read(3)
            f.close()
            if word == 'end':
                exit()
        else:
            f.close()

        shell_cmd = 'python ' + exec_file
        cmd = shlex.split(shell_cmd)
        p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        log_fp.write('start '
                     '------------------------------------------------------------------------------------------------'
                     '-------------------------------------------------------------------------------------------------'
                     '--------------------------------------------- \n')
        while p.poll() is None:
            line = p.stdout.readline()
            line = line.strip()
            linestring = str(line)[2:-1]
            if len(linestring) > 1:
                log_fp.write(linestring + '\n')
                log_fp.flush()

        if p.returncode() == 0:
            log_fp.write('end')
        log_fp.close()
    main()
