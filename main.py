from dotenv import load_dotenv
load_dotenv()

from app import app

if __name__ == '__main__':
    # use_reloader=False to prevent duplicate bot instances
    # Flask reloader spawns 2 processes, both would start bot polling
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
