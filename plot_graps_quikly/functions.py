import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import optimize
from matplotlib.ticker import FormatStrFormatter


def minElem(data=[], quant=0):
    if quant == 0:
        return 0
    if quant == 1:
        return np.min(data[0])
    min_elements = []
    for i in range(quant):
        min_elements.append(np.min(data[i]))
    return min(min_elements)

def maxElem(data=[], quant=0):
    if quant == 0:
        return 0
    if quant == 1:
        return np.max(data[0])
    max_elements = []
    for i in range(quant):
        max_elements.append(np.max(data[i]))
    return max(max_elements)

def returnMinAndMaxElementForData(data, quant, stretch_graph_coefficients):
    minimalElement_x = []
    minimalElement_y = []
    maximumElement_x = []
    maximumElement_y = []
    for i in range(quant):
        if  data[i].shape[0] == 4:
            minimalElement_x.append(np.min(data[i][0] - data[i][1]))
            minimalElement_y.append(np.min(data[i][2] - data[i][3]))
            maximumElement_x.append(np.max(data[i][0] + data[i][1]))
            maximumElement_y.append(np.max(data[i][2] + data[i][3]))

        elif  data[i].shape[0] == 3:
            minimalElement_x.append(np.min(data[i][0] - data[i][1]))
            minimalElement_y.append(np.min(data[i][2]))
            maximumElement_x.append(np.max(data[i][0] - data[i][1]))
            maximumElement_y.append(np.max(data[i][2]))

        elif  data[i].shape[0] == 2:
            minimalElement_x.append(np.min(data[i][0]))
            minimalElement_y.append(np.min(data[i][1]))
            maximumElement_x.append(np.max(data[i][0]))
            maximumElement_y.append(np.max(data[i][1]))
    if(quant == 1):
        minEl = [minimalElement_x[0], minimalElement_y[0]] 
        maxEl = [maximumElement_x[0], maximumElement_y[0]]
    else:
        minEl = [min(minimalElement_x), min(minimalElement_y)]    
        maxEl = [max(maximumElement_x), max(maximumElement_y)]
    minEl[0] *= stretch_graph_coefficients[0]
    minEl[1] *= stretch_graph_coefficients[2]
    maxEl[0] *= stretch_graph_coefficients[1]
    maxEl[1] *= stretch_graph_coefficients[3]
    return (minEl, maxEl)

def extend_parameters(parameter, quant, element_extend_by):
    if len(parameter) < quant and len(parameter) > 0:
        for i in range(len(parameter), quant):
            parameter.append(parameter[i - 1])
    elif len(parameter) == 0:
        parameter = [element_extend_by] * quant
    return parameter

#data is a massive where each data is different element.
#each element has a structure: index = 0 - x_data, index=1 - sigma_x_data, index=2, y_data, index=3 - sigma_y_data
#if lenght of the element is three then it's structure is: index = 0 - x_data, index=1 - sigma_x_data, index=2, y_data
#if lenght of the element is two then it's structure is: index = 0 - x_data, index=1, y_data
#first title is x-axis, second - y-axis, third - graph title
# point_start_to_end has two elements x and y parameters
def plot_graph(data,quant, titles=['X', 'Y', 'title'], colors=['r'], stretch_graph_coefficients=[0, 1.1, 0, 1.1], lses=[''], labels=[''], markersizes=[3], legend_position='upper right', axes_round=['%0.2f', '%0.2f'], name_fig='graph.svg', markers=["o"], save_flag=True, points_draw_lines_to=[], point_start_to_end=[None, None], ticks_and_font_size=[8, 8, 10]):
    fig, ax = plt.subplots()
    plt.xlabel(titles[0])
    plt.ylabel(titles[1])
    ticks_and_font_size = extend_parameters(ticks_and_font_size, 3, element_extend_by=10)
    fig.suptitle(titles[2], fontsize=ticks_and_font_size[2], fontweight="bold")

    if point_start_to_end[0] == None and point_start_to_end[1] == None:
        minEl, maxEl = returnMinAndMaxElementForData(data, quant, stretch_graph_coefficients)

        ax.xaxis.set_ticks_position("bottom")
        ax.yaxis.set_ticks_position("left")
        ax.spines["left"].set_position(("data", minEl[0]))
        ax.spines["bottom"].set_position(("data", minEl[1]))
        ax.set(xlim=(minEl[0], maxEl[0]),ylim=(minEl[1], maxEl[1]))
        plt.xticks(np.linspace(minEl[0], maxEl[0], 8), rotation=0, size=ticks_and_font_size[0])
        plt.yticks(np.linspace(minEl[1], maxEl[1], 8),size=ticks_and_font_size[1])
    elif point_start_to_end[0] == None and point_start_to_end[1] != None:
        minEl, maxEl = returnMinAndMaxElementForData(data, quant, stretch_graph_coefficients)
        ax.xaxis.set_ticks_position("bottom")
        ax.yaxis.set_ticks_position("left")
        ax.spines["left"].set_position(("data", minEl[0]))
        ax.spines["bottom"].set_position(("data", point_start_to_end[1][0]))
        ax.set(xlim=(minEl[0], maxEl[0]),ylim=(point_start_to_end[1][0], point_start_to_end[1][1]))
        plt.xticks(np.linspace(minEl[0], maxEl[0], 8), rotation=0, size=ticks_and_font_size[0])
        plt.yticks(np.linspace(point_start_to_end[1][0], point_start_to_end[1][1], point_start_to_end[1][2]),size=ticks_and_font_size[1]) 
        minEl[1], maxEl[1] = point_start_to_end[1][0], point_start_to_end[1][1]

    elif point_start_to_end[0] != None and point_start_to_end[1] == None:
        minEl, maxEl = returnMinAndMaxElementForData(data, quant, stretch_graph_coefficients)
        ax.xaxis.set_ticks_position("bottom")
        ax.yaxis.set_ticks_position("left")
        ax.spines["left"].set_position(("data", point_start_to_end[0][0]))
        ax.spines["bottom"].set_position(("data", minEl[1]))
        ax.set(xlim=(point_start_to_end[0][0], point_start_to_end[0][1]),ylim=(minEl[1], maxEl[1]))
        plt.xticks(np.linspace(point_start_to_end[0][0], point_start_to_end[0][1], point_start_to_end[0][2]), rotation=0, size=ticks_and_font_size[0])
        plt.yticks(np.linspace(minEl[1], maxEl[1], 8),size=ticks_and_font_size[1])
        minEl[0], maxEl[0] = point_start_to_end[0][0], point_start_to_end[0][1]

    elif point_start_to_end[0] != None and point_start_to_end[1] != None:
        ax.xaxis.set_ticks_position("bottom")
        ax.yaxis.set_ticks_position("left")
        ax.spines["left"].set_position(("data", point_start_to_end[0][0]))
        ax.spines["bottom"].set_position(("data", point_start_to_end[1][0]))
        ax.set(xlim=(point_start_to_end[0][0], point_start_to_end[0][1]),ylim=(point_start_to_end[1][0], point_start_to_end[1][1]))
        plt.xticks(np.linspace(point_start_to_end[0][0], point_start_to_end[0][1], point_start_to_end[0][2]), rotation=0, size=ticks_and_font_size[0])
        plt.yticks(np.linspace(point_start_to_end[1][0], point_start_to_end[1][1], point_start_to_end[1][2]),size=ticks_and_font_size[1]) 
        minEl, maxEl = [point_start_to_end[0][0], point_start_to_end[1][0]], [point_start_to_end[0][1], point_start_to_end[1][1]]



    colors = extend_parameters(colors, quant, 'r')
    lses = extend_parameters(lses, quant, '')
    labels = extend_parameters(labels, quant, '')
    markersizes = extend_parameters(markersizes, quant, 3)
    markers = extend_parameters(markers, quant, 'o')

    for i in range(quant):
        if(data[i].shape[0] == 4):
            ax.errorbar(x=data[i][0], y=data[i][2], xerr=data[i][1], yerr=data[i][3], lw=0.5, color=colors[i], marker=markers[i], label=labels[i], markersize=markersizes[i], ls=lses[i],)
        elif(data[i].shape[0] == 3):
            ax.errorbar(x=data[i][0], y=data[i][2], xerr=data[i][1], lw=0.5, color=colors[i], marker=markers[i], label=labels[i], markersize=markersizes[i], ls=lses[i],)
        elif(data[i].shape[0] == 2):
            ax.plot(data[i][0], data[i][1], lw=0.5, color=colors[i], marker=markers[i], label=labels[i], markersize=markersizes[i], ls=lses[i],)
    
    if(len(axes_round) == 1):
        ax.yaxis.set_major_formatter(FormatStrFormatter(axes_round[0]))
        ax.xaxis.set_major_formatter(FormatStrFormatter(axes_round[0]))
    elif(len(axes_round) == 2):
        ax.yaxis.set_major_formatter(FormatStrFormatter(axes_round[0]))
        ax.xaxis.set_major_formatter(FormatStrFormatter(axes_round[1]))
    
    ax.tick_params(direction ='in')
    ax.legend(loc=legend_position, frameon=False)
    ax.grid(linewidth="0.2")
    ax.minorticks_on()
    ax.tick_params(axis='x', which='minor', direction='in', length=2, width=1, color='black')
    ax.tick_params(axis='y', which='minor', direction='in', length=2, width=1, color='black')

    for i in range(len(points_draw_lines_to)):
        ax.axvline(x = points_draw_lines_to[i][0], ymax = (points_draw_lines_to[i][1] - minEl[1])/ (maxEl[1] - minEl[1]),color = 'green', linestyle='dashed') 
        ax.axhline(y = points_draw_lines_to[i][1], xmax = (points_draw_lines_to[i][0] - minEl[0]) / (maxEl[0] - minEl[0]), color = 'green', linestyle='dashed')
        if len(points_draw_lines_to[i]) == 2: 
            ax.text(x=points_draw_lines_to[i][0] +0.05, y = minEl[1] + 0.3, s=str(round(points_draw_lines_to[i][0], 2)), fontsize = ticks_and_font_size[0])
            ax.text(x=minEl[0] +0.05, y = points_draw_lines_to[i][1] + 0.25, s=str(round(points_draw_lines_to[i][1], 2)), fontsize = ticks_and_font_size[1])
        elif len(points_draw_lines_to[i]) == 3: 

            ax.text(x=points_draw_lines_to[i][0] +0.05, y = minEl[1] + 0.3, s=str(round(points_draw_lines_to[i][0], 2)), fontsize = points_draw_lines_to[i][2])
            ax.text(x=minEl[0] +0.05, y = points_draw_lines_to[i][1] + 0.25, s=str(round(points_draw_lines_to[i][1], 2)), fontsize = points_draw_lines_to[i][2])
        elif len(points_draw_lines_to[i]) >= 4: 
            ax.text(x=points_draw_lines_to[i][0] +0.05, y = minEl[1] + 0.3, s=str(round(points_draw_lines_to[i][0], 2)), fontsize = points_draw_lines_to[i][2])
            ax.text(x=minEl[0] +0.05, y = points_draw_lines_to[i][1] + 0.25, s=str(round(points_draw_lines_to[i][1], 2)), fontsize = points_draw_lines_to[i][3])

        

    if save_flag:
        plt.savefig(name_fig)
    return fig, ax

def mnk(x, y):
    k = (np.mean(x * y) - np.mean(x) * np.mean(y)) / (np.mean(x ** 2) - np.mean(x) ** 2)
    b = np.mean(y) - k * np.mean(x)
    dxx = np.mean(x ** 2) - np.mean(x) ** 2
    dyy = np.mean(y ** 2) - np.mean(y) ** 2
    errK = np.sqrt((dyy / dxx - k**2) / (x.shape[0] - 2))
    errB = errK * np.sqrt(np.mean(x ** 2))
    coef = np.array([k, b])
    error = np.array([errK, errB])
    return (coef, error)


    # if len(lses) < quant and len(lses) > 0:
    #     for i in range(len(lses), quant):
    #         lses.append(lses[i - 1])
    # elif len(lses) == 0:
    #     lses = [''] * quant
    # if len(labels) < quant and len(labels) > 0:
    #     for i in range(len(labels), quant):
    #         labels.append(labels[i - 1])
    # elif len(labels) == 0:
    #     labels = [''] * quant

    # if len(markersizes) < quant and len(markersizes) > 0:
    #     for i in range(len(markersizes), quant):
    #         markersizes.append(markersizes[i - 1])
    # elif len(markersizes) == 0:
    #     markersizes = [3] * quant

    # if len(markers) < quant and len(markers) > 0:
    #     for i in range(len(markers), quant):
    #         markers.append(markers[i - 1])
    # elif len(markers) == 0:
    #     markers = ["o"] * quant