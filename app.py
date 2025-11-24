from fastapi import FastAPI
from db import fetch_all, execute_query

app = FastAPI()



@app.on_event("startup")
def setup_db():
    execute_query("""
        CREATE TABLE IF NOT EXISTS todos (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            completed BOOLEAN DEFAULT FALSE
        );
    """)


# GET /todos
@app.get("/todos")
def get_todos():
    rows = fetch_all("SELECT id, title, completed FROM todos;")
    return {"todos": rows}

# POST /todos
@app.post("/todos")
def create_todo(title: str):
    execute_query(
        "INSERT INTO todos (title, completed) VALUES (%s, %s)",
        (title, False),
    )
    return {"message": f"{title} created"}

# PUT /todos/{id}
@app.put("/todos/{todo_id}")
def toggle_todo(todo_id: int):
    execute_query(
        "UPDATE todos SET completed = NOT completed WHERE id = %s",
        (todo_id,),
    )
    return {"message": "Todo toggled"}

# DELETE /todos/{id}
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    execute_query("DELETE FROM todos WHERE id = %s", (todo_id,))
    return {"message": "Todo deleted"}


@app.get("/")
def home():
    return {"message": "Todo API is running"}

