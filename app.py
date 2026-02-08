import os  # <--- Make sure this is imported at the top!
import psycopg2
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def get_db_connection():
    # 1. Try to get the URL from the cloud environment
    db_url = os.environ.get('DATABASE_URL')
    
    if db_url:
        # If we are on the cloud (Render), use the provided URL
        conn = psycopg2.connect(db_url)
    else:
        # If we are on localhost, use your local settings
        conn = psycopg2.connect(
            host="localhost",
            database="todo_app",
            user="postgres",
            password="KamalHassan@2005"
        )
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # 1. Fetch all available categories (for the dropdown menu)
    cur.execute('SELECT * FROM categories')
    categories = cur.fetchall()

    # 2. Fetch tasks AND their category names (using a JOIN)
    # This matches the 'category_id' in todos with the 'id' in categories
    cur.execute('''
        SELECT t.id, t.title, t.status, t.due_date, c.name 
        FROM todos t
        LEFT JOIN categories c ON t.category_id = c.id
        ORDER BY t.due_date ASC;
    ''')
    todos = cur.fetchall()
    
    cur.close()
    conn.close()
    return render_template('index.html', todos=todos, categories=categories)

@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    due_date = request.form['due_date']
    category_id = request.form['category']  # <--- Get the chosen category ID
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Insert the task with the category_id
    cur.execute('''
        INSERT INTO todos (title, status, due_date, category_id) 
        VALUES (%s, %s, %s, %s)
    ''', (title, False, due_date, category_id))
    
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/complete/<int:id>')
def complete(id):
    conn = get_db_connection()
    cur = conn.cursor()
    # Mark the task as "True" (Completed)
    cur.execute("UPDATE todos SET status = TRUE WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    cur = conn.cursor()
    # Delete the task row entirely
    cur.execute("DELETE FROM todos WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

# --- TEMPORARY SETUP ROUTE ---
@app.route('/setup')
def setup_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # 1. Create Categories Table
        cur.execute("CREATE TABLE IF NOT EXISTS categories (id SERIAL PRIMARY KEY, name VARCHAR(50) NOT NULL);")
        
        # 2. Add Default Categories (Only if empty)
        cur.execute("SELECT COUNT(*) FROM categories")
        if cur.fetchone()[0] == 0:
            cur.execute("INSERT INTO categories (name) VALUES ('Work'), ('Personal'), ('School'), ('Urgent');")
        
        # 3. Create Todos Table
        cur.execute("CREATE TABLE IF NOT EXISTS todos (id SERIAL PRIMARY KEY, title VARCHAR(100) NOT NULL, status BOOLEAN DEFAULT FALSE, due_date TIMESTAMP, category_id INTEGER REFERENCES categories(id));")
        
        conn.commit()
        return "Database Tables Created Successfully! You can now go to the home page."
    except Exception as e:
        return f"An error occurred: {e}"
    finally:
        cur.close()
        conn.close()


if __name__ == '__main__':
    app.run(debug=True)