from transformers import pipeline
classifier = pipeline("text-classification", model="textattack/roberta-base-CoLA")
res = classifier("Yeah, I am the best!")

def score_sentence(sentence):
    result = classifier(sentence)[0]
    label = result['label']
    score = result['score']

    scaled_score = round(score * 10, 2)

    return {
        "sentence": sentence,
        "label": label,  # 'LABEL_1' = acceptable, 'LABEL_0' = not acceptable
        "confidence": round(score, 3),
        "proficiency_score": scaled_score,
        "interpretation": (
            "Excellent grammar" if label == "LABEL_1" and scaled_score >= 8 else
            "Decent grammar" if label == "LABEL_1" else
            "Poor grammar"
        )
    }

# Example usage
if __name__ == "__main__":
    sentence = input("Enter a sentence to evaluate:\n> ")
    result = score_sentence(sentence)
    print("\n--- Evaluation ---")
    for k, v in result.items():
        print(f"{k}: {v}")