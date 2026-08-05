
def main():
    print("=== Loading ... ===")
    from banking_nlu import BankingNLUPredictor

    predictor = BankingNLUPredictor.load(
        model_name="xlm-roberta-base",
        saved_model_path="./_model/banking_nlu_model_02_d1014_e30.pt",
        intent_metadata_path="./_metadata/intents.json",
        entity_metadata_path="./_metadata/entities.json",
    )
    print("======= Start Testing =======")
    while True:
        prompt = input("Enter prompt : ")
        if prompt.lower() == "exit" or prompt.lower() == "0":
            break
        output = predictor.predict(prompt)
        print(output.model_dump_json(indent=2))
    print("======= End Testing =======")

if __name__ == "__main__":
    main()