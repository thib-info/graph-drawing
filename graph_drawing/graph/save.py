import os
import matplotlib.backends.backend_pdf
import matplotlib.pyplot as plt
import networkx as nx
import shutil
import glob
from PIL import Image


def create_pdf_page(name):
    path = './graph_drawing/stocked-graph/report/' + name + '.pdf'
    pdf = matplotlib.backends.backend_pdf.PdfPages(path)
    return pdf


def close_pdf_page(pdf):
    pdf.close()


def save_pdf(graph, pdf):
    # visualize the graph using networkx
    pos = {int(n): data['pos'] for n, data in graph.nodes(data=True)}
    nx.draw(graph, pos=pos, with_labels=True)
    labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)

    # add the plot to the PDF file
    pdf.savefig()

    # close the PDF file
    plt.clf()


def save_screenshot(graph, name):
    name = './graph_drawing/stocked-graph/' + name
    nbrElem = len(os.listdir(name))
    fig = plt.figure(figsize=(8, 8))
    pos = {int(n): data['pos'] for n, data in graph.nodes(data=True)}
    nx.draw(graph, pos=pos, with_labels=True)
    labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    fig.savefig(name + "/screenshot-" + str(nbrElem))
    plt.close(fig)


def init_gif(name):
    if os.path.exists('./graph_drawing/stocked-graph/' + name):
        shutil.rmtree('./graph_drawing/stocked-graph/' + name, ignore_errors=True)

    os.mkdir('./graph_drawing/stocked-graph/' + name)


def create_gif_from_images(name):
    def sort_by_number(filename):
        return int(''.join(filter(str.isdigit, filename)))

    folder_path = './graph_drawing/stocked-graph/' + name

    frames = [Image.open(image) for image in sorted(glob.glob(f"{folder_path}/*.png"), key=sort_by_number)]
    frame_one = frames[0]
    frame_one.save(folder_path + '/' + name + '.gif', format="GIF", append_images=frames,
                   save_all=True, duration=100*len(frames), loop=0)
