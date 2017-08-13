LOGIN_LINK = "//article/div/div/p/a[text()='Log in']"
LOGIN_BUTTON = "//form/span/button[text()='Log in']"
LOGIN_INPUT_USERNAME = "//input[@name='username']"
LOGIN_INPUT_PASSWORD = "//input[@name='password']"
OPTIONS_BUTTON = "//form/span/button[text()='Options']"

# UPLOAD PICTURE
UPLOAD_PICTURE_INPUT_FILE = "//input[@type='file']"
UPLOAD_PICTURE_NEXT_LINK = "//header/div/button[text()='Next']"
UPLOAD_PICTURE_TEXTAREA_COMMENT = "//section/div/textarea"
UPLOAD_PICTURE_SHARE_LINK = "//button[text()='Share']"
UPLOAD_PICTURE_CAMARA_CSS_CLASS = "coreSpriteCameraInactive"

# FOLLOW/UNFOLLOW
FOLLOW_UNFOLLOW_BUTTON = "//*[contains(text(), 'Follow')]"
FOLLOW_BUTTON_TEXT = "Follow"
UNFOLLOW_BUTTON_TEXT = "Following"

# LIKE/UNLIKE
LIKE_BUTTON_TEXT = "Like"
UNLIKE_BUTTON_TEXT = "Unlike"

SUCCESS_LIKE_POST_MESSAGE = "Now you like the post: {0}"
FAIL_LIKE_POST_MESSAGE = "You already like the post: {0}"
SUCCESS_UNLIKE_POST_MESSAGE = "Now you do not like the post: {0}"
FAIL_UNLIKE_POST_MESSAGE = "You already do not like the post: {0}"

# COMMENT POST
REQUEST_NEW_COMMENT_BUTTON = "//a/span[contains(text(), 'Comment')]"
SEND_COMMENT_BUTTON = "//form/button[contains(text(), 'Post')]"
COMMENT_TEXTEAREA = "//form/textarea"

# PROFILE PAGE
USER_FOLLOWING = "//a[@href='/{0}/following/']/span"
USER_FOLLOWERS = "//a[@href='/{0}/followers/']/span"
