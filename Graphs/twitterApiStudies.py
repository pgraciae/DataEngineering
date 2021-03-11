import pickle
import networkx as nx
import tweepy

#### APARTAT PER A FUNCIONS AUXILIARS QUE CREGUEU D'UTILITAT #####

#### FUNCIONS QUE ES DEMANEN EN L'ENUNCIAT DE LA PRACTICA   #####
auth = tweepy.OAuthHandler("jCfS2u3maPqQZ9tU1rtd9iQj0", "PJv9jlK8iL7WQLGMLe9JvTwpH2bXkEhzsJhj9xxv8Bd7npc1pj")
auth.set_access_token("788369185348911104-eoft8MRz0Cjlc7EQQH4ROpYTIHsBiNI", "RpudouauIEdIRt8tfdT4VIKL3sObnSCbZ0wDeQKDYcTIJ")

api = tweepy.API(auth,  wait_on_rate_limit_notify=True, wait_on_rate_limit=True )

seed_node = api.get_user("lapizlasulo")._json["screen_name"]


max_nodes_to_crawl = 45

max_followers = 10000


def crawler(seed_node, max_nodes_to_crawl, max_followers):
    '''
    :param seed_node: node_id of the first node to explore by the crawler
    :param max_nodes_to_crawl: total number of nodes to explore. The crawler stops after the number has been reached.
    :param max_followers: maximum number of followers a user can have for being crawled. Users with more than those
        followers will be discarded and not crawled
    :return: the function does not return any parameter.
    '''
    n = 1
    queue = api.friends_ids(seed_node)
    graf = []
    while n < max_nodes_to_crawl:
        graf += [[seed_node, n] for n in api.friends_ids(seed_node) if len(n._json["friends"]) < 10000]
        seed_node = queue[n]
        n+=1

    with open("id_seed_node_n.txt", "w") as file:
        for n in graf:
            file.write(str(n[0]) +" "+ str(n[1]) + "\n")


    ### INCLOUEU AQUI LA VOSTRA IMPLEMENTACIO DE LA FUNCIO #####


def export_edges_to_graph(file_name):
    '''
    :param file_name: name of the txt file that contains the edges of the graf.
    :return: the function does not return any parameter.
    '''

    ### INCLOUEU AQUI LA VOSTRA IMPLEMENTACIO DE LA FUNCIO #####
    import networkx as nx
    arestes = []
    with open(file_name, "r") as file:
        for line in file:
            line = line.split()
            arestes += [(line[0], line[1])]

    G = nx.DiGraph()

    G.add_edges_from(arestes)

    nx.write_gpickle(G, file_name[:-4]+".pickle")

def export_graph_to_gexf(g, file_name):
    '''
    :param g: A graph with the corresponding networkx format.
    :param file_name: name of the file that will be saved.
    :return: the function does not return any parameter.
    '''

    ### INCLOUEU AQUI LA VOSTRA IMPLEMENTACIO DE LA FUNCIO #####
    import networkx as nx
    G = nx.read_gpickle(g)
    nx.write_gexf(G, file_name)


#export_graph_to_gexf("nou_id_seed_node_n.pickle", "nou_id_seed_node_n.gexf")