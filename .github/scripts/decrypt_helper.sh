#!/bin/sh
#
# Script:               decrypt_helper.sh
# Synopsis:             This script decrypts Helper configuration files that have been PGP encrypted
# Created By:           Jeff Shurtliff
# Last Modified By:     Jeff Shurtliff
# Modified Date:        2020-04-26
# Version:              1.0.0

# Decrypt the file
mkdir $HOME/secrets
gpg --quiet --batch --yes --decrypt --passphrase="$HELPER_DECRYPT_PASSPHRASE" \
--output $HOME/secrets/khoros_helper.yml ../encrypted/khoros_helper.yml.gpg
