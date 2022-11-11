import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def get_logplot(logpath, parameter_toplt, max_memory, total_mem_limit = 5000, layer_id_limit=100,out_image_path="img.png",
                trigger_memory = None, ddr_memory=None, stop_memory=None):
    
    
    PLOT_MEM = parameter_toplt
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

        
        #capping at 5000.
        # delete ID's greater than 100
        if PLOT_MEM == "total_mem":

            logdataframe["total_mem"] = (logdataframe.iloc[:,1:5].sum(axis="columns")) / 1000
            print("Log table: \n", logdataframe)
            logdataframe = logdataframe[logdataframe["ID"] <= LAYER_ID_LIMIT]
            logdataframe["total_mem"] = np.where(logdataframe["total_mem"] < TOTAL_MEM_LIMIT, logdataframe["total_mem"], TOTAL_MEM_LIMIT)
            graph = plot_dataframe(logdataframe["ID"],logdataframe["total_mem"],MAX_MEMORY,TRIGGER_MEMORY,DDR_MEMORY,STOP_MEMORY,LAYER_ID_LIMIT,ylabel="total_mem")
        
        else:

            logdataframe[PLOT_MEM] = logdataframe[PLOT_MEM] / 1000
            print("Log table: \n", logdataframe)    
            logdataframe = logdataframe[logdataframe["ID"] <= LAYER_ID_LIMIT]
            logdataframe[PLOT_MEM] = np.where(logdataframe[PLOT_MEM] < TOTAL_MEM_LIMIT, logdataframe[PLOT_MEM], TOTAL_MEM_LIMIT)
            graph = plot_dataframe(logdataframe["ID"],logdataframe[PLOT_MEM],MAX_MEMORY,TRIGGER_MEMORY,DDR_MEMORY,STOP_MEMORY,LAYER_ID_LIMIT,ylabel=PLOT_MEM)
            



def plot_dataframe(x, y, MAX_MEMORY, TRIGGER_MEMORY, DDR_MEMORY, STOP_MEMORY,LAYER_ID_LIMIT,ylabel):
        
    NUM_LAYER = 15
    plot_number = np.ceil(LAYER_ID_LIMIT / NUM_LAYER).astype(np.int32)
    plots_required = np.ceil(len(x.values)/15).astype(np.int32)
    rows, cols = plots_required//2 , plot_number//2
    fig = plt.figure(figsize=(20,10))
    for idx in range(plots_required):
        
        plt.subplot(rows,cols, idx+1)
        plt.plot(x.iloc[(idx*NUM_LAYER):(idx+1)*NUM_LAYER], y.iloc[(idx*NUM_LAYER):(idx+1)*NUM_LAYER])
        plt.scatter(x.iloc[(idx*NUM_LAYER):(idx+1)*NUM_LAYER], y.iloc[(idx*NUM_LAYER):(idx+1)*NUM_LAYER], color="r")

        plt.axhline(y = MAX_MEMORY, color = 'cyan', linestyle = 'dashed', label = "MAX MEMORY")
        plt.axhline(y = TRIGGER_MEMORY, color = 'green', linestyle = 'dashed', label = "TRIGGER MEMORY")
        plt.axhline(y = DDR_MEMORY, color = 'black', linestyle = 'dashed', label = "DDR MEMORY")
        plt.axhline(y = STOP_MEMORY, color = 'gold', linestyle = 'dashed', label = "STOP MEMORY")
        plt.xlabel("ID")
        plt.ylabel(ylabel)
        plt.xticks(x.iloc[(idx*NUM_LAYER):(idx+1)*NUM_LAYER],rotation=90)

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
    get_logplot(logpath = path, parameter_toplt = "output_mem", max_memory = max_memory,total_mem_limit = total_mem_limit,
                    out_image_path=out_image_path)
