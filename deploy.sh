#!/usr/bin/env sh
# The single instance production install script.
# More install options will be added in the future.
# Adapted from the beautiful https://raw.githubusercontent.com/posthog/posthog/HEAD/bin/deploy-hobby 

DJANGO_SECRET_KEY=$(base64 /dev/urandom | head -c50)

# Talk to the user
echo "Welcome to the single instance Hulahoop installer."
echo ""

echo "Let's get the exact domain Hulahoop will be installed on"
echo "Make sure that you have a Host A DNS record pointing to this instance!"
#echo "This will be used for TLS 🔐"
#echo "ie: test.example.com (NOT an IP address)"
read -r SITE_HOSTNAME
export SITE_HOSTNAME=$SITE_HOSTNAME
export SITE_HTTP_SCHEME="http"

echo ""
echo "We will need sudo access so the next question is for you to give us superuser access"
echo "Please enter your sudo password now:"
sudo echo ""
echo "Thanks! 🙏"
echo ""
echo "Ok! We'll take it from here 🚀"

echo "Making sure any stack that might exist is stopped"
sudo -E docker-compose -f docker-compose.prod.yml stop &> /dev/null || true

# Write .env file
cp .env.example .env.prod
envsubst >> .env.prod <<EOF
DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY
SITE_HOSTNAME=$SITE_HOSTNAME
SITE_HTTP_SCHEME=$SITE_HTTP_SCHEME
EOF




