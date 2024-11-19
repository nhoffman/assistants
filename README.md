# Feature Assistant

## Local development environment

Minimal environment for the application (requires uv):

```
uv virtualenv py3-env
source py3-env/bin/activate
uv pip install -r requirements.txt
```

```
export OPENAI_API_KEY="..."
```

Add the password and API key to a secrets file for local testing; see
https://docs.streamlit.io/knowledge-base/deploy/authentication-without-sso:

```
mkdir -p .streamlit
OPENAI_API_KEY=foo cat > .streamlit/secrets.toml <<EOF
PASSWORD = "password"
OPENAI_API_KEY = "$OPENAI_API_KEY"
EOF
```

```
streamlit run Home.py
```

## Build a Docker image and run locally

```
docker build --platform=linux/amd64 . -t feature-assistant
```

```
docker run --platform=linux/amd64 --rm -p 8000:8000 -e OPENAI_API_KEY="$OPENAI_API_KEY" -e OPENAI_BASE_URL="$OPENAI_BASE_URL" feature-assistant
```
