# d = {"dream": 0, "car": 99, "blockdmask": 1, "error": 30, "app": 20}

# d2 = sorted(d.items(), key=lambda x: x[1], reverse=False)
# print(d2)

# print(d2[0][1])
import os
import shutil
import glob

output = glob.glob('C:\\Users\\USER\\cp2\\data\\2.Validation/*/*/*/*/*/*')

for full_file_path in output:
    new_file_path = full_file_path.split('\\')
    file_name = new_file_path[-1]

    if file_name.split('_')[-3] == 'T':
        new_file_path.pop()
        del new_file_path[:7]
        new_file_path = '/'.join(new_file_path)
        new_file_path = 'C:/Users/USER/cp2/integrated_data/VS'+new_file_path[2:-1]

        if os.path.exists(new_file_path):
            shutil.move(full_file_path, new_file_path+'/'+file_name)
            print(f'move {full_file_path} To {new_file_path}')
        else:
            os.makedirs(new_file_path)
            shutil.move(full_file_path, new_file_path+'/'+file_name)
            print(f'move {full_file_path} To {new_file_path}')
    else:
        continue
        
    print(file_name.split('_')[-3])

