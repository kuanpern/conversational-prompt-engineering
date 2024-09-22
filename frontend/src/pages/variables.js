let login_url  = "";
let logout_url = "";
let user_info_url = "";
let manual_login_url = "";

if (process.env.BUILDENV === "local") {
  login_url     = "http://127.0.0.1:9000/cpe/authorize";
  logout_url    = "http://127.0.0.1:9000/cpe/logout";
  user_info_url = "http://127.0.0.1:9000/cpe/get_user_info";
  manual_login_url = "http://127.0.0.1:9000/cpe/manual_login";
} else {
  login_url     = process.env.PROXY_PATH_PREFIX + "/authorize";
  logout_url    = process.env.PROXY_PATH_PREFIX + "/logout";
  user_info_url = process.env.PROXY_PATH_PREFIX + "/get_user_info";
  manual_login_url = process.env.PROXY_PATH_PREFIX + "/manual_login";
} // end if

const maintainer_email = "kptan86@gmail.com";

export { maintainer_email, login_url, logout_url, user_info_url, manual_login_url};
