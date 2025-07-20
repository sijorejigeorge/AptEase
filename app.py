from flask import Flask, request, jsonify, render_template
import sqlite3
import openai  # You need to install the OpenAI Python package
from text_to_sql import generate_sql_query  # type: ignore
from generate_summary import generate_summary_text  # Import the new summary generation function

app = Flask(__name__)

def execute_sql_query(sql_query):
    conn = sqlite3.connect("apartments.db")
    cursor = conn.cursor()
    try:
        # Execute the query
        cursor.execute(sql_query)
        rows = cursor.fetchall()

        # Get column names dynamically
        column_names = [description[0] for description in cursor.description]

        # Format results as a list of dictionaries
        results = [dict(zip(column_names, row)) for row in rows]

        # Count total results
        total_results = len(results)

        conn.close()
        return {"total_results": total_results, "data": results}
    except Exception as e:
        conn.close()
        return {"error": str(e)}

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/query', methods=['POST'])
def query():
    natural_language_query = request.get_json().get('query')
    print(f"User Query: {natural_language_query}")

    # Generate SQL query from natural language query
    sql_query = generate_sql_query(natural_language_query)

    # Execute the SQL query and get the results
    result = execute_sql_query(sql_query)

    return jsonify({"sql_query": sql_query, "result": result})

# New endpoint to generate the summary
@app.route('/generate-summary', methods=['POST'])
def generate_summary():
    results = request.get_json().get('results')

    # Call the summary generation function
    summary = generate_summary_text(results)

    return jsonify({"summary": summary})

if __name__ == '__main__':
    app.run(debug=True)
