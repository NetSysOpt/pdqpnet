
# Python program to read
# json file
import os
import json



# filters='8938'
filters='mm'
filters='8785'
filters='8906'

def read_json(fnm):
    # Opening JSON file
    f = open(fnm)
    # returns JSON object as 
    # a dictionary
    data = json.load(f)
    # Closing file
    f.close()
    return data

file_map = {}

ori_log = './ori'
ori_log = '../../logs'

ori_files = os.listdir(ori_log)
ori_files = [x for x in ori_files if '.json' in x and '.gz' not in x]
for fnm in ori_files:
    if fnm not in file_map:
        file_map[fnm] = []
    file_map[fnm].append([-1,-1])
    logs = read_json(f'{ori_log}/{fnm}')
    itnm = logs['iteration_count']
    tttm = logs['solve_time_sec']
    # print(logs)
    # print(itnm)
    # print(tttm)
    file_map[fnm][0][0] = itnm
    file_map[fnm][0][1] = tttm

wms_files1 = os.listdir('./warmstart')

to_process = [x for x in wms_files1 if os.path.isdir(f'./warmstart/{x}')]

folder_names = ['warmstart']

ntypes = 2

wms_files = [x for x in wms_files1 if '.json' in x and '.gz' not in x]
for fnm in wms_files:
    if fnm not in file_map:
        file_map[fnm] = []
    file_map[fnm].append([-1,-1])
    logs = read_json(f'./warmstart/{fnm}')
    itnm = logs['iteration_count']
    tttm = logs['solve_time_sec']
    # print(logs)
    # print(itnm)
    # print(tttm)
    file_map[fnm][-1][0] = itnm
    file_map[fnm][-1][1] = tttm
    

for pro_folder in to_process:

    wms_files1 = os.listdir(f'./warmstart/{pro_folder}')
    folder_names.append(pro_folder)
    wms_files = [x for x in wms_files1 if '.json' in x and '.gz' not in x]

    for fnm in wms_files:
        if fnm not in file_map:
            file_map[fnm] = []
        file_map[fnm].append([-1,-1])
        logs = read_json(f'./warmstart/{pro_folder}/{fnm}')
        itnm = logs['iteration_count']
        tttm = logs['solve_time_sec']
        # print(logs)
        # print(itnm)
        # print(tttm)
        file_map[fnm][-1][0] = itnm
        file_map[fnm][-1][1] = tttm

ntypes = len(file_map[fnm])


f = open('res.csv','w')
st = f'ins ori_time ori_iter '
for ff in folder_names:
    st+=f'{ff}_time ratio {ff}_iter ratio '
st+='\n'
print(st)
f.write(st)
# all_rat1 = 0.0
# all_rat2 = 0.0
all_rats1=[0]*ntypes
all_rats2=[0]*ntypes

keys = []
for fnm in file_map:
    keys.append(fnm)
keys.sort()

if filters=='mm':
    tars_sums = os.listdir('/home/lxyang/git/pdqpnet/pkl/valid')
    keys = [x.replace('.QPS.pkl','_summary.json') for x in tars_sums]
elif len(filters)!=0:
    keys = [x for x in keys if filters in x]

for fnm in keys:

    print(fnm,file_map[fnm])
    if len(file_map[fnm])<2:
        continue
    st = f'{fnm} {file_map[fnm][0][1]} {file_map[fnm][0][0]} '
    for idx in range(1,len(file_map[fnm])):
        ent = file_map[fnm][idx]
        print(fnm,ent)
        ratio1 = (file_map[fnm][0][1] - file_map[fnm][idx][1])/(file_map[fnm][0][1]+1e-8)
        all_rats1[idx] +=ratio1
        st += f'{file_map[fnm][idx][1]} {round(ratio1*100,2)}% '

        ratio1 = (file_map[fnm][0][0] - file_map[fnm][idx][0])/(file_map[fnm][0][0]+1e-8)
        all_rats2[idx] +=ratio1
        st += f'{file_map[fnm][idx][0]} {round(ratio1*100,2)}% '
    st+='\n'
    print(st)
    f.write(st)

for idx in range(1,len(all_rats2)):
    all_rats1[idx] /=len(file_map)
    all_rats2[idx] /=len(file_map)
st = f'avg / / '
for idx in range(1,len(all_rats2)):
    st += f'/ {all_rats1[idx]} / {all_rats2[idx]} '
st+='\n'

f.write(st)
f.close()