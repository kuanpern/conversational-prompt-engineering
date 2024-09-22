# cpe-ui (cpe-ui)

UI for Conversational Prompt Engineering

## Install the dependencies
```bash
yarn
# or
npm install
```

## Install the dependencies
```bash
npm install
```

### Start the app in development mode (hot-code reloading, error reporting, etc.)
```bash
# export LOCAL_PROXY_PATH_PREFIX=/sundial
quasar dev
```

Note: By default auth guard is activated. To disable it during development, please set the environment variable `DISABLE_AUTH` to "true", e.g.
```bash
export DISABLE_AUTH=true
quasar dev
```

### Build the app for production
```bash
# export BUILDENV=local # <- set this if deployed behind reverse proxy with path removal
quasar build
```
