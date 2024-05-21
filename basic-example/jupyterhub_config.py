# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Configuration file for JupyterHub
import os

c = get_config()  # noqa: F821

# We rely on environment variables to configure JupyterHub so that we
# avoid having to rebuild the JupyterHub container every time we change a
# configuration parameter.

# Spawn single-user servers as Docker containers
c.JupyterHub.spawner_class = "dockerspawner.DockerSpawner"

# Spawn containers from this image
c.DockerSpawner.image = os.environ["DOCKER_NOTEBOOK_IMAGE"]

# Connect containers to this Docker network
network_name = os.environ["DOCKER_NETWORK_NAME"]
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = network_name

# Explicitly set notebook directory because we'll be mounting a volume to it.
# Most `jupyter/docker-stacks` *-notebook images run the Notebook server as
# user `jovyan`, and set the notebook directory to `/home/jovyan/work`.
# We follow the same convention.
notebook_dir = os.environ.get("DOCKER_NOTEBOOK_DIR", "/home/jovyan/work")
c.DockerSpawner.notebook_dir = notebook_dir

# Mount the real user's Docker volume on the host to the notebook user's
# notebook directory in the container
c.DockerSpawner.volumes = {"jupyterhub-user-{username}": notebook_dir}

# Remove containers once they are stopped
c.DockerSpawner.remove = True

# For debugging arguments passed to spawned containers
c.DockerSpawner.debug = True

# User containers will access hub by container name on the Docker network
c.JupyterHub.hub_ip = "jupyterhub"
c.JupyterHub.hub_port = 8080

# Persist hub data on volume mounted inside container
c.JupyterHub.cookie_secret_file = "/data/jupyterhub_cookie_secret"
c.JupyterHub.db_url = "sqlite:////data/jupyterhub.sqlite"

# Authenticate users with Native Authenticator
#c.JupyterHub.authenticator_class = "nativeauthenticator.NativeAuthenticator"

# Allow anyone to sign-up without approval
#c.NativeAuthenticator.open_signup = True

# Authenticate all users regardless of password
#c.JupyterHub.authenticator_class = "dummy"

# -------------------------------------------
# Authenticate users with JTW Authenticator
c.JupyterHub.authenticator_class = "jwtauthenticator.JSONWebTokenLocalAuthenticator"

# Only one of two following fields must be set.  
# If both, then "secret" will be the signing method used.
# The secrect key used to generate the given token
c.JSONWebTokenAuthenticator.secret = '<secret-key>'   
         
# -OR-
# The certificate used to sign the incoming JSONWebToken, must be in PEM Format
#c.JSONWebTokenAuthenticator.signing_certificate = '/foo/bar/adfs-signature.crt'

# The claim field contianing the username/sAMAccountNAme/userPrincipalName
c.JSONWebTokenAuthenticator.username_claim_field = 'username'

# This config option should match the aud field of the JSONWebToken, empty string to disable the validation of this field.
#c.JSONWebTokenAuthenticator.expected_audience = 'https://myApp.domain.local/'
c.JSONWebTokenAuthenticator.expected_audience = ''

# This will enable local user creation upon authentication, requires JSONWebTokenLocalAuthenticator
#c.JSONWebLocalTokenAuthenticator.create_system_users = True
c.LocalAuthenticator.create_system_users = True

# Only the one of three follwing sources for JWT token must be set at the time. If you want to disable inspection
# of some of sources, set corresponding value to '' 

# URL for redirecting to in the case of invalid auth token
#c.JSONWebTokenAuthenticator.auth_url = 'https://auth.example.com' 
c.JSONWebTokenAuthenticator.auth_url = 'http://www.quickmeme.com/img/31/315664151c156dd45dcb9421ce259b352c1867e92fbbde4e66693004c8bd95c1.jpg' 

# Name of query param for auth_url to pass return URL
c.JSONWebTokenAuthenticator.retpath_param = 'retpath' 

# Header name to retrieve JWT token
c.JSONWebTokenAuthenticator.header_name = 'X-Auth-Token'  
 
# Cookie name to retrieve JWT token                      
c.JSONWebTokenAuthenticator.cookie_name = 'auth_token'

# Query param to retrieve JWT token                         
c.JSONWebTokenAuthenticator.param_name = 'auth_token'


# -----------------------------

# Allowed admins
admin = os.environ.get("JUPYTERHUB_ADMIN")
if admin:
    c.Authenticator.admin_users = [admin]
