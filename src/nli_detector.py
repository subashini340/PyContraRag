from transformers import pipeline

class NLIDetector:
    def __init__(self):
        print("Loading NLI model (first time konjam neram edukum)...")
        # Using a small, fast model specifically trained for NLI
        self.classifier = pipeline(
            "text-classification", 
            model="cross-encoder/nli-deberta-v3-small"
        )

    def check_conflict(self, text1: str, text2: str):
        """Checks if two texts contradict each other."""
        # DeBERTa expects a pair of sequences
        input_pair = f"{text1} [SEP] {text2}"
        
        result = self.classifier(input_pair)[0]
        
        # The model returns labels: ENTAILMENT, NEUTRAL, CONTRADICTION
        label = result['label']
        score = result['score']
        
        is_conflict = (label == "CONTRADICTION" and score > 0.5)
        
        return {
            "label": label,
            "score": round(score, 4),
            "is_conflict": is_conflict
        }

# --- Test block ---
if __name__ == "__main__":
    detector = NLIDetector()
    
    # Test 1: Contradiction
    t1 = "Python dictionaries maintain insertion order."
    t2 = "Insertion order is not guaranteed in Python dictionaries."
    res1 = detector.check_conflict(t1, t2)
    print(f"\nTest 1 (Conflict Expected): {res1['label']} ({res1['score']}) | Conflict: {res1['is_conflict']}")
    
    # Test 2: Agreement
    t3 = "Python dictionaries are unordered."
    t4 = "The order of items in a dictionary is not preserved."
    res2 = detector.check_conflict(t3, t4)
    print(f"Test 2 (Agreement Expected): {res2['label']} ({res2['score']}) | Conflict: {res2['is_conflict']}")