#!/bin/python3

from tasks import *

needsroot()

# Redefine some commands for the sake of scalability
prerun("""
function apt {
    /usr/bin/apt --assume-yes $@
}
function flatpak {
    /usr/bin/flatpak -y $@
}
function ask_prompt {
    # Argument 1: Message
    # Argument 2: If yes (function name)
    # 3: If no (function name)
    # 4: Default

    message=$1
    yes=$2
    no=$3

    default=$yes
    p="[Y/n]"

    if [ -z $4 ]; then
        true
    elif [ $4 == "n" ]; then
        default=$no
        p="[y/N]"
    fi


    read -p "$message $p: " input
    if [ -z $input ]; then
        $default
    elif [ ${input,,} == "y" -o ${input,,} == "yes" ]; then
        $yes
    elif [ ${input,,} == "n" -o ${input,,} == "no" ]; then
        $no
    else
        ask_prompt $@
    fi
}

""")



Task("Flatpak w/ Flathub (app repository)","""
            apt install flatpak plasma-discover-backend-flatpak
            flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
            """, reboot=True, selected=True)
Task("ZRAM (enhancement)", """
            apt install zram-tools
            echo -e "ALGO=zstd\nPERCENT=65\nPRIORITY=100" | tee -a /etc/default/zramswap
            service zramswap reload
            """, selected=True)
Task("Command Not Found (enhancement)","""
            apt install command-not-found
            apt update
            """, selected=True)
Task("Pipewire w/ Wireplumber (enhancement)",
            "apt install pipewire-audio pipewire-jack",
            reboot=True, selected=True)

# Scripts
Task("KDE Debloat (script)", """
            apps=

            function rmpkg {
                apps="$apps $@"
            }
            # Libreoffice
            
            rmpkg libreoffice-*
            
            # Random KDE apps
            rmpkg kontrast 
     
            apt remove $apps
            apt autoremove
            apt autoclean
""")

# Apps
Task("VLC (app)",
            "apt install vlc")
Task("mpv (app)",
            "apt install mpv",
            selected=True)

# Controversial
Task("OnlyOffice (app)",
            "flatpak install app/org.onlyoffice.desktopeditors/x86_64/stable")
Task("Google Chrome (app)","""
            echo "Google Chrome terms of service: https://policies.google.com/terms https://www.google.com/chrome/terms"
            echo "Would you like to install Google Chrome? By installing Google Chrome, you agree to its terms of service."
            ask_prompt "Do you want to install Google Chrome?" true exit

            chrome_pkg="google-chrome-stable_current_amd64.deb"
            wget https://dl.google.com/linux/direct/$chrome_pkg
            apt install ./$chrome_pkg
            echo "Cleaning $PWD/$chrome_pkg"
            rm $chrome_pkg
            """)

run_tasks()