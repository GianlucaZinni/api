from flask import Flask

app = Flask(__name__)

# Lógica para gestionar recetas
@app.route('/recipes/<recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    # Recupera y devuelve la receta
    return f'Recipe {recipe_id} details'

if __name__ == '__main__':
    app.run(port=5002)
