#!/bin/sh
#
# Script:               decrypt_control_data.sh
# Synopsis:             This script decrypts control data JSON files that have been PGP encrypted
# Created By:           Jeff Shurtliff
# Last Modified By:     Jeff Shurtliff
# Modified Date:        2022-09-29
# Version:              1.1.0


# Decrypt the Communities control data
gpg --quiet --batch --yes --decrypt --passphrase="$HELPER_DECRYPT_PASSPHRASE" \
--output "$HOME"/secrets/communities_control_data.json ./.github/encrypted/communities_control_data.json.gpg

# Decrypt the Categories control data
gpg --quiet --batch --yes --decrypt --passphrase="$HELPER_DECRYPT_PASSPHRASE" \
--output "$HOME"/secrets/categories_control_data.json ./.github/encrypted/categories_control_data.json.gpg
