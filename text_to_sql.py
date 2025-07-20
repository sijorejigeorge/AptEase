from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Path to your fine-tuned model directory
model_path = "./fine_tuned_model"  # Adjust this to the correct path where your model is saved

# Load the tokenizer and model from the fine-tuned model directory
model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)


def generate_sql_query(natural_language_query):
    # Prepare the input text for translation (from English to SQL)
    input_text = f"translate English to SQL: {natural_language_query}"

    # Tokenize the input text
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids

    # Generate the SQL query
    output_ids = model.generate(input_ids)

    # Decode the output to get the SQL query
    sql_query = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    sql_query = sql_query.replace("review_score", "review_scores_rating")

    print(sql_query)
    return sql_query
