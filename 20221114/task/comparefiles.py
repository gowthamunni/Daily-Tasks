def read_compare(file_read_path,file_path_write,listnum = 32, num_elements=32400):

    LIMIT = num_elements
    LIST_NUM = listnum
    ITERATION = 4096
    
    with open(file_read_path, "r") as outfile:
        out_list = outfile.readlines()

    data_list = []
    for data in out_list:
        data = data.strip()
            
        data_list.append(data)
    


    write_list = []
    for i in range(LIST_NUM):
        write_list.append([i])


    txt_idx = 0
    while txt_idx < (LIST_NUM*LIMIT) - 1:
        for list_idx in range(LIST_NUM):
            for i in range(ITERATION):
                if len(write_list[list_idx]) == LIMIT+1:
                    break
                write_list[list_idx].append(data_list[txt_idx])
                txt_idx+=1

                print(txt_idx)


    for i in range(listnum):
        write_list[i].pop(0)


    with open(file_path_write,"a") as write_file:
        for i in range(len(write_list)):
            for j in range(len(write_list[i])):
                write_file.write(write_list[i][j]+"\n")







if __name__ == "__main__":
    file_read_path = "out_data_mbv2.txt"
    file_path_write = "outfile.txt"

    read_compare(file_read_path, file_path_write)
