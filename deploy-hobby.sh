#!/usr/bin/env sh
# The single instance production install script.
# Adapted from the beautiful https://raw.githubusercontent.com/posthog/posthog/HEAD/bin/deploy-hobby 

# Generate new secrets
export DJANGO_SECRET_KEY=$(base64 /dev/urandom | head -c50)
export POSTGRES_PASSWORD=$(base64 /dev/urandom | head -c50)

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

# Write configuration file
envsubst < .env.tmpl > .env

echo ""
echo "We will need sudo access so the next question is for you to give us superuser access"
echo "Please enter your sudo password now:"
sudo echo ""
echo "Thanks! 🙏"
echo ""
echo "Ok! We'll take it from here 🚀"

echo "Making sure any Hulahoop stack that might run is stopped"
sudo docker-compose stop &> /dev/null || true

echo "Starting the stack!"
sudo docker-compose up -d

echo ""
echo "🎉🎉🎉  Done! 🎉🎉🎉"
echo ""
echo "To stop the stack run 'docker-compose stop'"
echo "To start the stack again run 'docker-compose start'"
echo "It is generally a good idea to setup backups of the database located in ./volumes/postgres/"
echo ""
echo "Hulahoop will be up at the location you provided!"
echo "${SITE_HTTP_SCHEME}://${SITE_HOSTNAME}"
echo ""







