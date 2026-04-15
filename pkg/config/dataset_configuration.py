from pkg.adapter.volley_match_adapter import VolleyMatchAdapter


class DatasetConfiguration:

    def __init__(self, dataset_path_match, dataset_sep_match, adapter_match):
        self.dataset_path_match = dataset_path_match
        self.dataset_sep_match = dataset_sep_match
        self.adapter_match = adapter_match


volleyball_configuration = DatasetConfiguration(
    dataset_path_match="resources/data/volleyball/match_men.csv",
    dataset_sep_match=",",
    adapter_match=VolleyMatchAdapter(),
)
