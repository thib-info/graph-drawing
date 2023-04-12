import matplotlib.backends.backend_pdf
import matplotlib.pyplot as plt
import networkx as nx


def create_pdf_page(name):
    path = './stocked-graph/report/' + name + '.pdf'
    pdf = matplotlib.backends.backend_pdf.PdfPages(path)
    return pdf


def close_pdf_page(pdf):
    pdf.close()


def save_pdf(G, pdf):
    # visualize the graph using networkx
    pos = {int(n): data['pos'] for n, data in G.nodes(data=True)}
    nx.draw(G, pos=pos, with_labels=True)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    # add the plot to the PDF file
    pdf.savefig()

    # close the PDF file
    plt.clf()
