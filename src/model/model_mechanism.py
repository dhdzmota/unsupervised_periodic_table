import os

from src.data.download_data import read_data_as_csv
from src.model.model_utils import (
    som_model_fit,
    som_results,
    create_reciprocal_distance_matrix,
    include_rdm_in_results,
    obtain_exploded_df_from_results,
    create_graph_from_exploded_results,
    get_communities_with_weight,
    explainability
)


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
    # TODO: get classification images

    explainability(transformed_pt, classifications)
    print(classifications)
    # TODO: get shap images
    # TODO: Save entities: G, classifications, SOM
