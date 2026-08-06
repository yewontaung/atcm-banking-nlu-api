from banking_nlu import BankingNLUPredictor


banking_nlu:BankingNLUPredictor = None

def load_nlu(
        model_name:str,
        saved_model_path:str,
        intent_metadata_path:str,
        entity_metadata_path:str,
        device:str = "cpu"):
    global banking_nlu
    banking_nlu = BankingNLUPredictor.load(
        model_name=model_name,
        saved_model_path=saved_model_path,
        intent_metadata_path=intent_metadata_path,
        entity_metadata_path=entity_metadata_path,
        device=device
    )