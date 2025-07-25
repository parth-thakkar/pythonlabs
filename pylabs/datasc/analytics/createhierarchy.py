import pandas as pd

def main():
    data = {
        'parent_id': [1, 2, 3, 4, 5, 6, 7, 8],
        'child_id': [2, 3, 4, 5, 6, 7, 8, 9]
    }
    df = build_hierarchy(data,'parent_id')
    print(df)


def build_hierarchy(df, parent_id=None, level=5):
    """
    Recursively builds a hierarchical structure from parent-child relationships.

    Args:
        df: The input DataFrame.
        parent_id: The parent ID to start from.
        level: The current hierarchy level.

    Returns:
        A DataFrame with hierarchical columns.
    """

    # Base case: No parent ID, return an empty DataFrame
    if parent_id is None:
        return pd.DataFrame()

    # Filter rows based on the parent ID
    filtered_df = df[df['parent_id'] == parent_id]

    # Create a new column for the current level
    level_name = f'level_{level}'
    filtered_df[level_name] = filtered_df['child_id']

    # Recursively build the hierarchy for each child
    child_hierarchy = pd.concat([build_hierarchy(df, child_id, level + 1) for child_id in filtered_df['child_id']], axis=1)

    # Merge the current level with the child hierarchy
    result_df = pd.concat([filtered_df[[level_name]], child_hierarchy], axis=1)

    return result_df

if __name__ == "__main__" :
    main()ShriHari:

