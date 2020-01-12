from views import *

if __name__ == '__main__':
    db.generate_mapping(create_tables=True)
    app.run(debug=True)
