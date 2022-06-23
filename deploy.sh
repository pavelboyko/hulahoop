#!/usr/bin/env sh
# The single instance production install script.
# More install options will be added in the future.
# Adapted from the beautiful https://raw.githubusercontent.com/posthog/posthog/HEAD/bin/deploy-hobby 

export DJANGO_SECRET_KEY=$(base64 /dev/urandom | head -c50)

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

echo "Making sure any Hulahoop stack that might run is stopped"
sudo -E docker-compose stop &> /dev/null || true

echo "Creating the Hulahoop data directory ./volumes"
for dir in etc postgres redis
do
    sudo mkdir -p ./volumes/$dir
done
echo "Copying configuration files"
sudo cp -r etc/* ./volumes/etc

# Write .env file
envsubst < .env.tmpl > .env

echo "Starting the stack!"
sudo docker-compose up -d

echo "We will need to wait ~5-10 minutes for things to settle down, migrations to finish, and TLS certs to be issued"
echo ""
echo "⏳ Waiting for Hulahoop web to boot (this will take a few minutes)"
bash -c 'while [[ "$(curl -s -o /dev/null -w ''%{http_code}'' localhost:8000/_health)" != "200" ]]; do sleep 5; done'
echo "⌛️ Hulahoop looks up!"
echo ""
echo "🎉🎉🎉  Done! 🎉🎉🎉"
echo ""
echo "To stop the stack run 'docker-compose stop'"
echo "To start the stack again run 'docker-compose start'"
echo "If you have any issues at all delete everything in this directory and run the deploy.sh script again"
echo ""
echo "Hulahoop will be up at the location you provided!"
echo "${SITE_HTTP_SCHEME}://${SITE_HOSTNAME}"
echo ""







