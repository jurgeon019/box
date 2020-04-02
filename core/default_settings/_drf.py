# 'DEFAULT_AUTHENTICATION_CLASSES'= (
#     # 'rest_framework.authentication.SessionAuthentication',
#     'box.core.authentication.CsrfExemptSessionAuthentication',
#     'rest_framework.authentication.BasicAuthentication'
# ),

REST_FRAMEWORK = {
    # 'DATETIME_FORMAT': "%Y-%m-%d - %H:%M:%S", 
    'DATETIME_FORMAT': "%d-%m-%Y %H:%M",
}