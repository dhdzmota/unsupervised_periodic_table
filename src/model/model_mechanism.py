import networkx as nx
import os
import pandas as pd
import numpy as np
import shap
import matplotlib.pyplot as plt

from minisom import MiniSom as SOM
from sklearn.ensemble import RandomForestClassifier
from scipy.spatial import distance_matrix
from src.data.download_data import read_data_as_csv


def som_model_fit(
    df,
    projection_size=11,
    sigma=1,
    learning_rate=0.1,
    random_seed=42,
    train_iterations=100000
):
    som = SOM(
        x=projection_size,
        y=projection_size,
        input_len=df.shape[1],
        sigma=sigma,
        learning_rate=learning_rate,
        topology='rectangular',
        random_seed=random_seed,
    )
    som.random_weights_init(transformed_pt.values)
    som.train(transformed_pt.values, train_iterations)
    return som

def som_results(som, df, c=('projection_x', 'projection_y')):
    projection_localization = []
    for element_pos in range(df.shape[0]):
        element_to_evaluate = df.iloc[element_pos].values
        projection_localization.append(
            som.winner(element_to_evaluate)
        )
    results = pd.DataFrame(projection_localization, index=df.index, columns=c)
    results.reset_index(inplace=True)
    results['pair'] = (
            results[c[0]].astype('str') + ' ' + results[c[1]].astype('str')
    )
    return results


def create_reciprocal_distance_matrix(results, column_name):
    values_for_distances = results[['projection_x', 'projection_y']].values
    pairwise_distances = distance_matrix(
        values_for_distances,
        values_for_distances
    )
    pairwise_distances = pd.DataFrame(
        pairwise_distances,
        columns=results[column_name],
        index=results[column_name]
    )
    pairwise_reciprocal_distances = 1 / (np.exp(pairwise_distances ** 2))
    return pairwise_reciprocal_distances


def include_rdm_in_results(reciprocal_distance_matrix, results, column_name):
    results_c = results.copy()
    relations = []
    distances = []
    for element in results_c[column_name]:
        related_reciprocal_distances = reciprocal_distance_matrix.loc[element]
        relation_list = related_reciprocal_distances.index.to_list()
        relations.append(relation_list)
        distance_list = list(related_reciprocal_distances.values)
        distances.append(distance_list)
    results_c['relations'] = relations
    results_c['distances'] = distances
    return results_c


def obtain_exploded_df_from_results(df, column_name):
    # index_col='AtomicNumber'
    results_relation = df[[column_name, 'relations']].explode('relations')
    results_distances = df[[column_name, 'distances']].explode('distances')
    results_relation['distances'] = results_distances.distances
    return results_relation


def create_graph_from_exploded_results(
    exploded_results,
    column_from,
    column_to
):
    G = nx.from_pandas_edgelist(
        exploded_results,
        source=column_from,
        target=column_to,
        edge_attr=True
    )
    return G

def get_communities_with_weight(G, weight):
    communities = nx.community.greedy_modularity_communities(G, weight=weight)
    return communities


def plot_individual_communities(G, communities):
    for c in communities:
        sG = G.subgraph(c)
        pos = nx.kamada_kawai_layout(sG)
        nx.draw_networkx_nodes(sG, pos=pos, node_size=250, node_color='r')
        nx.draw_networkx_edges(sG, pos=pos, node_size=250)
        nx.draw_networkx_labels(sG, pos=pos, font_size=10)
        plt.title(
            f'Network Representation for the following atomic numbers: {c}'
        )
        plt.show()


def explainability(df, classifications):
    for idx, class_group in enumerate(classifications):
        try:
            df.loc[class_group, 'class_group'] = idx
        except KeyError:
            pass

    model = RandomForestClassifier(n_estimators=1000)
    x, y = df.drop('class_group', axis=1), df.class_group.fillna(-1)
    model.fit(x, y)
    explainer = shap.TreeExplainer(model)

    for nb in sorted(y.unique()):
        shap_values = explainer.shap_values(x)[int(nb)]
        shap.summary_plot(shap_values, x, max_display=5, show=False)

if __name__ == '__main__':
    file_path = os.path.dirname(os.path.abspath(__file__))
    general_path = os.path.join(file_path, '..', '../')
    data_processed_path = os.path.join(general_path, 'data', 'processed')
    data_processed_filename = os.path.join(
        data_processed_path,
        'processed_data.csv'
    )
    transformed_pt = read_data_as_csv(data_processed_filename, keep_na=True)
    som = som_model_fit(
        transformed_pt,
        projection_size=11,
        sigma=1,
        learning_rate=0.1,
        random_seed=42,
        train_iterations=100000
    )
    results = som_results(som, transformed_pt)
    pairwise_reciprocal_distances = create_reciprocal_distance_matrix(
        results=results,
        column_name='AtomicNumber'
    )
    results_with_relation = include_rdm_in_results(
        reciprocal_distance_matrix=pairwise_reciprocal_distances,
        results=results,
        column_name='AtomicNumber'
    )
    elemental_results_relations = obtain_exploded_df_from_results(
        df=results_with_relation,
        column_name='AtomicNumber',
    )

    G = create_graph_from_exploded_results(
        exploded_results=elemental_results_relations,
        column_from='AtomicNumber', column_to='relations'
    )

    classifications = get_communities_with_weight(G, weight='distances')
    #TODO: get classification images

    explainability(transformed_pt, classifications)
    #TODO: get shap images
    # TODO: Save entities: G, classifications, SOM
