from dotenv import load_dotenv

load_dotenv()

from server import globals as g

if __name__ == '__main__':
    g.app.run(debug=False, host="0.0.0.0", port=5001)
