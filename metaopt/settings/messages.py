from django.contrib.messages import constants

# Set message tags
MESSAGE_TAGS = {
    constants.DEBUG: 'alert alert-primary alert-dismissible fade show',
    constants.ERROR: 'alert alert-danger alert-dismissible fade show',
    constants.INFO: 'alert alert-info alert-dismissible fade show',
    constants.SUCCESS: 'alert alert-success alert-dismissible fade show',
    constants.WARNING: 'alert alert-warning alert-dismissible fade show',
}