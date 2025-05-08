from sentence_transformers import SentenceTransformer, util
import json
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# ✅ Load the JSON file
with open("grapeshms_curated_training_data.json", "r", encoding="utf-8") as f:
    grapeshms_curated_training_data = json.load(f)

# ✅ Extract question-answer pairs
questions = [item["question"] for item in grapeshms_curated_training_data]
answers = [item["answer"] for item in grapeshms_curated_training_data]

# ✅ Load the SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')  # Lightweight and fast model
question_embeddings = model.encode(questions, convert_to_tensor=True)

def preprocess_input(user_input):
    words = user_input.lower().split()
    # Only remove stopwords that are not critical for intent
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words or word in ["what", "is", "about"]]
    return ' '.join(words)

def get_response(user_input):
    user_input = preprocess_input(user_input)
    user_embedding = model.encode(user_input, convert_to_tensor=True)
    similarities = util.cos_sim(user_embedding, question_embeddings)
    best_match_idx = similarities.argmax().item()
    confidence = similarities[0, best_match_idx].item()

    if confidence < 0.4:  # Lowered threshold
        return "Sorry, I didn't understand that."
    return answers[best_match_idx]

# ✅ Run the chatbot
if __name__ == "__main__":
    print("MediAssist Chatbot (type 'exit' to quit)")
    while True:
        q = input("You: ")
        if q.lower() in ["exit", "quit"]:
            print("Bot: Goodbye!")
            break
        print("Bot:", get_response(q))




