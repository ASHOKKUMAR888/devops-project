from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>Welcome to DevOps Project</h1>
    <h2>Application: Running</h2>
    <h2>Version: 1.0</h2>
    <h2>Environment: Kubernetes</h2>
    """

@app.route("/health")
def health():
    return {
        "status": "healthy"
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
