let publicPath;
let content;
let DISABLE_AUTH;

// set proxy path prefix to "/app-directory" if build environment is set
if (process.env.PROXY_PATH_PREFIX === undefined) {
  if (process.env.BUILDENV === undefined) {
    process.env.PROXY_PATH_PREFIX = "";
  } else {
    process.env.PROXY_PATH_PREFIX = "/app-directory";
  } // end if
} // end if
// console.log("PROXY_PATH_PREFIX: "+process.env.PROXY_PATH_PREFIX)

// set other environment variables
publicPath = process.env.PROXY_PATH_PREFIX+"/llm-apps/";
// console.log("publicPath: "+publicPath)
DISABLE_AUTH = process.env.DISABLE_AUTH;
// console.log("DISABLE_AUTH: "+DISABLE_AUTH)
content = {
  BUILDENV: process.env.BUILDENV,
  PROXY_PATH_PREFIX: process.env.PROXY_PATH_PREFIX,
  DISABLE_AUTH: DISABLE_AUTH
};


module.exports = {
  "custom_vars": content,
  "publicPath": publicPath,
};
