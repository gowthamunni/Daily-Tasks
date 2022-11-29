import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def get_logplot(logpath, max_memory, total_mem_limit = 5000, layer_id_limit=100,out_image_path="img.png",
                trigger_memory = None, ddr_memory=None, stop_memory=None):
    
    
    MAX_MEMORY = max_memory
    TRIGGER_MEMORY = MAX_MEMORY * 0.75 if trigger_memory is None else trigger_memory
    DDR_MEMORY = MAX_MEMORY * 0.5  if ddr_memory is None else ddr_memory
    STOP_MEMORY = MAX_MEMORY * 0.25 if stop_memory is None else stop_memory
    TOTAL_MEM_LIMIT = total_mem_limit
    LAYER_ID_LIMIT = layer_id_limit

    with open(logpath, "r") as logfile:

        files_list = logfile.readlines()
    
        logdatatable = {"ID":[],"layer_mem":[], 'const_mem':[],'input_mem':[],'output_mem':[]}
        for txts in files_list:

            splits = txts.strip().split(" ", 11)

            #to get ID
            id_split = splits[5].split(":")
            logdatatable["ID"].append(int(id_split[1]))

            inter_dict = eval(splits[11])
            # adding other memories
            logdatatable["layer_mem"].append(inter_dict["layer_mem"])
            logdatatable['const_mem'].append(inter_dict['const_mem'])
            logdatatable['input_mem'].append(inter_dict['input_mem'])
            logdatatable['output_mem'].append(inter_dict['output_mem'])


        # convert to dataframe
        logdataframe = pd.DataFrame(logdatatable)
        logdataframe["total_mem"] = (logdataframe.iloc[:,1:5].sum(axis="columns")) / 1000
        print("Log table: \n", logdataframe)

        
        #capping at 5000.
        # delete ID's greater than 100
        logdataframe = logdataframe[logdataframe["ID"] <= LAYER_ID_LIMIT]
        logdataframe["total_mem"] = np.where(logdataframe["total_mem"] < TOTAL_MEM_LIMIT, logdataframe["total_mem"], TOTAL_MEM_LIMIT)

        graph = plot_dataframe(logdataframe,MAX_MEMORY,TRIGGER_MEMORY,DDR_MEMORY,STOP_MEMORY,LAYER_ID_LIMIT)



def plot_dataframe(logdataframe, MAX_MEMORY, TRIGGER_MEMORY, DDR_MEMORY, STOP_MEMORY,LAYER_ID_LIMIT):
        
    NUM_LAYER = 15
    plot_number = np.ceil(LAYER_ID_LIMIT / NUM_LAYER).astype(np.int32)
    plots_required = np.ceil(len(logdataframe["ID"].values)/15).astype(np.int32)
    rows, cols = plots_required//2 , plot_number//2
    fig = plt.figure(figsize=(20,10))
    for idx in range(plots_required):
        
        plt.subplot(rows,cols, idx+1)
        plt.plot(logdataframe["ID"].iloc[(idx*NUM_LAYER):(idx+1)*NUM_LAYER], logdataframe["total_mem"].iloc[(idx*NUM_LAYER):(idx+1)*NUM_LAYER])
        plt.scatter(logdataframe["ID"].iloc[(idx*NUM_LAYER):(idx+1)*NUM_LAYER], logdataframe["total_mem"].iloc[(idx*NUM_LAYER):(idx+1)*NUM_LAYER], color="r")

        plt.axhline(y = MAX_MEMORY, color = 'cyan', linestyle = 'dashed', label = "MAX MEMORY")
        plt.axhline(y = TRIGGER_MEMORY, color = 'green', linestyle = 'dashed', label = "TRIGGER MEMORY")
        plt.axhline(y = DDR_MEMORY, color = 'black', linestyle = 'dashed', label = "DDR MEMORY")
        plt.axhline(y = STOP_MEMORY, color = 'gold', linestyle = 'dashed', label = "STOP MEMORY")
        plt.xlabel("ID")
        plt.ylabel("Total Memory")
        plt.xticks(logdataframe["ID"].iloc[(idx*NUM_LAYER):(idx+1)*NUM_LAYER],rotation=90)

        # to delete unwanted plots.
        if idx+1 > plots_required:
            plt.delaxes()

    lines = []
    labels = []
    for ax in fig.axes:
        Line, Label = ax.get_legend_handles_labels()
        lines.extend(Line)
        labels.extend(Label)
    
    fig.legend(set(lines), set(labels), loc="upper right")
    plt.savefig(out_image_path)
    plt.show()
    


if __name__ == "__main__":

    path = "MM.log.mbv2"
    max_memory = 3000
    total_mem_limit = 5000
    out_image_path = "./graphs/1110log_plotmbv2.png"
    get_logplot(path,max_memory,total_mem_limit,out_image_path=out_image_path)
