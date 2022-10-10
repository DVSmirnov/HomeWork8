from subprocess import run
import datetime


def process_information():
    result = run("ps aux", shell=True, capture_output=True).stdout.decode('utf-8').rstrip()
    res_of_list = result.split('\n')
    all_processes = len(res_of_list) - 1
    proc_of_user = {}
    cpu = 0
    memory = 0
    max_cpu = [res_of_list[1].split()[10][:20], 0]
    max_memory = [res_of_list[1].split()[10][:20], 0]
    logs = f"{datetime.datetime.now().strftime('%d-%m-%Y-%H:%M')}-scan.txt"

    for i in res_of_list[1:]:
        line = i.split()
        if line[0] in proc_of_user.keys():
            proc_of_user[line[0]] += 1
        else:
            proc_of_user[line[0]] = 1
        cpu += float(line[2])
        memory += float(line[3])
        if float(line[2]) > max_cpu[1]:
            max_cpu[0], max_cpu[1] = line[10][:20], float(line[2])
        if float(line[3]) > max_memory[1]:
            max_memory[0], max_memory[1] = line[10][:20], float(line[3])
    memory = round(memory, 1)
    cpu = round(cpu, 1)

    with open(logs, 'w') as f:
        rec_to_file("Отчёт о состоянии системы:", f)
        rec_to_file(f"Пользователи системы: {', '.join(i for i in proc_of_user.keys())}", f)
        rec_to_file(f"Процессов запущено: {all_processes}", f)
        rec_to_file("Пользовательских процессов:", f)
        for key, value in proc_of_user.items():
            rec_to_file(f"{key}: {value}", f)
        rec_to_file(f"Всего памяти используется: {memory}%", f)
        rec_to_file(f"Всего CPU используется: {cpu}%", f)
        rec_to_file(f"Больше всего памяти использует: {max_memory[0]}", f)
        rec_to_file(f"Больше всего CPU использует: {max_cpu[0]}", f)


def rec_to_file(text, file_name):
    print(text)
    file_name.write(text + '\n')


if __name__ == '__main__':
    process_information()
    