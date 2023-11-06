import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import os
import pandas as pd
import pickle
import shap

from minisom import MiniSom as SOM
from sklearn.ensemble import RandomForestClassifier
from scipy.spatial import distance_matrix


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
    som.random_weights_init(df.values)
    som.train(df.values, train_iterations)
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
    zfill_val = len(str(len(communities)))
    for i, c in enumerate(communities):
        sG = G.subgraph(c)
        pos = nx.kamada_kawai_layout(sG)
        nx.draw_networkx_nodes(sG, pos=pos, node_size=250, node_color='r')
        nx.draw_networkx_edges(sG, pos=pos, node_size=250)
        nx.draw_networkx_labels(sG, pos=pos, font_size=10)
        plt.title(
            f'Network Representation for the following'
            f' atomic numbers:\n {list(c)}'
        )
        path = get_expected_basepath('results')
        name = f'classification_{str(i).zfill(zfill_val)}.png'
        filepath = os.path.join(path, name)
        plt.savefig(filepath)
        plt.close()


def explainability(df, classifications, plot=True):
    class_group_dict = {}
    for idx, class_group in enumerate(classifications):
        try:
            df.loc[class_group, 'class_group'] = idx
            class_group_dict[idx] = list(class_group)
        except KeyError:
            pass

    model = RandomForestClassifier(n_estimators=1000)
    x, y = df.drop('class_group', axis=1), df.class_group.fillna(-1)
    model.fit(x, y)
    explainer = shap.TreeExplainer(model)

    zfill_val = len(str(y.nunique()))
    for nb in sorted(y.unique()):
        shap_values = explainer.shap_values(x)[int(nb)]
        plt.title(f'Most important features with corresponding '
                  f'shap_values for\n'
                  f'the following atomic numbers: \n {class_group_dict[nb]}')
        shap.summary_plot(shap_values, x, max_display=5, show=False)

        if plot:
            path = get_expected_basepath('results')
            name = f'shap_classification_{str(nb).zfill(zfill_val)}.png'
            filepath = os.path.join(path, name)
            plt.savefig(filepath)
            plt.close()


def get_general_path():
    file_path = os.path.dirname(os.path.abspath(__file__))
    general_path = os.path.join(file_path, '..', '../')
    return general_path


def get_expected_basepath(expected_path):
    general_path = get_general_path()
    path = os.path.join(general_path, expected_path)
    return path


def save_entity_as_pickle(entity, name):
    models_path = get_expected_basepath('models')
    entity_path = os.path.join(models_path, name)
    with open(f'{entity_path}.pkl', 'wb') as file:
        pickle.dump(entity, file)
