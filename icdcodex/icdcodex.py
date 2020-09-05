"""Main module."""

class IcdGraphicalStructure:
    def __init__(self) -> None:
        ...


class IcdEmbedder:
    
    def __init__(self) -> None:
        ...

    def transform(X):
        """transform an ICD code into a continuous representation
        
        Args:
            X (List[str]): icd code(s)
        
        Returns:
            continuous representation
        """