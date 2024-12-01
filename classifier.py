import time
import requests
from typing import List, Dict

class CommentClassifier:
    def __init__(self, mistral_api_key: str, rate_limit_delay: float = 1.0):
        self.api_key = mistral_api_key
        self.base_url = "https://api.mistral.ai/v1/chat/completions"
        self.rate_limit_delay = rate_limit_delay

    def classify_comments(self,
                          root_comment: str,
                          parent_comment: str,
                          categories: List[str] = [
    # Emotional and Tonal Categories
    "positive_emotion",        # Encompasses "nice", "positive_supportive", "humoristic"
    "neutral_emotion",         # Existing "neutral"
    "negative_emotion",        # Covers "condescending", "sarcastic", "egotist"
    
    # Discriminatory and Harmful Content
    "hate_speech",             # Broad category covering "derogatory_general", "hate_general"
    
    # Specific Discrimination Types
    "racial_discrimination",   # Includes "racist", "xenophobic"
    "religious_discrimination", # Covers "antisemitic", "islamophobic", "anti_christian"
    "gender_discrimination",   # Encompasses "sexist", "homophobic"
    
    # Intention and Content Types
    "violent_intent",          # "inciting_violence"
    "factual_statement",       # "true", "false"
]) -> Dict[str, List[str]]:
        prompt = f"""
        You are a professional comment classifier specializing in detecting nuanced discriminatory and hateful language.
        Your task is to categorize comments strictly into one or more of these categories: {', '.join(categories)}.

        Guidelines:
        - Read the comment carefully and detect subtle stereotypes, coded language, and implied biases.
        - Choose ONE OR MORE primary categories if applicable.
        - Respond with EXACTLY the category names in lowercase, separated by commas if multiple categories apply.

        Parent Content: {parent_comment}

        Classification:
        """
        print("prompt:", prompt)
        payload = {
            "model": "mistral-medium",
            "messages": [
                {"role": "system", "content": "You are a precise and culturally sensitive comment classification assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.1,
            "max_tokens": 50,
            "stop": ["\n"]
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        for _ in range(3):  # Retry up to 3 times
            try:
                time.sleep(self.rate_limit_delay)

                response = requests.post(self.base_url, json=payload, headers=headers, timeout=10)
                response.raise_for_status()

                response_data = response.json()
                classification = response_data['choices'][0]['message']['content'].lower().strip()

                classifications = [cat.strip() for cat in classification.split(',')]
                valid_classifications = [cat for cat in classifications if cat in categories]

                if not valid_classifications:
                    valid_classifications = ["neutral"]

                return {
                    "root_comment": root_comment,
                    "parent_comment": parent_comment,
                    "classification": valid_classifications
                }

            except requests.exceptions.RequestException as e:
                print(f"API Request Error for comments: {root_comment}, {parent_comment}")
                print(f"Error details: {e}")
                time.sleep(5)  # Wait before retrying
            except Exception as e:
                print(f"Unexpected error processing comments: {root_comment}, {parent_comment}")
                print(f"Error details: {e}")
                time.sleep(5)  # Wait before retrying

        return {
            "root_comment": root_comment,
            "parent_comment": parent_comment,
            "classification": ["neutral"]
        }