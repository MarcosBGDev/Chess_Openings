class CleanConfig:
    def __init__(self, start_year, end_year, n_top, modalities, color="white"):
        self.start_year = start_year
        self.end_year = end_year
        self.n_top = n_top
        self.modalities = modalities or ["blitz", "bullet"]
        self.color = color